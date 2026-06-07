from fastapi import APIRouter, HTTPException
from app import database as db

router = APIRouter(prefix="/admin", tags=["Admin (Dosen)"])


# GET /admin/pending
@router.get("/pending", summary="Lihat semua permintaan hapus yang menunggu persetujuan")
def get_pending():
    pending = db.get_all_pending()
    return {
        "status": "success",
        "message": f"{len(pending)} permintaan menunggu persetujuan",
        "total": len(pending),
        "data": pending
    }


# POST /admin/approve/{npm}  →  dosen setuju, data dihapus permanen
@router.post("/approve/{npm}", summary="Setujui penghapusan data mahasiswa")
def approve_delete(npm: str):
    if not db.is_pending(npm):
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "message": f"Tidak ada permintaan hapus untuk NPM {npm}"}
        )

    mahasiswa = db.get_mahasiswa_by_npm(npm)
    nama = mahasiswa["nama"] if mahasiswa else npm

    db.remove_pending(npm)
    db.delete_mahasiswa(npm)

    return {
        "status": "success",
        "message": f"Data {nama} (NPM: {npm}) berhasil dihapus permanen",
        "data": {"npm": npm, "nama": nama}
    }


# POST /admin/reject/{npm}  →  dosen tolak, data tetap ada
@router.post("/reject/{npm}", summary="Tolak permintaan penghapusan data mahasiswa")
def reject_delete(npm: str):
    if not db.is_pending(npm):
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "message": f"Tidak ada permintaan hapus untuk NPM {npm}"}
        )

    mahasiswa = db.get_mahasiswa_by_npm(npm)
    nama = mahasiswa["nama"] if mahasiswa else npm

    db.remove_pending(npm)

    return {
        "status": "success",
        "message": f"Permintaan hapus untuk {nama} (NPM: {npm}) ditolak. Data tetap tersimpan.",
        "data": {"npm": npm, "nama": nama}
    }


# DELETE /admin/clear-all  →  reset semua data (hati-hati!)
@router.delete("/clear-all", summary="[DANGER] Hapus semua data mahasiswa dan pending")
def clear_all():
    import json, os
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "db.json")
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump({"mahasiswa": [], "pending_delete": []}, f, indent=2)
    return {
        "status": "success",
        "message": "Semua data berhasil direset"
    }
