from fastapi.testclient import TestClient
import pytest

from app.main import app


def test_global_due_review_and_native_undo():
    pytest.importorskip("anki")
    from app import collection

    collection.close_collection()
    with TestClient(app, follow_redirects=False) as client:
        collection.upsert_notes([
            {"deck": "CALC::Limits", "front": "Limit due", "back": "Answer"},
            {"deck": "PROG::Arrays", "front": "Array due", "back": "Answer"},
            {"deck": "PROG::Arrays", "front": "New syntax", "back": "Answer"},
        ])
        with collection.locked_collection() as col:
            due = [cid for cid in col.find_cards("") if "due" in col.get_card(cid).note()["Front"]]
            col.sched.set_due_date(due, "0")
            selected = col.decks.current()["id"]
        prior_logs = collection.stats_summary()["reviews_logged"]
        client.post("/login", data={"username": "tester", "password": "secret"})
        csrf = client.cookies["anki_tether_csrf"]
        assert client.post("/study", data={"csrf": csrf}).headers["location"] == "/review?all_due=1"
        card = collection.next_card(all_due=True)["card"]
        cid = card["card_id"]
        assert cid in due
        rating = {"csrf": csrf, "card_id": cid, "rating": "easy", "all_due": "true"}
        assert client.post("/review/answer", data=rating).status_code == 303
        assert client.post(f"/cards/{cid}/flag", data={"csrf": csrf, "reason": "need_practice"}).status_code == 303
        assert "Undo last review" in client.get("/review?all_due=1").text
        assert client.post("/review/undo", data={"csrf": csrf, "all_due": "true"}).status_code == 303
        assert collection.next_card(all_due=True)["card"]["card_id"] == cid
        assert collection.browse_card(cid)["flag"] == "need_practice"
        assert client.post("/review/undo", data={"csrf": csrf}).status_code == 409
        for _ in due:
            card = collection.next_card(all_due=True)["card"]
            assert card["card_id"] in due
            collection.answer_card(card["card_id"], "easy", all_due=True)
        assert collection.next_card(all_due=True)["done"]
        with collection.locked_collection() as col:
            assert col.decks.current()["id"] == selected
        assert collection.stats_summary()["reviews_logged"] == prior_logs + 2


def test_course_recall_recent_miss_and_session_summary():
    pytest.importorskip("anki")
    from app import collection

    collection.close_collection()
    with TestClient(app, follow_redirects=False) as client:
        collection.upsert_notes([
            {"deck": "CALC::Limits", "front": "Limit question", "back": "Answer"},
            {"deck": "PROG::Arrays", "front": "Array question", "back": "Answer"},
        ])
        with collection.locked_collection() as col:
            col.sched.set_due_date(col.find_cards(""), "0")
        client.post("/login", data={"username": "tester", "password": "secret"})
        csrf = client.cookies["anki_tether_csrf"]
        client.post("/study", data={"csrf": csrf})
        first = collection.next_card(all_due=True)["card"]
        assert first["deck"] == "CALC::Limits"
        collection.answer_card(first["card_id"], "again", all_due=True)
        collection.set_card_flag(first["card_id"], "dont_understand")
        for _ in range(2):
            card = collection.next_card(all_due=True)["card"]
            collection.answer_card(card["card_id"], "easy", all_due=True)
        done = client.get("/review?all_due=1").text
        assert "3 ratings across" in done
        assert "2 cards this session · 1 Again" in done
        stats = client.get("/stats").text
        assert "Recently rated Again" in stats and "Limit question" in stats
        assert "/browse?flag=dont_understand" in stats
        progress = {row["name"]: row for row in collection.learning_progress(7)["courses"]}
        assert progress["CALC"]["reviews"] == 2
        assert progress["CALC"]["first_attempt_percent"] == 0
        assert progress["PROG"]["reviews"] == 1
        assert progress["PROG"]["first_attempt_percent"] == 100
        assert collection.performance()["first_attempt_percent"] == 50
