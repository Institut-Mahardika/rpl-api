import json
import os
from typing import Any
import threading

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "db.json")


def _read() -> dict:
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


_lock = threading.Lock()

def _write(data: dict) -> None:
    with _lock:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# ---------- mahasiswa ----------

def get_all_mahasiswa() -> list:
    return _read()["mahasiswa"]


def get_mahasiswa_by_npm(npm: str) -> dict | None:
    for m in _read()["mahasiswa"]:
        if m["npm"] == npm:
            return m
    return None


def create_mahasiswa(data: dict) -> dict:
    db = _read()
    db["mahasiswa"].append(data)
    _write(db)
    return data


def update_mahasiswa(npm: str, updates: dict) -> dict | None:
    db = _read()
    for i, m in enumerate(db["mahasiswa"]):
        if m["npm"] == npm:
            db["mahasiswa"][i].update(updates)
            _write(db)
            return db["mahasiswa"][i]
    return None


def delete_mahasiswa(npm: str) -> bool:
    db = _read()
    before = len(db["mahasiswa"])
    db["mahasiswa"] = [m for m in db["mahasiswa"] if m["npm"] != npm]
    if len(db["mahasiswa"]) < before:
        _write(db)
        return True
    return False


# ---------- pending delete ----------

def get_all_pending() -> list:
    return _read()["pending_delete"]


def add_pending(npm: str, nama: str) -> dict:
    db = _read()
    # hindari duplikat
    if not any(p["npm"] == npm for p in db["pending_delete"]):
        entry = {"npm": npm, "nama": nama}
        db["pending_delete"].append(entry)
        _write(db)
        return entry
    return next(p for p in db["pending_delete"] if p["npm"] == npm)


def remove_pending(npm: str) -> bool:
    db = _read()
    before = len(db["pending_delete"])
    db["pending_delete"] = [p for p in db["pending_delete"] if p["npm"] != npm]
    if len(db["pending_delete"]) < before:
        _write(db)
        return True
    return False


def is_pending(npm: str) -> bool:
    return any(p["npm"] == npm for p in _read()["pending_delete"])
