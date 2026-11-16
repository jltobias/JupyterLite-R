"""Check notebook schemas, paired sources, chapter inventory, and local Markdown links."""
from pathlib import Path
import re
import nbformat
import yaml
from make_notebooks import notebook_from_script

ROOT = Path(__file__).resolve().parents[1]
sources = sorted((ROOT / "chapters").glob("*.R"))
assert len(sources) == 10, "Expected ten chapter sources"
for source in sources:
    target = ROOT / "notebooks" / (source.stem + ".ipynb")
    nb = nbformat.read(target, as_version=4)
    nbformat.validate(nb)
    expected = notebook_from_script(source)
    assert [(c.cell_type,c.source) for c in nb.cells] == [(c.cell_type,c.source) for c in expected.cells], f"Regenerate {target}"
    assert nb.metadata.kernelspec.name == "webR"
    assert not any(o.output_type == "error" for c in nb.cells if c.cell_type == "code" for o in c.outputs)
    assert re.search(r"^# %%", source.read_text(encoding="utf-8"), re.M)
config = yaml.safe_load((ROOT / "myst.yml").read_text(encoding="utf-8"))
def walk(items):
    for item in items:
        if "file" in item:
            assert (ROOT / item["file"]).is_file(), item["file"]
        walk(item.get("children", []))
walk(config["project"]["toc"])
for path in [ROOT / "README.md", *list((ROOT / "book").glob("*.md"))]:
    body = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
    for link in re.findall(r"\]\(([^)]+)\)", body):
        if ":" not in link and not link.startswith("#"):
            assert (path.parent / link.split("#")[0]).exists(), f"Broken local link: {path}: {link}"
print("PASS: ten valid notebooks; source synchronization, kernel, TOC, and local Markdown links")
