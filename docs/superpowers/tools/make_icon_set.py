#!/usr/bin/env python3
"""Favicon standard kit: SVG mark -> favicon.ico (BMP 16+32) + apple-touch-icon.png (180).

Renders with headless Chrome (real SVG engine) on an opaque plate of the
site's ground color, always in the canonical light rendition (dark media
blocks stripped), converts via sips to BMP for pixel access, packs classic
32bpp BMP-ICO entries. Stdlib only.

usage: make_icon_set.py <mark.svg> <outdir> <plate-hex e.g. f7f5ef> [pad-percent]
"""
import os, struct, subprocess, sys, tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def strip_dark_media(svg_text):
    out, i = [], 0
    while True:
        j = svg_text.find("@media", i)
        if j < 0:
            out.append(svg_text[i:])
            break
        head = svg_text[j:svg_text.find("{", j)]
        if "prefers-color-scheme" not in head or "dark" not in head:
            k = svg_text.find("{", j) + 1
            out.append(svg_text[i:k]); i = k
            continue
        out.append(svg_text[i:j])
        depth, k = 0, svg_text.find("{", j)
        while k < len(svg_text):
            if svg_text[k] == "{": depth += 1
            elif svg_text[k] == "}":
                depth -= 1
                if depth == 0: break
            k += 1
        i = k + 1
    return "".join(out)


def shot(svg, size, plate, pad, out_png):
    with tempfile.TemporaryDirectory() as td:
        light = os.path.join(td, "light.svg")
        open(light, "w").write(strip_dark_media(open(svg).read()))
        inner = round(size * (100 - 2 * pad) / 100)
        off = (size - inner) / 2
        html = os.path.join(td, "w.html")
        open(html, "w").write(
            f'<!doctype html><style>html,body{{margin:0;width:{size}px;height:{size}px;'
            f'background:#{plate};overflow:hidden}}img{{position:absolute;left:{off}px;top:{off}px}}</style>'
            f'<img src="file://{light}" width="{inner}" height="{inner}">'
        )
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             f"--screenshot={out_png}", f"--window-size={size},{size}",
             "--force-color-profile=srgb", f"file://{html}"],
            check=True, capture_output=True)


def bmp_pixels(path):
    d = open(path, "rb").read()
    off = struct.unpack("<I", d[10:14])[0]
    w, h = struct.unpack("<ii", d[18:26])
    bpp = struct.unpack("<H", d[28:30])[0]
    assert bpp in (24, 32), f"bpp {bpp}"
    step = bpp // 8
    row = ((w * step + 3) // 4) * 4
    px = []
    for y in range(abs(h) - 1, -1, -1) if h > 0 else range(abs(h)):
        r = []
        base = off + y * row
        for x in range(w):
            b, g, rr = d[base + x * step:base + x * step + 3]
            r.append((rr, g, b))
        px.append(r)
    return w, px


def ico_entry(size, rows):
    header = struct.pack("<IiiHHIIiiII", 40, size, size * 2, 1, 32, 0, 0, 0, 0, 0, 0)
    xor = bytearray()
    for y in range(size - 1, -1, -1):
        for r, g, b in rows[y]:
            xor += bytes((b, g, r, 0xFF))
    mask = bytes((((size + 31) // 32) * 4) * size)
    return header + bytes(xor) + mask


def main(svg, outdir, plate, pad):
    with tempfile.TemporaryDirectory() as td:
        entries = []
        for size in (16, 32):
            p = os.path.join(td, f"{size}.png")
            shot(svg, size, plate, pad, p)
            b = os.path.join(td, f"{size}.bmp")
            subprocess.run(["sips", "-s", "format", "bmp", p, "--out", b],
                           check=True, capture_output=True)
            w, rows = bmp_pixels(b)
            assert w == size
            entries.append((size, ico_entry(size, rows)))
        ico = struct.pack("<HHH", 0, 1, len(entries))
        offset = 6 + 16 * len(entries)
        body = b""
        for size, blob in entries:
            ico += struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(blob), offset)
            body += blob
            offset += len(blob)
        open(os.path.join(outdir, "favicon.ico"), "wb").write(ico + body)
        shot(svg, 180, plate, pad, os.path.join(outdir, "apple-touch-icon.png"))
    print(f"kit -> {outdir} (plate #{plate}, pad {pad}%)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else 12.0)
