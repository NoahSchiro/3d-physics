from electric_field import *
from physics_engine import *
import math

# Constant variables
scene.width  = 1600
scene.height = 800

# Create field
my_field = electric_field()

system
my_charge = point_charge(0.001, -1E-9, 10, 10, 10)

while True:

    # Set frame rate
    rate(20)

    # This allows the charge to bounce around
    if my_charge.pos[0] >= 10:
        my_charge.apply_force([-0.1, -0.1, -0.1])
    if my_charge.pos[0] <= -10:
        my_charge.apply_force([0.1, 0.1, 0.1])

    # Calculates the influence of the charge on space
    my_field.calculate_field([my_charge])

    # Allow drag to take effect on point charge
    my_charge.apply_force(my_charge.point_charge_drag())

    # Moves the charge
    my_charge.update_position()