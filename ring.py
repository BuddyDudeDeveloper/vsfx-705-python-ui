# Imports all necessary modules.
from maya.cmds import polyTorus, polySmooth, instance;
from planetary_system_generator import *;
from planet import *;

# This class handles the data management and creation of the rings that surround the planet.
class Ring(object):
	
	# Constructor
	#
	# self: A pointer to itself in memory.
	# index: The location of the ring in the groups of rings.
	def __init__(self, index, planet_radius, number_of_rings):
		
		# The index is used when determining the scale and rotation of the ring.
		self.__index = index;
		
		# To shrink each successive ring, a decrement value is calculated.
		self.__scale_decrement_value = .5 / number_of_rings; 
		
		# Names the ring.
		name = "Ring";
		
		# If this is the first ring created, create a polyTorus.
		if(index == 0):
			
			# Since this is the first ring, the outer radius is stored and used when calculating how far away the moons and starfields should be.
			radius = self.__radius = float(planet_radius + number_of_rings);
			
			# The torus that makes the ring is created then smoothed.
			instance_nodes = polyTorus(name = name, radius = radius, sectionRadius = (radius/100));
			polySmooth(divisions = 2);
			
			# Since this is the first ring, its transform node is also stored as a class member.
			self.__transform_node = instance_nodes[0];
			
		# Otherwise, instance the initial ring.
		else:
			
			# Creates an instance of the initial ring and stores the nodes.
			nodes = instance(name);
			
			# The transform node of the ring is stored as an instance member.
			self.__transform_node = nodes[0];
			
	# Based on the index, calculate the rotation of the ring.
	#
	# self: A pointer to itself in memory.
	def calculate_rotation(self):
		
		# Fetches a copy of the index from the instance.
		index = self.__index;
		
		# Every ring is given one of three variations with additional variation if the index is a multiple of 2 and 3.
		variation = index % 3;

		# The default axis rotation is 45 degrees with the half-angle being -22.5 degrees.
		angle = 45.0;
		half_angle = (angle/2);

		# Based on the variation, return the rotation on each axis as a tuple.
		if (variation == 0):
			if(index % 2 == 0 and index != 0): half_angle *= -1; # If the index is a multiple of 6 (2 and 3) and not the first ring, flip the angle.
			return (half_angle, 0, half_angle);
		if (variation == 1):
			return (0, 0, angle);
		if (variation == 2):
			return (angle, 0, 0);
			
	# Using the index and decrement value, the scale is calculated
	#
	# self: A pointer to itself in memory.
	def calculate_scale(self):
		return (1 - (self.__scale_decrement_value * self.__index));
		
	# Returns the transform node of the ring.
	#
	# self: A pointer to itself in memory.
	def get_transform_node(self):
		return self.__transform_node;
		
	# Returns the radius of the ring.
	#
	# self: A pointer to itself in memory.
	def get_radius(self):
		return self.__radius;
		
