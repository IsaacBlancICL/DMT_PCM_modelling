import numpy as np

#Head losses calculated empirically - for straight pipes, using friction factor, and for pipe bends, using K value
#For straight pipes, h = fV^2L/2gDi, and for bends, h = KV^2/2g per bend

def Pressure_loss(Q, Di, nu, e, CtoC, g, L, n):

#Vol. flowrate, pipe diameter, fluid kin. viscosity, roughness, Centre-Centre distance, g, total pipe length, number of turns

    Re = (4*Q)/(np.pi*Di*nu)      #Reynolds numbers

    v = (4Q)/(np.pi*Di**2)        #Fluid velocity

    inverserootf = -1.8*np.log10((e/(Di*3.7))**1.11 + (69/Re))      #1/(friction factor)**0.5

    f = (1/inverserootf)**2         #Friction factor

    K = ((CtoC/Di)**(-0.5))*(0.003625 + 0.038*((Re*((Di/CtoC)**2))**(-0.25)))   #K value for single

    h = f*(V**2/(2*g))*(L/Di) + (2*n-1)*K*(V**2/(2*g))

    return(h)



