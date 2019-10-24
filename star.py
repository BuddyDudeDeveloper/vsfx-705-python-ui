# Import all necessary modules.
from planet import *;
from planetary_system_generator import *;
from ring import *;
from maya.cmds import polySuperShape, setAttr, instance, rename;
from math import sin, cos, hypot;

# Manages the data for and creates the shape for the stars in the scene.
class Star(object):
	
	# Constructor
	#
	# self: A pointer to itself in memory.
	# index: The location of the current star in the group of stars.
	# planet_radius: The radius of the planet.
	def __init__(self, index, planet_radius):
		
		# Stores the location for use when calculating the position.
		self.__index = index;
		
		# Names each star.
		name = "Star";
				
		# This stores the shape and transform nodes of the star.
		nodes = [];
		
		# If this is the first star created, create a polySuperShape.
		if(index == 0):
			
			# Each star will always be 100 times smaller than the planet.
			radius = planet_radius / 100.0;
			
			# Creates the polySuperShape and stores the transform and shape nodes.
			nodes = polySuperShape(radius = radius);
			
			# Since the polySuperShape has no name property, it is manually renamed.
			rename("pSuperShape1", name);
			
			# Sets the ellipse 0 attribute to give the star a star-esque shape.
			setAttr("%s.ellipse0" % ("polySuperShape1"), 3);
			
			# Stores the transform node as a class member.	
			self.__transform_node = name;
			
		# Otherwise, instance the original star.
		else:
			
			# Based on the index, the object's transform node is labeled and stored.
			transform_node = name + (str(index) if(index > 0) else "");
			nodes = instance(name, name = transform_node);
			self.__transform_node = transform_node;
		
	
	# Calculates the x, y and z location of the star based on the field's location in the group of fields.
	#
	# self: A pointer to itself in memory.
	# current_field_index: The current location of the field this star is in.
	# outer_ring_radius: The radius of the largest ring.
	# moon_radius: The radius of the moon.
	#
	# Returns the x, y and z locations as a tuple.
	def calculate_position(self, current_field_index, outer_ring_radius, moon_radius):

		# Fetches a copy of the stars location
		index = self.__index;
		
		# To determine how far away the star should be from the planet, the field index is multiplied against a value added to the outer ring's radius.
		multiplier = outer_ring_radius + moon_radius + (.5 * current_field_index);

		# To create more visual variation, the vertical location of each moon is factored based on its index.
		y_distance_factor_divisor = float(index + 2);

		# This is a flag for whether the star or moon is stored at an even index. Used for visual variation.
		is_even = (index % 2 == 0);

		# If the star is stored at an even index, it will go below the center of the planet on the y-axis. Otherwise, it will go above.
		y_distance_factor = (1/y_distance_factor_divisor) * (1 if is_even else -1) * 10;

		# Using trigonometric functions, the x and z locations are calcuated.
		x = sin(index) * multiplier;
		z = cos(index) * multiplier;

		# To give each object a unique vertical position, the hypotenuse is used.
		y = hypot(x, z) * y_distance_factor;

		# Return those calculated values as a tuple.
		return (x, y, z);
		
	# Returns the transform node of the star.
	#
	# self: A pointer to itself in memory.
	def get_transform_node(self):
		return self.__transform_node;
