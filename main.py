import os
import sys
import glob
import re
import readline
import signal
sys.path.append(os.path.join(os.path.dirname(__file__), 'build/agr_generator'))

from datetime import datetime
from GEmptyFrame import *
from GReadFile import *
from GGenerator import *

# =============== Preparation ================ # 
# Enable tab-completion for file paths
def complete_path(text, state):
  matches = glob.glob(text + '*')  # Get all matching files/folders
  return matches[state] if state < len(matches) else None

# Function to enable file path completion dynamically
def enable_path_completion():
  readline.set_completer(complete_path)
  readline.set_completer_delims(' \t\n') # Allow file paths with '/'
  readline.parse_and_bind("tab: complete")

# Function to sanitize file names
def sanitize_title(title):
  return re.sub(r'[<>:"/\\|?*]', '_', title)  # Replace invalid characters with "_"


# ================================================================= #    
# Step1: Input # of isotopes and select the format
def gInitialize():
  # Get format type with input validation
  valid_formats = {1, 2}  # Future formats can be added here
  while True:
    try:
      format_type = int(input("Enter the format # (default is 1): "))
      if format_type not in valid_formats:
        print(f"Format {format_type} doesn't exist. Please enter a valid number.\n")
      else:
        break
    except ValueError:
      print("Invalid input. Please enter an integer.")

  # Define valid Nisotopes range based on format_type
  valid_Nisotopes = {
    1: {1, 2},  # Format 1 allows only 1 or 2 isotopes
    2: set(range(1, 11))  # Format 2 allows 1 to 10 isotopes
  }

  # Get number of isotopes with validation (must be a non-zero integer within the allowed range)
  while True:
    try:
      Nisotopes = int(input("Enter number of isotopes to plot: "))
      if Nisotopes not in valid_Nisotopes[format_type]:
        print(f"Invalid input. For format {format_type}, Nisotopes must be in {sorted(valid_Nisotopes[format_type])}.\n")
      else:
        agr_content = gframe(Nisotopes)
        if agr_content:  # Ensure gframe returns a valid frame
          break
        else:
          print("Invalid number of isotopes. Please enter a valid number.\n")
    except ValueError:
      print("Invalid input. Please enter a non-zero positive integer.")
  
  return agr_content, Nisotopes, format_type

# ================================================================= #    
# Step2: Read input files and fill their info into agr_content
def Generate(agr_content, Nisotopes, format_type):
  # Read input files and process each isotope
  for niso in range(Nisotopes):
    while True:
      enable_path_completion()  # Enable tab-completion before input
      input_file = input(f"Enter file path for isotope {niso + 1}: ").strip()
      if not os.path.exists(input_file):
        print(f"File '{input_file}' does not exist. Please try again.\n")
        continue  # Ask for input again
      
      try:
        isotope, states, se = gReadFile(input_file)
      except Exception as e:
        print(f"Error reading file '{input_file}': {e}\nPlease try again.\n")
        continue  # Ask for input again

      # Apply format type for plotting
      match format_type:
        case 1:
          agr_content = generator1(agr_content, niso, isotope, states, se)
        case 2:
          agr_content = generator2(agr_content, niso, isotope, states, se)
        case _:
          print(f"Format {format_type} is not supported yet. Skipping this isotope.\n")
          continue  # If unsupported format, skip this isotope

      break  # If everything succeeds, exit the loop for this isotope

  return agr_content

# ================================================================= #    
# Step3: Write the modified content to an output file
def gOutput(agr_content, format_type):
  title = input(f"Enter a title for the .agr file (default: output_format{format_type}.agr): ").strip()
  title = sanitize_title(title)
  
  if title:
    output_file = f"{title}.agr"
  else:
    output_file = f"output_format{format_type}.agr"
  
  while os.path.exists(output_file):
    choice = input(f"File '{output_file}' already exists. Do you want to replace it? (y/n): ").strip().lower()
    if choice == 'y':
      break
    elif choice == 'n':
      title = f"{title}_copy" if title else f"output_format{format_type}_copy"
      output_file = f"{title}.agr"
    else:
      print("Invalid input. Please enter 'y' for yes or 'n' for no.")
  
  with open(output_file, 'w') as file:
    file.writelines(agr_content)
  
  print(f"Output saved to \033[1m{output_file}\033[0m")

# ================================================================= #    
# Main Execution
def handle_interrupt(signal, frame):
  print("\n\033[1;31mWarnig: .agr generation incomplete. No file has been created.\033[0m")
  exit(1)

signal.signal(signal.SIGINT, handle_interrupt)

if __name__ == "__main__":
  agr_content, Nisotopes, format_type = gInitialize()
  agr_content = Generate(agr_content, Nisotopes, format_type)
  gOutput(agr_content, format_type)
