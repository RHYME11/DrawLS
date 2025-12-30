# scripts/check_step2.py

import sys

from src.io_read import read_dat, report_duplicate_transitions
from src.integrate import (
  EI_MERGE_TOL_KEV,
  EF_MATCH_TOL_KEV,
  build_candidate_states_and_resolved_finals,
)


def _fmt_band(b: int) -> str:
  return str(b) if b != -1 else "<missing>"


def _fmt_jpi(j: str) -> str:
  return j if j != "" else "<missing>"


def main() -> None:
  if len(sys.argv) < 2:
    raise RuntimeError("Usage: python scripts/check_step2.py <input.dat>")

  input_dat = sys.argv[1]

  # Step 1: read + duplicate check
  transitions = read_dat(input_dat)
  print("\n=== Step 1: read_dat ===")
  print(f"Transitions read = {len(transitions)}")
  report_duplicate_transitions(transitions)

  # Step 2: build candidates + resolve finals (will print warnings if needed)
  print("\n=== Step 2: build_candidate_states_and_resolved_finals ===")
  print(f"EI_MERGE_TOL_KEV = {EI_MERGE_TOL_KEV}")
  print(f"EF_MATCH_TOL_KEV = {EF_MATCH_TOL_KEV}")

  candidates, resolved = build_candidate_states_and_resolved_finals(
    transitions,
    gs_band=1,
    gs_jpi="",  # optional for now
  )

  print(f"\nResolved finals = {len(resolved)}")
  print(f"Candidate states (pre-clustering) = {len(candidates)}")

  # Sanity check: no negative final energies
  neg_final_count = sum(1 for (_, ef_e, _, _) in resolved if ef_e < 0)
  if neg_final_count != 0:
    print(f"[ERROR] Found Ef_energy < 0 in resolved finals: {neg_final_count} (should be 0)")
  else:
    print("OK: No negative final energies in resolved finals.")

  # Count how many NEW Ef states were created (unknown band/jpi)
  new_ef_count = sum(1 for (_, _, ef_b, ef_j) in resolved if (ef_b == -1 and ef_j == ""))
  print(f"New Ef states created (unknown band/jpi) = {new_ef_count}")

  # Band summary (candidates)
  band_counts = {}
  for s in candidates:
    band_counts[s.band] = band_counts.get(s.band, 0) + 1

  print("\nCandidate band counts:")
  for b in sorted(band_counts.keys()):
    print(f"  Band {_fmt_band(b)}: {band_counts[b]}")

  # Show first few resolved transitions
  print("\nFirst 10 resolved transitions:")
  for i, (t, ef_e, ef_b, ef_j) in enumerate(resolved[:10]):
    print(
      f"  #{i:02d} (line {t.lineno}) "
      f"Egamma={t.egamma_keV:.3f} Ei={t.ei_keV:.3f} "
      f"-> Ef={ef_e:.3f} (Band={_fmt_band(ef_b)}, Jpi={_fmt_jpi(ef_j)})"
    )

  print("\nDONE.")


if __name__ == "__main__":
  main()

