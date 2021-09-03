from vpython import *   # 3d engine
import math

#Accepts a point charge, and a point in space (a vector)
def force_for_electric_field(point_charge, vector):

    # Assume point charge to be 0.1 coloumb
    charge = 10**-9

    # Colomb constant
    k = 9 * (10**9)

    # Get the distance between the two points
    d_x = vector.pos.x - point_charge.pos.x
    d_y = vector.pos.y - point_charge.pos.z
    d_z = vector.pos.z - point_charge.pos.z
    distance = math.sqrt(d_x**2 + d_y**2 + d_z**2)

    return (k * charge) / (distance**2)


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
    

    # This function makes all of the arrows 
    # point to the location of an object instead of the origin
    def point_to_charge(self, obj):
        
        # Access all arrows in matrix
        for x in range(-5,5):
            for y in range(-5, 5):
                for z in range(-5,5):
                    
                    # Get the difference in x, y, and z components
                    x_diff = self.arr[x][y][z].pos.x - obj.pos.x
                    y_diff = self.arr[x][y][z].pos.y - obj.pos.y
                    z_diff = self.arr[x][y][z].pos.z - obj.pos.z

                    # Set axis to that difference
                    self.arr[x][y][z].axis = vector(x_diff, y_diff, z_diff)
                    
    
    def change_magnitude(self, point_charge):

        # Access all arrows in matrix
        for x in range(-5,5):
            for y in range(-5,5):
                for z in range(-5,5):
                    
                    # Calculate the magnitude of the force between the 
                    # point charge and every point in the system
                    magnitude = force_for_electric_field(point_charge, self.arr[x][y][z])
                    
                    # Set the length of the vector to the calculated magnitude 
                    # (unless it's greater than 1, in which case let's rate 
                    # limit it so it doesnt go crazy). We also are flipping 
                    # the direction of the arrows because vpython handles vectors weirdly
                    if magnitude > 1:
                        self.arr[x][y][z].length = -1
                    else:
                        self.arr[x][y][z].length = -magnitude

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

        self.velocity     = [0,0,0]                     # Always is 0
        self.acceleration = [0,0,0]                     # Always is 0

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


    # Force must be applied as a 3 element list!
    def apply_force(self, force):

        # F/m = a
        
        # This turns the force vector into an acceleration vector
        for dimension in force:
            dimension /= self.mass

        # This will add (or subtract) to the current velocity
        for i in range(len(force)):
            self.velocity[i] += force[i]
        