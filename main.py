# IMPORTING LIBRARIES
import matplotlib.pyplot as plt
import temp_distr as td

# RUNNING TRIALS
for number in range(4,30,4):
    td.trial(number)
    
# MAKING GRAPH PRETTY
plt.xlabel('Distance along pipe (m)')
plt.ylabel('Fluid temperature (deg C)')
plt.legend()