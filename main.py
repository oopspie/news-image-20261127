"""Entry point: draw the 27 November 2026 news front page to entry.png.

Writes to MAKEFUN_OUTPUT_DIR when set, otherwise /output. Deterministic:
same code, same bytes, every run.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from draw_entry import draw

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
draw(os.path.join(out_dir, "entry.png"))
