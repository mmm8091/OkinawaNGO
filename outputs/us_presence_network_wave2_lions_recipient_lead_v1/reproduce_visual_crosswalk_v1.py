from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image
from scipy.fftpack import dct


ROOT = Path(__file__).resolve().parent
LEFT = ROOT / "artifacts" / "lions_okinawa_military_shop_child_cancer_image.png"
RIGHT = ROOT / "artifacts" / "dvids_8251055_group_photo.jpg"


def phash64(path: Path) -> tuple[str, np.ndarray, tuple[int, int]]:
    with Image.open(path) as image:
        dimensions = image.size
        gray = image.convert("L").resize((32, 32), Image.Resampling.LANCZOS)
        pixels = np.asarray(gray, dtype=float)
    coefficients = dct(dct(pixels, axis=0, norm="ortho"), axis=1, norm="ortho")[:8, :8]
    flattened = coefficients.flatten()
    median = np.median(flattened[1:])
    bits = flattened > median
    value = 0
    for bit in bits:
        value = (value << 1) | int(bit)
    return f"{value:016x}", bits, dimensions


left_hash, left_bits, left_dimensions = phash64(LEFT)
right_hash, right_bits, right_dimensions = phash64(RIGHT)
distance = int(np.count_nonzero(left_bits != right_bits))

print(f"left_dimensions={left_dimensions[0]}x{left_dimensions[1]}")
print(f"right_dimensions={right_dimensions[0]}x{right_dimensions[1]}")
print(f"left_phash64={left_hash}")
print(f"right_phash64={right_hash}")
print(f"hamming_distance={distance}/64")
