# src/draw_states.py
# ============================================================
# State drawing defaults (GLOBAL CONFIG)
# ============================================================

# Geometry
STATE_SOLID_LEN = 4.0
BAND_GAP = 1.0

# Energy -> y scaling (keV to Grace world y-unit)
Y_SCALE = 1.0

# Level (state) line style
STATE_LINEWIDTH = 2.0
STATE_LINESTYLE = 1  # 1 = solid (Grace default)
STATE_LINECOLOR = 1  # 1 = black

# Label flags
DRAW_JPI_LABEL = True
DRAW_ENERGY_LABEL = True

# Label offsets (in world units)
# These are relative to the level y-position.
JPI_DX = 0.10
JPI_DY = 20.0

ENERGY_DX = 0.10
ENERGY_DY = 20.0

# Label font size (Grace char size)
# Label just centered
LABEL_CHAR_SIZE = 0.80
LABEL_JUST = 14 

# Formatting
ENERGY_FMT = "{:.0f}"  # e.g. "1500" (change to "{:.1f}" if you want decimals)

# ============================================================

from dataclasses import dataclass
from typing import Dict, List, Tuple

from src.data_model import State


@dataclass(frozen=True)
class BandLayout:
  x0: float
  x1: float
  xc: float


@dataclass(frozen=True)
class StateLayout:
  state: State
  band: int
  x0: float
  x1: float
  xc: float
  y: float


def _sorted_bands_present(states: List[State]) -> Tuple[List[int], bool]:
  """
  Return (bands_present_sorted, has_no_band).
  bands_present_sorted contains only bands >= 1 that appear in data.
  no-band (band=-1) is handled separately.
  """
  bands = sorted({s.band for s in states if s.band >= 1})
  has_no_band = any(s.band == -1 for s in states)
  return bands, has_no_band


def compute_band_layout(states: List[State]) -> Dict[int, BandLayout]:
  """
  Compute x-positions for each band:
    - Only bands that appear (>=1) are allocated columns (no gaps for missing band numbers)
    - band=-1 (no-band) is placed as the last column (rightmost)
  """
  bands_present, has_no_band = _sorted_bands_present(states)

  layout: Dict[int, BandLayout] = {}

  # Assign columns for present bands (compressed)
  for col_idx, b in enumerate(bands_present):
    x0 = col_idx * (STATE_SOLID_LEN + BAND_GAP)
    x1 = x0 + STATE_SOLID_LEN
    xc = 0.5 * (x0 + x1)
    layout[b] = BandLayout(x0=x0, x1=x1, xc=xc)

  # Place band=-1 at far right, after the last present band
  if has_no_band:
    col_idx = len(bands_present)
    x0 = col_idx * (STATE_SOLID_LEN + BAND_GAP)
    x1 = x0 + STATE_SOLID_LEN
    xc = 0.5 * (x0 + x1)
    layout[-1] = BandLayout(x0=x0, x1=x1, xc=xc)

  return layout


def compute_state_layout(states: List[State], band_layout: Dict[int, BandLayout]) -> List[StateLayout]:
  """
  Compute per-state geometry using band_layout and Y_SCALE.
  """
  out: List[StateLayout] = []
  for s in states:
    b = s.band if s.band in band_layout else -1
    bl = band_layout[b]
    y = s.energy_keV * Y_SCALE
    out.append(StateLayout(state=s, band=b, x0=bl.x0, x1=bl.x1, xc=bl.xc, y=y))
  return out


def _agr_line_object(x0: float, y0: float, x1: float, y1: float) -> str:
  """
  Draw one line object in world coordinates on g0 (NOT a dataset).
  """
  lines: List[str] = []
  lines.append("@with line")
  lines.append("@    line on")
  lines.append("@    line loctype world")
  lines.append("@    line g0")
  lines.append(f"@    line {x0:.6f}, {y0:.6f}, {x1:.6f}, {y1:.6f}")
  lines.append(f"@    line linewidth {STATE_LINEWIDTH:.3f}")
  lines.append(f"@    line linestyle {STATE_LINESTYLE}")
  lines.append(f"@    line color {STATE_LINECOLOR}")
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
  lines.append(f"@    string just {LABEL_JUST}")
  lines.append(f"@    string char size {char_size:.3f}")
  lines.append(f"@    string def \"{safe_text}\"")
  return "\n".join(lines) + "\n"


def build_states_block(
  candidates: List[State],
  draw_jpi: bool = DRAW_JPI_LABEL,
  draw_energy: bool = DRAW_ENERGY_LABEL,
) -> Tuple[str, Dict[int, BandLayout], List[StateLayout], Tuple[float, float, float, float]]:
  """
  Build the .agr block for states ONLY (no transitions).

  Returns:
    agr_text: the text to append after frame block
    band_layout: band -> BandLayout
    state_layouts: list of per-state layout objects
    data_range: (x_min_data, x_max_data, y_min_data, y_max_data) of the drawn content
  """
  if not candidates:
    return "", {}, [], (0.0, 1.0, 0.0, 1.0)

  band_layout = compute_band_layout(candidates)
  state_layouts = compute_state_layout(candidates, band_layout)

  # Data range for frame/world
  x_min_data = min(sl.x0 for sl in state_layouts)
  x_max_data = max(sl.x1 for sl in state_layouts)
  y_min_data = min(sl.y for sl in state_layouts)
  y_max_data = max(sl.y for sl in state_layouts)

  # Build line objects + labels
  agr_parts: List[str] = []

  for sl in state_layouts:
    # Level line (solid only)
    agr_parts.append(_agr_line_object(sl.x0, sl.y, sl.x1, sl.y))

    # Labels must sit on the SOLID part (your rule).
    if draw_jpi and sl.state.jpi != "":
      # left-top of solid segment
      agr_parts.append(_agr_string(sl.x0 + JPI_DX, sl.y + JPI_DY, sl.state.jpi))

    if draw_energy:
      # right-top of solid segment
      e_txt = ENERGY_FMT.format(sl.state.energy_keV)
      agr_parts.append(_agr_string(sl.x1 - ENERGY_DX, sl.y + ENERGY_DY, e_txt))

  return "".join(agr_parts), band_layout, state_layouts, (x_min_data, x_max_data, y_min_data, y_max_data)

