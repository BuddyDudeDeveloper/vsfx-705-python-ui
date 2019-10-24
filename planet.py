# Import all necessary modules.
from maya.cmds import polyPlatonicSolid, polyBevel3, polySmooth;
from cratering import *;
from planetary_system_generator import *;

# This is the core of the scene; it is the planet at the center of the starfield.
class Planet(object):
	
	# Constructor
	#
	# self: A pointer to itself in memory
	# generator: A pointer to the generator manager.
	def __init__(self, generator):
		
		# Creates a pointer to the generator.
		self.__generator = generator;
				
		# The radius and cratering data is fetched from the UI.
		self.__get_values();
		
		# Maya generates the shape.
		polyPlatonicSolid(radius = self.__radius, name = "Planet");
		
		# The cratering data is fetched,
		cratering = self.__cratering;
		
		# For aesthetics, the polyPlatonicSolid is beveled (based on the user's input) and smoothed.
		polyBevel3(depth = cratering.get_depth(), segments = cratering.get_segments(), fraction = cratering.get_fraction());
		polySmooth(divisions = 2);
		
		# Cleanup objects that are no long necessary.
		self.__generator = None;
		self.__cratering = None;
	
	# Fetches the values from the UI and stores them privately.
	#
	# self: A pointer to itself in memory.
	def __get_values(self):
		
		# Fetches a pointer to the generator.
		generator = self.__generator;
		
		# The radius and cratering data are stored privately to prevent changes from outside the class.
		self.__radius = generator.get_spinbox_value("planet_radius");
		self.__cratering = Cratering(generator.get_spinbox_value("planet_cratering_depth") * (-1 if(generator.get_checkbox_is_checked("planet_cratering_negative")) else 1), generator.get_spinbox_value("planet_cratering_segments"), generator.get_spinbox_value("planet_cratering_fraction"));
		
	# Returns the size of the planet.
	#
	# self: A pointer to itself in memory.
	def get_radius(self):
		return self.__radius;

