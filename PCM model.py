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
        self.n = number                     # number of pipes           (unitless)
        # calculate other variables
        self.Do = self.Di+(2*self.t)        # external diameter         (m)
        self.Ac = np.pi*(self.Di**2)*0.25   # cross sectional area      (m^3)
        self.Lc = self.Di/2                 # characteristic length     (m)
        self.Asi = np.pi*self.Di*self.L     # inner surface area        (m^3)
        self.Aso = np.pi*self.Do*self.L     # outer surface area        (m^3)
        
class fluidClass:
    """contains all the variables related to the heat transfer fluid"""
    def __init__(self, thermal_cond, density, flowrate, dynamic_visc, specific_heat):
        # entered variables
        self.k = thermal_cond               # thermal conductivity      (W/m*K)
        self.p = density                    # density                   (kg/m^3)
        self.Q = flowrate                   # coolant flowrate          (m^3/s)
        self.mu = dynamic_visc              # dynamic viscosity         (Pa*s)
        self.c = specific_heat              # specific heat @ const P   (J/kg*K)
        # calculate other variables
        



class PCMClass:
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



# DECLARING INSTANCES OF CLASSES

# thermal conductivity and density are both from Incropera pg899 for pure copper at 300K
pipes = pipesClass(thermal_cond=401,
                   density=8933,
                   wall_thickness=0.0008,
                   internal_diam=0.0044,
                   length=3.43,
                   number=8)

# values just taken from Alex's spreadsheet. Shall find sources for values once model is working
fluid = fluidClass(thermal_cond=0.25,
                   density=1079,
                   flowrate=0.00016,
                   dynamic_visc=0.0028,
                   specific_heat=3473)

# values just taken from Alex's spreadsheet. Shall find sources for values once model is working
PCM = PCMClass(thermal_cond=0.22,
               density=900,
               specific_latent=900,
               volumetric_heat=176,
               specific_heat=2.2,
               centre_to_centre=0.018,
               pipe_external_diam=pipes.Do)