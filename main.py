# IMPORTING LIBRARIES
import matplotlib.pyplot as plt
import parameter_classes as pc
import temp_distr as td

# TRIALING DIFFERENT VALUES FOR STUFF
for var in range(4,30,4):
    # creating instances of each class
    pipes  = pc.pipesClass(number=var, length=100)
    fluid  = pc.fluidClass()
    pcm    = pc.pcmClass(pipe_external_diam=pipes.Do)
    system = pc.systemClass(pipes, fluid)
    # simulating temp distribution
    solution = td.solve(pipes,fluid,pcm,system)
    # graphing
    plt.plot(solution[0],solution[1],label=f"{var} pipes")
    
# MAKING GRAPH PRETTY
plt.xlabel('Distance along pipe (m)')
plt.ylabel('Fluid temperature (deg C)')
plt.legend()