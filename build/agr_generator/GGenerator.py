
# =========== Global variables =============#
glb_state_color = 1.0 # color = 1.0 ==> black
glb_state_style = 1.0 # style = 1.0 ==> solid line
glb_state_width = 2.0 # width = 2.0
glb_txt_color   = 1.0 # color = 1.0 ==> black
glb_txt_rot     = 0.0 # rot = 0.0 deg
glb_txt_font    = 0.0 # font - 0.0 ==> Time-Romance
glb_cr_just     = 12.0# just = 12.0 ==> center right (row1,col3 in grace)
glb_txt_size    = 1.25 # char size = 0.9 ==> 90 (in grace)
glb_cl_just     = 13.0# just = 13.0 ==> center left (row3,col3 in grace)

def generator1(agr_content, niso, isotope, states, se):
  # 1.Adjust Y-axis range based on the highest Ex in the input file
  Z = isotope[1]
  N = isotope[2]
  ex_highest = max(states[0]) # highest Ex
  axis_x1 = axis_x2 = axis_y1 = axis_y2 = float("inf")
  for i, line in enumerate(agr_content):
    if line.startswith("@    world"):
      parts = line.split(", ")
      axis_x1 = float(parts[0].split()[-1])  # Extract original xlower = -0.5 (default)
      axis_x2 = float(parts[2])              # Extract original xupper = 1.5 (default)
      axis_y1 = float(parts[1].split()[-1])  # Extract original ylower = -200 (default)
      axis_y2 = float(parts[3])              # Extract original yupper = 2000 (default)
      if axis_y2 < ex_highest * 1.1:
        # axis_y1 = -0.1 * ex_highest # Fixed the ylower now
        axis_y2 = 1.1 * ex_highest
      agr_content[i] = f"@    world {axis_x1}, {axis_y1}, {axis_x2}, {axis_y2}\n"
      break

# 2. States 
# Lines Xposition based on x-axis range and # of isotopes
# Fixed Ex    string position (default: right at states line )
# Fixed Jpi   string position (default: left at states line )
# t1/2 will be in Jpi string
  linex1 = axis_x1 + 0.5 + 1.0*niso  # the first line offset from the x-axis is 0.5, space between beginning of lines = 1.0
  linex2 = linex1 + 0.5            # line length = 0.5
  if niso == 0:
    pos_ex = linex2 + 0.02
    pos_jpi= linex1 - 0.02  
  else:
    pos_jpi= linex2 + 0.02
    pos_ex= linex1 - 0.02  

  for idx, ex in enumerate(states[0]):
    # 2.1 States Ex Lines
    agr_content.append(f"# State Lines Ex = {int(ex)} keV\n")
    agr_content.append("@with line\n")
    agr_content.append("@    line on\n")
    agr_content.append("@    line loctype world\n")  # Local world (the other option is viewport)
    agr_content.append("@    line g0\n") # g0 is the current graph. (grace allow multiple graphs in the same canvas)
    agr_content.append(f"@    line {linex1}, {ex}, {linex2}, {ex}\n") # line location [x1, y1, x2, y2]
    agr_content.append(f"@    line linewidth {glb_state_width}\n") # linewdith = 2.0 (default)
    agr_content.append(f"@    line linestyle {glb_state_style}\n") # linestyle 1= solid line 
    agr_content.append(f"@    line color {glb_state_color}\n") # color 1 = black
    agr_content.append("@    line arrow 0\n") # no arrow
    agr_content.append("@    line arrow type 0\n") # no arrow
    agr_content.append("@    line arrow length 1.000000\n") # no arrow
    agr_content.append("@    line arrow layout 1.000000, 1.000000\n") # no arrow
    agr_content.append("@line def\n")
    agr_content.append("\n")
    # 2.2 State Ex strings  
    agr_content.append(f"# State String Ex = {int(ex)} keV\n")
    agr_content.append("@with string\n")
    agr_content.append("@    string on\n")
    agr_content.append("@    string loctype world\n") # Local world (the other option is viewport)
    agr_content.append("@    string g0\n") # g0 is the current graph. (grace allow multiple graphs in the same canvas)
    agr_content.append(f"@    string {pos_ex}, {ex}\n") # left at ex lines and same height(y-axis)
    agr_content.append(f"@    string color {glb_txt_color}\n") 
    agr_content.append(f"@    string rot {glb_txt_rot}\n") 
    agr_content.append(f"@    string font {glb_txt_font}\n")
    if niso == 0: 
      agr_content.append(f"@    string just {glb_cr_just}\n") 
    else:  
      agr_content.append(f"@    string just {glb_cl_just}\n") 
    agr_content.append(f"@    string char size {glb_txt_size}\n") 
    if ex == 0:
      agr_content.append(f'@    string def "g.s."\n')
    else:  
      ex = int(ex)
      agr_content.append(f'@    string def "{ex}"\n')
    agr_content.append("\n")
    # Step 2.3: Jpi + t1/2
    if states[1][idx] is not None or states[2][idx] is not None:
      agr_content.append(f"# State String Jpi / t1/2 = {int(ex)} keV\n")
      agr_content.append("@with string\n")
      agr_content.append("@    string on\n")
      agr_content.append("@    string loctype world\n") # Local world (the other option is viewport)
      agr_content.append("@    string g0\n") # g0 is the current graph. (grace allow multiple graphs in the same canvas)
      agr_content.append(f"@    string {pos_jpi}, {ex}\n") # left at ex lines and same height(y-axis)
      agr_content.append(f"@    string color {glb_txt_color}\n")
      agr_content.append(f"@    string rot {glb_txt_rot}\n") 
      agr_content.append(f"@    string font {glb_txt_font}\n") 
      if niso == 0:
        agr_content.append(f"@    string just {glb_cl_just}\n") 
      else:
        agr_content.append(f"@    string just {glb_cr_just}\n") 
      agr_content.append(f"@    string char size {glb_txt_size}\n") 
      if states[1][idx] is not None:
        filling_str = states[1][idx]
        if states[2][idx] is not None:
          filling_str += ", "
          filling_str += states[2][idx]
      else:
        filling_str = states[2][idx]
      agr_content.append(f'@    string def "{filling_str}"\n')  

  # 3. Separation Energies
  se_linex1 = linex1 - 0.1
  se_linex2 = linex2 + 0.1
  if niso == 0:
    pos_se = se_linex1 - 0.02
  else:
    pos_se = se_linex2 + 0.02
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
      agr_content.append(f"@    string color {glb_txt_color}\n") 
      agr_content.append(f"@    string rot {glb_txt_rot}\n") 
      agr_content.append(f"@    string font {glb_txt_font}\n") 
      if niso == 0:
        agr_content.append(f"@    string just {glb_cl_just}\n") 
      else:
        agr_content.append(f"@    string just {glb_cr_just}\n") 
      agr_content.append(f"@    string char size {glb_txt_size}\n") 
      agr_content.append(f'@    string def "{se[0][idx]} = {se_val} keV"\n')
      break 

  # Final: Isotope Strings
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
  agr_content.append(f'@    string def "\\S\\v{{-.2}}{Z+N}\\N\\h{{-.8}}\\s\\v{{.2}}{Z}\\N{isotope[0]}\\s\\v{{.2}}{N}"\n')
  agr_content.append("\n")

  return agr_content
















