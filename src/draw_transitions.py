# src/draw_transitions.py
# ============================================================
# Draw transitions (gamma) using ONLY StateLayout geometry
# - inside-band: vertical arrow at xc
# - cross-band: fixed angle, direction decided by relative x (left/right)
# - all transitions are ARROW objects
# - final level dashed extension uses x_end
# ============================================================

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

from src.data_model import Transition
from src.draw_states import StateLayout, STATE_LINECOLOR, LABEL_JUST

# ----------------------------
# Rules / Config
# ----------------------------

# C0) Fixed linewidth for ALL gamma lines
GAMMA_LINEWIDTH = 2.0  # [EDIT L22]
GAMMA_LINESTYLE = 1
GAMMA_LINECOLOR = STATE_LINECOLOR

# Small y padding so arrow endpoints don't sit exactly on the level line
Y_PAD = 14.0

# C3 label placement
DRAW_GAMMA_LABEL = True
LABEL_CHAR_SIZE = 0.80
LABEL_DX = 0.0
LABEL_DY = 10.0

# Final dashed extension for levels (C2.4)
FINAL_EXT_LINESTYLE = 3
FINAL_EXT_LINEWIDTH = 2.0
FINAL_EXT_LINECOLOR = STATE_LINECOLOR

# Small inward offset from level edge to avoid overlap with arrow/level
# Unit: world x coordinate
EDGE_EPS = 0.05

# C2.2 slot step (world x units)
SLOT_JITTER = 0.5

# C2 fixed tilt angle (degrees)
# If theta=30, tan(theta)=0.577..., dx = dy / tan(theta) gives a 60-degree-ish line in x-y.
CROSS_ANGLE_DEG = 89.95  # [EDIT L49]
CROSS_TAN = math.tan(math.radians(CROSS_ANGLE_DEG))  # [EDIT L50]
if CROSS_TAN == 0.0:
  raise ValueError("CROSS_ANGLE_DEG leads to tan=0, invalid for cross-band slope.")


@dataclass
class DataRange:
  x_min: float = float("inf")
  x_max: float = float("-inf")
  y_min: float = float("inf")
  y_max: float = float("-inf")

  def update_point(self, x: float, y: float) -> None:
    self.x_min = min(self.x_min, x)
    self.x_max = max(self.x_max, x)
    self.y_min = min(self.y_min, y)
    self.y_max = max(self.y_max, y)

  def update_segment(self, x0: float, y0: float, x1: float, y1: float) -> None:
    self.update_point(x0, y0)
    self.update_point(x1, y1)


def _agr_arrow_object(
  x0: float, y0: float, x1: float, y1: float,
  linewidth: float, linestyle: int, color: int
) -> str:
  """
  Draw one LINE object with arrow head in world coordinates on g0.
  (Grace arrow style is controlled by 'line arrow' fields.)
  """
  # [EDIT L80] Switch from '@with arrow' to '@with line' + arrow properties.
  lines: List[str] = []
  lines.append("@with line")                              # [EDIT L82]
  lines.append("@    line on")
  lines.append("@    line loctype world")
  lines.append("@    line g0")
  lines.append(f"@    line {x0:.6f}, {y0:.6f}, {x1:.6f}, {y1:.6f}")
  lines.append(f"@    line linewidth {linewidth:.3f}")
  lines.append(f"@    line linestyle {linestyle}")
  lines.append(f"@    line color {color}")

  # [EDIT L91-L97] Add arrow settings matching user's example.
  lines.append("@    line arrow 2")
  lines.append("@    line arrow type 1")
  lines.append("@    line arrow length 1.000000")
  lines.append("@    line arrow layout 1.000000, 0.000000")

  lines.append("@line def")
  return "\n".join(lines) + "\n"


def _agr_line_object(
  x0: float, y0: float, x1: float, y1: float,
  linewidth: float, linestyle: int, color: int
) -> str:
  """
  Draw one line object in world coordinates on g0 (used for dashed extension only).
  """
  lines: List[str] = []
  lines.append("@with line")
  lines.append("@    line on")
  lines.append("@    line loctype world")
  lines.append("@    line g0")
  lines.append(f"@    line {x0:.6f}, {y0:.6f}, {x1:.6f}, {y1:.6f}")
  lines.append(f"@    line linewidth {linewidth:.3f}")
  lines.append(f"@    line linestyle {linestyle}")
  lines.append(f"@    line color {color}")
  # [EDIT L118] Force arrow OFF to avoid inheriting arrow state from previous objects
  lines.append("@    line arrow 0")
  lines.append("@    line arrow type 0")
  lines.append("@    line arrow length 0.000000")
  lines.append("@    line arrow layout 0.000000, 0.000000")

  lines.append("@line def")
  return "\n".join(lines) + "\n"


def _agr_string(x: float, y: float, text: str, char_size: float = LABEL_CHAR_SIZE) -> str:
  """
  Add a Grace string in world coordinates on g0.
  """
  safe_text = text.replace('"', r'\"')
  lines: List[str] = []
  lines.append("@with string")
  lines.append("@    string on")
  lines.append("@    string loctype world")
  lines.append("@    string g0")
  lines.append(f"@    string {x:.6f}, {y:.6f}")
  lines.append(f"@    string color {GAMMA_LINECOLOR}")
  #lines.append(f"@    string font 0")
  lines.append(f"@    string char size {char_size:.3f}")
  lines.append(f"@    string just {LABEL_JUST}")
  lines.append(f"@    string def \"{safe_text}\"")
  return "\n".join(lines) + "\n"


def _cross_sign(sl_i: StateLayout, sl_f: StateLayout) -> int:
  """
  Decide cross-band direction.
  If initial is to the LEFT of final -> left-top -> right-bottom -> +1
  Else -> right-top -> left-bottom -> -1
  """
  return 1 if sl_i.xc < sl_f.xc else -1


def _find_layout_by_band_energy(
  state_layouts: List[StateLayout], band: int, energy_keV: float, tol_keV: float = 1.0
) -> Optional[StateLayout]:
  """
  Find a StateLayout by (band, energy) within tolerance.
  """
  best: Optional[StateLayout] = None
  best_de = float("inf")
  for sl in state_layouts:
    if sl.band != band:
      continue
    de = abs(sl.state.energy_keV - energy_keV)
    if de <= tol_keV and de < best_de:
      best = sl
      best_de = de
  return best


def _assign_crossband_jitter_index(
  resolved: List[Tuple[Transition, float, int, str]],
  state_layouts: List[StateLayout],
  tol_keV: float = 1.0
) -> Dict[Tuple[int, float, float, int, float], int]:
  """
  Assign a small integer jitter index for cross-band transitions from the same initial state.

  Scheme A:
    - Start x is ALWAYS at the edge (left or right) decided by sign.
    - slot/jitter is ONLY used to separate multiple cross-band gammas from the SAME initial state.

  Returns:
    (band_i, Ei_keV, Egamma_keV, band_f, Ef_keV) -> jitter_index (0,1,2,...)
  """
  # Group by initial state (band_i, Ei_keV)
  groups: Dict[Tuple[int, float], List[Tuple[Transition, StateLayout, StateLayout]]] = {}
  for t, ef_e, ef_b, _ef_j in resolved:
    # only cross-band
    if t.band == ef_b:
      continue
    sl_i = _find_layout_by_band_energy(state_layouts, t.band, t.ei_keV, tol_keV=tol_keV)
    sl_f = _find_layout_by_band_energy(state_layouts, ef_b, ef_e, tol_keV=tol_keV)
    if sl_i is None or sl_f is None:
      continue
    gk = (sl_i.band, sl_i.state.energy_keV)
    groups.setdefault(gk, []).append((t, sl_i, sl_f))

  out: Dict[Tuple[int, float, float, int, float], int] = {}
  for (_bi, _ei), items in groups.items():
    # Deterministic ordering so jitter indices are stable
    # Sort by final xc, then by Ef energy, then Egamma
    items_sorted = sorted(items, key=lambda x: (x[2].xc, x[2].state.energy_keV, x[0].egamma_keV))

    for idx, (t, sl_i, sl_f) in enumerate(items_sorted):
      key = (sl_i.band, sl_i.state.energy_keV, t.egamma_keV, sl_f.band, sl_f.state.energy_keV)
      out[key] = idx

  return out


def build_transitions_block(
  resolved: List[Tuple[Transition, float, int, str]],
  state_layouts: List[StateLayout],
  y_pad: float = Y_PAD,
  draw_gamma_label: bool = DRAW_GAMMA_LABEL,
  tol_keV: float = 1.0
) -> Tuple[str, Tuple[float, float, float, float]]:
  """
  Build gamma transitions as Grace objects, plus final dashed extensions (C2.4).

  Returns:
    agr_block (str),
    range (x_min, x_max, y_min, y_max) computed from the ACTUAL drawn objects.
  """
  if not resolved:
    return "", (0.0, 1.0, 0.0, 1.0)

  dr = DataRange()
  parts: List[str] = []

  # Pre-assign cross-band jitter index (Scheme A)
  cross_j_map = _assign_crossband_jitter_index(resolved, state_layouts, tol_keV=tol_keV)  # [EDIT L227] Scheme A

  # Track required dashed extension for final states: (band, energy_keV) -> x_need
  final_ext_need: Dict[Tuple[int, float], float] = {}

  for t, ef_e, ef_b, _ef_j in resolved:
    sl_i = _find_layout_by_band_energy(state_layouts, t.band, t.ei_keV, tol_keV=tol_keV)
    sl_f = _find_layout_by_band_energy(state_layouts, ef_b, ef_e, tol_keV=tol_keV)
    if sl_i is None or sl_f is None:
      continue

    y_i = sl_i.y
    y_f = sl_f.y

    # Ensure direction is high -> low
    if y_i < y_f:
      sl_i, sl_f = sl_f, sl_i
      y_i, y_f = y_f, y_i

    # C1: inside-band (vertical at xc)
    if sl_i.band == sl_f.band:
      x = sl_i.xc
      x0, y0 = x, y_i - y_pad
      x1, y1 = x, y_f + y_pad

      parts.append(_agr_arrow_object(x0, y0, x1, y1, GAMMA_LINEWIDTH, GAMMA_LINESTYLE, GAMMA_LINECOLOR))
      dr.update_segment(x0, y0, x1, y1)

      if draw_gamma_label:
        eg_txt = f"{t.egamma_keV:.0f}"
        xm = x + LABEL_DX
        ym = 0.5 * (y0 + y1) + LABEL_DY
        parts.append(_agr_string(xm, ym, eg_txt))
        dr.update_point(xm, ym)

      continue

    # cross-band
    sign = _cross_sign(sl_i, sl_f)  # [EDIT L266] decide left/right direction

    key = (sl_i.band, sl_i.state.energy_keV, t.egamma_keV, sl_f.band, sl_f.state.energy_keV)
    solid_left_i = min(sl_i.x0, sl_i.x1)
    solid_right_i = max(sl_i.x0, sl_i.x1)

    # Scheme A: start ALWAYS from the edge; jitter ONLY separates multiple cross-band from same initial state
    j = cross_j_map.get(key, 0)  # [EDIT L273] jitter index (0,1,2,...)

    if sign > 0:
      # left-top -> right-bottom: start from RIGHT edge
      x_start = solid_right_i - EDGE_EPS - j * SLOT_JITTER  # [EDIT L277]
    else:
      # right-top -> left-bottom: start from LEFT edge
      x_start = solid_left_i + EDGE_EPS + j * SLOT_JITTER  # [EDIT L280]

    # Clamp inside the solid interval (avoid sitting exactly on corners)
    x_start = min(x_start, solid_right_i - EDGE_EPS)  # [EDIT L283]
    x_start = max(x_start, solid_left_i + EDGE_EPS)  # [EDIT L284]

    x0, y0 = x_start, y_i - y_pad

    dy = (y_i - y_f)
    dx = dy / CROSS_TAN
    x1 = x0 + sign * dx  # [EDIT L294] rule (2): fixed angle with direction
    y1 = y_f + y_pad

    parts.append(_agr_arrow_object(x0, y0, x1, y1, GAMMA_LINEWIDTH, GAMMA_LINESTYLE, GAMMA_LINECOLOR))
    dr.update_segment(x0, y0, x1, y1)

    # C2.4 dashed extension need for final state based on StateLayout solid interval
    solid_left_f = min(sl_f.x0, sl_f.x1)
    solid_right_f = max(sl_f.x0, sl_f.x1)

    if x1 < solid_left_f - 1e-9 or x1 > solid_right_f + 1e-9:
      fkey = (sl_f.band, sl_f.state.energy_keV)
      prev = final_ext_need.get(fkey, None)
      if prev is None:
        final_ext_need[fkey] = x1
      else:
        if x1 > solid_right_f:
          final_ext_need[fkey] = max(prev, x1)
        if x1 < solid_left_f:
          final_ext_need[fkey] = min(prev, x1)

    # C3 label
    if draw_gamma_label:
      eg_txt = f"{t.egamma_keV:.0f}"
      xm = 0.5 * (x0 + x1) + LABEL_DX
      ym = 0.5 * (y0 + y1) + LABEL_DY
      parts.append(_agr_string(xm, ym, eg_txt))
      dr.update_point(xm, ym)

  # Draw dashed extensions for final states (C2.4)
  for (b, e), x_need in final_ext_need.items():
    sl_f = _find_layout_by_band_energy(state_layouts, b, e, tol_keV=tol_keV)
    if sl_f is None:
      continue

    y = sl_f.y
    solid_left = min(sl_f.x0, sl_f.x1)
    solid_right = max(sl_f.x0, sl_f.x1)

    if x_need > solid_right:
      xa, xb = solid_right, x_need
    else:
      xa, xb = solid_left, x_need

    parts.append(_agr_line_object(
      xa, y, xb, y,
      FINAL_EXT_LINEWIDTH, FINAL_EXT_LINESTYLE, FINAL_EXT_LINECOLOR
    ))
    dr.update_segment(xa, y, xb, y)

  if dr.x_min == float("inf"):
    return "".join(parts), (0.0, 1.0, 0.0, 1.0)

  return "".join(parts), (dr.x_min, dr.x_max, dr.y_min, dr.y_max)

