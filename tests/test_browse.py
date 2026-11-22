from fastapi.testclient import TestClient
import pytest

from app.main import app


def test_browse_completed_card_without_changing_schedule():
    pytest.importorskip("anki")
    from app import collection

    collection.close_collection()
    with TestClient(app, follow_redirects=False) as client:
        assert client.get("/browse").headers["location"] == "/login"
        assert client.get("/browse/1").headers["location"] == "/login"
        client.post("/login", data={"username": "tester", "password": "secret"})
        assert client.get("/browse?deck=").status_code == 200
        assert "No cards match" in client.get("/browse").text
        collection.upsert_notes([
            {"deck": "Math::Limits", "front": r"Find \(x^2\).", "back": "A unique answer",
             "tags": ["calculus-basics"]},
            {"deck": "Programming", "front": "What is an array?", "back": "Indexed values"},
        ])
        decks = {d["name"]: d["id"] for d in collection.deck_summaries()}
        collection.select_deck(decks["Math::Limits"])
        cid = collection.next_card()["card"]["card_id"]
        collection.answer_card(cid, "easy")
        assert collection.next_card()["done"]
        with collection.locked_collection() as col:
            before = col.get_card(cid)
            selected = col.decks.current()["id"]

        listings = client.get("/browse?deck=&q=calculus")
        assert listings.status_code == 200
        assert f'href="/browse/{cid}?' in listings.text
        assert "What is an array?" not in listings.text
        assert f'href="/browse/{cid}?' in client.get("/browse?q=unique+answer").text
        assert f'href="/browse/{cid}?' in client.get(f"/browse?deck={decks['Math']}").text
        assert f'href="/browse/{cid}?' not in client.get(f"/browse?deck={decks['Programming']}").text
        assert client.get("/browse?q=%22%3A%2A").status_code == 200
        card = client.get(f"/browse/{cid}?q=calculus")
        assert card.status_code == 200
        assert "<math " in card.text
        assert "A unique answer" in card.text
        assert "Back to cards" in card.text
        assert client.get("/browse/1").status_code == 404
        assert client.get("/browse?deck=9223372036854775807").status_code == 404
        with collection.locked_collection() as col:
            after = col.get_card(cid)
            assert (after.due, after.queue, after.ivl, after.reps) == (before.due, before.queue, before.ivl, before.reps)
            assert col.decks.current()["id"] == selected
        assert collection.stats_summary()["reviews_logged"] == 1


def test_browse_paginates_results():
    pytest.importorskip("anki")
    from app import collection

    collection.close_collection()
    with TestClient(app, follow_redirects=False) as client:
        collection.upsert_notes([{"front": f"Topic {i}", "back": "Answer"} for i in range(31)])
        client.post("/login", data={"username": "tester", "password": "secret"})
        first = client.get("/browse?q=Topic")
        assert first.status_code == 200
        assert "Page 1 of 2" in first.text
        assert first.text.count('href="/browse/') == 30
        second = client.get("/browse?q=Topic&page=2")
        assert second.status_code == 200
        assert "Page 2 of 2" in second.text
        assert second.text.count('href="/browse/') == 1
