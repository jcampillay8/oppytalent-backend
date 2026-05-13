import re

DRIVE_THUMBNAIL = "https://drive.google.com/thumbnail?id={id}&sz=w1000"
DRIVE_FILE_PATTERN = re.compile(r"drive\.google\.com/file/d/([^/]+)")
DRIVE_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{25,}$")


def parse_image_url(value: str | None) -> str | None:
    if not value:
        return None

    stripped = value.strip()

    if stripped.startswith(("http://", "https://", "data:")):
        m = DRIVE_FILE_PATTERN.search(stripped)
        if m:
            return DRIVE_THUMBNAIL.format(id=m.group(1))
        return stripped

    if DRIVE_ID_PATTERN.match(stripped):
        return DRIVE_THUMBNAIL.format(id=stripped)

    return stripped
