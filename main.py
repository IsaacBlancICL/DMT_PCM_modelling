# IMPORTING LIBRARIES
import matplotlib.pyplot as plt
import parameter_classes as pc
import temp_distr as td

# RUNNING TRIALS
for var in range(4,30,4):
    # creating instances of each class
    pipes  = pc.pipesClass(number=var)
    fluid  = pc.fluidClass()
    pcm    = pc.pcmClass(pipe_external_diam=pipes.Do)
    system = pc.systemClass(pipes, fluid)
    # simulating and graphing temp distribution
    td.graph(pipes,fluid,pcm,system,label=f"{var} pipes")
    
# MAKING GRAPH PRETTY
plt.xlabel('Distance along pipe (m)')
plt.ylabel('Fluid temperature (deg C)')
plt.legend()