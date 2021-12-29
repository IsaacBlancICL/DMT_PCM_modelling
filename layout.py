# IMPORTING LIBRARIES
import numpy as np
import matplotlib.pyplot as pl
import math
from matplotlib.lines import Line2D
import pandas as pd
 

# DEFINING FUNCTIONS
def PipeMaker(case,pipes,pcm,table=False,visualisation=False):
    """
    Function uses the following information, stored in 'case', 'pipes' and 'pcm' respectively...
        - the case dimensions
        - the number of pipes that the main coolant pipe splits into, as well as their diameter and thickness
        - the PCM volume requirement
    
    Function returns a dictionary containing:
        Lp          : length of each pipe going through the PCM
        CtoC        : centre-to-centre distance (diagram on spreadsheet)
        designPass  : is this a valid design? (enough volume of PCM and the pipes don't interfere with one another)
    
    Two additional features of the function are turned off by default but can be turned on
        - It prints a results table table=True.
        - It makes a visualisation of the pipe layout if visualisation=True.
    
    THE FUNCTION IS WRITTEN WITH SOME DIFFERENT NAMING CONVENTIONS TO THE OTHER PYTHON FILES!
    Eg: Alex uses 'passes' to refer to the number of small pipes that the main coolant hose splits into,
    which I refer to as 'number' in the other code.
    """

    # CALCULATIONS
    #Center to Center Distance:
    CtoC = case.W /  (pipes.n + np.cos(np.pi / 3))
    sidewallgap = CtoC / 2
    CtoCx = CtoC * np.cos(np.pi / 3)
    CtoCy = CtoC * np.sin(np.pi / 3)
    returns = math.floor( case.H / CtoCy ) #Calculates number of returns. Essentially number of pipes in the z direction. This is deliberately rounded down.
    #Misc:
    n = returns * pipes.n                               #Number of pipe lengths overall
    Lp = returns * case.L                               #Total length of pipe per pass
    Lt = n * case.L                                     #Total length of pipe in system
    excess = case.H - ((CtoCy * (returns - 1)) + CtoC)  #The excess height 
    #Surface Area:
    pipesurfaceinner = np.pi * pipes.Di * Lt            #Total inner surface area of the pipes
    pipesurfaceouter = np.pi * pipes.Do * Lt            #Total outer surface area of the pipes
    #Volume:
    totalvolume = case.L * case.W * case.H
    pipevolume = 0.25 * np.pi * (pipes.Do**2) * Lt
    pcmvolume = totalvolume - pipevolume
    if pcmvolume >= pcm.volReq:
        pcmVolPass = True
    if pcmvolume <= pcm.volReq:
        pcmVolPass = False
    excessvolume = totalvolume - pcm.volReq
    wastedvolume = excess * case.L * case.W #Wasted volume, this is filled up by PCM but not efficiently heated by copper pipe
    if CtoC >= pipes.Do:
        pipeIntPass = True
    if CtoC <= pipes.Do:
        pipeIntPass = False
 
    
    # DISPLAYING RESULTS TABLE
    if table:
        values = [
            case.W,
            case.H,
            case.L,
            pipes.Do,
            pipes.Di,
            pipes.t,
            CtoC,
            sidewallgap,
            pipes.n,
            returns,
            n,
            Lp,
            Lt,
            pipesurfaceinner,
            pipesurfaceouter,
            totalvolume,
            pipevolume,
            pcmvolume,
            pcmVolPass,
            excessvolume,
            excess,
            wastedvolume,
            pipeIntPass]
        units = ["m","m","m","m","m","m","m","m","","","","m","m","m^3","m^2","m^2","m^3","m^3","","m^3","m","m^3",""]
        df = pd.DataFrame(list(zip(values,units)), index =[
            "Container Width",
            "Container Height",
            "Container Length",
            "Pipe Outer Diameter",
            "Pipe Inner Diameter",
            "Pipe Thickness",
            "Center to Center Distance",
            "Side Wall Gap",
            "Pipe Passes",
            "Pipe Returns",
            "Number of Pipe Straights",
            "Pipe Length per Pass",
            "Total Pipe Length",
            "Total Inner Pipe Surface Area",
            "Total Outer Pipe Surface Area",
            "Container Volume",
            "Pipe Volume",
            "PCM Volume",
            "Sufficient PCM Volume Check",
            "Excess PCM Volume",
            "Excess Container Height",
            "Wasted Volume",
            "Pipe Interference Check"], 
            columns = [
            "Values:",
            "Units:"])
        print(df)
 
 
    # DISPLAYING CROSS SECTION VISUALISATION
    if visualisation:
        #Setting up grid:
        x = [0] * pipes.n * returns
        y = [0] * pipes.n * returns
        columns = pipes.n*2 #Number of vertical columns
        #Filling empty arrays with data:
        for j in range (0,columns):
            for i in range(j,pipes.n*returns,columns):
                x[i] = sidewallgap + (j * CtoC * 0.5) #Creates the x value locations. 1st term is offset from the corner, 2nd term is the following spacing
            for k in range(j,pipes.n*returns,columns):
                y[k] = sidewallgap + ((2*CtoCy * (k-j))/columns) + ((CtoCy)* (-0.5) * (((-1)**j) -1)) #Creates the y value locations. 1st term is the offset from the corner, 2nd term is the vertical spacing, 3rd term is the additional extra offset from every 2nd column
        #Plotting:
        fig, ax = pl.subplots()
        pl.rcParams["figure.figsize"] = [12,12] #Adjusts size of plot
        for i in range(0,pipes.n*returns): #Plotting outer radius of pipes
            circle = pl.Circle((x[i],y[i]),pipes.Do/2,color="b",fill=False)
            ax.add_patch(circle)
        for i in range(0,pipes.n*returns): #Plotting outer radius of tubular PCM volume
            circle = pl.Circle((x[i],y[i]),sidewallgap,color="r",fill=False)
            ax.add_patch(circle)
        pl.scatter(x,y,color='black') #Plots pipe locations
        #Graph Annotations/Formatting:
        pl.xlim(0,case.W) #Sets scale of axis to the dimensions of the cross-section of the container
        pl.ylim(0,case.H)
        ax.set_title("PCM Heat Exchanger Cross Section:",fontsize=20)
        ax.set_xlabel('Container Width (m)',fontsize=16)
        ax.set_ylabel('Container Height (m)',fontsize=16)
        custom_lines = [Line2D([0], [0], color="red", lw=4),
                    Line2D([0], [0], color="blue", lw=4),
                    Line2D([0], [0], color="black", lw=4)]
        ax.legend(custom_lines, ['PCM Tubular Volume Boundary', 'Copper Pipe', 'Pipe Centrepoint'],loc="upper left",borderaxespad=0.,bbox_to_anchor=(1.05, 1))
        pl.show()
    
    
    # RETURNING RESULTS
    return {"Lp":Lp, "CtoC":CtoC, "designPass":(pcmVolPass & pipeIntPass)}