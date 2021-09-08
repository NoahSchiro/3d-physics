from vpython import *
import math

class point_charge:

    def __init__(self, mass, charge, pos_x=0, pos_y=0, pos_z=0):

        # The following statements are for vpython
        self.obj = sphere()         # The object is a sphere
        self.obj.radius = 0.2       # with this radius
        
        # If negative, make it blue, if positive, make it red
        if charge < 0:
            self.obj.color = color.blue
        else:
            self.obj.color = color.red
        
        # vpython AND the class must have a concept of the position
        self.obj.pos = vector(pos_x, pos_y, pos_z)
        self.pos = [pos_x, pos_y, pos_z]

        # The following statements are for physics stuff
        self.mass   = mass                              # Must be intialized
        self.charge = charge                            # Must be intialized

        self.velocity     = [0,0,0]                     # Always is 0 on intialization
        self.acceleration = [0,0,0]                     # Always is 0 on intialization

    def update_position(self):

        # Get current position
        curr_x = self.pos[0]
        curr_y = self.pos[1]
        curr_z = self.pos[2]

        # Add current velocity to this for both vypthon and the class
        self.obj.pos = vector(curr_x+self.velocity[0],
                              curr_y+self.velocity[1],
                              curr_z+self.velocity[2])
        
        self.pos = [curr_x+self.velocity[0],
                    curr_y+self.velocity[1],
                    curr_z+self.velocity[2]]

    # Calculates a drag force for point charges
    def point_charge_drag(self):
        
        # Technically, the drag coeffcienct for a sphere varies 
        # wildly due to some weird fluid dynamic stuff but 
        # this is just a simplification
        drag_coeffcient = 0.5
        # Air density (I may change this to make the simulation prettier)
        fluid_density = 1.225
        cross_sec_area = self.obj.radius
        
        velocity_mag = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2 + self.velocity[2]**2)

        # Avoidance of divide by 0 problems
        if velocity_mag == 0:
            velocity_dir = [0,0,0]
        else:
            velocity_dir = [self.velocity[0]/velocity_mag, self.velocity[1]/velocity_mag, self.velocity[2]/velocity_mag]

        # Use drag equation to calculate force magnitude
        force_mag = (fluid_density * velocity_mag**2 * drag_coeffcient * cross_sec_area) / 2
        # Direction will be opposite of velocity
        force_dir = [-velocity_dir[0], -velocity_dir[1], -velocity_dir[2]]
        
        return [force_mag * force_dir[0], force_mag * force_dir[1], force_mag * force_dir[2]] 

    # Force must be applied as a 3 element list!
    def apply_force(self, force):

        # F/m = a
        
        # This turns the force vector into an acceleration vector
        for dimension in force:
            dimension /= self.mass

        # This will add (or subtract) to the current velocity
        for i in range(len(force)):
            self.velocity[i] += force[i]

class engine():

    # Adds an arbitrary amount of vectors with 3 dimensions
    def vector_addition(list_of_vectors):

        # Answer that will be returned
        ans = [0,0,0]

        # Loop through all vectors and add up their components
        for vector in list_of_vectors:
            ans[0] += vector[0]
            ans[1] += vector[1]
            ans[2] += vector[2]
        
        # Return the answer
        return ans

    # Returns the electric force that point_charge1 excerts on point_charge2
    def electric_force(point_charge1, point_charge2):
        # Colomb constant
        k = 9 * (10**9)

        # Get the distance between the two points
        d_x = point_charge1.pos[0] - point_charge2.pos[0]
        d_y = point_charge1.pos[1] - point_charge2.pos[1]
        d_z = point_charge1.pos[2] - point_charge2.pos[2]
        distance = math.sqrt(d_x**2 + d_y**2 + d_z**2)

        magnitude = (k * point_charge1.charge * point_charge2.charge) / distance**2
        # Direction is as a unit vector. Additionally, the value we are 
        # returning is the force that point_charge1 exerts on point_charge2
        direction = [-d_x/distance, -d_y/distance, -d_z/distance]

        # Direction times magnitude is our resultant vector
        return [direction[0] * magnitude, direction[1] * magnitude, direction[2] * magnitude]
    
    # Returns the electric field at a given point for a given charge
    def electric_force_for_field(point_charge1, point_in_space):

        # Colomb constant
        k = 9 * (10**9)

        # Get the distance between the two points
        d_x = point_charge1.pos[0] - point_in_space[0]
        d_y = point_charge1.pos[1] - point_in_space[1]
        d_z = point_charge1.pos[2] - point_in_space[2]
        distance = math.sqrt(d_x**2 + d_y**2 + d_z**2)

        # If statement avoid divide by 0 issues
        if distance == 0:
            magnitude = 0
            direction = [0,0,0]
        else:
            magnitude = (k * point_charge1.charge) / distance**2
            # Direction is as a unit vector. Additionally, the value we are 
            # returning is the force that point_charge1 exerts on point_charge2
            direction = [d_x/distance, d_y/distance, d_z/distance]

        # Direction times magnitude is our resultant vector
        return [direction[0] * magnitude, direction[1] * magnitude, direction[2] * magnitude]