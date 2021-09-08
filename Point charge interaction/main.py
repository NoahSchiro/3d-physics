from electric_field import *
from physics_engine import *
import math

# Constant variables
scene.width  = 1600
scene.height = 800

# Create field
my_field = electric_field()

# Make four charges at different positions
sys_charges = []
sys_charges.append(point_charge(10E-15, -10E-8, 1, 1, 1))
sys_charges.append(point_charge(10E-15,  10E-8, 0, 0, 0))
sys_charges.append(point_charge(10E-15, -10E-8, 1, 1, 0))
sys_charges.append(point_charge(10E-15, -10E-8, 0, 1, 1))

while True:

    # Set frame rate
    rate(20)

    # Calculates the influence of the charge on space
    my_field.calculate_field(sys_charges)

    # Loop through every charge in the system
    for i in range(len(sys_charges)):

        # Collect all forces on charge
        total_forces = []

        # Drag is added to forces
        total_forces.append(sys_charges[i].point_charge_drag())

        # Loop through all the other charges
        for j in range(len(sys_charges)):
            if sys_charges[i] != sys_charges[j]:

                # Add the electric forces to our list
                total_forces.append(pe.electric_force(sys_charges[j], sys_charges[i]))
        
        # Add up all those forces
        total_force = pe.vector_addition(total_forces)

        # Apply force
        sys_charges[i].apply_force(total_force)

        # Moves the charge
        sys_charges[i].update_position()