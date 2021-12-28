# IMPORTING LIBRARIES
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


def graph(pipes,fluid,pcm,system,label=None):
    """
    Produces a graph of the temperature distribution along the pipe x-axis.
    
    The arguments are instances of the four parameter classes. The fifth argument is optional,
    for giving the graph series a label if you want a legend.
    
    In the 'solve_ivp' documentation, 't' is the independant variable and 'y' is the dependant variable.
    In this script, 'x' (distance along pipe) is the indendant variable and 'T' (fluid temperature) is
    the dependant variable.
    
    Frustratingly, you still have to write 't' and 'y' sometimes when using 'solve_ivp'.
    """
    
    # DEFINING THE ODE GRADIENT FUNCTION (ie: dT/dx where T is coolant temperature)
    def f(x, T):
        numerator = pcm.T - T
        denominator = (1/(np.pi*pipes.Di*system.h)) + (np.log(pipes.Do/pipes.Di)/(2*np.pi*pipes.k)) + (np.log(pcm.CtoC/pipes.Do)/(2*np.pi*pcm.k))
        return (1/(system.m*fluid.c)) * (numerator/denominator)
    
    # SOLVING THE ODE
    solution = solve_ivp(f, [0, pipes.L], [system.Ti], max_step=0.01) # arguments are: (gradient function, range of x values, initial value for T, max step in x)
    
    # GRAPHING THE SOLUTION
    plt.plot(solution.t, solution.y[0], label=label)