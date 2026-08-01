import json
import os
import secrets
import string
from pathlib import Path

from algos.hashing_sha_256.sha_256 import sha_256
from algos.encrypt_aes_256.aes_256 import aes_256
from algos.decrypt_aes_256.decrypt_aes_256 import decrypt_aes_256
from validat_data import validator

ROOT_DIR = Path(__file__).resolve().parent.parent
USER_FILE = ROOT_DIR / ".user.json"
VAULT_FILE = ROOT_DIR / ".passwords.json"


def master_key(password: str) -> str:
    return sha_256(password, flag=1)[:32]


def user_file_exists() -> bool:
    return USER_FILE.exists()


def validate_credentials(login: str, password: str):
    err = validator.validate_login(login)
    if err:
        return err
    err = validator.validate_password(password)
    if err:
        return err
    return None


def create_user(login: str, password: str):
    err = validate_credentials(login, password)
    if err:
        raise ValueError(err)
    data = {"login": sha_256(login), "password": sha_256(password)}
    with open(USER_FILE, "w") as f:
        json.dump(data, f, indent=2)
    try:
        os.chmod(USER_FILE, 0o444)
    except OSError:
        pass


def authenticate(login: str, password: str) -> str:
    if not USER_FILE.exists():
        raise ValueError("No account found. Create an account first.")
    err = validator.validat_password_login(login, password)
    if err:
        raise ValueError(err)
    return master_key(password)


# ---------------------------------------------------------------------------
# Vault (password manager data)
# ---------------------------------------------------------------------------

def load_vault() -> list:
    if not VAULT_FILE.exists():
        return []
    try:
        with open(VAULT_FILE, "r") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_vault(entries: list):
    with open(VAULT_FILE, "w") as f:
        json.dump(entries, f, indent=2)
    try:
        os.chmod(VAULT_FILE, 0o600)
    except OSError:
        pass


def strip_padding(plain: str) -> str:
    if not plain:
        return plain
    run_char = plain[-1]
    run_len = 0
    for ch in reversed(plain):
        if ch == run_char:
            run_len += 1
        else:
            break
    if run_len >= 16:
        return plain
    p = 16 - run_len
    j, k = p // 4, p % 4
    expected = 16 - (j + 1) * k
    if expected == ord(run_char):
        return plain[:-run_len]
    return plain


def encrypt_value(text: str, key: str) -> str:
    return aes_256(text, key)


def decrypt_value(cipher: str, key: str) -> str:
    if not cipher:
        return ""
    return strip_padding(decrypt_aes_256(cipher, key))


def decrypt_entries(entries: list, key: str) -> list:
    out = []
    for e in entries:
        out.append({
            "platform name": e.get("platform name", ""),
            "email or user name": decrypt_value(e.get("email or user name", ""), key),
            "password": decrypt_value(e.get("password", ""), key),
        })
    return out


def add_entry(platform: str, email: str, password: str, key: str) -> list:
    entries = load_vault()
    entries.append({
        "platform name": platform,
        "email or user name": encrypt_value(email, key),
        "password": encrypt_value(password, key),
    })
    save_vault(entries)
    return entries


def update_entry(index: int, platform: str, email: str, password: str, key: str) -> list:
    entries = load_vault()
    entries[index] = {
        "platform name": platform,
        "email or user name": encrypt_value(email, key),
        "password": encrypt_value(password, key),
    }
    save_vault(entries)
    return entries


def delete_entry(index: int) -> list:
    entries = load_vault()
    if 0 <= index < len(entries):
        entries.pop(index)
        save_vault(entries)
    return entries


def generate_password(length: int = 16) -> str:
    length = max(8, min(length, 32))
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    special = "!@#$&*-+=_"
    pool = lower + upper + digits + special
    pw = [secrets.choice(lower), secrets.choice(upper),
          secrets.choice(digits), secrets.choice(special)]
    for _ in range(length - 4):
        pw.append(secrets.choice(pool))
    secrets.SystemRandom().shuffle(pw)
    return "".join(pw)
