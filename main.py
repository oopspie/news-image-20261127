"""Entry point: render the front page to entry.png.

The output directory comes from the MAKEFUN_OUTPUT_DIR environment
variable and defaults to /output. The image is written by this program;
nothing is copied in from elsewhere.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from draw_entry import save_entry


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = save_entry(output_dir)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
