"""Build portable R notebooks from reviewable percent-format R chapter sources.

Project: JupyterLite-R. Created 2026-11-16 by the project contributors with Codex.
Inputs: chapters/*.R. Outputs: notebooks/*.ipynb. Requires nbformat.
No code executes here. Edit chapters, then regenerate notebooks.
"""
from pathlib import Path
import hashlib
import re
import nbformat

ROOT = Path(__file__).resolve().parents[1]


def notebook_from_script(path: Path):
    """Convert explicit cell markers, preserving code verbatim and stable cell IDs."""
    cells = []
    for chunk in re.split(r"(?m)^# %%", path.read_text(encoding="utf-8"))[1:]:
        marker, _, body = chunk.partition("\n")
        if "[markdown]" in marker:
            body = "\n".join(re.sub(r"^# ?", "", line) for line in body.splitlines()).strip()
            cell = nbformat.v4.new_markdown_cell(body)
        else:
            cell = nbformat.v4.new_code_cell(body.strip())
            if "[optional]" in marker:
                cell.metadata.tags = ["optional-package"]
        cell.id = hashlib.sha256((path.stem + str(len(cells))).encode()).hexdigest()[:12]
        cells.append(cell)
    nb = nbformat.v4.new_notebook(cells=cells, metadata={
        "kernelspec": {"name": "webR", "language": "R", "display_name": "R (webR)"},
        "language_info": {"name": "R", "file_extension": ".R", "mimetype": "text/x-rsrc"},
        "jupyterlite_r": {"source": path.relative_to(ROOT).as_posix(), "data": "original synthetic data"},
    })
    nbformat.validate(nb)
    return nb


if __name__ == "__main__":
    (ROOT / "notebooks").mkdir(exist_ok=True)
    for path in sorted((ROOT / "chapters").glob("*.R")):
        nbformat.write(notebook_from_script(path), ROOT / "notebooks" / f"{path.stem}.ipynb", split_lines=False)
        print(path.stem)
