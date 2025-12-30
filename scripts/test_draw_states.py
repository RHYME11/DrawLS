# scripts/test_draw_states.py

import os
import sys

from src.io_read import read_dat, report_duplicate_transitions
from src.integrate import build_candidate_states_and_resolved_finals
from src.grace_frame import build_frame_block
from src.draw_states import build_states_block


def main() -> None:
  if len(sys.argv) < 3:
    raise RuntimeError(
      "Usage:\n"
      "  python scripts/test_draw_states.py <input.dat> <out.agr>\n"
      "Example:\n"
      "  python scripts/test_draw_states.py data/example.dat out_states.agr"
    )

  in_dat = sys.argv[1]
  out_agr = sys.argv[2]

  transitions = read_dat(in_dat)
  print(f"Transitions read = {len(transitions)}")
  report_duplicate_transitions(transitions)

  candidates, _resolved = build_candidate_states_and_resolved_finals(transitions)
  print(f"Candidate states (Ei + Ef + GS) = {len(candidates)}")

  # Build states block (line objects, no transitions)
  states_block, _band_layout, _state_layouts, (x_min, x_max, y_min, y_max) = build_states_block(candidates)

  # Build frame based on states' data range
  frame_block = build_frame_block(
    x_min_data=x_min,
    x_max_data=x_max,
    y_min_data=y_min,
    y_max_data=y_max,
  )

  agr_text = frame_block + states_block

  out_dir = os.path.dirname(out_agr)
  if out_dir and not os.path.isdir(out_dir):
    os.makedirs(out_dir, exist_ok=True)

  with open(out_agr, "w", encoding="utf-8") as f:
    f.write(agr_text)

  print(f"Wrote: {out_agr}")
  print("Open with: xmgrace " + out_agr)


if __name__ == "__main__":
  main()

