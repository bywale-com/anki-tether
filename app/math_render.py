from html import unescape
import re
from xml.etree import ElementTree as ET

from latex2mathml.converter import convert

from app.card_format import MATH_DELIMITER

MATH_NS = "http://www.w3.org/1998/Math/MathML"
MATH_TAGS = set(
    "math mrow mi mn mo mtext mspace mfrac msqrt mroot msup msub msubsup munder "
    "mover munderover mtable mtr mtd mstyle mpadded mphantom mmultiscripts "
    "mprescripts none menclose".split()
)
MATH_ATTRIBUTES = set(
    "display displaystyle scriptlevel mathvariant stretchy symmetric fence separator "
    "form largeop movablelimits accent accentunder lspace rspace width height depth "
    "linethickness columnalign rowalign columnspacing rowspacing notation".split()
)
TAG = re.compile(r"(<[^>]+>)")


def _safe_mathml(latex: str, display: bool) -> str:
    tree = ET.fromstring(convert(latex, display="block" if display else "inline"))
    for element in tree.iter():
        tag = element.tag.removeprefix(f"{{{MATH_NS}}}")
        if tag not in MATH_TAGS:
            raise ValueError("unsupported math element")
        element.tag = tag
        element.attrib = {key: value for key, value in element.attrib.items() if key in MATH_ATTRIBUTES}
    tree.set("xmlns", MATH_NS)
    return ET.tostring(tree, encoding="unicode")


def _render_text(text: str) -> str:
    parts = []
    start = None
    offset = 0
    for token in MATH_DELIMITER.finditer(text):
        delimiter = token.group()
        if delimiter in (r"\(", r"\["):
            start = token
        elif start and (start.group(), delimiter) in {(r"\(", r"\)"), (r"\[", r"\]")}:
            latex = unescape(text[start.end():token.start()])
            if latex.strip() and len(latex) <= 4000:
                try:
                    display = delimiter == r"\]"
                    math = _safe_mathml(latex, display)
                    css_class = "math-display" if display else "math-inline"
                    # Inline layout stays valid even when display syntax is inside a paragraph.
                    parts.extend((text[offset:start.start()], f'<span class="{css_class}">{math}</span>'))
                    offset = token.end()
                except Exception:
                    # A converter error must not hide the rest of an existing card.
                    pass
            start = None
    return "".join(parts) + text[offset:]


def render_math(sanitized_html: str) -> str:
    """Render text nodes from sanitized cards, skipping literal code."""
    if "\\" not in sanitized_html:
        return sanitized_html
    literal_depth = 0
    parts = TAG.split(sanitized_html)
    for index, part in enumerate(parts):
        if index % 2:
            if part in ("<pre>", "<code>"):
                literal_depth += 1
            elif part in ("</pre>", "</code>"):
                literal_depth -= 1
        elif literal_depth == 0:
            parts[index] = _render_text(part)
    return "".join(parts)
