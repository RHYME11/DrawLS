# src/grace_frame.py
# ============================================================
# Frame defaults (GLOBAL CONFIG)
# ============================================================
SHOW_X_AXIS = False
SHOW_Y_AXIS = False

# World-range margins (ratios applied to data span)
X_MARGIN_RATIO = 0.10
Y_MARGIN_BOTTOM_RATIO = 0.05
Y_MARGIN_TOP_RATIO = 0.10

# Page / frame view (normalized device coordinates)
# Feel free to tweak these if you want larger/smaller plotting area on the page.
VIEW_XMIN = 0.12
VIEW_XMAX = 0.92
VIEW_YMIN = 0.12
VIEW_YMAX = 0.92
# ============================================================

from typing import Tuple, Optional


def compute_world_with_margins(
  x_min_data: float,
  x_max_data: float,
  y_min_data: float,
  y_max_data: float,
  x_margin_ratio: float = X_MARGIN_RATIO,
  y_margin_bottom_ratio: float = Y_MARGIN_BOTTOM_RATIO,
  y_margin_top_ratio: float = Y_MARGIN_TOP_RATIO,
) -> Tuple[float, float, float, float]:
  """
  Compute Grace 'world' range with margins applied.

  Margins are expressed as ratios of data span:
    x_span = x_max_data - x_min_data
    y_span = y_max_data - y_min_data

  Special cases:
    - If span is 0, a small default span is used to avoid zero-range.
  """
  x_span = x_max_data - x_min_data
  y_span = y_max_data - y_min_data

  # Avoid zero span (Grace dislikes identical world min/max)
  if x_span == 0.0:
    x_span = 1.0
  if y_span == 0.0:
    y_span = 1.0

  x_min = x_min_data - x_margin_ratio * x_span
  x_max = x_max_data + x_margin_ratio * x_span

  y_min = y_min_data - y_margin_bottom_ratio * y_span
  y_max = y_max_data + y_margin_top_ratio * y_span

  return x_min, x_max, y_min, y_max


def grace_header() -> str:
  """
  Minimal, stable header for an .agr file.
  You can extend this later (fonts, colors, defaults, etc.).
  """
  lines = []
  lines.append("@version 50125")
  lines.append("@page size 792, 612")  # US letter landscape-like default
  lines.append("@page scroll 5%")
  lines.append("@page inout 5%")
  lines.append("@link page off")
  lines.append("@background color 0")
  lines.append("@page background fill on")
  lines.append("@timestamp off")
  return "\n".join(lines) + "\n"


def grace_g0_frame(
  world: Tuple[float, float, float, float],
  show_x_axis: bool = SHOW_X_AXIS,
  show_y_axis: bool = SHOW_Y_AXIS,
  view_xmin: float = VIEW_XMIN,
  view_xmax: float = VIEW_XMAX,
  view_ymin: float = VIEW_YMIN,
  view_ymax: float = VIEW_YMAX,
) -> str:
  """
  Generate g0 frame settings:
    - frame view (position on page)
    - world (data coordinate range)
    - axis on/off (both off by default for level scheme)
  """
  x_min, x_max, y_min, y_max = world

  lines = []

  lines.append("@with g0")
  lines.append(f"@    view {view_xmin:.6f}, {view_ymin:.6f}, {view_xmax:.6f}, {view_ymax:.6f}")
  lines.append(f"@    world {x_min:.6f}, {y_min:.6f}, {x_max:.6f}, {y_max:.6f}")

  # Turn axes off by default (level scheme style)
  if not show_x_axis:
    lines.append("@    xaxis  off")
    lines.append("@    xaxis  tick off")
    lines.append("@    xaxis  label \"\"")
  else:
    lines.append("@    xaxis  on")

  if not show_y_axis:
    lines.append("@    yaxis  off")
    lines.append("@    yaxis  tick off")
    lines.append("@    yaxis  label \"\"")
  else:
    lines.append("@    yaxis  on")

  # Frame box: keep on (so Grace has a frame), but you can turn it off if you want
  lines.append("@    frame type 0")
  lines.append("@    frame linestyle 0")
  lines.append("@    frame linewidth 0.0")

  return "\n".join(lines) + "\n"


def build_frame_block(
  x_min_data: float,
  x_max_data: float,
  y_min_data: float,
  y_max_data: float,
  show_x_axis: bool = SHOW_X_AXIS,
  show_y_axis: bool = SHOW_Y_AXIS,
) -> str:
  """
  Convenience wrapper:
    - compute world with default margins
    - return header + g0 frame block
  """
  world = compute_world_with_margins(x_min_data, x_max_data, y_min_data, y_max_data)
  return grace_header() + grace_g0_frame(world, show_x_axis=show_x_axis, show_y_axis=show_y_axis)

