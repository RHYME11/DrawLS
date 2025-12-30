# src/integrate.py
# ============================================================
# Tolerances (GLOBAL CONFIG)
# ============================================================
# Merge Ei states (input-file states only):
#   - Same band required
#   - |Ei1 - Ei2| <= EI_MERGE_TOL_KEV
EI_MERGE_TOL_KEV = 0.5

# Match Ef_raw to existing Ei states:
#   - |Ei - Ef_raw| <= EF_MATCH_TOL_KEV
EF_MATCH_TOL_KEV = 1.0
# ============================================================

from typing import List, Tuple
from src.data_model import Transition, State


def _fmt_band(b: int) -> str:
  return str(b) if b != -1 else "<missing>"


def _fmt_jpi(j: str) -> str:
  return j if j != "" else "<missing>"


def merge_ei_states(transitions: List[Transition]) -> List[State]:
  """
  Merge Ei states from input transitions.

  Rules:
    - Only Ei states are merged (i.e., states that appear in the input file as Ei)
    - Must have the SAME band to be merged (band can be -1; -1 only merges with -1)
    - |ΔE| <= EI_MERGE_TOL_KEV
    - Jpi handling:
        * if one has Jpi and the other doesn't -> keep the non-empty one
        * if both non-empty and different -> keep the first, print warning
  Note:
    - This is a light merge to reduce repeated Ei entries due to multiple decays.
    - Canonical clustering across ALL states (Ei+Ef) should be handled in Step 3.
  """
  merged: List[State] = []

  for t in transitions:
    placed = False

    for idx, s in enumerate(merged):
      # Same band is required
      if s.band != t.band:
        continue

      # Energy closeness check
      if abs(s.energy_keV - t.ei_keV) <= EI_MERGE_TOL_KEV:
        # Merge into existing state
        new_energy = 0.5 * (s.energy_keV + t.ei_keV)

        # Merge Jpi (optional)
        new_jpi = s.jpi
        if s.jpi == "" and t.jpi != "":
          new_jpi = t.jpi
        elif s.jpi != "" and t.jpi != "" and s.jpi != t.jpi:
          print("\n[WARNING] Conflicting Jpi while merging Ei states")
          print(
            f"  Existing Ei={s.energy_keV:.3f} keV, Jpi={_fmt_jpi(s.jpi)}, Band={_fmt_band(s.band)} (from line {s.lineno})"
          )
          print(
            f"  New      Ei={t.ei_keV:.3f} keV, Jpi={_fmt_jpi(t.jpi)}, Band={_fmt_band(t.band)} (from line {t.lineno})"
          )
          print("  Keeping the first Jpi.\n")

        merged[idx] = State(
          energy_keV=new_energy,
          band=s.band,
          jpi=new_jpi,
          lineno=s.lineno,  # keep earliest source line for traceability
        )
        placed = True
        break

    if not placed:
      merged.append(
        State(
          energy_keV=t.ei_keV,
          band=t.band,
          jpi=t.jpi,
          lineno=t.lineno,
        )
      )

  return merged


def add_ground_state(states: List[State], gs_band: int = 1, gs_jpi: str = "") -> None:
  """
  Force ground state to exist:
    - Energy = 0 keV
    - Band   = 1 (fixed by your rule)
  """
  states.append(
    State(
      energy_keV=0.0,
      band=gs_band,
      jpi=gs_jpi,
      lineno=-1,  # synthetic
    )
  )


def find_ei_matches(states: List[State], e_query_keV: float) -> List[State]:
  """
  Find all existing Ei states with |Ei - e_query| <= EF_MATCH_TOL_KEV.
  Matching is based on STATE ENERGY only (Ei/Ef), not gamma energy.
  """
  matches: List[State] = []
  for s in states:
    if abs(s.energy_keV - e_query_keV) <= EF_MATCH_TOL_KEV:
      matches.append(s)
  return matches


def select_best_match(matches: List[State], e_query_keV: float) -> State:
  """
  Select the match with the smallest |dE| relative to e_query_keV.
  """
  return min(matches, key=lambda s: abs(s.energy_keV - e_query_keV))


def warn_ef_negative(t: Transition, ef_raw: float, gs_band: int = 1) -> None:
  """
  Warning for Ef_raw < 0 keV: force final state to ground state.
  """
  print("\n[WARNING] Ef_raw < 0 keV, forced to ground state")
  print(
    f"  Transition (line {t.lineno}): Egamma={t.egamma_keV:.3f}, Ei={t.ei_keV:.3f}, "
    f"Jpi={_fmt_jpi(t.jpi)}, Band={_fmt_band(t.band)}"
  )
  print(f"  Ef_raw = {ef_raw:.3f} -> using GS (E=0.000, Band={gs_band})")


def warn_multiple_matches(t: Transition, ef_raw: float, matches: List[State], chosen: State) -> None:
  """
  Warning for multiple Ei matches for Ef_raw.
  Print transition and each candidate Ei (energy, band, jpi, source line).
  """
  print(f"\n[WARNING] Multiple Ei matches for Ef_raw within ±{EF_MATCH_TOL_KEV:.3f} keV")
  print(
    f"  Transition (line {t.lineno}): Egamma={t.egamma_keV:.3f}, Ei={t.ei_keV:.3f}, "
    f"Jpi={_fmt_jpi(t.jpi)}, Band={_fmt_band(t.band)}"
  )
  print(f"  Ef_raw = {ef_raw:.3f}")
  print("  Candidates:")
  for s in matches:
    tag = "  <-- selected" if s == chosen else ""
    src = f"line {s.lineno}" if s.lineno != -1 else "GS"
    de = abs(s.energy_keV - ef_raw)
    print(
      f"    - Ei={s.energy_keV:.3f} keV "
      f"(Band={_fmt_band(s.band)}, Jpi={_fmt_jpi(s.jpi)}, from {src}), "
      f"|dE|={de:.3f}{tag}"
    )


def resolve_final_state(t: Transition, ei_states: List[State], gs_band: int = 1) -> Tuple[float, int, str]:
  """
  Resolve final state (Ef_energy, Ef_band, Ef_jpi) for one transition.

  Frozen rules:
    - Ef_raw = Ei - Egamma
    - Ef_raw must be >= 0:
        if Ef_raw < 0 -> force GS (E=0, Band=1), print warning
    - Match Ef_raw to existing Ei states by STATE ENERGY within EF_MATCH_TOL_KEV
        * 0 matches: new state (Ef_raw, band=-1, jpi="")
        * 1 match: use matched state's (energy, band, jpi)
        * >1 matches: choose closest; print warning with candidates
  """
  ef_raw = t.ei_keV - t.egamma_keV

  # Rule 0: negative energy -> ground state
  if ef_raw < 0.0:
    warn_ef_negative(t, ef_raw, gs_band=gs_band)
    return 0.0, gs_band, ""

  matches = find_ei_matches(ei_states, ef_raw)

  if len(matches) == 0:
    return ef_raw, -1, ""

  if len(matches) == 1:
    s = matches[0]
    return s.energy_keV, s.band, s.jpi

  chosen = select_best_match(matches, ef_raw)
  warn_multiple_matches(t, ef_raw, matches, chosen)
  return chosen.energy_keV, chosen.band, chosen.jpi


def build_candidate_states_and_resolved_finals(
  transitions: List[Transition],
  gs_band: int = 1,
  gs_jpi: str = ""
) -> Tuple[List[State], List[Tuple[Transition, float, int, str]]]:
  """
  Step 2 entry point.

  Returns:
    candidates: List[State]
      - merged Ei states (same band + EI_MERGE_TOL_KEV)
      - forced GS
      - any new Ef states that are not matched to existing Ei and Ef_raw >= 0
        (new Ef states always have band=-1 and jpi="")

    resolved: List[(Transition, Ef_energy, Ef_band, Ef_jpi)]
      - per input transition, the resolved final state info
  """
  # 1) Merge repeated Ei states from the input (same band only)
  ei_states = merge_ei_states(transitions)

  # 2) Force ground state
  add_ground_state(ei_states, gs_band=gs_band, gs_jpi=gs_jpi)

  # 3) Build outputs
  candidates: List[State] = list(ei_states)
  resolved: List[Tuple[Transition, float, int, str]] = []

  for t in transitions:
    ef_e, ef_b, ef_j = resolve_final_state(t, ei_states, gs_band=gs_band)
    resolved.append((t, ef_e, ef_b, ef_j))

    # Add NEW Ef states only when they are truly new unknown states
    if ef_b == -1 and ef_j == "":
      candidates.append(
        State(
          energy_keV=ef_e,
          band=-1,
          jpi="",
          lineno=t.lineno,
        )
      )

  return candidates, resolved

