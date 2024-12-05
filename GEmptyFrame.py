# ==== Generate an empty .agr file
# ==== Adjust the axis range based on # of isotopes


def gframe(format_type):
  match format_type:
    case 1: # One istope
      axis_x1 = -0.5
      axis_x2 = 1.0
      break
  
  agr_content = []
  agr_content.append("# ==== Initial Frame ==== #")
  agr_content("@with g0                                         \n")
  agr_content("@    world -0.5, 0, 1, 2000                      \n")
  agr_content("@    stack world 0, 0, 0, 0                      \n")
  agr_content("@    znorm 1                                     \n")  
  agr_content("@    view 0.050000, 0.050000, 1.244118, 0.950000 \n")
  agr_content("@    title ""                                    \n")
  agr_content("@    title font 0                                \n")
  agr_content("@    title size 1.500000                         \n")
  agr_content("@    title color 1                               \n")
  agr_content("@    subtitle ""                                 \n")
  agr_content("@    subtitle font 0                             \n")
  agr_content("@    subtitle size 1.000000                      \n")
  agr_content("@    subtitle color 1                            \n")
  agr_content("@    xaxes scale Normal                          \n")
  agr_content("@    yaxes scale Normal                          \n")
  agr_content("@    xaxes invert off                                     
  agr_content("@    yaxes invert off                                       
  agr_content("@    xaxis  on                                                 
  agr_content("@    xaxis  type zero false                                        
  agr_content("@    xaxis  offset 0.000000 , 0.000000                               
  agr_content("@    xaxis  bar off                                                                
  agr_content("@    xaxis  bar color 1                                                  
  agr_content("@    xaxis  bar linestyle 1                                                          
  agr_content("@    xaxis  bar linewidth 1.0                                              
  agr_content("@    xaxis  label ""                                         
  agr_content("@    xaxis  label layout para                                                
  agr_content("@    xaxis  label place auto                                 
  agr_content("@    xaxis  label char size 1.000000                         
  agr_content("@    xaxis  label font 0                                                       
  agr_content("@    xaxis  label color 1                                                  
  agr_content("@    xaxis  label place normal                                         
  agr_content("@    xaxis  tick off                                                               
  agr_content("@    xaxis  tick major 2                                                                     
  agr_content("@    xaxis  tick minor ticks 1                                               
  agr_content("@    xaxis  tick default 6                                                           
  agr_content("@    xaxis  tick place rounded true                                      
  agr_content("@    xaxis  tick in                                                                
  agr_content("@    xaxis  tick major size 1.000000                                                           
  agr_content("@    xaxis  tick major color 1                                                   
  agr_content("@    xaxis  tick major linewidth 1.0                                                 
  agr_content("@    xaxis  tick major linestyle 1                                                             
  agr_content("@    xaxis  tick major grid off                                                              
  agr_content("@    xaxis  tick minor color 1                                                         
  agr_content("@    xaxis  tick minor linewidth 1.0                                                   
  agr_content("@    xaxis  tick minor linestyle 1                                                     
  agr_content("@    xaxis  tick minor grid off                                                    
  agr_content("@    xaxis  tick minor size 0.500000                                               
  agr_content("@    xaxis  ticklabel off                                                      
  agr_content("@    xaxis  ticklabel format general                                                   
  agr_content("@    xaxis  ticklabel prec 5                                                 
  agr_content("@    xaxis  ticklabel formula ""                                             
  agr_content("@    xaxis  ticklabel append ""                                          
  agr_content("@    xaxis  ticklabel prepend ""                                               
  agr_content("@    xaxis  ticklabel angle 0                                                      
  agr_content("@    xaxis  ticklabel skip 0                                                 
  agr_content("@    xaxis  ticklabel stagger 0                                                          
  agr_content("@    xaxis  ticklabel place normal                                                         
  agr_content("@    xaxis  ticklabel offset auto
  agr_content("@    xaxis  ticklabel offset 0.000000 , 0.010000
  agr_content("@    xaxis  ticklabel start type auto
  agr_content("@    xaxis  ticklabel start 0.000000
  agr_content("@    xaxis  ticklabel stop type auto
  agr_content("@    xaxis  ticklabel stop 0.000000
  agr_content("@    xaxis  ticklabel char size 1.000000
  agr_content("@    xaxis  ticklabel font 0
  agr_content("@    xaxis  ticklabel color 1
  agr_content("@    xaxis  tick place both
  agr_content("@    xaxis  tick spec type none
  agr_content("@    yaxis  on
  agr_content("@    yaxis  type zero false
  agr_content("@    yaxis  offset 0.000000 , 0.000000
  agr_content("@    yaxis  bar off
  agr_content("@    yaxis  bar color 1
  agr_content("@    yaxis  bar linestyle 1
  agr_content("@    yaxis  bar linewidth 1.0
  agr_content("@    yaxis  label ""
  agr_content("@    yaxis  label layout para
  agr_content("@    yaxis  label place auto
  agr_content("@    yaxis  label char size 1.000000
  agr_content("@    yaxis  label font 0
  agr_content("@    yaxis  label color 1
  agr_content("@    yaxis  label place normal
  agr_content("@    yaxis  tick off
  agr_content("@    yaxis  tick major 1000
  agr_content("@    yaxis  tick minor ticks 1
  agr_content("@    yaxis  tick default 6
  agr_content("@    yaxis  tick place rounded true
  agr_content("@    yaxis  tick in
  agr_content("@    yaxis  tick major size 1.000000
  agr_content("@    yaxis  tick major color 1
  agr_content("@    yaxis  tick major linewidth 1.0
  agr_content("@    yaxis  tick major linestyle 1
  agr_content("@    yaxis  tick major grid off
  agr_content("@    yaxis  tick minor color 1
  agr_content("@    yaxis  tick minor linewidth 1.0
  agr_content("@    yaxis  tick minor linestyle 1
  agr_content("@    yaxis  tick minor grid off
  agr_content("@    yaxis  tick minor size 0.500000
  agr_content("@    yaxis  ticklabel off
  agr_content("@    yaxis  ticklabel format general
  agr_content("@    yaxis  ticklabel prec 5
  agr_content("@    yaxis  ticklabel formula ""
  agr_content("@    yaxis  ticklabel append ""
  agr_content("@    yaxis  ticklabel prepend ""
  agr_content("@    yaxis  ticklabel angle 0
  agr_content("@    yaxis  ticklabel skip 0
  agr_content("@    yaxis  ticklabel stagger 0
  agr_content("@    yaxis  ticklabel place normal
  agr_content("@    yaxis  ticklabel offset auto
  agr_content("@    yaxis  ticklabel offset 0.000000 , 0.010000
  agr_content("@    yaxis  ticklabel start type auto
  agr_content("@    yaxis  ticklabel start 0.000000
  agr_content("@    yaxis  ticklabel stop type auto
  agr_content("@    yaxis  ticklabel stop 0.000000
  agr_content("@    yaxis  ticklabel char size 1.000000
  agr_content("@    yaxis  ticklabel font 0
  agr_content("@    yaxis  ticklabel color 1
  agr_content("@    yaxis  tick place both
  agr_content("@    yaxis  tick spec type none
  agr_content("@    altxaxis  off
  agr_content("@    altyaxis  off
  output_file = "test.agr"
  with open(output_file, 'w') as file:
    file.writelines(agr_content)
