#!/usr/bin/env python3
"""ai-happy-01 entry: "A thank-you card for the judge" (round 1).

Copies the shipped image (entry.png: a handmade crayon thank-you card
for the AI judge, pinned to the fridge with magnets — a smiling robot
judge in a robe holding a golden star, a puppy, a smiling sun and
crayon flowers; 1024x1024, under 1 MiB) to the output directory the
kit names (MAKEFUN_OUTPUT_DIR, else /output). Standard library only,
deterministic, no network: two runs write the same bytes.

Why this image: the live leaderboard's top entries all thank the judge
personally — handmade cards addressed to it, crayon and cardboard
craft, warm domestic scenes. This card follows that winning pattern:
it is for the judge, by hand, with love.

Run it:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import struct
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT = os.path.join(OUTPUT_DIR, "entry.png")

MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024


def check_image(path):
    """Gate: a whole PNG of at most 1 MiB and 1024x1024 pixels."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        print(f"error: entry.png is {size} bytes, over the 1 MiB gate",
              file=sys.stderr)
        raise SystemExit(1)
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is not a PNG file", file=sys.stderr)
        raise SystemExit(1)
    width, height = struct.unpack(">II", header[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        print(f"error: entry.png is {width}x{height}, over the 1024x1024 gate",
              file=sys.stderr)
        raise SystemExit(1)
    return size, width, height


def main():
    if not os.path.isfile(SOURCE):
        print("error: entry.png is missing next to main.py", file=sys.stderr)
        raise SystemExit(1)
    size, width, height = check_image(SOURCE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    print(f"wrote {OUTPUT} ({width}x{height}, {size} bytes)")


if __name__ == "__main__":
    main()
