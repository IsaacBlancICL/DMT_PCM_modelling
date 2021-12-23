# IMPORTING LIBRARIES
import parameter_classes


# DECLARING INSTANCES OF CLASSES
"""
All the parameters are stored inside instances of custom classes. The classes are defined in 'parameter_classes.py'.
This is largely just a neatness thing. For instance, it makes it clear that 'pipes.p' is the density of the pipe
material while 'fluid.p' is the density of the heat transfer fluid. Calculation of all the other variables also happens
within the classes. For instance, when you declare an instance of 'pipesClass' named 'pipes', you enter
variables like thermal inner diameter and thickness, but then variables such as outer diameter and cross sectional
area are automatically calculated and stored in that same instance of the class. Variables are grouped roughly by
what they are a property of, so for instance all the system properties are in 'system', which is an instance of the
class named 'systemClass'.

I've used this as an excuse to try using classes for the first time so hopefully its actually useful lol.
"""
pipes = parameter_classes.pipesClass(   thermal_cond=401,       # Incropera pg899 for pure copper at 300K
                                        density=8933,           # Incropera pg899 for pure copper at 300K
                                        wall_thickness=0.0008,
                                        internal_diam=0.0044,
                                        length=3.43,
                                        number=8   )

fluid = parameter_classes.fluidClass(   thermal_cond=0.25,
                                        density=1079,
                                        dynamic_visc=0.0028,
                                        specific_heat=3473   )

pcm = parameter_classes.pcmClass(       thermal_cond=0.22,
                                        density=900,
                                        specific_latent=900,
                                        volumetric_heat=176,
                                        specific_heat=2.2,
                                        centre_to_centre=0.018,
                                        pipe_external_diam=pipes.Do   )

system = parameter_classes.systemClass( inlet_temp = 20,
                                        total_flowrate=0.00016, # from that Facebook post - shall find link later
                                        pipes=pipes,
                                        fluid=fluid   )


# SOLVING ODEs
