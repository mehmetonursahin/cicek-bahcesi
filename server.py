# Bizim Bahçe — çok basit paylaşım sunucusu (Python, sıfır ek kurulum)
# Çalıştırmak için: python server.py   ->  http://localhost:3000
#
# Node.js kurmak istemiyorsan bunu kullan. server.js ile birebir aynı işi yapar:
#  - Oyunu (cicek-bahcesi.html) "/" adresinde sunar.
#  - İki cihazın paylaştığı veriyi /api/kv'de tutar ve data.json'a yazar.

import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

PORT = int(os.environ.get("PORT", "3000"))
HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "cicek-bahcesi.html")
DB   = os.path.join(HERE, "data.json")

# --- paylaşılan anahtar-değer deposu (diske yazılır) ---
_lock = threading.Lock()
try:
    with open(DB, "r", encoding="utf-8") as f:
        store = json.load(f)
except Exception:
    store = {}


def persist():
    with _lock:
        with open(DB, "w", encoding="utf-8") as f:
            json.dump(store, f)


class Handler(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._json(204, {})

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/api/kv":
            key = (parse_qs(u.query).get("key") or [""])[0]
            self._json(200, {"value": store.get(key)})
            return
        if u.path in ("/", "/index.html", "/cicek-bahcesi.html"):
            try:
                with open(HTML, "rb") as f:
                    data = f.read()
            except Exception:
                self.send_response(500); self.end_headers(); self.wfile.write(b"oyun dosyasi bulunamadi")
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_response(404); self.end_headers(); self.wfile.write(b"yok")

    def do_POST(self):
        if urlparse(self.path).path != "/api/kv":
            self._json(404, {"ok": False}); return
        try:
            n = int(self.headers.get("Content-Length", "0"))
            if n > 1_000_000:
                self._json(413, {"ok": False}); return
            payload = json.loads(self.rfile.read(n) or b"{}")
            key = payload.get("key")
            if isinstance(key, str):
                store[key] = payload.get("value")
                persist()
            self._json(200, {"ok": True})
        except Exception:
            self._json(400, {"ok": False})

    def log_message(self, *args):
        pass  # sessiz


if __name__ == "__main__":
    print("Bizim Bahce -> http://localhost:%d" % PORT)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
