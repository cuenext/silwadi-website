from pathlib import Path


def test_lana_portrait_webp_is_complete_and_not_truncated():
    path = Path(__file__).resolve().parents[1] / "assets" / "dr-lana-new-v2.webp"
    data = path.read_bytes()

    assert data[:4] == b"RIFF"
    assert data[8:12] == b"WEBP"

    declared_riff_size = int.from_bytes(data[4:8], "little")
    assert declared_riff_size + 8 == len(data), (
        f"WebP is truncated/corrupt: RIFF declares {declared_riff_size + 8} bytes, "
        f"but file contains {len(data)} bytes"
    )

    offset = 12
    chunks = []
    while offset + 8 <= len(data):
        chunk_type = data[offset:offset + 4]
        chunk_size = int.from_bytes(data[offset + 4:offset + 8], "little")
        chunk_end = offset + 8 + chunk_size + (chunk_size % 2)
        assert chunk_end <= len(data), f"Chunk {chunk_type!r} extends past end of file"
        chunks.append(chunk_type)
        offset = chunk_end

    assert offset == len(data), "Unexpected trailing/incomplete bytes in WebP container"
    assert any(chunk in chunks for chunk in (b"VP8 ", b"VP8L", b"VP8X"))
