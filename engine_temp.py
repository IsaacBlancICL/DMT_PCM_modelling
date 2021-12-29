# IMPORTING LIBRARIES
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import parameter_classes as pc
import temp_distr as td

#Instances of all the classes needed to run td solution
case   = pc.caseClass()
pcm    = pc.pcmClass()
pipes  = pc.pipesClass(case=case, pcm=pcm)
fluid  = pc.fluidClass()
system = pc.systemClass(pipes=pipes, fluid=fluid)

#Rate of heat release of engine, specific heat, and mass. Could be put into a class?
qe = 1
cpe = 1
me = 1

def EngineTempTime(qe,cpe,me,pipes,fluid,system,pcm):

    def qf(system,fluid,pipes,pcm):
        solution = td.solve(pipes, fluid, pcm, system)              #Temperature distribution along PCM
        x = solution[0]                                             #Relabeled to help relate to the on-paper maths
        Tpcm = solution[1]

        qfResult = (system.m*fluid.c/pipes.L) * sc.integrate.simpson(Tpcm,x)    #Mean heat transfered from PCM
        return(qfResult)

    def f(t, system.Ti):
        return((1/(me*cpe))*(qe + qf(pipes,fluid,system,pcm)))

    TempTime = sc.integrate.solve_ivp(f,[0,600],system.Ti) # arguments are: (gradient function, range of x values, initial value for T, max step in x)



    return(TempTime)

print(EngineTempTime(qe,cpe,me,pipes,fluid,system,pcm))