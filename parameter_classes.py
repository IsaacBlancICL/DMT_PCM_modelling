"""
All the parameters are stored inside instances of custom classes. The classes are defined in 'parameter_classes.py'.
This is largely just a neatness thing. For instance, it makes it clear that 'pipes.p' is the density of the pipe
material while 'fluid.p' is the density of the heat transfer fluid. Calculation of all the other variables also happens
within the classes. For instance, when you declare an instance of 'pipesClass' named 'pipes', you enter
variables like thermal inner diameter and thickness, but then variables such as outer diameter and cross sectional
area are automatically calculated and stored in that same instance of the class. Variables are grouped roughly by
what they are a property of, so for instance all the system properties are in 'system', which is an instance of the
class named 'systemClass'.

The __init__ function for each class is written so that you only need to specify the important variables when
creating an instance of each class; the rest all go to default values. For instance 'pipesClass(internal_diam=0.006)'
returns an instance of the 'pipes' with internal diameter set to 6mm and all other variables set to default.
Similarly, 'pipesClass(density=7000)' returns an instance with all variables set to default apart from density.
You can set as many of as few variables to non-default values as you like. Eg: 'pipesClass(internal_diam=0.006, density=7000)'

I've used this as an excuse to try using classes for the first time so hopefully its actually useful lol.
"""


# IMPORTING LIBRARIES
import numpy as np


# CLASSES FOR CONSTANTS
class caseClass:
    """
    contains all the variables related to the case that contains the PCM and pipes.
    This class doesn't have an __init__ function because these dimensions are totally fixed. We're never
    gonna trial different options for the case dimensions.
    
    Values are from Alex's CAD.
    """
    length=0.35
    width=0.16
    height=0.16


class pipesClass:
    """
    contains all the variables related to pipes.
    Default values for thermal_cond and density are from Incropera pg899 for pure copper at 300K
    """
    def __init__(self, thermal_cond=401, density=8933, wall_thickness=0.0008, internal_diam=0.0044, length=3.43, number=8):
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
    """
    contains all the variables related to the heat transfer fluid.
    Default values are from Alex's spreadsheet for 50/50 glycol/water mix - I don't know the sources
    """
    def __init__(self, thermal_cond=0.25, density=1079, dynamic_visc=0.0028, specific_heat=3473):
        # entered variables
        self.k = thermal_cond               # thermal conductivity      (W/m*K)
        self.p = density                    # density                   (kg/m^3)
        self.mu = dynamic_visc              # dynamic viscosity         (Pa*s)
        self.c = specific_heat              # specific heat @ const P   (J/kg*K)
        # calculate other variables
        self.alpha = self.k/(self.p*self.c) # thermal diffusivity       (m^2/s)
        self.Pr = self.mu/(self.p*self.alpha)   # Prandt number         (dimensionless)


class pcmClass:
    """
    contains all the variables related to the PCM.
    Default values are from Alex's spreadsheet - not sure what PCM he took the properties of
    """
    def __init__(self, pipe_external_diam, thermal_cond=0.22, density=900, specific_latent=900, volumetric_heat=176, specific_heat=2.2, centre_to_centre=0.018, temp_fusion=118, energy_capacity=1250000):
        # entered variables
        self.k = thermal_cond               # thermal conductivity      (W/m*K)
        self.p = density                    # density                   (kg/m^3)
        self.lh = specific_latent           # specific latent heat      (J/kg)
        self.cvol = volumetric_heat         # volumetric heat @ const P (J/m^3*K)
        self.c = specific_heat              # specific heat @ const P   (J/kg*K)
        self.CtoC = centre_to_centre        # centre-to-centre distance (m)
        self.T = temp_fusion                # temperature of fusion     (C)
        self.E = energy_capacity            # energy storage capacity   (J)
        # calculate other variables
        self.t = (self.CtoC - pipe_external_diam)/2     # thickness     (m)
        self.volReq = self.E/(self.lh*self.p)       # required volume   (m^3)
        
        
class systemClass:
    """
    contains all the variables that descibe the system.
    Most of these are calculated from variables in the other classes.
    Default for total_flowrate is from that Facebook post - shall find link later
    """
    def __init__(self, pipes, fluid, inlet_temp = 20, total_flowrate=0.00016):
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