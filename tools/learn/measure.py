#!/usr/bin/env python3
"""
measure.py: measure a creator's videos before you study them (LEARN.md, step 2). Numbers, not guesses.

  python measure.py VIDEO [VIDEO ...] --out learn/measure [--ingest learn/ingest]

For every video it writes <out>/<NN-slug>/:
  measure.json    duration, size, fps; cuts (count, per minute, shot lengths, first cut);
                  loudness (integrated LUFS, true peak); speech share and kept-pause lengths
                  (how tight the creator cuts); palette (6 hex colours + share), brightness, saturation;
                  words per minute if <ingest>/<NN-slug>/words.json exists (from sf.py ingest)
  sheets/         flip-book sheets, 2 fps, 6x4 = 12 s per sheet   (cell k of sheet s = (s-1)*12 + k*0.5 s)
  hook.jpg        the first 3 s at 8 fps, 6x4                      (cell k = k*0.125 s)
and <out>/summary.md: one row per video + the median row. READ every sheet; the numbers only tell
you where to look.

Needs: ffmpeg/ffprobe (or env FFMPEG), numpy, pillow.
"""
import json, os, re, statistics, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "shortform"))
from sf import FF, probe, load_wav_mono, energy_db, speech_threshold, silences, opt  # noqa: E402


def slug(i, path):
    s = re.sub(r"[^a-z0-9]+", "-", os.path.splitext(os.path.basename(path))[0].lower()).strip("-")
    return f"{i:02d}-{s[:40] or 'video'}"


def ff(args):
    return subprocess.run([FF, "-hide_banner", *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def cuts(src, dur):
    r = ff(["-i", src, "-vf", "select='gt(scene,0.3)',showinfo", "-an", "-f", "null", "-"])
    ts = [round(float(t), 3) for t in re.findall(r"pts_time:([\d.]+)", r.stderr)]
    edges = [0.0] + ts + [dur]
    shots = [b - a for a, b in zip(edges, edges[1:]) if b - a > 0.04]
    return {"count": len(ts), "per_min": round(len(ts) / dur * 60, 1) if dur else 0,
            "first": ts[0] if ts else None, "times": ts,
            "shot_mean": round(statistics.mean(shots), 2) if shots else dur,
            "shot_median": round(statistics.median(shots), 2) if shots else dur,
            "shot_min": round(min(shots), 2) if shots else dur,
            "shot_max": round(max(shots), 2) if shots else dur}


def loudness(src):
    r = ff(["-nostats", "-i", src, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", tail)
    p = re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail)
    return {"lufs": float(i.group(1)) if i else None, "true_peak": float(p.group(1)) if p else None}


def speech(src):
    import numpy as np
    x, sr = load_wav_mono(src)
    if not len(x):
        return {}
    db = energy_db(x, sr)
    on = db >= speech_threshold(db)
    idx = np.flatnonzero(on)
    if not len(idx):
        return {"speech_share": 0}
    a, b = idx[0] / 100, idx[-1] / 100
    inner = [s1 - s0 for s0, s1 in silences(db, 0.12) if s0 > a and s1 < b]
    q = lambda p: round(float(np.percentile(inner, p)), 2) if inner else None
    return {"speech_share": round(float(on.mean()), 2), "speech_span": [round(a, 2), round(b, 2)],
            "pauses": len(inner), "pause_median": q(50), "pause_p90": q(90),
            "pause_max": round(max(inner), 2) if inner else None,
            "lead_in": round(a, 2)}


def palette(src, dur, tmp):
    from PIL import Image, ImageStat
    n = 16
    ff(["-v", "error", "-y", "-i", src, "-vf", f"fps={n / max(dur, 0.5):.4f},scale=160:-2,tile=4x4",
        "-frames:v", "1", tmp])
    if not os.path.exists(tmp):
        return {}
    im = Image.open(tmp).convert("RGB")
    q = im.quantize(colors=10, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:30]
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    merged = []                                   # fold near-identical colours (black bars, shadows) together
    for c, k in counts:
        rgb = pal[k * 3:k * 3 + 3]
        hit = next((m for m in merged if sum((x - y) ** 2 for x, y in zip(m[1], rgb)) < 28 ** 2), None)
        if hit: hit[0] += c
        else: merged.append([c, rgb])
    cols = [{"hex": "#%02X%02X%02X" % tuple(rgb), "share": round(c / total, 2)} for c, rgb in merged[:6]]
    hsv = im.convert("HSV")
    st = ImageStat.Stat(hsv)
    os.remove(tmp)
    return {"palette": cols, "brightness": round(st.mean[2] / 255, 2), "saturation": round(st.mean[1] / 255, 2)}


def wpm(words_json, span):
    if not os.path.exists(words_json):
        return None
    with open(words_json, encoding="utf-8") as f:
        j = json.load(f)
    n = sum(len(s["words"]) for s in j.get("segments", []))
    mins = (span[1] - span[0]) / 60 if span else 0
    return round(n / mins) if mins else None


def sheets(src, d):
    sd = os.path.join(d, "sheets")
    os.makedirs(sd, exist_ok=True)
    ff(["-v", "error", "-y", "-i", src, "-vf", "fps=2,scale=320:-2,tile=6x4", "-q:v", "4", os.path.join(sd, "sheet_%02d.jpg")])
    ff(["-v", "error", "-y", "-t", "3", "-i", src, "-vf", "fps=8,scale=320:-2,tile=6x4", "-frames:v", "1", "-q:v", "4",
        os.path.join(d, "hook.jpg")])
    return len([f for f in os.listdir(sd) if f.endswith(".jpg")])


def med(rows, key):
    v = [r[key] for r in rows if isinstance(r.get(key), (int, float))]
    return round(statistics.median(v), 2) if v else "–"


def main(a):
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    out = opt(a, "--out", "learn/measure")
    ingest = opt(a, "--ingest", None)
    vids, skip = [], False
    for x in a:
        if skip:
            skip = False; continue
        if x in ("--out", "--ingest"):
            skip = True; continue
        vids.append(x)
    os.makedirs(out, exist_ok=True)
    rows = []
    for i, src in enumerate(vids, 1):
        name = slug(i, src)
        d = os.path.join(out, name)
        os.makedirs(d, exist_ok=True)
        info = probe(src)
        m = {"name": name, "src": os.path.abspath(src), **info}
        m["cuts"] = cuts(src, info["duration"])
        if info["has_audio"]:
            m["loudness"] = loudness(src)
            m["speech"] = speech(src)
            if ingest:
                m["wpm"] = wpm(os.path.join(ingest, name, "words.json"), m["speech"].get("speech_span"))
        m["look"] = palette(src, info["duration"], os.path.join(d, "_pal.png"))
        m["sheets"] = sheets(src, d)
        with open(os.path.join(d, "measure.json"), "w", encoding="utf-8") as f:
            json.dump(m, f, indent=1)
        sp, ld, lk = m.get("speech", {}), m.get("loudness", {}), m["look"]
        rows.append({"name": name, "dur": round(info["duration"], 1), "size": f"{info['width']}x{info['height']}",
                     "fps": info["fps"], "cuts_min": m["cuts"]["per_min"], "shot_med": m["cuts"]["shot_median"],
                     "pause_med": sp.get("pause_median"), "pause_p90": sp.get("pause_p90"),
                     "lead_in": sp.get("lead_in"), "wpm": m.get("wpm"), "lufs": ld.get("lufs"),
                     "bright": lk.get("brightness"), "sat": lk.get("saturation"),
                     "palette": " ".join(c["hex"] for c in lk.get("palette", [])[:4])})
        r = rows[-1]
        print(f"{name}: {r['dur']}s {r['size']} | {r['cuts_min']} cuts/min, shot {r['shot_med']}s | "
              f"pause {r['pause_med']}s | {r['lufs']} LUFS | {m['sheets']} sheets")
    cols = ["name", "dur", "size", "fps", "cuts_min", "shot_med", "pause_med", "pause_p90", "lead_in", "wpm",
            "lufs", "bright", "sat", "palette"]
    lines = ["# Measurements (LEARN.md step 2)", "",
             "cuts_min = hard cuts per minute · shot_med = median shot length (s) · pause_med / pause_p90 = kept "
             "pauses inside speech (s; small = tight cutting) · lead_in = silence before the first word · "
             "lufs = integrated loudness · bright/sat = 0–1", "",
             "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        lines.append("| " + " | ".join("–" if r[c] is None else str(r[c]) for c in cols) + " |")
    lines.append("| **median** | " + " | ".join(
        "" if c == "size" else str(med(rows, c)) for c in cols[1:-1]) + " | |")
    with open(os.path.join(out, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("->", os.path.join(out, "summary.md"))


if __name__ == "__main__":
    main(sys.argv[1:])
