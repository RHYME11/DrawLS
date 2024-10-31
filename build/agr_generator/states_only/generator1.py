# =========== Generate .agr Files ============ #
# Only draw states and realted information 
# ============================================ #

import os
from datetime import datetime

# ================================================================= #    
# Step1: Open and read the file
while True:
  input_file = input("Enter the filename (with path if needed): ")
  if os.path.exists(input_file):
    break
  else:
    print("File does not exist. Please try again.")

isotope, Z, N = None, None, None
states = [[], []]  # 2D array for storing Ex and Jpi values

with open(input_file, 'r') as file:
    read_states = False
    for line in file:
        # Ignore lines starting with "#"
        if line.startswith("#"):
            continue
        
        # Extract isotope, Z, and N
        if line.startswith("Isotope:"):
            isotope = line.split(":")[1].strip()
        elif line.startswith("Z ="):
            Z = int(line.split("=")[1].strip())
        elif line.startswith("N ="):
            N = int(line.split("=")[1].strip())
        
        # Start reading states after encountering "Ex  Jpi"
        elif line.strip() == "Ex	  Jpi":
            read_states = True
            continue
        
        # Read the 5 lines of Ex and Jpi values into `states`
        if read_states:
            parts = line.split()
            if len(parts) == 2:
                states[0].append(float(parts[0]))  # Ex values
                states[1].append(parts[1])         # Jpi values


# ================================================================= #    
# Step2: Choose the format and extract the empty format
# TODO: Formats display
while True:
  format_type = input("Enter the formate # (default is 1): ")
  format_file = f"formats/empty{format_type}.agr"
  if os.path.exists(format_file):
    break
  else:
    print("File does not exist. Please try again.")

with open(format_file, 'r') as file:
  agr_content = file.readlines()

agr_content.append("\n")

# ================================================================= #    
# Step3: Based on input file information
# Step3.1: Adjust the frame information
# ! After Step 3.1, the plot should still be empty, 
# but the y-axis and other basic information will be adjusted

# 3.1.1. Generate the current timestamp in the specified format
current_timestamp = datetime.now().strftime("%a %b %d %H:%M:%S %Y")

# 3.1.2.Adjust Y-axis range based on the highest Ex in the input file
highest = max(states[0]) # highest Ex
ylower = -0.1 * highest
yupper = 1.1 * highest

# Update .agr
# "@timestamp def" in line 57
# "@    world" in line 104
for i, line in enumerate(agr_content):
  if line.startswith("@timestamp def"):
    agr_content[i] = f'@timestamp def "{current_timestamp}"\n'
  if line.startswith("@    world"):
    parts = line.split(", ")
    xlower = float(parts[0].split()[-1])  # Extract original xlower = -1 (default)
    xupper = float(parts[2])              # Extract original xupper = 3 (default)
    agr_content[i] = f"@    world {xlower}, {ylower}, {xupper}, {yupper}\n"
    break

# Step3.2: Isotope Strings
# Calculate string Xposition based on formate x-axis range
iso_stringx = (xlower + xupper) / 2 
agr_content.append("# ==== Isotope Strings ==== #\n")
agr_content.append("@with string\n")
agr_content.append("@    string on\n")
agr_content.append("@    string loctype world\n") # Local world (the other option is viewport)
agr_content.append("@    string g0\n") # g0 is the current graph. (grace allow multiple graphs in the same canvas)
agr_content.append(f"@    string {iso_stringx}, {ylower*0.6}\n") # string position. x = center of the graph, y = y-axis_lower * 0.6
agr_content.append("@    string color 1\n") # color 1 = black
agr_content.append("@    string rot 0\n") # rot = rotation (unit: deg)
agr_content.append("@    string font 2\n") # font 2 = "Times-Bold"
agr_content.append("@    string just 14\n") # just 14 = center
agr_content.append("@    string char size 2.0\n") # char size 2.0 = 200 (in grace)
agr_content.append(f'@    string def "\\S\\v{{-.2}}{Z+N}\\N\\h{{-.8}}\\s\\v{{.2}}{Z}\\N{isotope}\\s\\v{{.2}}{N}"\n')
agr_content.append("\n")


# Step3.3: States lines
# Calculate lines Xposition based on format x-axis range
linex1 = xlower + 0.5
linex2 = xupper - 0.5
agr_content.append("# ==== States Lines ==== #\n")
for ex in states[0]:
  agr_content.append(f"# State Ex = {int(ex)} keV\n")
  agr_content.append("@with line\n")
  agr_content.append("@    line on\n")
  agr_content.append("@    line loctype world\n")  # Local world (the other option is viewport)
  agr_content.append("@    line g0\n") # g0 is the current graph. (grace allow multiple graphs in the same canvas)
  agr_content.append(f"@    line {linex1}, {ex}, {linex2}, {ex}\n") # line location [x1, y1, x2, y2]
  agr_content.append("@    line linewidth 2.0\n") # linewdith = 2.0 (default)
  agr_content.append("@    line linestyle 1\n") # linestyle 1= solid line 
  agr_content.append("@    line color 1\n") # color 1 = black
  agr_content.append("@    line arrow 0\n") # no arrow
  agr_content.append("@    line arrow type 0\n") # no arrow
  agr_content.append("@    line arrow length 1.000000\n") # no arrow
  agr_content.append("@    line arrow layout 1.000000, 1.000000\n") # no arrow
  agr_content.append("@line def\n")
  agr_content.append("\n")

# ================================================================= #    
# Write the modified content to a new output file
base_filename = os.path.splitext(os.path.basename(input_file))[0]
output_file = f"{base_filename}_output.agr"
with open(output_file, 'w') as file:
  file.writelines(agr_content)








# ======= Test the extracted data ======== #
#print(f"isotope: {isotope}")
#print(f"Z: {Z}")
#print(f"N: {N}")
#print("states:", states)
