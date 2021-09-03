from classes import *
import math

# Constant variables
scene.width  = 1600
scene.height = 800

# Create field
my_field = electric_field()
my_charge = point_charge(0.001, -1E-9, 10, 10, 10)