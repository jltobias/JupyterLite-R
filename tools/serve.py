"""Serve generated _site locally with webR isolation headers; no external exposure by default."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        super().end_headers()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-isolation", action="store_true", help="Simulate GitHub Pages to test the Lab worker")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / "_site"
    if not (root / "index.html").is_file():
        raise SystemExit("Build first: python tools/build.py")
    cls = SimpleHTTPRequestHandler if args.no_isolation else Handler
    print(f"Preview: http://127.0.0.1:{args.port}/", flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), partial(cls, directory=str(root))).serve_forever()
