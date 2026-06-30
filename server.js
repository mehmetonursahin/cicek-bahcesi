// Bizim Bahçe — çok basit paylaşım sunucusu (sıfır bağımlılık, tek dosya)
// Çalıştırmak için: node server.js  →  http://localhost:3000
//
// Ne yapar:
//  - Oyunu (cicek-bahcesi.html) "/" adresinde sunar.
//  - İki cihazın paylaştığı veriyi (konum, vazo, posta) /api/kv'de tutar
//    ve data.json dosyasına yazar; sunucu yeniden başlasa da kaybolmaz.

const http = require("http");
const fs   = require("fs");
const path = require("path");

const PORT = process.env.PORT || 3000;
const HTML = path.join(__dirname, "cicek-bahcesi.html");
const DB   = path.join(__dirname, "data.json");

// --- paylaşılan anahtar-değer deposu (diske yazılır) ---
let store = {};
try { store = JSON.parse(fs.readFileSync(DB, "utf8")); } catch (e) { store = {}; }

let saveTimer = null;
function persist() {                       // kısa gecikmeyle topluca diske yaz
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    fs.writeFile(DB, JSON.stringify(store), () => {});
  }, 200);
}

function sendJSON(res, code, obj) {
  res.writeHead(code, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
  });
  res.end(JSON.stringify(obj));
}

const server = http.createServer((req, res) => {
  const u = new URL(req.url, "http://localhost");

  if (req.method === "OPTIONS") { sendJSON(res, 204, {}); return; }   // CORS preflight

  // --- paylaşılan veri API'si ---
  if (u.pathname === "/api/kv") {
    if (req.method === "GET") {
      const key = u.searchParams.get("key") || "";
      sendJSON(res, 200, { value: key in store ? store[key] : null });
      return;
    }
    if (req.method === "POST") {
      let raw = "";
      req.on("data", c => { raw += c; if (raw.length > 1e6) req.destroy(); });
      req.on("end", () => {
        try {
          const { key, value } = JSON.parse(raw);
          if (typeof key === "string") { store[key] = value; persist(); }
          sendJSON(res, 200, { ok: true });
        } catch (e) { sendJSON(res, 400, { ok: false }); }
      });
      return;
    }
    sendJSON(res, 405, { ok: false });
    return;
  }

  // --- oyunun kendisi ---
  if (u.pathname === "/" || u.pathname === "/index.html" || u.pathname === "/cicek-bahcesi.html") {
    fs.readFile(HTML, (err, data) => {
      if (err) { res.writeHead(500); res.end("oyun dosyası bulunamadı"); return; }
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      res.end(data);
    });
    return;
  }

  res.writeHead(404); res.end("yok");
});

server.listen(PORT, () => console.log("Bizim Bahçe → http://localhost:" + PORT));
