# THE WORLD TODAY — Friday, 27 November 2026

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/oopspie/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/oopspie/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

Built for the make.fun `news-image-20261127` competition: https://make.fun/bounty/news-image-20261127

A newspaper front page drawn entirely in code with Pillow. No photos,
no downloaded images, no network calls: every pictogram on the page is
built from lines, arcs, ellipses and polygons in `draw_entry.py`.

## The five stories

1. **Lead — Energy markets.** Iran's Revolutionary Guards say two
   tankers struck mines in the Strait of Hormuz. Brent crude settles at
   $96.57, up about 8% over three sessions.
2. **Kuwait.** A drone attack on 26 Nov hit a Kuwaiti air-defence site,
   killing two Italian technicians. Italy says the drones were of
   Iranian origin; Iran denies responsibility.
3. **Brussels.** The special EU summit ended early on 27 Nov with no
   decision on a €45 billion Ukraine loan, pushed to December. The
   2028–2034 EU budget also unresolved.
4. **Ukraine.** Ukrainian intelligence says North Korea has suspended
   KN-23 missile deliveries to Russia.
5. **London.** The UK government is contacting 100,000 retired
   military personnel over military readiness, for the first time since
   the Cold War.

Every number on the page comes from the verified facts above; nothing
else was invented.

## How to run

```bash
python3 main.py
```

This writes `entry.png` (1024×1024) to the directory named by the
`MAKEFUN_OUTPUT_DIR` environment variable, defaulting to `/output`.
For example:

```bash
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

Requires Python 3 and Pillow (`pip install pillow`). The DejaVu fonts
shipped with the system are used; no fonts are bundled.

## Determinism

The program reads no clock, no network and no random source, so two
runs produce byte-identical PNG files. You can check with:

```bash
MAKEFUN_OUTPUT_DIR=/tmp/run1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/run2 python3 main.py
sha256sum /tmp/run1/entry.png /tmp/run2/entry.png
```

## Layout

- Masthead `THE WORLD TODAY`, dated Friday, 27 November 2026.
- Lead story across the top with a large tanker-and-mine pictogram.
- The other four stories in a 2×2 grid, each with its own small
  pictogram: a quadcopter drone, a ring of EU stars, a missile, and a
  soldier's helmet above a call-up letter.
- Newsprint palette: off-white paper, black ink, one red accent.
