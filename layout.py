import numpy as np
import matplotlib.pyplot as pl
import matplotlib.patches as patches
import math
from matplotlib.lines import Line2D
import pandas as pd
 
#Input Information:
 
#Container Dimensions:
width = 0.16 #Distance in x direction
height = 0.16 #Distance in z direction
length = 0.35 #Distance in y direction
#Pipe Information:
pipeOD = 0.006
pipethick = 0.0005 
#Further Heat Exchanger Design Parameters:
passes = 12 #How many pipes the big inlet pipe splits into
pcmvolumereq = 0.00712 #Required volume of PCM in m^3
 
 
#Function for calculatuing max pipe density and other information for a few given parameters:
def PipeMaker(length,width,height,pipeOD,pipethick,passes,pcmvolumereq):
    #Calculating Center to Center Distance:
    CtoC = width /  (passes + np.cos(np.pi / 3))
    sidewallgap = CtoC / 2
    CtoCx = CtoC * np.cos(np.pi / 3)
    CtoCy = CtoC * np.sin(np.pi / 3)
    returns = math.floor( height / CtoCy ) #Calculates number of returns. Essentially number of rows. This is deliberately rounded down.
 
    #Misc Results:
    n = returns * passes #Number of pipe lengths overall
    Lp = returns * length #Total length of pipe per pass
    Lt = n * length #Total length of pipe in system
    pipeID = pipeOD - (2 * pipethick)
    excess = height - ((CtoCy * (returns - 1)) + CtoC) #The excess height 
 
    #Surface Area Results:
    pipesurfaceinner = np.pi * pipeID * Lt #Total outer and inner surface area of the pipes
    pipesurfaceouter = np.pi * pipeOD * Lt 
 
    #Volume Results:
    totalvolume = length * width * height
    pipevolume = 0.25 * np.pi * (pipeOD**2) * Lt
    pcmvolume = totalvolume - pipevolume
    if pcmvolume >= pcmvolumereq:
        pcmpass = "Pass"
    if pcmvolume <= pcmvolumereq:
        pcmpass = "Fail"
    excessvolume = totalvolume - pcmvolumereq
    wastedvolume = excess * length * width #Wasted volume, this is filled up by PCM but not efficiently heated by copper pipe
    if CtoC >= pipeOD:
        pipeinterference = "Pass"
    if CtoC <= pipeOD:
        pipeinterference = "Fail"
 
 
#Same as prev. function but displays results in table. Use this for specific cases, not for a set of data
def PipeMakerResults(length,width,height,pipeOD,pipethick,passes,pcmvolumereq):
    #Calculating Center to Center Distance:
    CtoC = width /  (passes + np.cos(np.pi / 3))
    sidewallgap = CtoC / 2
    CtoCx = CtoC * np.cos(np.pi / 3)
    CtoCy = CtoC * np.sin(np.pi / 3)
    returns = math.floor( height / CtoCy ) #Calculates number of returns. Essentially number of pipes in the z direction. This is deliberately rounded down.
 
    #Misc Results:
    n = returns * passes #Number of pipe lengths overall
    Lp = returns * length #Total length of pipe per pass
    Lt = n * length #Total length of pipe in system
    pipeID = pipeOD - (2 * pipethick)
    excess = height - ((CtoCy * (returns - 1)) + CtoC) #The excess height 
 
    #Surface Area Results:
    pipesurfaceinner = np.pi * pipeID * Lt #Total outer and inner surface area of the pipes
    pipesurfaceouter = np.pi * pipeOD * Lt 
 
    #Volume Results:
    totalvolume = length * width * height
    pipevolume = 0.25 * np.pi * (pipeOD**2) * Lt
    pcmvolume = totalvolume - pipevolume
    if pcmvolume >= pcmvolumereq:
        pcmpass = "Pass"
    if pcmvolume <= pcmvolumereq:
        pcmpass = "Fail"
    excessvolume = totalvolume - pcmvolumereq
    wastedvolume = excess * length * width #Wasted volume, this is filled up by PCM but not efficiently heated by copper pipe
    if CtoC >= pipeOD:
        pipeinterference = "Pass"
    if CtoC <= pipeOD:
        pipeinterference = "Fail"
 
    #Displayed Results:
 
    #Table:
    values = [
        width,
        height,
        length,
        pipeOD,
        pipeID,
        pipethick,
        CtoC,
        sidewallgap,
        passes,
        returns,
        n,
        Lp,
        Lt,
        pipesurfaceinner,
        pipesurfaceouter,
        totalvolume,
        pipevolume,
        pcmvolume,
        pcmpass,
        excessvolume,
        excess,
        wastedvolume,
        pipeinterference]
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
 
 
    #Cross Section Visualization:
 
    #Setting up grid:
    x = [0] * passes * returns
    y = [0] * passes * returns
    columns = passes*2 #Number of vertical columns
    #Filling empty arrays with data:
    for j in range (0,columns):
        for i in range(j,passes*returns,columns):
            x[i] = sidewallgap + (j * CtoC * 0.5) #Creates the x value locations. 1st term is offset from the corner, 2nd term is the following spacing
        for k in range(j,passes*returns,columns):
            y[k] = sidewallgap + ((2*CtoCy * (k-j))/columns) + ((CtoCy)* (-0.5) * (((-1)**j) -1)) #Creates the y value locations. 1st term is the offset from the corner, 2nd term is the vertical spacing, 3rd term is the additional extra offset from every 2nd column
 
    #Plotting:
    fig, ax = pl.subplots()
    pl.rcParams["figure.figsize"] = [12,12] #Adjusts size of plot
    for i in range(0,passes*returns): #Plotting outer radius of pipes
        circle = pl.Circle((x[i],y[i]),pipeOD/2,color="b",fill=False)
        ax.add_patch(circle)
    for i in range(0,passes*returns): #Plotting outer radius of tubular PCM volume
        circle = pl.Circle((x[i],y[i]),sidewallgap,color="r",fill=False)
        ax.add_patch(circle)
    pl.scatter(x,y,color='black') #Plots pipe locations
    #Graph Annotations/Formatting:
    pl.xlim(0,width) #Sets scale of axis to the dimensions of the cross-section of the container
    pl.ylim(0,height)
    ax.set_title("PCM Heat Exchanger Cross Section:",fontsize=20)
    ax.set_xlabel('Container Width (m)',fontsize=16)
    ax.set_ylabel('Container Height (m)',fontsize=16)
    custom_lines = [Line2D([0], [0], color="red", lw=4),
                Line2D([0], [0], color="blue", lw=4),
                Line2D([0], [0], color="black", lw=4)]
    ax.legend(custom_lines, ['PCM Tubular Volume Boundary', 'Copper Pipe', 'Pipe Centrepoint'],loc="upper left",borderaxespad=0.,bbox_to_anchor=(1.05, 1))
    pl.show()
    return
 
 
 
#Function for plotting a diagram of the cross-section of the PCM container
#[AAAAAAAAAAAAAAAA] Not functioning properly as a function. Unable to draw required values from the results of prev functions?? Leads to the graph not actually being updated despite changes in initial parameters..
 
def Crosssection(passes,returns):  
    #Setting up grid:
    x = [0] * passes * returns
    y = [0] * passes * returns
    columns = passes*2 #Number of vertical columns
    #Filling empty arrays with data:
    for j in range (0,columns):
        for i in range(j,passes*returns,columns):
            x[i] = sidewallgap + (j * CtoC * 0.5) #Creates the x value locations. 1st term is offset from the corner, 2nd term is the following spacing
        for k in range(j,passes*returns,columns):
            y[k] = sidewallgap + ((2*CtoCy * (k-j))/columns) + ((CtoCy)* (-0.5) * (((-1)**j) -1)) #Creates the y value locations. 1st term is the offset from the corner, 2nd term is the vertical spacing, 3rd term is the additional extra offset from every 2nd column
 
    #Plotting:
    fig, ax = pl.subplots()
    pl.rcParams["figure.figsize"] = [12,12] #Adjusts size of plot
    for i in range(0,passes*returns): #Plotting outer radius of pipes
        circle = pl.Circle((x[i],y[i]),pipeOD/2,color="b",fill=False)
        ax.add_patch(circle)
    for i in range(0,passes*returns): #Plotting outer radius of tubular PCM volume
        circle = pl.Circle((x[i],y[i]),sidewallgap,color="r",fill=False)
        ax.add_patch(circle)
    pl.scatter(x,y,color='black') #Plots pipe locations
    #Graph Annotations/Formatting:
    pl.xlim(0,width) #Sets scale of axis to the dimensions of the cross-section of the container
    pl.ylim(0,height)
    ax.set_title("PCM Heat Exchanger Cross Section:",fontsize=20)
    ax.set_xlabel('Container Width (m)',fontsize=16)
    ax.set_ylabel('Container Height (m)',fontsize=16)
    custom_lines = [Line2D([0], [0], color="red", lw=4),
                Line2D([0], [0], color="blue", lw=4),
                Line2D([0], [0], color="black", lw=4)]
    ax.legend(custom_lines, ['PCM Tubular Volume Boundary', 'Copper Pipe', 'Pipe Centrepoint'],loc="upper left",borderaxespad=0.,bbox_to_anchor=(1.05, 1))
    pl.show()
    return
 
 
 
 
#Time to use them functions:
 
 
#PipeMaker(length,width,height,pipeOD,pipethick,passes,pcmvolumereq)
 
PipeMakerResults(length,width,height,pipeOD,pipethick,passes,pcmvolumereq)
 
#Crosssection(passes,returns)