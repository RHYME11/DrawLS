# scripts/test_frame.py

import os
import sys

from src.grace_frame import build_frame_block


def main() -> None:
  if len(sys.argv) < 6:
    raise RuntimeError(
      "Usage:\n"
      "  python scripts/test_frame.py <out.agr|out.agv> <x_min> <x_max> <y_min> <y_max>\n"
      "Example:\n"
      "  python scripts/test_frame.py test_frame.agr -1 20 -50 3500"
    )

  out_path = sys.argv[1]
  x_min = float(sys.argv[2])
  x_max = float(sys.argv[3])
  y_min = float(sys.argv[4])
  y_max = float(sys.argv[5])

  agr_text = build_frame_block(
    x_min_data=x_min,
    x_max_data=x_max,
    y_min_data=y_min,
    y_max_data=y_max,
  )

  out_dir = os.path.dirname(out_path)
  if out_dir and not os.path.isdir(out_dir):
    os.makedirs(out_dir, exist_ok=True)

  with open(out_path, "w", encoding="utf-8") as f:
    f.write(agr_text)

  print(f"Wrote: {out_path}")
  print("Try opening with: xmgrace " + out_path)


if __name__ == "__main__":
  main()

