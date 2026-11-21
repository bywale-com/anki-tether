from pathlib import Path


def test_css_has_mobile_constraints():
    css = Path("app/static/style.css").read_text(encoding="utf-8")
    assert "viewport" not in css
    html = Path("app/templates/base.html").read_text(encoding="utf-8")
    assert "width=device-width" in html
    assert "min-height: 48px" in css
    assert "overflow-x: auto" in css
    assert "100dvh" in css
    assert "env(safe-area-inset-bottom)" in css
