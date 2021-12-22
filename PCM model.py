# IMPORTING LIBRARIES
import numpy as np


# DEFINING CONSTANTS

# operating conditions
Tmi=20                  # initial temperature       (C)

pipe = {
    "t":0.0008,                         # wall thickness            (m)
    "Di":0.0044,                        # internal diameter         (m)
    "L":3.43,                           # length (per pipe)         (m)
    "n":8,                              # number of pipes           (unitless)
    "km":401,                           # thermal conductivity      (W/m*K)     Incropera pg899 for pure copper at 300K
    "pm":8933,	                        # density                   (kg/m^3)    Incropera pg899 for pure copper at 300K
}

"Do":pipe["Di"]+(2*pipe["t"]),      # external diameter         (m)
"A":np.pi*(pipe["Di"]**2)*0.25,     # cross sectional area      (m^3)
"Lc":pipe["Di"]/2,                  # characteristic length     (m)         characteristic length is the pipe internal radius
"Asi":np.pi*pipe["Di"]*pipe["L"],   # inner surface area        (m^3)
"Aso":np.pi*pipe["Do"]*pipe["L"]    # outer surface area        (m^3)






# coolant (50/50 water/glycol mix) properties
