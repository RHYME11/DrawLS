# =========== Generate .agr Files ============ #
# Only draw states and realted information
# One Isotope Only 
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
states = [[], [], []]  # 3D array for storing [[Ex], [Jpi], [t1/2]]
se = [[], []] # 2D array for storing separation energy [[Sp, Sn], [value1, value2]]

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
    
    # Start reading states after "Ex"
    elif line.startswith("Ex"):
      read_states = True
      continue 
    # End reading states with "end"
    elif line.strip() == "states_end":
      read_states = False;
    # Read the 3 lines of Ex and Jpi values into `states`
    if read_states: 
      parts = line.split()
      states[0].append(float(parts[0].strip())) # Ex values
      states[1].append(parts[1].strip() if len(parts) > 1 else states[1].append(None)) # Jpi values
      states[2].append(parts[2].strip() if len(parts) > 2 else states[2].append(None)) # t1/2 values
    
    # Read separation energy 
    if line.startswith("Sp"):
      parts = line.split("=")
      se[0].append(parts[0].strip())
      se[1].append(parts[1].strip())
    if line.startswith("Sn"):
      parts = line.split("=")
      se[0].append(parts[0].strip())
      se[1].append(parts[1].strip())
       

# ================================================================= #    
# Step2: Choose the format and extract the empty format
# TODO: Formats display
while True:
  format_type = input("Enter the formate # (default is 1): ")
  format_file = f"formats/agr_format/empty{format_type}.agr"
  if os.path.exists(format_file):
    break
  else:
    print("Format file does not exist. Please try again.")

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
ex_highest = max(states[0]) # highest Ex
axis_y1 = -0.1 * ex_highest
axis_y2 = 1.1 * ex_highest

# Update .agr
# "@timestamp def" in line 57
# "@    world" in line 104
for i, line in enumerate(agr_content):
  if line.startswith("@timestamp def"):
    agr_content[i] = f'@timestamp def "{current_timestamp}"\n'
  if line.startswith("@    world"):
    parts = line.split(", ")
    axis_x1 = float(parts[0].split()[-1])  # Extract original xlower = -1 (default)
    axis_x2 = float(parts[2])              # Extract original xupper = 2 (default)
    agr_content[i] = f"@    world {axis_x1}, {axis_y1}, {axis_x2}, {axis_y2}\n"
    break

# Step3.2: States 
# Lines Xposition based on format x-axis range
# Fixed Ex    string position (default: right at states line )
# Fixed Jpi   string position (default: left at states line )
# t1/2 will be in Jpi string
linex1 = axis_x1 + 1.0 
linex2 = axis_x2 - 0.5 
pos_ex = linex2 + 0.02
pos_jpi= linex1 - 0.02
 
agr_content.append("# ==== States ==== #\n")
for idx, ex in enumerate(states[0]):
  agr_content.append(f"# State Lines Ex = {int(ex)} keV\n")
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
# Step 3.3: State Ex strings  
  agr_content.append(f"# State String Ex = {int(ex)} keV\n")
  agr_content.append("@with string\n")
  agr_content.append("@    string on\n")
  agr_content.append("@    string loctype world\n") # Local world (the other option is viewport)
  agr_content.append("@    string g0\n") # g0 is the current graph. (grace allow multiple graphs in the same canvas)
  agr_content.append(f"@    string {pos_ex}, {ex}\n") # left at ex lines and same height(y-axis)
  agr_content.append("@    string color 1\n") # color 1 = black
  agr_content.append("@    string rot 0\n") # rot = rotation (unit: deg)
  agr_content.append("@    string font 0\n") # font 0 = "Times-Romance"
  agr_content.append("@    string just 12\n") # just 12 = center right (row1,col3 in grace)
  agr_content.append("@    string char size 1.25\n") # char size 1.25 = 125 (in grace)
  if ex == 0:
    agr_content.append(f'@    string def "g.s."\n')
  else:
    ex = int(ex)
    agr_content.append(f'@    string def "{ex}"\n')
  agr_content.append("\n")
# Step 3.4: Jpi + t1/2
  if states[1][idx] is not None or states[2][idx] is not None:
    agr_content.append(f"# State String Jpi / t1/2 = {int(ex)} keV\n")
    agr_content.append("@with string\n")
    agr_content.append("@    string on\n")
    agr_content.append("@    string loctype world\n") # Local world (the other option is viewport)
    agr_content.append("@    string g0\n") # g0 is the current graph. (grace allow multiple graphs in the same canvas)
    agr_content.append(f"@    string {pos_jpi}, {ex}\n") # left at ex lines and same height(y-axis)
    agr_content.append("@    string color 1\n") # color 1 = black
    agr_content.append("@    string rot 0\n") # rot = rotation (unit: deg)
    agr_content.append("@    string font 0\n") # font 0 = "Times-Romance"
    agr_content.append("@    string just 13\n") # just 13 = center left (row3,col3 in grace)
    agr_content.append("@    string char size 1.25\n") # char size 1.25 = 125 (in grace)
    if states[1][idx] is not None:
      filling_str = states[1][idx]
      if states[2][idx] is not None:
        filling_str += ", "
        filling_str += states[2][idx]
    else:
      filling_str = states[2][idx]
    agr_content.append(f'@    string def "{filling_str}"\n')
    
# Step 3.5: Separation Energies
se_linex1 = linex1 - 0.2
se_linex2 = linex2 + 0.2
pos_se = se_linex1 - 0.02
for idx in range(len(se[1])):
  se_val = int(se[1][idx])
  if se_val != 0:
    agr_content.append(f"# SE Lines = {int(se_val)} keV\n")
    agr_content.append("@with line\n")
    agr_content.append("@    line on\n")
    agr_content.append("@    line loctype world\n")  # Local world (the other option is viewport)
    agr_content.append("@    line g0\n") # g0 is the current graph. (grace allow multiple graphs in the same canvas)
    agr_content.append(f"@    line {se_linex1}, {se_val}, {se_linex2}, {se_val}\n") # line location [x1, y1, x2, y2]
    agr_content.append("@    line linewidth 2.0\n") # linewdith = 2.0 (default)
    agr_content.append("@    line linestyle 3\n") # linestyle 3= dashed line 
    agr_content.append("@    line color 1\n") # color 1 = black
    agr_content.append("@    line arrow 0\n") # no arrow
    agr_content.append("@    line arrow type 0\n") # no arrow
    agr_content.append("@    line arrow length 1.000000\n") # no arrow
    agr_content.append("@    line arrow layout 1.000000, 1.000000\n") # no arrow
    agr_content.append("@line def\n")
    agr_content.append("\n")
    agr_content.append(f"# SE String  = {int(se_val)} keV\n")
    agr_content.append("@with string\n")
    agr_content.append("@    string on\n")
    agr_content.append("@    string loctype world\n") # Local world (the other option is viewport)
    agr_content.append("@    string g0\n") # g0 is the current graph. (grace allow multiple graphs in the same canvas)
    agr_content.append(f"@    string {pos_se}, {se_val}\n") # left at se lines and same height(y-axis)
    agr_content.append("@    string color 1\n") # color 1 = black
    agr_content.append("@    string rot 0\n") # rot = rotation (unit: deg)
    agr_content.append("@    string font 0\n") # font 0 = "Times-Romance"
    agr_content.append("@    string just 13\n") # just 13 = center left (row3,col3 in grace)
    agr_content.append("@    string char size 1.25\n") # char size 1.25 = 125 (in grace)
    agr_content.append(f'@    string def "{se[0][idx]} = {se_val} keV"\n')
    break 



# Step3.final: Isotope Strings
# Calculate string Xposition based on formate x-axis range
posx_iso_string = (linex1 + linex2) / 2 
agr_content.append("# ==== Isotope Strings ==== #\n")
agr_content.append("@with string\n")
agr_content.append("@    string on\n")
agr_content.append("@    string loctype world\n") # Local world (the other option is viewport)
agr_content.append("@    string g0\n") # g0 is the current graph. (grace allow multiple graphs in the same canvas)
agr_content.append(f"@    string {posx_iso_string}, {axis_y1*0.6}\n") # string position. x = center of the graph, y = y-axis_lower * 0.6
agr_content.append("@    string color 1\n") # color 1 = black
agr_content.append("@    string rot 0\n") # rot = rotation (unit: deg)
agr_content.append("@    string font 2\n") # font 2 = "Times-Bold"
agr_content.append("@    string just 14\n") # just 14 = center
agr_content.append("@    string char size 2.0\n") # char size 2.0 = 200 (in grace)
agr_content.append(f'@    string def "\\S\\v{{-.2}}{Z+N}\\N\\h{{-.8}}\\s\\v{{.2}}{Z}\\N{isotope}\\s\\v{{.2}}{N}"\n')
agr_content.append("\n")




# =========================== Output file ================================== #    
# Write the modified content to a new output file
output_file = f"{isotope}{N+Z}_format{format_type}.agr"
with open(output_file, 'w') as file:
  file.writelines(agr_content)








# ======= Test the extracted data ======== #
#print(f"isotope: {isotope}")
#print(f"Z: {Z}")
#print(f"N: {N}")
#print("states:", states)
