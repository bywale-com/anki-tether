import hashlib
import json
import shutil

from fastapi.testclient import TestClient
import httpx
import pytest

from app.math_render import render_math
from scripts import authored_cards as authored


@pytest.fixture
def batches(tmp_path):
    root = tmp_path / "batches"
    shutil.copytree(authored.ROOT, root)
    return root


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (lambda b: b["cards"][0].update(front="   <br>"), "empty"),
        (lambda b: b["cards"][0].update(front=r"\(x\]"), "math delimiters"),
        (lambda b: b["cards"][0].update(front='<strong onclick="alert(1)">x</strong>'), "unsupported HTML"),
        (lambda b: b["cards"][0].update(front="x" * 8001), "maxLength"),
        (lambda b: b["cards"][0].update(id="bad-id\n"), "pattern"),
        (lambda b: b.update(deck="MATH-1110::::Bad deck"), "deck must start"),
        (lambda b: b.update(schema_version=2), "const"),
    ],
)
def test_invalid_batch_blocks_publication(batches, monkeypatch, change, message, capsys):
    path = batches / "MATH-1110/derivatives-001.json"
    batch = json.loads(path.read_text())
    change(batch)
    path.write_text(json.dumps(batch))
    monkeypatch.setattr(authored, "ROOT", batches)
    monkeypatch.setattr(authored.sys, "argv", ["authored_cards", "publish"])

    def unexpected_request(*args, **kwargs):
        pytest.fail("invalid batches must not open a publisher client")

    monkeypatch.setattr(authored.httpx, "Client", unexpected_request)
    assert authored.main() == 1
    assert message in capsys.readouterr().err


def test_rejects_malformed_json_and_cross_file_duplicate_ids(batches):
    original = batches / "COIS-1020/arrays-001.json"
    duplicate = original.with_name("duplicate.json")
    shutil.copyfile(original, duplicate)
    with pytest.raises(ValueError, match="duplicate card ID"):
        authored.load_cards(batches)
    duplicate.write_text("{ malformed")
    with pytest.raises(ValueError, match="Expecting property name"):
        authored.load_cards(batches)


def test_packet_sizes_and_failed_import_reporting(capsys):
    cards = authored.load_cards()
    authored_card = {**cards[0], "front": "∫" * 8000}
    packets = list(authored.requests_for([authored_card] * 30))
    assert len(packets) > 1
    assert sum(count for count, _ in packets) == 30
    assert all(len(body) <= authored.MAX_REQUEST_BYTES for _, body in packets)

    def reject(request):
        assert request.headers["authorization"] == "Bearer test-token"
        return httpx.Response(401, text="test-token")

    with httpx.Client(transport=httpx.MockTransport(reject)) as client:
        with pytest.raises(ValueError, match="HTTP 401"):
            authored.publish(cards, "https://study.example", "test-token", client)
    output = capsys.readouterr().out
    assert json.loads(output)["failed"] == len(cards)
    assert "test-token" not in output


def test_render_calculus_and_leave_code_literal():
    markup = render_math(
        r"<p>\(\frac{dy}{dx}=3x^2\)</p>"
        r"\[\lim_{x\to 0}\frac{\sin x}{x}=1\]"
        r"\[\int x^2\,dx=\frac{x^3}{3}+C\]"
        r"<pre><code>\(literal\)</code></pre>"
    )
    assert markup.count("<math ") == 3
    assert "display=\"block\"" in markup and "<mfrac>" in markup and "<msup>" in markup
    assert "lim" in markup and "∫" in markup
    assert r"<pre><code>\(literal\)</code></pre>" in markup
    assert "href=" not in render_math(r"\(\href{javascript:alert(1)}{x}\)")
    assert "<img" not in render_math(r"\(\text{&lt;img src=x&gt;}\)")


def test_publish_review_and_update_across_courses():
    pytest.importorskip("anki")
    from app import collection
    from app.main import app

    collection.close_collection()
    cards = authored.load_cards()
    sample_ids = {
        "cois1020-arrays-index-001", "cois1020-arrays-bound-001", "cois1020-arrays-mutation-001",
        "math1110-power-rule-001", "math1110-sine-limit-001", "math1110-power-integral-001",
    }
    guids = {"authored-" + hashlib.sha256(cid.encode()).hexdigest() for cid in sample_ids}
    cards = [card for card in cards if card["guid"] in guids]
    with TestClient(app, base_url="http://localhost", follow_redirects=False) as client:
        def publish(batch=cards):
            return authored.publish(batch, "http://localhost", "import-secret", client)

        assert publish() == {"created": 6, "updated": 0, "skipped": 0, "failed": 0}
        assert publish() == {"created": 0, "updated": 0, "skipped": 6, "failed": 0}
        assert client.post("/login", data={"username": "tester", "password": "secret"}).status_code == 303
        decks = {d["name"]: d["id"] for d in collection.deck_summaries()}
        csrf = client.cookies["anki_tether_csrf"]
        for deck, expected in (("COIS-1020::Arrays", "<pre><code>"), ("MATH-1110::Derivatives", "<math ")):
            assert client.post(f"/study/{decks[deck]}", data={"csrf": csrf}).status_code == 303
            assert expected in client.get("/review").text
            assert client.get("/review?show=1").status_code == 200

        active = collection.next_card()["card"]["card_id"]
        with collection.locked_collection() as col:
            guid = col.get_card(active).note().guid
        assert client.post("/review/answer", data={"csrf": csrf, "card_id": active, "rating": "good"}).status_code == 303
        original = next(c for c in cards if c["guid"] == guid)
        changed = {**original, "back": "Corrected answer", "tags": ["corrected"]}
        assert publish([changed])["updated"] == 1
        assert publish([changed])["skipped"] == 1
        with collection.locked_collection() as col:
            reviewed = col.get_card(active)
            assert reviewed.reps == 1
            assert reviewed.note()["Back"] == "Corrected answer"
            assert reviewed.note().tags == ["corrected"]
            assert reviewed.did == decks["MATH-1110::Derivatives"]
        moved = {**changed, "deck": "MATH-1110::Practice"}
        assert publish([moved])["updated"] == 1
        assert publish([moved])["skipped"] == 1
        with collection.locked_collection() as col:
            reviewed = col.get_card(active)
            assert reviewed.did == col.decks.by_name(moved["deck"])["id"]
            assert reviewed.reps == 1
        assert collection.stats_summary()["reviews_logged"] == 1
        assert collection.stats_summary()["cards"] == 6
