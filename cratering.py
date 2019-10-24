# This is a container for the data used to create the bevels on the planet and moons.
class Cratering(object):
	
	# Constructor
	#
	# Sets the properties of the cratering instance.
	#
	# self: A pointer to itself in memory.
	# depth: How deep the beveling is.
	# segments: The solidity of the edges of the beveling.
	# fraction: The intensity of the beveling.
	def __init__(self, depth, segments, fraction):
		self.__depth = depth;
		self.__segments = segments;
		self.__fraction = fraction;
	
	# Returns how deep the bevel is.
	#
	# self: A pointer to itself in memory.
	def get_depth(self):
		return self.__depth;
	
	# Returns the solidity of the edges of the beveling.
	#
	# self: A pointer to itself in memory.
	def get_segments(self):
		return self.__segments;
		
	# Returns the intensity of the beveling.
	#
	# self: A pointer to itself in memory.
	def get_fraction(self):
		return self.__fraction;

