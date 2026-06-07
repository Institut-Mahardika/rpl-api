# rpl-api — Praktikum API Institut Mahardika

Repository monorepo untuk praktikum pengenalan REST API.

**Mata Kuliah:** Rekayasa Perangkat Lunak  
**Teknologi:** FastAPI (Python) + HTML/JS Vanilla  
**Tools:** Postman Web

---

## 🗂️ Struktur Repository

```
rpl-api/
├── server/          # FastAPI server — dijalankan lokal oleh dosen
│   ├── main.py
│   ├── requirements.txt
│   ├── admin_ui.html
│   ├── data/
│   │   └── db.json
│   └── app/
│       ├── database.py
│       ├── models.py
│       ├── router_mahasiswa.py
│       └── router_admin.py
└── client/          # GitHub Pages — diakses mahasiswa via browser
    ├── index.html                      ← landing page
    ├── client-mahasiswa-template.html  ← file tugas mahasiswa
    ├── panduan-client.html             ← panduan mengerjakan template
    └── panduan-postman.html            ← panduan Postman Web
```

---

## 🖥️ Menjalankan Server (Dosen)

```bash
# Clone repo
git clone https://github.com/institut-mahardika/rpl-api.git
cd rpl-api/server

# Install dependencies (sekali saja)
pip install -r requirements.txt

# Jalankan server — ganti 0.0.0.0 agar bisa diakses satu jaringan
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

Cari IP laptop dosen:
```bash
# macOS / Linux
ifconfig | grep "inet "

# Windows
ipconfig
```

Bagikan ke mahasiswa: `http://<IP-DOSEN>:3000`

| URL | Keterangan |
|-----|-----------|
| `http://<IP>:3000/docs` | Dokumentasi API otomatis (Swagger) |
| `http://<IP>:3000/admin/ui` | Panel admin — approve/reject DELETE |
| `http://<IP>:3000/api/status` | Cek status server |

---

## 📋 Endpoint API

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/status` | Cek server aktif |
| GET | `/api/mahasiswa` | Ambil semua data |
| GET | `/api/mahasiswa/{npm}` | Ambil data by NPM |
| POST | `/api/mahasiswa` | Tambah data baru |
| PUT | `/api/mahasiswa/{npm}` | Update data |
| DELETE | `/api/mahasiswa/{npm}` | Request hapus (→ pending) |
| GET | `/admin/pending` | Lihat antrian hapus |
| POST | `/admin/approve/{npm}` | Setujui hapus |
| POST | `/admin/reject/{npm}` | Tolak hapus |
| DELETE | `/admin/clear-all` | Reset semua data |

---

## 🌐 Client (Mahasiswa)

Diakses via GitHub Pages:

| Halaman | URL |
|---------|-----|
| Landing page | `https://institut-mahardika.github.io/rpl-api/` |
| Template tugas | `https://institut-mahardika.github.io/rpl-api/client-mahasiswa-template.html` |
| Panduan client | `https://institut-mahardika.github.io/rpl-api/panduan-client.html` |
| Panduan Postman | `https://institut-mahardika.github.io/rpl-api/panduan-postman.html` |

---

## ⚙️ Setup GitHub Pages

1. Buka **Settings** repository → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` — Folder: `/client`
4. Klik **Save** — tunggu 1–2 menit
5. URL live: `https://institut-mahardika.github.io/rpl-api/`
