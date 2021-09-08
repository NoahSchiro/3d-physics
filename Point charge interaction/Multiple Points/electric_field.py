from vpython import *                       # 3d engine
from physics_engine import engine as pe     # Home brewed physics
import math                                 #Sqrt and tanh function

# Represents an electric field as a matrix of vectors at set intervals
class electric_field:

    def __init__(self):
        
        # Matrix that stores all arrows
        self.arr = []

        #X axis
        for x in range(-5, 5):
            
            x_arr = []

            #Y axis
            for y in range(-5, 5):

                y_arr = []
                
                #Z axis
                for z in range(-5, 5):

                    # Creates an arrow at coord (x,y,z)
                    arr0w            = arrow(pos=vector(x*2,y*2,z*2))
                    # Determines where the arrow points, on intialization, let's make this the origin.
                    arr0w.axis = vector(x * -1, y* -1, z* -1)
                    # Determine the length of the arrow
                    arr0w.length = 0.5
                    # Determines the thickness of the arrow
                    arr0w.shaftwidth = 0.05


                    # Adds arrow to middle (y) array
                    y_arr.append(arr0w)
                
                # Adds middle array to outer array
                x_arr.append(y_arr)
            
            # Adds outer array to the matrix
            self.arr.append(x_arr)
    

    # This function aims to change the direction and magnitude of all
    # the vectors in this space given an array of charges in the system
    def calculate_field(self, arr_of_charges):

        # Access all arrows in matrix
        for x in range(-5,5):
            for y in range(-5, 5):
                for z in range(-5,5):

                    # Intialize an array which will be populated with electric fields
                    all_electric_fields = []
                    # Grab the vector position of our arrow
                    vector_pos = [self.arr[x][y][z].pos.x, 
                                  self.arr[x][y][z].pos.y,
                                  self.arr[x][y][z].pos.z]
                    
                    # Access all charges
                    for charge in arr_of_charges:

                        # Calculate the charges influence on that space and 
                        # then add it to our list of all electric fields
                        all_electric_fields.append(pe.electric_force_for_field(charge, vector_pos))
                    
                    # Add up all fields for this given vector
                    total_field = pe.vector_addition(all_electric_fields)

                    # Point the 3d arrow to the same direction as the total_field. The way "pointing" 
                    # an arrow in vpython works assumes that the origin is wherever the tail of our 
                    # arrow is. A bit different from the mathematical norm but we work with what we got
                    self.arr[x][y][z].axis = vector(total_field[0],
                                                    total_field[1],
                                                    total_field[2])

                    # Calculate the magnitude
                    magnitude = math.sqrt(total_field[0]**2 + total_field[1]**2 + total_field[2]**2)
                    # We don't want arrows that are crazy long so we are going to squash our 
                    # numbers down to a range of -1 to 1. We can do this with a hyperbolic tangent
                    squashed_mag = math.tanh(magnitude)
                    self.arr[x][y][z].length = -squashed_mag

                    # Finally, let's change the color of the arrow to reflect the intensity of it's magnitude
                    self.arr[x][y][z].color = vec(1, 1-squashed_mag, 1- squashed_mag)        