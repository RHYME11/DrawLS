# scripts/check_input.py

import sys
from src.io_read import read_dat, report_duplicate_transitions


if len(sys.argv) < 2:
  raise RuntimeError("Usage: python check_input.py <input.dat>")

input_dat = sys.argv[1]

transitions = read_dat(input_dat)
report_duplicate_transitions(transitions)

print("\n=== Input Summary ===")
print(f"Transitions read = {len(transitions)}")
bands = sorted({t.band for t in transitions})
print(f"Bands found      = {bands}")
