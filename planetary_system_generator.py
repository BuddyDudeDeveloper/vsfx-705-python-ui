# Import all necessary modules.
from planet import *;
from ring import *;
from moon import *;
from star import *;
from maya.cmds import select, move, rotate, scale, group;
try:
	from PyQt4.QtCore import *;
	from PyQt4.QtGui import *;
	from PyQt4 import uic;
except ImportError:
	from PySide2.QtGui import *;
	from PySide2.QtWidgets import *;
	from PySide2.QtCore import *;
	from PySide2.QtUiTools import *;

# The manager for the entire planetary system generation plugin.
class PlanetarySystemGenerator(object):

	# Creates the planetary system.
	#
	# self: A pointer to itself in memory.
	# ui: A reference to the QT UI.
	def __init__(self, ui):
		
		# Stores the UI reference.
		self.__ui = ui;
		
		# Creates the planet.
		self.__create_planet();
		
		# Creates the rings that surround the planet.
		self.__create_rings();
		
		# Creates the moons that surround the planet.
		self.__create_moons();
		
		# Creates the starfield that surrounds the entire system.
		self.__create_starfield();
	
	# Creates the planet at the center of the system.
	#
	# self: A pointer to itself in memory.
	def __create_planet(self):
		
		# Creates a single instance of the planet.
		self.__planet = Planet(generator = self);
	
	# Creates the moons that surround the planet.
	#
	# self: A pointer to itself in memory.
	def __create_moons(self):
		
		# This is used to group all the moons in Maya's outliner.
		moons = [];
		
		# Fetches the number of moons from the UI.
		number_of_moons = self.get_spinbox_value("moon_number");
		
		# Fetches the outer radius of the planet.
		planet_radius = self.__planet.get_radius();
		
		# For each moon that needs to be created, create a moon.
		# 
		# currentMoonIndex: The location in the collection of moons where the newly created moon will be stored.
		for current_moons_index in range(0, number_of_moons):

			# This creates the moon.
			moon = Moon(index = current_moons_index, generator = self);
			
			# If this was the first moon created, store its radius.
			if(current_moons_index == 0): self.__moon_radius = moon.get_radius();

			# The location of the moon in the scene is depends on its index.
			position = moon.calculate_position(self.__outer_ring_radius);

			# Using the position, the moon is given a unique rotation.
			rotation = moon.calculate_rotation(position);

			# To make sure the correct moon is selected, the selection list is cleared then the moon is selected.
			self.__clear_then_select(moon.get_transform_node());

			# Apply all calculated transform data.
			rotate(rotation[0], rotation[1], rotation[2]);
			move(position[0], position[1], position[2]);

			# Store the moon in a group of moons to help organize the outliner.
			moons.append(moon.get_transform_node());

		# After all the moons are created, they are grouped together.
		group(moons, name = "Moons");

	# Creates the rings that surround the planet.
	#
	# self: A pointer to the class in memory.
	def __create_rings(self):
		
		# This groups the rings in Maya's outliner.
		rings = [];
		
		# Fetches the number of rings from the UI.
		number_of_rings = self.get_spinbox_value("ring_number");
		
		# Fetches the planet's radius.
		planet_radius = self.__planet.get_radius();
		
		# For each ring the user wants to create, create one.
		#
		# current_rings_index: The current location of the ring in the rings group.
		for current_rings_index in range(0, number_of_rings):
			
			# This creates the stores the ring.
			ring = Ring(index = current_rings_index, planet_radius = planet_radius, number_of_rings = number_of_rings);
			
			# If this is the first ring created, store the radius for use later.
			if(current_rings_index == 0):
				self.__outer_ring_radius = ring.get_radius();
			
			# Calculates the rotation of the x, y and z axes.
			rotation_values = ring.calculate_rotation();
			
			# Calculates the scale. All axes are scaled the same to preserve the shape.
			scalar = ring.calculate_scale();
			
			# To ensure the the moon is transform, the selection list is cleared then the ring is reselected.
			self.__clear_then_select(ring.get_transform_node());
			
			# Transforms the shape based on the calculated data.
			scale(scalar, scalar, scalar);
			rotate(rotation_values[0], rotation_values[1], rotation_values[2]);

			# To help organize the outliner, the ring is stored for grouping.
			rings.append(ring.get_transform_node());

		# This groups all the rings together to help organize the outliner.
		group(rings, name = "Rings");
	
	# Creates the field of stars that surround the planet.
	#
	# self: A pointer to itself in memory.
	def __create_starfield(self):

		# This stores all the transform nodes of each star made.
		stars = [];

		# This is the total number of stars created per field.
		number_of_stars = self.get_spinbox_value("stars_number");

		# This is the total number of bands.
		number_of_bands = self.get_spinbox_value("stars_fields");
		
		# The current location of the star in the collection of stars.
		index = 0;
		
		# Fetches a pointer to the planet.
		planet_radius = self.__planet.get_radius();
		
		# Fetches a copy of the size of the outermost ring.
		outer_ring_radius = self.__outer_ring_radius;
		
		# Fetches a copy of the size of the moons.
		moon_radius = self.__moon_radius;

		# For each field, create stars.
		#
		# current_field_count: The current number of fields being generated. 
		for current_field_count in range(1, number_of_bands + 1):

			# For the number of starts to be created, create a star.
			#
			# current_star_count: The current number of stars created.
			for current_star_count in range(0, number_of_stars):

				# Create and store the current star. If this is not the first star, instance the first one made.
				star = Star(index, planet_radius);

				# Based on how far away the star is from the planet, calculate its position. 
				position = star.calculate_position(float(current_field_count), outer_ring_radius, moon_radius);

				# To make sure we are transforming the star that was last created, the selection list is cleared and the star is selected.
				self.__clear_then_select(star.get_transform_node());

				# Moves the star to its desired location.
				move(position[0], position[1], position[2]);

				# Stores the star in the group of stars
				stars.append(star.get_transform_node());
				
				# Increment the index.
				index += 1;

		# To help organize the outliner, all stars are grouped together and labeled.
		group(stars, name = "Stars");
		
	# Fetches the value from a spinbox in the UI.
	#
	# self: A pointer to itself in memory.
	# name: The name of the UI element.
	def get_spinbox_value(self, name):
		return getattr(self.__ui, name).value();
		
	# Clears the selection list then reselects an object.
	#
	# self: A pointer to itself in memory.
	# transform_node: The transform node of the object to be selected.
	def __clear_then_select(self, transform_node):
		select(clear = True);
		select(transform_node);
		
	# Fetches whether or not the user checked a checkbox.
	#
	# self: A pointer to itself in memory.
	# name: The name of the UI element.
	def get_checkbox_is_checked(self, name):
		return getattr(self.__ui, name).isChecked();
