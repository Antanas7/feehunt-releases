"""At-rest encryption for the Gmail OAuth token, using Windows DPAPI (per-user).

The saved OAuth token (access + refresh) can read the user's whole Gmail, so it
should not sit on disk as plain text. On Windows we wrap it with DPAPI
(CryptProtectData), which ties the ciphertext to the current Windows user
account: another user on the same machine — or the file copied elsewhere —
cannot decrypt it. No password to manage and no third-party dependency (DPAPI is
reached through ctypes).

seal()/unseal() are symmetric. A short magic header marks DPAPI-wrapped blobs so
older plain-text tokens (written by builds before this change) are still read
transparently and re-sealed on the next save. If DPAPI is unavailable — e.g. a
non-Windows dev machine — we fall back to plain text so the app keeps working.
"""

from __future__ import annotations

import sys

# Marks a DPAPI-wrapped blob. Anything without this prefix is treated as legacy
# plain-text (older build) or a non-Windows fallback.
_MAGIC = b"FHDPAPI1\n"

# CRYPTPROTECT_UI_FORBIDDEN — never pop a UI prompt; just fail if it can't run
# silently (FeeHunt's scan runs headless in a subprocess).
_CRYPTPROTECT_UI_FORBIDDEN = 0x01


def is_available() -> bool:
    """True when Windows DPAPI can be used on this machine."""
    if sys.platform != "win32":
        return False
    try:
        import ctypes

        return hasattr(ctypes, "windll") and bool(ctypes.windll.crypt32)
    except Exception:
        return False


def _dpapi(func_name: str, data: bytes) -> bytes:
    """Call CryptProtectData / CryptUnprotectData (same signature) on `data`."""
    import ctypes
    from ctypes import wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [
            ("cbData", wintypes.DWORD),
            ("pbData", ctypes.POINTER(ctypes.c_char)),
        ]

    buffer = ctypes.create_string_buffer(data, len(data))
    blob_in = DATA_BLOB(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_char)))
    blob_out = DATA_BLOB()

    func = getattr(ctypes.windll.crypt32, func_name)
    ok = func(
        ctypes.byref(blob_in),  # pDataIn
        None,                   # szDataDescr
        None,                   # pOptionalEntropy
        None,                   # pvReserved
        None,                   # pPromptStruct
        _CRYPTPROTECT_UI_FORBIDDEN,
        ctypes.byref(blob_out),
    )
    if not ok:
        raise OSError(f"{func_name} failed (error {ctypes.get_last_error()})")
    try:
        return ctypes.string_at(blob_out.pbData, int(blob_out.cbData))
    finally:
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)


def seal(text: str) -> bytes:
    """Encrypt `text` for storage. Returns bytes to write to disk. Falls back to
    plain UTF-8 (no magic header) if DPAPI is unavailable or errors."""
    raw = text.encode("utf-8")
    if is_available():
        try:
            return _MAGIC + _dpapi("CryptProtectData", raw)
        except Exception:
            return raw
    return raw


def unseal(blob: bytes) -> str:
    """Decrypt bytes produced by seal(). Transparently passes through legacy
    plain-text content that has no magic header."""
    if blob.startswith(_MAGIC):
        return _dpapi("CryptUnprotectData", blob[len(_MAGIC):]).decode("utf-8")
    return blob.decode("utf-8")
