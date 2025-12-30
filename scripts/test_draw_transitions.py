# scripts/test_draw_transition.py

import os
import sys
from typing import Tuple

from src.io_read import read_dat, report_duplicate_transitions
from src.integrate import build_candidate_states_and_resolved_finals
from src.grace_frame import build_frame_block
from src.draw_states import build_states_block
from src.draw_transitions import build_transitions_block


def _merge_ranges(
  r1: Tuple[float, float, float, float],
  r2: Tuple[float, float, float, float]
) -> Tuple[float, float, float, float]:
  x1, x2, y1, y2 = r1
  a1, a2, b1, b2 = r2
  return (min(x1, a1), max(x2, a2), min(y1, b1), max(y2, b2))


def main() -> None:
  if len(sys.argv) < 2:
    raise RuntimeError(
      "Usage:\n"
      "  python scripts/test_draw_transition.py <input.dat> [output.agr] [--no-label]\n"
      "Example:\n"
      "  python scripts/test_draw_transition.py data/example.dat\n"
      "  python scripts/test_draw_transition.py data/example.dat out.agr\n"
      "  python scripts/test_draw_transition.py data/example.dat out.agr --no-label\n"
    )

  in_dat = sys.argv[1]

  # Default output
  out_agr = "output.agr"
  no_label = False

  # parse optional args (simple, no argparse)
  # [EDIT L33-L52] optional output + flag
  for arg in sys.argv[2:]:
    if arg == "--no-label":
      no_label = True
    else:
      out_agr = arg

  transitions = read_dat(in_dat)
  print(f"Transitions read = {len(transitions)}")
  report_duplicate_transitions(transitions)

  candidates, resolved = build_candidate_states_and_resolved_finals(transitions)
  print(f"Candidate states (Ei + Ef + GS) = {len(candidates)}")
  print(f"Resolved transitions = {len(resolved)}")

  # 1) states
  states_block, _band_layout, state_layouts, r_states = build_states_block(candidates)

  # 2) transitions
  trans_block, r_trans = build_transitions_block(
    resolved=resolved,
    state_layouts=state_layouts,
    draw_gamma_label=(not no_label),
  )

  # 3) frame based on merged range (avoid cropping slanted/dashed parts)
  r_all = _merge_ranges(r_states, r_trans)
  x_min, x_max, y_min, y_max = r_all
  frame_block = build_frame_block(
    x_min_data=x_min,
    x_max_data=x_max,
    y_min_data=y_min,
    y_max_data=y_max,
  )

  agr_text = frame_block + states_block + trans_block

  out_dir = os.path.dirname(out_agr)
  if out_dir and not os.path.isdir(out_dir):
    os.makedirs(out_dir, exist_ok=True)

  with open(out_agr, "w", encoding="utf-8") as f:
    f.write(agr_text)

  print(f"Wrote: {out_agr}")
  print("Open with: xmgrace " + out_agr)


if __name__ == "__main__":
  main()

