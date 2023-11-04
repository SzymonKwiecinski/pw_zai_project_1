import functools
from pathlib import Path

from flask import session, redirect, url_for, current_app
from werkzeug.datastructures import FileStorage

ROOT_DIR = Path(__file__).parent
IMG_DIR = ROOT_DIR / "static" / "img"
CATEGORY_DIR = IMG_DIR / "category"
EVENT_DIR = IMG_DIR / "event"

HASH_TYPE = "pbkdf2-sha256"
ROUND = "29000"
SALT_SIZE = 32


def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for(".login"))

        return route(*args, **kwargs)

    return route_wrapper


def extract_hash_pwd_with_salt(pbkdf2_sha256_output: str) -> str:
    return pbkdf2_sha256_output.split("$", maxsplit=3)[-1]


def add_config_vars_to_pwd(hash_pwd_with_salt: str) -> str:
    return f"${HASH_TYPE}${ROUND}${hash_pwd_with_salt}"


def file_exist(folder: Path, file: str) -> bool:
    full_path = folder / file
    if full_path.exists():
        return True
    return False


def category_exits(file: str) -> bool:
    return file_exist(CATEGORY_DIR, file)


def event_exits(file: str) -> bool:
    return file_exist(EVENT_DIR, file)


def remove_file(folder: Path, file: str) -> None:
    full_path = folder / file
    full_path.unlink()


def remove_file_from_category(file: str) -> None:
    remove_file(CATEGORY_DIR, file)


def remove_file_from_event(file: str) -> None:
    remove_file(EVENT_DIR, file)


def add_file(file: FileStorage, folder: str) -> None:
    current_app.photos.save(file, folder=folder)


def add_file_to_category(file: FileStorage) -> None:
    add_file(file, "category")


def add_file_to_event(file: FileStorage) -> None:
    add_file(file, "event")
