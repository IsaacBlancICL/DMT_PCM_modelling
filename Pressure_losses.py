import numpy as np

def Pressure_loss(Q, Di, nu, e, CtoC, g, L, n):
    """
    Head losses calculated empirically - for straight pipes, using friction factor, and for pipe bends, using K value
    For straight pipes, h = fV^2L/2gDi, and for bends, h = KV^2/2g per bend

    Parameters
    ----------
    Q       : Vol. flowrate
    Di      : pipe diameter
    nu      : fluid kin. viscosity
    e       : roughness
    CtoC    : Centre-Centre distance
    g       : acceleration due to gravity
    L       : total pipe length
    n       : number of turns

    Returns
    -------
    head losses in meters
    """

    Re = (4*Q)/(np.pi*Di*nu)      #Reynolds numbers

    V = (4*Q)/(np.pi*Di**2)        #Fluid velocity

    inverserootf = -1.8*np.log10((e/(Di*3.7))**1.11 + (69/Re))      #1/(friction factor)**0.5

    f = (1/inverserootf)**2         #Friction factor

    K = ((CtoC/Di)**(-0.5))*(0.003625 + 0.038*((Re*((Di/CtoC)**2))**(-0.25)))   #K value for single

    h = f*(V**2/(2*g))*(L/Di) + (2*n-1)*K*(V**2/(2*g)) #head loss in m
    
    hb = h*1000*g/1e5 #pressure loss in bar

    return(hb)

