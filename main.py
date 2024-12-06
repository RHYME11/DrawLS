import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'build/agr_generator'))

from datetime import datetime
from GEmptyFrame import *
from GReadFile import *
from GGenerator import *

# ================================================================= #    
# Step1: Input # of isotopes and selectr the format
# 1.1: # of isotopes will determine the frame size
# 1.2: format means y-axis, Ex mark and so on

def gInitialize():
  agr_content = []
  
  # Enter # of isotopes
  while not agr_content:
    Nisotopes = input("Enter number of isotopes to plot: ")
    if Nisotopes.isdigit():
      Nisotopes = int(Nisotopes)
      agr_content = gframe(Nisotopes)
           
  # TODO: Formats plotting examples display 
  # TODO: functions to change the format, the input should be agr_content
  format_type = -1
  if agr_content:
    while format_type < 0:
      format_type = int(input("Enter the formate # (default is 1): "))
      if format_type != 1:
        print(f"Format{format_type} has not been ready yet. Try a differenty style\n")
      else:
        break

  return agr_content, Nisotopes, format_type





# ================================================================= #    
# Step2: Read inputfiles and fill their info into agr_content
def Generate(agr_content, Nisotopes):
  # Input isotopes.dat files
  for niso in range(Nisotopes):
    input_file = ""
    while not os.path.exists(input_file):
      input_file = input(f"Enter file{niso+1} path: ")
      if not os.path.exists(input_file):
        print(f"{input_file} does not exits. Please try again\n")
      else:
        isotope, states, se = gReadFile(input_file)
        agr_content = generator1(agr_content, niso, isotope, states, se)
        break
  return agr_content, isotope





# =========================== Output file ================================== #    
# Write the modified content to a new output file
def gOutput(agr_content):
  #output_file = f"{isotope}{N+Z}_format{format_type}.agr"
  output_file = "output.agr"
  with open(output_file, 'w') as file:
    file.writelines(agr_content)



# ====================== Main ========================= #
agr_content, Nisotopes, format_type = gInitialize()
agr_content, isotope = Generate(agr_content,Nisotopes)
gOutput(agr_content) 


