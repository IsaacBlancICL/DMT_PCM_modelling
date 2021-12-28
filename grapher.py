# Libraries:
import matplotlib.pyplot as pl
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits.mplot3d import Axes3D
 
def outletTempGraph(results):
    
    # Reading Results:
     
    x = results[0] #Pipe Diamters
    y = results[1] #Number of Pipes
    z = results[2] #Outlet Temperatures
     
    # It's time to plot:
     
    # 3D Plot:
     
    print("Scatter Plot:")
    pl.rcParams["figure.figsize"] = [9,9] #This will adjust the size of the plot
    pl.rcParams["figure.autolayout"] = True
    fig = pl.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter( x , y , z , c = 'black') #Creates Scatter Graph
    p = ax.plot_trisurf(x, y, z, linewidth=0.2, antialiased=True,cmap='plasma')
     
    #3D Plot Annotations:
    ax.set_xlabel('Pipe Diameter')
    ax.set_ylabel('Number of Pipes')
    ax.set_zlabel('Outlet Temperature')
    pl.colorbar(p,fraction=0.03,pad=0.1)
    #ax.view_init(90, -90) #Used to adjust viewing angle
     
    pl.show()
     
     
    # Pipe Diameters vs Number of Pipes:
     
     
    # 2D version of the 3D plot essentially
    print("Pipe Diameters vs Number of Pipes:")
    fig, ax = pl.subplots()
    dl = 500 #How many levels in the contouring
    levels = np.linspace(min(z), max(z), dl)
    #ax.triplot(x, y,c='black') #Triangulation of scatter data
    #ax.tripcolor(x, y,z,cmap = 'plasma') #Creates triangular surface with use of z values
    p2 = ax.tricontourf(x, y, z, cmap = 'plasma',levels=levels) #Creates Contour map
    pl.scatter(x,y,c='black')
     
    #2D Plot Annotations:
    ax.set_xlabel('Pipe Diameter')
    ax.set_ylabel('Number of Pipes')
    pl.colorbar(p2,fraction=0.03,pad=0.1)
     
    pl.show()