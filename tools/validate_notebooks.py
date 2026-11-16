"""Execute exact notebook cells in clean native R processes and retain evidence.

Project: JupyterLite-R. Created 2026-11-16, project contributors with Codex.
Inputs: notebooks, optional project R library. Outputs: logs, PNGs, JSON run report.
Use --extensions for package integration checks; --embed saves CORE native outputs for the book.
This validates R semantics, not the browser kernel. Browser checks are separate.
"""
from pathlib import Path
import argparse
import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import nbformat
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def run(args):
    """Execute each notebook in a new R session, failing on any cell error."""
    rscript = args.rscript or shutil.which("Rscript")
    if not rscript:
        raise SystemExit("Rscript not found; use --rscript PATH. No execution was validated.")
    mode = "extensions" if args.extensions else "core"
    out = ROOT / "validation" / "runs" / mode
    out.mkdir(parents=True, exist_ok=True)
    report = {"runtime": "native R", "mode": mode, "notebooks": []}
    failures = []
    for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
        nb = nbformat.read(path, as_version=4)
        folder = out / path.stem
        folder.mkdir(exist_ok=True)
        statements = ["options(warn=1)", "env <- new.env(parent=globalenv())"]
        if args.extensions:
            lib = (ROOT / ".cache" / "R-library").as_posix()
            statements.append(f".libPaths(c({json.dumps(lib)}, .libPaths()))")
        executed = []
        for i, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue
            optional = "optional-package" in cell.metadata.get("tags", [])
            if optional and not args.extensions:
                continue
            executed.append(i)
            source = folder / f"cell-{i}.R"
            source.write_text(cell.source + "\n", encoding="utf-8")
            # Use one device per cell; %03d handles cells producing multiple figures.
            prefix = (folder / f"cell-{i}").as_posix()
            # Clear only exact generated cell outputs from this runner's owned directory.
            for old in folder.glob(f"cell-{i}-*.png"):
                old.unlink()
            statements += [
                f"sink({json.dumps(prefix + '.txt')})",
                f"png({json.dumps(prefix + '-%03d.png')}, width=1100, height=750, res=120)",
                f"source({json.dumps(source.as_posix())}, local=env, print.eval=TRUE)",
                "invisible(dev.off())", "sink()",
            ]
        statements += ["sessionInfo()"]
        runner = folder / "run.R"
        runner.write_text("\n".join(statements) + "\n", encoding="utf-8")
        env = os.environ.copy()
        env["LANG"] = "C"
        env["LC_ALL"] = "C"
        result = subprocess.run([rscript, "--vanilla", str(runner)], cwd=ROOT, env=env,
                                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
        (folder / "runtime.log").write_text(result.stdout + result.stderr, encoding="utf-8")
        entry = {"notebook": path.name, "exit_code": result.returncode,
                 "code_sha256": hashlib.sha256("\n".join(c.source for c in nb.cells if c.cell_type == "code").encode()).hexdigest(),
                 "executed_cells": len(executed), "skipped_optional_cells": sum(c.cell_type == "code" for c in nb.cells) - len(executed)}
        report["notebooks"].append(entry)
        print(f"{mode}: {path.name}: {'PASS' if result.returncode == 0 else 'FAIL'}", flush=True)
        if result.returncode:
            failures.append(path.name)
            print(result.stderr[-5000:])
        elif args.embed:
            if args.extensions:
                raise SystemExit("--embed is only supported for the portable core run")
            for i in executed:
                cell = nb.cells[i]
                cell.execution_count = executed.index(i) + 1
                output_text = (folder / f"cell-{i}.txt").read_text(encoding="utf-8", errors="replace")
                cell.outputs = [nbformat.v4.new_output("stream", name="stdout", text=output_text)] if output_text else []
                for png in sorted(folder.glob(f"cell-{i}-*.png")):
                    # R can emit an empty device page; don't publish blank notebook figures.
                    with Image.open(png) as rendered:
                        if all(low == high for low, high in rendered.convert("RGB").getextrema()):
                            continue
                    cell.outputs.append(nbformat.v4.new_output("display_data", data={
                        "image/png": base64.b64encode(png.read_bytes()).decode(),
                        "text/plain": f"Native R preview for {path.stem}, cell {i}. Rerun in webR to reproduce."}, metadata={}))
            nb.metadata["jupyterlite_r"]["saved_outputs"] = "Native R core execution; optional cells not executed. See validation/RESULTS.md."
            nbformat.write(nb, path, split_lines=False)
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Failed: " + ", ".join(failures))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rscript")
    parser.add_argument("--extensions", action="store_true")
    parser.add_argument("--embed", action="store_true")
    run(parser.parse_args())
