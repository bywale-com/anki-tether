from __future__ import annotations

import re

# Allow the same formatting in authored validation and the browser reviewer.
CARD_HTML_TAGS = {"b", "blockquote", "br", "code", "div", "em", "hr", "i", "li", "ol", "p", "pre", "strong", "ul"}
MATH_DELIMITER = re.compile(r"\\\\|\\[()[\]]")
