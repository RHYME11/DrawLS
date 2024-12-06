# ==== gReadFile ==== #
# Read input.data file:
# Each input.dat file should only contain 1 isotope and 3 parts of info
# Eg, data/Si29.dat


def gReadFile(input_file):
  isotope = [None, None, None] # isotope_name, Z, N
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
        isotope[0] = line.split(":")[1].strip()
      elif line.startswith("Z ="):
        isotope[1] = int(line.split("=")[1].strip())
      elif line.startswith("N ="):
        isotope[2] = int(line.split("=")[1].strip())
               
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

    return isotope, states, se
