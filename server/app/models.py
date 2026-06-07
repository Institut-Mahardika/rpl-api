from pydantic import BaseModel, Field
from typing import Optional


class MahasiswaCreate(BaseModel):
    npm: str = Field(..., min_length=8, max_length=10, pattern=r"^\d+[A-Z]?\d*$",
                     description="NPM mahasiswa, contoh: 624C0004")
    nama: str = Field(..., min_length=2, max_length=100)
    prodi: str = Field(..., min_length=2, max_length=100)
    kelas: str = Field(..., min_length=1, max_length=20)
    pesan: Optional[str] = Field(None, max_length=500)

    model_config = {
        "json_schema_extra": {
            "example": {
                "npm": "624C0004",
                "nama": "Budi Santoso",
                "prodi": "Teknik Informatika",
                "kelas": "TI-6A",
                "pesan": "Halo dari sesi praktik API!"
            }
        }
    }


class MahasiswaUpdate(BaseModel):
    nama: Optional[str] = Field(None, min_length=2, max_length=100)
    prodi: Optional[str] = Field(None, min_length=2, max_length=100)
    kelas: Optional[str] = Field(None, min_length=1, max_length=20)
    pesan: Optional[str] = Field(None, max_length=500)

    model_config = {
        "json_schema_extra": {
            "example": {
                "pesan": "Pesan saya diperbarui"
            }
        }
    }


class MahasiswaResponse(BaseModel):
    npm: str
    nama: str
    prodi: str
    kelas: str
    pesan: Optional[str] = None
    status: str = "active"


class StandardResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict | list] = None
