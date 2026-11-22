"""Extract source-labelled plain text from COIS 1020 PDF lectures and labs.

Generated material is a transcription aid, not proof of complete visual coverage.
"""
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"study-material"/"COIS-1020"
GROUPS=[("lectures", ROOT/"source-material", "P*.pdf"),
        ("labs", ROOT/"source-material"/"cois-anki-tether", "Lab *.pdf")]
for kind, directory, pattern in GROUPS:
    dest=OUT/kind
    dest.mkdir(parents=True,exist_ok=True)
    for source in sorted(directory.glob(pattern)):
        name=source.stem.replace(" ","-").replace("__","_")
        chunks=[f"# {source.name}","",f"Source: `{source.relative_to(ROOT)}`","",
                "Machine-extracted text; verify figures, tables and code against the original PDF.",""]
        with fitz.open(source) as pdf:
            for i,page in enumerate(pdf):
                chunks.extend([f"## PDF page {i+1}","","```text",page.get_text(sort=True).strip(),"```",""])
        (dest/(name+".md")).write_text("\n".join(chunks)+"\n",encoding="utf-8")
print("Prepared", len(list((OUT/"lectures").glob("*.md"))), "lectures and",len(list((OUT/"labs").glob("*.md"))),"labs")
