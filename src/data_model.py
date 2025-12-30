# src/data_model.py

from dataclasses import dataclass


@dataclass(frozen=True)
class Transition:
  """
  One gamma transition read from input file.
  band and jpi are optional properties tied to the INITIAL state energy Ei.
  """
  egamma_keV: float
  ei_keV: float
  jpi: str        # "" means missing/unknown
  band: int       # -1 means missing/unknown
  lineno: int     # line number in the input file (1-based)


@dataclass(frozen=True)
class State:
  """
  A record for a state energy (level) with optional band/Jpi metadata.
  """
  energy_keV: float
  band: int       # -1 means missing/unknown
  jpi: str        # "" means missing/unknown
  lineno: int     # source line number; -1 can be used for synthetic states (e.g. GS)

