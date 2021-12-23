# IMPORTING LIBRARIES
import numpy as np


# CLASSES FOR CONSTANTS
class pipesClass:
    """contains all the variables related to pipes"""
    def __init__(self, thermal_cond, density, wall_thickness, internal_diam, length, number):
        # entered variables
        self.k = thermal_cond               # thermal conductivity      (W/m*K)
        self.p = density                    # density                   (kg/m^3)
        self.t = wall_thickness             # wall thickness            (m)
        self.Di = internal_diam             # internal diameter         (m)
        self.L = length                     # length (per pipe)         (m)
        self.n = number                     # number of pipes           (dimensionless)
        # calculate other variables
        self.Do = self.Di+(2*self.t)        # external diameter         (m)
        self.Ac = np.pi*(self.Di**2)*0.25   # cross sectional area      (m^3)
        self.Lc = self.Di/2                 # characteristic length     (m)
        self.Asi = np.pi*self.Di*self.L     # inner surface area        (m^3)
        self.Aso = np.pi*self.Do*self.L     # outer surface area        (m^3)
        
        
class fluidClass:
    """contains all the variables related to the heat transfer fluid"""
    def __init__(self, thermal_cond, density, dynamic_visc, specific_heat):
        # entered variables
        self.k = thermal_cond               # thermal conductivity      (W/m*K)
        self.p = density                    # density                   (kg/m^3)
        self.mu = dynamic_visc              # dynamic viscosity         (Pa*s)
        self.c = specific_heat              # specific heat @ const P   (J/kg*K)
        # calculate other variables
        self.alpha = self.k/(self.p*self.c) # thermal diffusivity       (m^2/s)
        self.Pr = self.mu/(self.p*self.alpha)   # Prandt number         (dimensionless)


class pcmClass:
    """contains all the variables related to the PCM"""
    def __init__(self, thermal_cond, density, specific_latent, volumetric_heat, specific_heat, centre_to_centre, pipe_external_diam):
        # entered variables
        self.k = thermal_cond               # thermal conductivity      (W/m*K)
        self.p = density                    # density                   (kg/m^3)
        self.lh = specific_latent           # specific latent heat      (J/kg)
        self.cvol = volumetric_heat         # volumetric heat @ const P (J/m^3*K)
        self.c = specific_heat              # specific heat @ const P   (J/kg*K)
        self.CtoC = centre_to_centre        # centre-to-centre distance (m)
        # calculate other variables
        self.t = (self.CtoC - pipe_external_diam)/2     # thickness     (m)
        
        
class systemClass:
    """contains all the variables that descibe the system.
    These are almost all functions of the variables in the other classes"""
    def __init__(self, inlet_temp, total_flowrate, pipes, fluid):
        # entered variables
        self.Ti = inlet_temp                # fluid temp @ PCM inlet    (C)
        self.Qtot = total_flowrate          # total vol flowrate        (m^3/s)
        # calculate other variables
        self.Q = self.Qtot/pipes.n          # vol flowrate per pipe     (m^3/s)
        self.m = self.Q*fluid.p             # mass flowrate per pipe    (kg/s)
        self.u = self.Q/pipes.Ac            # flow velocity             (m/s)
        self.Re = pipes.Di*self.u*fluid.p/fluid.mu  # Reynolds number   (dimensionless)
        self.Nu = 0.023 * (self.Re**(4/5)) * (fluid.Pr**0.4) # Nusselt number from Incropera correlation eqn8.60d on pg519
        self.h = self.Nu*fluid.k/pipes.Lc   # convective HT coef        (W/m^2*K)