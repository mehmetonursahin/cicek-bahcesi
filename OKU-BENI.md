# 🌿 Bizim Bahçe — Kurulum ve Online Oynama

Oyun tek bir HTML dosyası (`cicek-bahcesi.html`). İki kişinin **aynı bahçeyi
paylaşması** için küçük bir sunucu gerekiyor; o da hazır (`server.py` veya `server.js`).

- **Özel veriler** (rolün, çantandaki çiçekler) → kendi cihazında saklanır.
- **Paylaşılan veriler** (konum, vazo, posta kutusu) → sunucuda saklanır ve
  `data.json` dosyasına yazılır; sunucu kapanıp açılsa da kaybolmaz.

---

## 1) Bilgisayarında çalıştır (test için)

Bilgisayarında **Python varsa** (sende var) hiçbir kurulum gerekmez:

```bash
cd cicek-bahcesi
python server.py
```

Sonra tarayıcıda **http://localhost:3000** adresini aç. Bu kadar.

> Node.js kurmak istersen aynı şeyi `node server.js` ile de çalıştırabilirsin
> (Render gibi sunucularda Node sürümü kullanılacak).

---

## 2) Aynı ev ağındaysanız (en hızlı, bedava)

İkiniz **aynı Wi‑Fi’deyseniz** internete kurulum yapmadan oynayabilirsiniz:

1. Sunucuyu çalıştıran bilgisayarın yerel IP’sini öğren
   (Mac: `Sistem Ayarları → Wi‑Fi → Ayrıntılar`, örn. `192.168.1.23`).
2. Telefonlardan **http://192.168.1.23:3000** adresini açın.
3. Biriniz “👧 Ben”, diğeriniz “🧑 Sevgilim” seçsin. Birbirinizi bahçede görürsünüz 💞

---

## 3) Her yerden online oynamak (sevgilin başka şehirdeyse)

Oyunu internette bir yere koymalısın. Sunucu sıradan bir Node uygulaması olduğu
için ücretsiz kataloglara kolayca girer. Örnek: **Render.com** (ücretsiz).

1. Bu klasördeki 4 dosyayı bir **GitHub deposuna** koy
   (`cicek-bahcesi.html`, `server.js`, `package.json`, `OKU-BENI.md`).
2. [render.com](https://render.com) → **New → Web Service** → GitHub deponu seç.
3. Ayarlar:
   - **Build Command:** `npm install`
   - **Start Command:** `node server.js`
4. **Deploy** de. Sana `https://...onrender.com` gibi bir adres verir.
   O adresi sevgilinle paylaş; ikiniz de açın. 🎉

Aynı mantık **Railway, Replit, Fly.io** gibi yerlerde de geçerli: tek
gereken `node server.js` komutunu çalıştırması.

### ⚠️ ÇOK ÖNEMLİ — veri kalıcılığı (mektuplar/çiçekler)

**1) `data.json`'ı ASLA commit etme.** (Zaten `.gitignore`'da.)
Eğer git'e eklersen, her `git push` → her deploy canlı veriyi **commit'teki eski
hâline döndürür**; yani sevgilinle biriktirdiğiniz mektuplar/çiçekler sıfırlanır.
İstemediğin tam da bu. Commit etme, sorun olmaz.

**2) Ama tek başına bu yetmez.** Render gibi ücretsiz planlarda disk
**geçicidir** (ephemeral): sen yeni kod push'ladığında ya da sunucu uyku sonrası
yeniden kalktığında `data.json` yine **silinir**. Yani "her server update'de
değişmesin" demek için **kalıcı bir yere** yazman gerekir.

**Kalıcı çözüm (önerilen) — kalıcı disk:**
Sunucu, `DATA_DIR` ortam değişkenini destekliyor. Render'da:
1. Servisine bir **Disk** ekle (Mount Path: `/var/data`).
2. **Environment** kısmına `DATA_DIR = /var/data` ekle.
3. Artık `data.json` o diske yazılır; deploy/restart'ta **silinmez.** ✅

> Render'da kalıcı disk genelde ücretli plan ister (aylık ~birkaç dolar).
> Tamamen ücretsiz ve kalıcı istiyorsan, paylaşımı bir veritabanına
> (Firebase / Supabase / Upstash) taşıyabiliriz — kod buna hazır, istersen ayarlarım.

**Yedek alma:** İstediğin an `https://<adres>/api/kv?key=shared_mailbox` ve
`...?key=shared_vase` adreslerini açıp çıkan metni bir yere kopyalayarak
mektupların/çiçeklerin yedeğini elle saklayabilirsin.

---

## Dosyalar
| Dosya | Görev |
|---|---|
| `cicek-bahcesi.html` | Oyunun kendisi (tarayıcıda çalışır) |
| `server.py` | Python sunucu — kurulum gerektirmez, yerelde test için ideal |
| `server.js` | Node sunucu — ücretsiz hosting’ler için |
| `package.json` | Node için başlangıç ayarı (`npm start`) |
| `data.json` | Paylaşılan veriler (ilk çalıştırmada otomatik oluşur) |
