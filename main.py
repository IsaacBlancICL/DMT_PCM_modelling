# IMPORTING LIBRARIES
import matplotlib.pyplot as plt
import parameter_classes as pc
import temp_distr as td

# RUNNING TRIALS

# case 1
# creating instances of each class
pipes  = pc.pipesClass(number=18, length=4.16)
fluid  = pc.fluidClass()
pcm    = pc.pcmClass(pipe_external_diam=pipes.Do)
system = pc.systemClass(pipes, fluid)
# simulating and graphing temp distribution
td.graph(pipes,fluid,pcm,system,label="Case 1")

# case 3
# creating instances of each class
pipes  = pc.pipesClass(number=9, length=2.7)
fluid  = pc.fluidClass()
pcm    = pc.pcmClass(pipe_external_diam=pipes.Do)
system = pc.systemClass(pipes, fluid)
# simulating and graphing temp distribution
td.graph(pipes,fluid,pcm,system,label="Case 3")
    
# MAKING GRAPH PRETTY
plt.xlabel('Distance along pipe (m)')
plt.ylabel('Fluid temperature (deg C)')
plt.legend()