ALLOWED_IMAGE_SIGNATURES = {
    "jpeg": (b"\xff\xd8\xff",),
    "png":  (b"\x89PNG\r\n\x1a\n",),
    "gif":  (b"GIF87a", b"GIF89a"),
    "webp": None,  # handled separately below
}

def is_valid_image(data: bytes) -> bool:
    """Check magic bytes to confirm data is a real image."""
    if not data:
        return False

    # JPEG
    if data[:3] == b"\xff\xd8\xff":
        return True
    # PNG
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return True
    # GIF
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return True
    # WebP (RIFF....WEBP)
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return True
    return False
