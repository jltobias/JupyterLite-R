"""Build the Book, Lab, and gallery into one GitHub Pages artifact.

Project: JupyterLite-R. Created 2026-11-16 by project contributors with Codex.
Input: notebooks, myst.yml, gallery, web, assets. Output: _site (generated only).
Requires requirements.txt, Node 22, and R with shinylive for app export. No remote publishing here.
"""
from pathlib import Path
import argparse
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="", help="e.g. /JupyterLite-R for GitHub Pages; empty for localhost")
    parser.add_argument("--rscript", default=shutil.which("Rscript"), help="Native Rscript for exporting Shiny")
    args = parser.parse_args()
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    scripts = Path(sys.executable).parent
    node_bin = ROOT / ".cache" / "node" / ("Scripts" if os.name == "nt" else "bin")
    env["PATH"] = os.pathsep.join([str(scripts), str(node_bin), env.get("PATH", "")])
    env["BASE_URL"] = args.base_url.rstrip("/") + "/book"
    site = ROOT / "_site"
    if not args.rscript:
        raise SystemExit("Rscript is needed for the Shiny export. Install R and pass --rscript /path/to/Rscript.")
    subprocess.run([args.rscript, "--vanilla", "tools/export_shiny.R"], cwd=ROOT, env=env, check=True)
    # Check generated targets before recursively removing prior build artifacts.
    for name in ("_lite", "_build/site", "_build/html", "_stage"):
        target = (ROOT / name).resolve()
        if target != ROOT.resolve() / name or not target.is_relative_to(ROOT.resolve()):
            raise RuntimeError(f"Unsafe generated target: {target}")
        if target.exists():
            shutil.rmtree(target)
    subprocess.run([sys.executable, "-m", "jupyter_book", "build", "--html"], cwd=ROOT, env=env, check=True)
    # Isolate Lite's recursive configuration discovery from previous generated sites.
    lite_source = ROOT / "_stage" / "lite-source"
    lite_source.mkdir(parents=True)
    shutil.copy2(ROOT / "jupyter-lite.json", lite_source / "jupyter-lite.json")
    subprocess.run([sys.executable, "-m", "jupyter", "lite", "build", "--contents", str(ROOT / "notebooks"),
                    "--output-dir", str(ROOT / "_lite")], cwd=lite_source, env=env, check=True)
    if site.exists():
        if site.resolve() != ROOT.resolve() / "_site":
            raise RuntimeError("Unsafe site output")
        shutil.rmtree(site)
    site.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "_build" / "html", site / "book")
    shutil.copytree(ROOT / "_lite", site / "lite")
    shutil.copytree(ROOT / "gallery", site / "gallery")
    shutil.copytree(ROOT / "_shiny", site / "shiny")
    shutil.copytree(ROOT / "assets", site / "assets")
    shutil.copy2(ROOT / "web" / "index.html", site / "index.html")
    lab = site / "lite" / "lab"
    for name in ("isolation.js", "isolation-sw.js"):
        shutil.copy2(ROOT / "web" / name, lab / name)
    index = lab / "index.html"
    text = index.read_text(encoding="utf-8")
    index.write_text(text.replace("<head>", '<head>\n<script src="./isolation.js"></script>', 1), encoding="utf-8")
    (site / ".nojekyll").touch()
    required = [site/"book"/"index.html", lab/"index.html", site/"gallery"/"data"/"terrain.csv", site/"shiny"/"index.html"]
    for path in required:
        if not path.is_file():
            raise RuntimeError(f"Build output missing: {path}")
    print(f"Built {site}. Preview with: python tools/serve.py")


if __name__ == "__main__":
    main()
