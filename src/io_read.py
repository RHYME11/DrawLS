# src/io_read.py

from typing import List, Dict, Tuple
from src.data_model import Transition


def read_dat(path: str) -> List[Transition]:
  """
  Read a whitespace-delimited .dat file.

  Allowed formats per data line (2~4 columns):
    1) Egamma  Ei
    2) Egamma  Ei  Jpi
    3) Egamma  Ei  Jpi  Band

  Rules:
    - Ignore blank lines
    - Ignore lines starting with '#'
    - Missing fields:
        Jpi  -> ""
        Band -> -1
  """
  transitions: List[Transition] = []

  with open(path, "r", encoding="utf-8") as f:
    for lineno, raw in enumerate(f, start=1):
      line = raw.strip()
      if not line or line.startswith("#"):
        continue

      parts = line.split()
      if len(parts) < 2 or len(parts) > 4:
        raise ValueError(
          f"Line {lineno}: expected 2~4 columns (Egamma Ei [Jpi] [Band]), got {len(parts)}"
        )

      egamma = float(parts[0])
      ei = float(parts[1])

      jpi = ""
      band = -1

      if len(parts) >= 3:
        jpi = parts[2].strip()

      if len(parts) == 4:
        band = int(parts[3])

      transitions.append(
        Transition(
          egamma_keV=egamma,
          ei_keV=ei,
          jpi=jpi,
          band=band,
          lineno=lineno,
        )
      )

  return transitions


def report_duplicate_transitions(
  transitions: List[Transition],
  round_ndp: int = 3
) -> None:
  """
  Print duplicate transitions.

  Duplicate definition:
    Same (Egamma, Ei, Jpi, Band) after rounding energies.
  Missing fields are part of the key:
    Jpi="" and Band=-1 are treated as real values.
  """
  key_map: Dict[Tuple[float, float, str, int], List[int]] = {}

  for t in transitions:
    key = (
      round(t.egamma_keV, round_ndp),
      round(t.ei_keV, round_ndp),
      t.jpi,
      t.band,
    )
    key_map.setdefault(key, []).append(t.lineno)

  duplicates = {k: v for k, v in key_map.items() if len(v) > 1}

  if not duplicates:
    print("No duplicate transitions found.")
    return

  print("\n=== DUPLICATE TRANSITIONS FOUND ===")
  for (eg, ei, jpi, band), lines in duplicates.items():
    jpi_show = jpi if jpi != "" else "<missing>"
    band_show = band if band != -1 else "<missing>"
    print(
      f"Lines {lines}: "
      f"Egamma={eg} keV, Ei={ei} keV, Jpi={jpi_show}, Band={band_show}"
    )
  print("=== END DUPLICATES ===\n")

