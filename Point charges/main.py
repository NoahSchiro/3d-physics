from vpython import * #3D Engine
import math

# Constant variables
scene.width  = 1600
scene.height = 800
RED = color.hsv_to_rgb(vector(0,1,1))

#Accepts a point charge, and a point in space (a vector)
def F_e(point_charge, vector):

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
                    
                    # Get the difference in x,y, and z components
                    x_diff = self.arr[x][y][z].pos.x - obj.pos.x
                    y_diff = self.arr[x][y][z].pos.y - obj.pos.y
                    z_diff = self.arr[x][y][z].pos.z - obj.pos.z

                    # Set axis to that difference
                    self.arr[x][y][z].axis = vector(x_diff, y_diff, z_diff)
                    # Flip direction and make it small (50 cm)
                    self.arr[x][y][z].length = -0.5
    
    def change_magnitude(self, point_charge):

        # Access all arrows in matrix
        for x in range(-5,5):
            for y in range(-5,5):
                for z in range(-5,5):
                    
                    # Calculate the magnitude of the force between the 
                    # point charge and every point in the system
                    magnitude = F_e(point_charge, self.arr[x][y][z])
                    
                    # Set the length of the vector to the calculated magnitude 
                    # (unless it's greater than 1, in which case let's rate 
                    # limit it so it doesnt go crazy)
                    if magnitude > 1:
                        self.arr[x][y][z].length = 1
                    else:
                        self.arr[x][y][z].length = magnitude


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
    my_field.change_magnitude(point_charge)


    # The point charge will bounce between -10, 10
    if point_charge.pos.x >= 10:
        point_charge.pos.x -= 0.1
    elif point_charge.pos.x <= -10:
        point_charge.pos.x += 0.1
    else:
        point_charge.pos.x -= 0.1