import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import parameter_classes as pc
import temp_distr as td

#Instances of all the classes needed to run td solution
pipes = pc.pipesClass()
fluid = pc.fluidClass()
pcm = pc.pcmClass(pipe_external_diam=pipes.Do)
system = pc.systemClass(pipes, fluid)

qe = 1              #Rate of heat release of engine, specific heat, and mass. Could be put into a class?
cpe = 1
me = 1

def EngineTempTime(qe,cpe,me,pipes,fluid,system,pcm):

    def qf(system,fluid,pipes,pcm):
        solution = td.solve(pipes, fluid, pcm, system)              #Temperature distribution along PCM
        x = solution[0]                                             #Relabeled to help relate to the on-paper maths
        Tpcm = solution[1]

        qf = (system.m*fluid.c/x[-1]) * sc.integrate.simpson(Tpcm,x)    #Mean heat transfered from PCM
        return(qf)

    def f(t, system.Ti):

        return((1/(me*cpe))*(qe + qf(pipes,fluid,system,pcm)))

    TempTime = sc.integrate.solve_ivp(f,[0,600],system.Ti)



    return(TempTime)

print(EngineTempTime(qe,cpe,me,pipes,fluid,system,pcm))