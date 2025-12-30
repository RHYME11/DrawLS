# DrawLS (beta2)
DrawLS_beta2 is a Python-based tool to generate nuclear level-scheme plots in XMGrace .agr format.
The design emphasizes clear separation between physics logic and drawing logic, and enforces a single-frame, object-based drawing model (no datasets).

This repository represents the beta2 architecture, where the core logic is considered stable.

## Project Philosophy
- One frame (g0), one canvas

- All states and transitions are Grace objects (line, arrow, string)

- No datasets are used

- Transition geometry is derived strictly from state geometry

- Physics logic and drawing logic are fully decoupled


## Project Structure

```text
DrawLS_beta2/
├── src/
│   ├── data_model.py
│   ├── io_read.py
│   ├── integrate.py
│   ├── draw_states.py
│   ├── draw_transitions.py
│   └── grace_frame.py
│
├── scripts/
│   ├── check_input.py
│   ├── check_step2.py
│   ├── test_draw_states.py
│   ├── test_draw_transition.py
│   └── test_frame.py
│
└── README.md

```

## Overall Logic FLow (src codes)
```text
input .dat
  ↓
io_read.read_dat()
  ↓
List[Transition]
  ↓
integrate.build_candidate_states_and_resolved_finals()
  ↓
candidate States + resolved Transitions
  ↓
draw_states.build_states_block()
  ↓
StateLayout (geometry)
  ↓
draw_transitions.build_transitions_block()
  ↓
Grace objects (states + transitions)
  ↓
grace_frame.build_frame_block()
  ↓
final .agr file

```
## src codes

1. data_model.py

Pure data definitions (no logic).

- Transition

  - One γ transition from input file

  - Stores Eγ, Ei, optional Jπ, optional band, and source line number

- State

  - Represents a nuclear level (Ei or Ef)

  - Immutable (frozen=True)

This file is the single source of truth for data structures.

2. io_read.py

Input parsing and sanity checks.

Main functions:

- read_dat(path)

  - Reads whitespace-delimited .dat files

  - Allowed formats:

```
Egamma Ei
Egamma Ei Jpi
Egamma Ei Jpi Band
```

- report_duplicate_transitions(transitions)

  - Reports duplicated transitions (after rounding)

No physics or drawing logic appears here.

3. integrate.py

Physics logic core (Step 2).

Responsibilities:

- Merge repeated initial states (Ei) within tolerance

- Resolve final states (Ef = Ei − Egamma)

- Force ground state when Ef < 0

- Match Ef to existing Ei states within tolerance

- Generate new unknown Ef states when necessary

Key configurable parameters:

```
EI_MERGE_TOL_KEV = 0.5
EF_MATCH_TOL_KEV = 1.0
```

Main entry point:

```
build_candidate_states_and_resolved_finals()
```

This module contains no geometry and no drawing logic.

4. draw_states.py

State geometry and drawing (Step 3a).

This module:

- Computes band layout

- Converts states into StateLayout objects

- Draws level lines and labels as Grace objects

Geometry rules

- Only bands that actually appear are allocated columns

- band = -1 (unknown) is always placed at the far right

- State height: y = energy_keV * Y_SCALE

Key adjustable parameters

```
STATE_SOLID_LEN = 4.0
BAND_GAP = 1.0
Y_SCALE = 1.0

STATE_LINEWIDTH = 2.0
STATE_LINESTYLE = 1
STATE_LINECOLOR = 1

DRAW_JPI_LABEL = True
DRAW_ENERGY_LABEL = True

JPI_DX = 0.10
JPI_DY = 20.0
ENERGY_DX = 0.10
ENERGY_DY = 20.0

LABEL_CHAR_SIZE = 0.80
ENERGY_FMT = "{:.0f}"
```

All states are drawn as line objects, not datasets.

5. draw_transitions.py

Gamma transition geometry and drawing (Step 3b).

All transitions are drawn as arrow objects.

Transition types

- Same-band transitions

  - Vertical arrows at xc

Cross-band transitions

- Fixed tilt angle

- Direction determined by relative band positions

- Slot-based start positions to reduce overlap

- Automatic dashed extension of final levels if needed

Key adjustable parameters

```
GAMMA_LINEWIDTH = 2.0
GAMMA_LINESTYLE = 1
GAMMA_LINECOLOR = STATE_LINECOLOR

Y_PAD = 14.0

DRAW_GAMMA_LABEL = True
LABEL_CHAR_SIZE = 0.80
LABEL_DX = 0.10
LABEL_DY = 20.0

CROSS_ANGLE_DEG = 89.95
SLOT_JITTER = 0.12

FINAL_EXT_LINESTYLE = 2
FINAL_EXT_LINEWIDTH = 2.0
```

Transition geometry is derived strictly from `StateLayout`.

Transitions never compute their own state positions.

6. grace_frame.py

Frame, world, and view control.

Responsibilities:

- Compute world range from actual drawn content

- Apply configurable margins

- Generate Grace header and g0 frame

Key adjustable parameters:

```
X_MARGIN_RATIO = 0.10
Y_MARGIN_BOTTOM_RATIO = 0.05
Y_MARGIN_TOP_RATIO = 0.10

VIEW_XMIN = 0.12
VIEW_XMAX = 0.92
VIEW_YMIN = 0.12
VIEW_YMAX = 0.92
```

This module ensures that slanted transitions and dashed extensions are never clipped.

## Scripts

Scripts are lightweight entry points for testing and usage.

**check_input.py**

- Reads input file

- Reports duplicated transitions

```
python scripts/check_input.py input.dat
```

**check_step2.py**

- Validates physics logic (Ei/Ef resolution)

- Prints warnings and summaries

```
python scripts/check_step2.py input.dat
```

**test_draw_states.py**

- Draws states only

- Useful for debugging band layout and geometry

```
python scripts/test_draw_states.py input.dat out_states.agr
```

**test_draw_transition.py**

- Full level scheme (states + transitions)

```
python scripts/test_draw_transition.py input.dat out.agr
python scripts/test_draw_transition.py input.dat out.agr --no-label
```

**test_frame.py**

- Tests frame/world/view independently

```
python scripts/test_frame.py test_frame.agr -1 20 -50 3500
```



