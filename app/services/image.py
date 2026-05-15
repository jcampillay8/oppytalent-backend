import re
from urllib.parse import quote

DRIVE_THUMBNAIL = "https://drive.google.com/thumbnail?id={id}&sz=w1000"
DRIVE_FILE_PATTERN = re.compile(r"drive\.google\.com/file/d/([^/]+)")
DRIVE_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{25,}$")
PROXY_BASE = "/api/v1/images/proxy"


def _drive_to_proxy(drive_url: str) -> str:
    return f"{PROXY_BASE}?url={quote(drive_url, safe='')}"


def parse_image_url(value: str | None) -> str | None:
    if not value:
        return None

    stripped = value.strip()

    if PROXY_BASE in stripped:
        return stripped

    if stripped.startswith(("http://", "https://", "data:")):
        m = DRIVE_FILE_PATTERN.search(stripped)
        if m:
            return _drive_to_proxy(DRIVE_THUMBNAIL.format(id=m.group(1)))
        if "drive.google.com/thumbnail" in stripped or "drive.google.com/uc" in stripped:
            return _drive_to_proxy(stripped)
        return stripped

    if DRIVE_ID_PATTERN.match(stripped):
        return _drive_to_proxy(DRIVE_THUMBNAIL.format(id=stripped))

    return stripped
