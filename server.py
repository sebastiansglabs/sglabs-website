"""Tiny static dev server that disables caching.

Serves the project directory over HTTP with no-cache headers so the browser
(and the Claude Code preview panel) always fetch the latest CSS/JS/HTML.

Uses a threaded server so multiple parallel browser connections work reliably
(a single-threaded server can refuse connections under a real browser).

Usage: python server.py [port]   (default port 5500)
"""
import http.server
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5500


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    # Always serve from this script's directory (the project root).
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    server = http.server.ThreadingHTTPServer(("", PORT), NoCacheHandler)
    print(f"Serving (no-cache, threaded) on http://localhost:{PORT}")
    server.serve_forever()
