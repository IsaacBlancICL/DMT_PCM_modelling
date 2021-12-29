# IMPORTING LIBRARIES
import scipy as sc
import parameter_classes as pc
import temp_distr as td


# creating instances of each class (except 'systemClass', which is declared in gradient function 'f')
case   = pc.caseClass()
pcm    = pc.pcmClass()
pipes  = pc.pipesClass(case=case, pcm=pcm)
fluid  = pc.fluidClass()


# DEFINING FUNCTION
def EngineTempTime(case,pcm,pipes,fluid, qe,cpe,me):

    # DEFINING THE ODE GRADIENT FUNCTION (ie: dT/dt where T is engine temperature)
    def f(t, T_engine):
        # an instance of systemClass is declared here, with the PCM inlet temperature set to whatever the engine temperature is
        system = pc.systemClass(inlet_temp=T_engine, pipes=pipes, fluid=fluid)
        
        # working out mean heat transfer from PCM to fluid
        solution = td.solve(pipes=pipes, fluid=fluid, pcm=pcm, system=system)   #Temperature distribution along PCM
        x = solution[0]                                                         #Relabeled to help relate to the on-paper maths
        Tpcm = solution[1]                                                      #Also relabeled
        qf = (system.m*fluid.c/pipes.L) * sc.integrate.simpson(Tpcm,x)          #Mean heat transfered from PCM
        
        # returning gradient
        return((1/(me*cpe))*(qe + qf))

    # SOLVING THE ODE
    TempTime = sc.integrate.solve_ivp(f, [0,600], [10], max_step=1) # arguments are: (gradient function, range of x values, initial value for T, max step in t)

    # RETURNING [t,T_engine]
    return [TempTime.t, TempTime.y[0]]






EngineTempTime(case,pcm,pipes,fluid, qe=1,cpe=1,me=1)