from electric_field import *
from physics_engine import *
import math

# Constant variables
scene.width  = 1600
scene.height = 800

# Create field
my_field = electric_field()

# Make a couples charges in a line
sys_charges = []
for i in range(-10,10):
    sys_charges.append(point_charge(0.001, 5*10E-11, i, 0, 0))

# Calculate the field strength
my_field.calculate_field(sys_charges)