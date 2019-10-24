# Import all necessary modules.
from planetary_system_generator import *;
from cratering import *;
from maya.cmds import polyBevel3, polySmooth, polyPlatonicSolid, instance, angleBetween, getAttr;
from math import sin, cos, hypot;

# This controls the data and shape of each moon.
class Moon(object):
	
	# Constructor
	#
	# self: A pointer to itself in memory.
	# index: The location of the moon in the group of moons.
	# generator: A reference to the planetary system generator.
	def __init__(self, index, generator):
		
		# Stores its location.
		self.__index = index;
		
		# Retrieves the values needed from the UI.
		self.__get_values(generator);
		
		# Fetches a pointer to the cratering data.
		cratering = self.__cratering;
		
		# Stores the transform and shape nodes.
		nodes = [];
		
		# If this is the first moon created, create a polyPlatonicSolid.
		if(index == 0):
			
			# Creates the shape.
			nodes = polyPlatonicSolid(radius = self.__radius, name = "Moon");
			
			# For aesthetics, the polyPlatonicSolid is beveled (based on the user's input) and smoothed.
			polyBevel3(offset = getAttr("polyBevel1.offset") * generator.get_spinbox_value("moon_ratio"), depth = cratering.get_depth(), segments = cratering.get_segments(), fraction = cratering.get_fraction());
			polySmooth(divisions = 2);
			
		# Otherwise, instance the original.
		else:
			nodes = instance("Moon");
			
		# Stores the transform node.
		self.__transform_node = nodes[0];
				
	# Fetches the values from the UI and stores them privately.
	#
	# self: A pointer to itself in memory.
	# generator: The reference to the planetary system generation manager.
	def __get_values(self, generator):
		
		# The radius and cratering data are stored privately to prevent changes from outside the class.
		self.__radius = generator.get_spinbox_value("planet_radius") * generator.get_spinbox_value("moon_ratio");
		self.__cratering = Cratering(generator.get_spinbox_value("moon_depth") * (-1 if(generator.get_checkbox_is_checked("moon_negative")) else 1), generator.get_spinbox_value("moon_segments"), generator.get_spinbox_value("moon_fraction"));
		
	# Calculates the x, y and z location of the moon.
	#
	# self: A pointer to itself in memory.
	# outer_ring_radius: The radius of the largest ring.
	#
	# Returns the x, y and z locations as a tuple.
	def calculate_position(self, outer_ring_radius):

		# Fetches a copy of the stars location
		index = self.__index;
		
		# To determine how far away the moon should be from the planet, a small value is added to the outer ring's radius.
		multiplier = outer_ring_radius + (self.__radius);

		# To create more visual variation, the vertical location of each moon is factored based on its index.
		y_distance_factor_divisor = float(index + 2);

		# This is a flag for whether the star or moon is stored at an even index. Used for visual variation.
		is_even = (index % 2 == 0);

		# If the star is stored at an even index, it will go below the center of the planet on the y-axis. Otherwise, it will go above.
		y_distance_factor = (1/y_distance_factor_divisor) * (1 if is_even else -1);

		# Using trigonometric functions, the x and z locations are calcuated.
		x = sin(index) * multiplier;
		z = cos(index) * multiplier;

		# To give each object a unique vertical position, the hypotenuse is used.
		y = hypot(x, z) * y_distance_factor;

		# Return those calculated values as a tuple.
		return (x, y, z);
		
	# Calculates the rotation of the moon.
	#
	# position: The x, y, and z location of the moon stored as a tuple.
	#
	# Returns the x, y and z rotations as tuples.
	def calculate_rotation(self, position):
		
		# This tuple is located on the opposite side of the planet.
		opposite_position = ((position[0] * -1), (position[1] * -1), (position[2] * -1));

		# Each moon is given a unique rotation based on the angle between the moon and the  on the opposite side of the planet.
		between_angle = angleBetween(euler = True, vector1=(position[0], position[1], position[2]), vector2=(opposite_position[0], opposite_position[1], opposite_position[2]));

		# Returns that unique rotation as a tuple.
		return (between_angle[0], between_angle[1], between_angle[2]);
	
	# Returns the transform node of the shape.
	#
	# self: A pointer to itself in memory.
	def get_transform_node(self):
		return self.__transform_node;
	
	# Returns the radius of the moon.
	#
	# self: A pointer to itself in memory.
	def get_radius(self):
		return self.__radius;
