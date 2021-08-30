from vpython import * #3D Engine
import math

# Constant variables
scene.width  = 1600
scene.height = 800
RED = color.hsv_to_rgb(vector(0,1,1))

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
                    arr0w            = arrow(pos=vector(x,y,z))
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
    def point_to_object(self, obj):
        
        # Access all arrows in matrix
        for x in range(-5,5):
            for y in range(-5, 5):
                for z in range(-5,5):
                    
                    x_diff = self.arr[x][y][z].pos.x - obj.pos.x
                    y_diff = self.arr[x][y][z].pos.y - obj.pos.y
                    z_diff = self.arr[x][y][z].pos.z - obj.pos.z

                    self.arr[x][y][z].axis = vector(x_diff, y_diff, z_diff)
                    self.arr[x][y][z].length = -0.5


# Create point charge
point_charge        = sphere()
point_charge.pos    = vector(10,0,0)
point_charge.radius = 0.1
point_charge.color  = RED

# Create field
my_field = electric_field()

while True:
    rate(10)

    my_field.point_to_object(point_charge)

    point_charge.pos.x -= 0.1

