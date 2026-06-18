#!/usr/bin/env python3
"""
Pick a fixed photo order for the justified gallery that maximizes the
display area of the *smallest* photos (so nothing ends up tiny).

It replicates the JS layout exactly (justified rows, max 3 per row),
tries many random orders plus hill-climbing, and writes:
  _data/photo_aspects.yml   filename -> aspect ratio (w/h)
  _data/photo_order.yml     ordered list of filenames

Run from repo root:  python3 scripts/optimize_photo_order.py
"""
import os, random, math
from PIL import Image, ImageOps

DIR = "images/photography"
W, GAP, TARGET, MAX_PER_ROW = 1200, 8, 300, 3   # must match the page's JS
ITERS, CLIMB = 40000, 40000
BOTTOM_FRAC = 0.10

def load():
    out = {}
    for f in sorted(os.listdir(DIR)):
        if not f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue
        try:
            im = ImageOps.exif_transpose(Image.open(os.path.join(DIR, f)))
            out[f] = im.width / im.height
        except Exception:
            pass
    return out

def rows(order, ar):
    """Replicate the JS justified layout; return rows as (list-of-files, height)."""
    out, row, s = [], [], 0.0
    i, n = 0, len(order)
    while i < n:
        a = order[i]; r = ar[a]
        row.append(a); s += r
        h = (W - (len(row) - 1) * GAP) / s
        filled = h <= TARGET
        if filled or len(row) >= MAX_PER_ROW:
            if filled and len(row) > 1:
                h_prev = (W - (len(row) - 2) * GAP) / (s - r)
                if abs(h_prev - TARGET) < abs(h - TARGET):
                    row.pop(); s -= r
                    out.append((row[:], (W - (len(row) - 1) * GAP) / s))
                    row, s = [a], r
                    i += 1
                    continue
            out.append((row[:], h))
            row, s = [], 0.0
        i += 1
    if row:
        out.append((row[:], min((W - (len(row) - 1) * GAP) / s, TARGET * 1.5)))
    return out

def areas(order, ar):
    """Each photo's display area under the justified layout."""
    res = []
    for files, h in rows(order, ar):
        for a in files:
            res.append(ar[a] * h * h)   # (w = ar*h) * h
    return res

def score(order, ar):
    a = sorted(areas(order, ar))
    k = max(1, int(math.ceil(len(a) * BOTTOM_FRAC)))
    return sum(a[:k]) / k      # mean area of the smallest 10%

def stem_num(f):
    """Return the integer if the filename (without extension) is a pure number."""
    base = os.path.splitext(f)[0]
    return int(base) if base.isdigit() else None

def main():
    ar = load()
    files = list(ar.keys())
    print(f"{len(files)} photos")

    # 1) Free optimization: find the order with the largest "smallest 10%" areas.
    best = sorted(files, key=lambda f: ar[f])   # aspect-sorted seed
    best_s = score(best, ar)
    for _ in range(ITERS):
        random.shuffle(files)
        s = score(files, ar)
        if s > best_s:
            best_s, best = s, files[:]

    cur, cur_s = best[:], best_s
    for _ in range(CLIMB):
        i, j = random.randrange(len(cur)), random.randrange(len(cur))
        cur[i], cur[j] = cur[j], cur[i]
        s = score(cur, ar)
        if s >= cur_s:
            cur_s = s
        else:
            cur[i], cur[j] = cur[j], cur[i]
    if cur_s > best_s:
        best, best_s = cur, cur_s

    # 2) Hoist the *rows* that contain numerically-named photos (1, 2, 3, ...)
    #    to the front, ordered by that number — keeping each row intact so the
    #    optimized layout is preserved.
    layout_rows = rows(best, ar)
    def row_num(files_):
        nums = [stem_num(f) for f in files_ if stem_num(f) is not None]
        return min(nums) if nums else None
    front = sorted([r for r in layout_rows if row_num(r[0]) is not None],
                   key=lambda r: row_num(r[0]))
    others = [r for r in layout_rows if row_num(r[0]) is None]
    best = [f for r in (front + others) for f in r[0]]
    if front:
        print(f"hoisted {len(front)} row(s) containing numbered photos to the front")

    a = sorted(areas(best, ar))
    print(f"smallest-10% mean area: {best_s:,.0f}px²")
    print(f"min {a[0]:,.0f}  median {a[len(a)//2]:,.0f}  max {a[-1]:,.0f}")
    print(f"area ratio max/min: {a[-1]/a[0]:.2f}x")

    with open("_data/photo_aspects.yml", "w") as fh:
        fh.write("# filename: aspect (w/h). Regenerate: python3 scripts/optimize_photo_order.py\n")
        for f in sorted(ar):
            fh.write(f'"{f}": {ar[f]:.4f}\n')
    with open("_data/photo_order.yml", "w") as fh:
        fh.write("# optimized display order. Regenerate: python3 scripts/optimize_photo_order.py\n")
        for f in best:
            fh.write(f'- "{f}"\n')
    print("wrote _data/photo_aspects.yml and _data/photo_order.yml")

if __name__ == "__main__":
    main()
