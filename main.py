# IMPORTING LIBRARIES
import csv
import matplotlib.pyplot as plt
import parameter_classes as pc
import temp_distr as td
#import engine_temp as et
import grapher


# PIPE CROSS SECTION OPTIONS
# from Alex's spreadsheet 'Copper Pipe Data' and of the form [internal diameter (m), thickness (m)]
pipeCSOptions = [ [0.0028, 0.0006],
                  [0.0034, 0.0008],
                  [0.0048, 0.0006],
                  [0.0068, 0.0006],
                  [0.0086, 0.0007],
                  [0.0108, 0.0006],
                  [0.0130, 0.0010],
                  [0.0136, 0.0007],
                  [0.0146, 0.0007],
                  [0.0196, 0.0012],
                  [0.0202, 0.0009] ]


# PIPE NUMBER OPTIONS
# ie: how many small pipes the main coolant pipe split into when it reaches the PCM
pipeNOptions = range(1,21)


# TRIALING COMBINATIONS OF OPTIONS
results = [[],[],[],[]] # [[inner diams], [numbers of pipes], [outlet temps], [CS ratios]]
for pipeCSOption in pipeCSOptions:
    for pipeNOption in pipeNOptions:
        # creating instances of each class
        case   = pc.caseClass()
        pcm    = pc.pcmClass()
        pipes  = pc.pipesClass(internal_diam=pipeCSOption[0], wall_thickness=pipeCSOption[1], number=pipeNOption, case=case, pcm=pcm)
        # only continue if this configuration is valid (ie: enough PCM volume and pipes don't interfere)
        if pipes.Pass:
            fluid  = pc.fluidClass()
            system = pc.systemClass(case=case, pipes=pipes, fluid=fluid)
            # simulating temp distribution
            print(f"Solving for: Int diam = {round(pipes.Di*1000,1)}mm, {pipes.n} pipes")
            solution = td.solve(pipes,fluid,pcm,system)
            # saving outlet temperature results
            results[0] += [pipes.Di]
            results[1] += [pipes.n]
            results[2] += [solution[1][-1]]
            results[3] += [system.hb]
            # simulating engine heating
            #ET_results = et.EngineTempTime(case=case,pcm=pcm,pipes=pipes,fluid=fluid, qe=1,cpe=1,me=1)
       
        
# GRAPHING RESULTS
grapher.graph(x=results[0],y=results[1],z=results[2],zlabel='PCM outlet temp (deg C)')
grapher.graph(x=results[0],y=results[1],z=results[3],zlabel='Pressure loss (Bar)')