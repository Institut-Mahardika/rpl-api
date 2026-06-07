from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

from app.router_mahasiswa import router as mahasiswa_router
from app.router_admin import router as admin_router

# ── App ────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="API Praktikum — Institut Mahardika",
    description=(
        "Server lokal untuk praktikum pengenalan API.\n\n"
        "**Endpoint Mahasiswa** — CRUD data diri.\n\n"
        "**Endpoint Admin** — approve/reject permintaan hapus."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    redirect_slashes=False,
)

# ── CORS — izinkan semua origin (karena jaringan lokal kelas) ───────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────
app.include_router(mahasiswa_router)
app.include_router(admin_router)


# ── Root & Status ──────────────────────────────────────────────────────────
@app.get("/", tags=["Status"])
def root():
    return {
        "status": "online",
        "message": "Server Praktikum API — Institut Mahardika",
        "docs": "/docs",
        "admin_ui": "/admin/ui",
        "endpoints": {
            "mahasiswa": "/api/mahasiswa",
            "admin": "/admin/pending"
        }
    }


@app.get("/api/status", tags=["Status"])
def api_status():
    from app import database as db
    total = len(db.get_all_mahasiswa())
    pending = len(db.get_all_pending())
    return {
        "status": "online",
        "message": "Server aktif dan siap menerima request",
        "data": {
            "total_mahasiswa": total,
            "pending_delete": pending
        }
    }


# ── Admin UI ───────────────────────────────────────────────────────────────
@app.get("/admin/ui", response_class=HTMLResponse, tags=["Admin (Dosen)"],
         summary="Halaman UI admin untuk dosen")
def admin_ui():
    html_path = os.path.join(os.path.dirname(__file__), "admin_ui.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()
