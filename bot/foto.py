"""Prepara le foto di un appartamento per Instagram: ritaglio quadrato 1080x1080, JPEG qualità 90.

Uso: python3 bot/foto.py <cartella_originali> <cartella_post> <foto:posizione> [<foto:posizione> ...]
La posizione (0-1) sposta il ritaglio: 0 = sinistra/alto, 0.5 = centro, 1 = destra/basso.
Le foto vengono salvate in ordine come slide1.jpg, slide2.jpg, ...
"""
import os
import sys

from PIL import Image, ImageOps


def square(path, pos):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    w, h = im.size
    s = min(w, h)
    if w > h:
        left = round((w - s) * pos)
        box = (left, 0, left + s, s)
    else:
        top = round((h - s) * pos)
        box = (0, top, s, top + s)
    return im.crop(box).resize((1080, 1080), Image.LANCZOS)


def main():
    src, dst, items = sys.argv[1], sys.argv[2], sys.argv[3:]
    os.makedirs(dst, exist_ok=True)
    for old in os.listdir(dst):
        if old.startswith("slide") and old.endswith(".jpg"):
            os.remove(os.path.join(dst, old))
    for i, item in enumerate(items, start=1):
        name, pos = item.split(":")
        out = os.path.join(dst, f"slide{i}.jpg")
        square(os.path.join(src, name), float(pos)).save(out, "JPEG", quality=90, optimize=True)
        print(out)


if __name__ == "__main__":
    main()
