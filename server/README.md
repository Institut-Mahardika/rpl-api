# Server Praktikum API — Institut Mahardika

Server FastAPI untuk sesi praktik pengenalan API.
Data disimpan di `data/db.json` (tidak butuh database eksternal).

---

## Cara menjalankan

### 1. Install dependencies (sekali saja)
```bash
pip install -r requirements.txt
```

### 2. Jalankan server
```bash
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

> `--host 0.0.0.0` agar bisa diakses dari laptop mahasiswa di jaringan yang sama.
> `--reload` agar server restart otomatis kalau ada perubahan kode.

### 3. Cari IP laptop dosen
```bash
# macOS / Linux
ifconfig | grep "inet "

# Windows
ipconfig
```
Cari IP yang dimulai `192.168.x.x` — itulah yang dibagikan ke mahasiswa.

### 4. Bagikan ke mahasiswa
```
Base URL : http://<IP-DOSEN>:3000
Docs     : http://<IP-DOSEN>:3000/docs
Admin UI : http://<IP-DOSEN>:3000/admin/ui
```

---

## Endpoint lengkap

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/status` | Cek server aktif |
| GET | `/api/mahasiswa` | Ambil semua data |
| GET | `/api/mahasiswa/{npm}` | Ambil data by NPM |
| POST | `/api/mahasiswa` | Tambah data baru |
| PUT | `/api/mahasiswa/{npm}` | Update data |
| DELETE | `/api/mahasiswa/{npm}` | Request hapus (→ pending) |
| GET | `/admin/pending` | Lihat permintaan pending |
| POST | `/admin/approve/{npm}` | Setujui hapus |
| POST | `/admin/reject/{npm}` | Tolak hapus |
| DELETE | `/admin/clear-all` | Reset semua data |
| GET | `/admin/ui` | Halaman admin dosen |

---

## Contoh body POST

```json
{
  "npm": "624C0004",
  "nama": "Budi Santoso",
  "prodi": "Teknik Informatika",
  "kelas": "TI-6A",
  "pesan": "Halo dari sesi praktik!"
}
```

## Contoh body PUT (semua field opsional)

```json
{
  "pesan": "Pesan baru saya"
}
```

---

## Struktur folder

```
server-praktikum-api/
├── main.py                  # Entry point FastAPI
├── requirements.txt
├── admin_ui.html            # UI admin dosen
├── data/
│   └── db.json              # Database JSON (auto-created)
└── app/
    ├── __init__.py
    ├── database.py          # Helper baca/tulis db.json
    ├── models.py            # Schema validasi (Pydantic)
    ├── router_mahasiswa.py  # Endpoint /api/mahasiswa
    └── router_admin.py      # Endpoint /admin
```
