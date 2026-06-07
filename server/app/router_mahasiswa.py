from fastapi import APIRouter, HTTPException
from app.models import MahasiswaCreate, MahasiswaUpdate
from app import database as db

router = APIRouter(prefix="/api/mahasiswa", tags=["Mahasiswa"])


# GET /api/mahasiswa
@router.get("", summary="Ambil semua data mahasiswa")
def get_all():
    data = db.get_all_mahasiswa()
    return {
        "status": "success",
        "message": f"{len(data)} data mahasiswa ditemukan",
        "total": len(data),
        "data": data
    }


# GET /api/mahasiswa/{npm}
@router.get("/{npm}", summary="Ambil data mahasiswa by NPM")
def get_one(npm: str):
    mahasiswa = db.get_mahasiswa_by_npm(npm)
    if not mahasiswa:
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "message": f"Mahasiswa dengan NPM {npm} tidak ditemukan"}
        )
    return {
        "status": "success",
        "message": "Data ditemukan",
        "data": mahasiswa
    }


# POST /api/mahasiswa
@router.post("", status_code=201, summary="Tambah data mahasiswa baru")
def create(payload: MahasiswaCreate):
    # cek duplikat NPM
    if db.get_mahasiswa_by_npm(payload.npm):
        raise HTTPException(
            status_code=409,
            detail={"status": "error", "message": f"NPM {payload.npm} sudah terdaftar"}
        )

    new_data = payload.model_dump()
    new_data["status"] = "active"
    db.create_mahasiswa(new_data)

    return {
        "status": "success",
        "message": "Data berhasil ditambahkan",
        "data": new_data
    }


# PUT /api/mahasiswa/{npm}
@router.put("/{npm}", summary="Update data mahasiswa")
def update(npm: str, payload: MahasiswaUpdate):
    existing = db.get_mahasiswa_by_npm(npm)
    if not existing:
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "message": f"Mahasiswa dengan NPM {npm} tidak ditemukan"}
        )

    # hanya update field yang dikirim (exclude None)
    updates = payload.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "Tidak ada field yang diperbarui"}
        )

    updated = db.update_mahasiswa(npm, updates)
    return {
        "status": "success",
        "message": "Data berhasil diperbarui",
        "data": updated
    }


# DELETE /api/mahasiswa/{npm}  →  masuk pending, bukan langsung hapus
@router.delete("/{npm}", summary="Request hapus data (butuh persetujuan dosen)")
def request_delete(npm: str):
    mahasiswa = db.get_mahasiswa_by_npm(npm)
    if not mahasiswa:
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "message": f"Mahasiswa dengan NPM {npm} tidak ditemukan"}
        )

    if db.is_pending(npm):
        raise HTTPException(
            status_code=409,
            detail={"status": "error", "message": f"NPM {npm} sudah dalam antrian penghapusan, tunggu persetujuan dosen"}
        )

    db.add_pending(npm, mahasiswa["nama"])
    return {
        "status": "pending",
        "message": f"Permintaan hapus untuk NPM {npm} ({mahasiswa['nama']}) sudah dikirim. Menunggu persetujuan dosen.",
        "data": {"npm": npm, "nama": mahasiswa["nama"]}
    }
