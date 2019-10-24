# Malcolm Kesson
# 27 August 2019
# 
# Useage:
# In your maya folder make a subdirectory named "Qt_Dev".
# Copy the file from Templates->Python->connection_utils.py to the "Qt_Dev" folder.
# In the Qt_Dev directory make a folder named "ui".
# Copy the file from Templates->Python->demo_sliders.ui to the "ui" folder.
# In a python tab of Maya's script editor copy and paste the following text.
# Save this file as:
#        maya/Qt_Dev/demo_sliders_ui.py
"""
import sys
sys.path.append("$USER/Documents/maya/Qt_Dev")

import planetary_system_generator_ui
reload(planetary_system_generator_ui)

mayaWin = planetary_system_generator_ui.getMayaMainWindow()
dialog = planetary_system_generator_ui.PlanetarySystemGeneratorDialog(mayaWin) 
"""
# Aternatively, run this script directly from Cutter.

isMaya = False
try:
	from PyQt4.QtCore import *
	from PyQt4.QtGui import *
	from PyQt4 import uic
except ImportError:
	from PySide2.QtGui import *
	from PySide2.QtWidgets import *
	from PySide2.QtCore import *
	from PySide2.QtUiTools import *
	isMaya = True
	import maya.OpenMayaUI as omui
	import shiboken2
		
import sys
import os
import math
from connection_utils import *
from planetary_system_generator import PlanetarySystemGenerator;
from random import seed, uniform;

#________________________________________________________
# getMayaMainWindow
#________________________________________________________
# Since Maya UI is written in the C++ version of Qt we use
# shiboken to obtain a reference to its main window as a
# PySide2 object.
def getMayaMainWindow():
	winPtr = omui.MQtUtil.mainWindow()
	return shiboken2.wrapInstance(long(winPtr), QWidget)

#________________________________________________________
#                     Widget Names
#________________________________________________________
#     sphereRad_DSpinBox	sphereRad_Slider
#     sphereNum_SpinBox	    sphereNum_Slider
#
# 			         doit_Button
#________________________________________________________
class PlanetarySystemGeneratorDialog(QDialog):
	def __init__(self, parent=None):
		super(PlanetarySystemGeneratorDialog, self).__init__(parent)
		pathToUi = os.path.join(os.path.dirname(__file__), 'ui', 'PythonUI.ui')
		
		# This loads all the icons and images.
		self.__rocket_icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'rocket.svg');
		self.__planet_icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'planet.svg');
		self.__rings_icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'rings.svg');
		self.__moons_icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'moon.svg');
		self.__stars_icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'star.svg');
		self.__rendering_path = os.path.join(os.path.dirname(__file__), 'icons', 'WideShot.jpg');
		
		if isMaya == False:
			self.ui = uic.loadUi(pathToUi,self)
			self.setWindowFlags(Qt.WindowStaysOnTopHint)
		else:
			loader = QUiLoader()
			self.ui = loader.load(pathToUi, self)
			self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
		self.makeConnections()
		self.ui.show()
	
	#________________________________________________
	def makeConnections(self):
		
		rocket_icon = QIcon();
		planet_icon = QPixmap(self.__planet_icon_path);
		rings_icon = QPixmap(self.__rings_icon_path);
		moons_icon = QPixmap(self.__moons_icon_path);
		stars_icon = QPixmap(self.__stars_icon_path);
		rendering = QPixmap(self.__rendering_path);
		
		rocket_icon.addPixmap(self.__rocket_icon_path);
		
		self.ui.setWindowIcon(rocket_icon);

		self.ui.rendering.setPixmap(rendering);
		self.ui.rendering.setMask(rendering.mask());
		
		self.ui.planet_icon.setPixmap(planet_icon);
		self.ui.planet_icon.setMask(planet_icon.mask());
		
		self.ui.rings_icon.setPixmap(rings_icon);
		self.ui.rings_icon.setMask(rings_icon.mask());
		
		self.ui.moons_icon.setPixmap(moons_icon);
		self.ui.moons_icon.setMask(moons_icon.mask());
		
		self.ui.stars_icon.setPixmap(stars_icon);
		self.ui.stars_icon.setMask(stars_icon.mask());
		
		self.__linked_planet_radius = FloatSlider(self.ui.planet_radius, self.ui.planet_radius_slider, 1); 
		self.__linked_planet_depth = FloatSlider(self.ui.planet_cratering_depth, self.ui.planet_cratering_depth_slider, 2);
		self.__linked_planet_segments = IntSlider(self.ui.planet_cratering_segments, self.ui.planet_cratering_segments_slider);
		self.__linked_planet_fraction = FloatSlider(self.ui.planet_cratering_fraction, self.ui.planet_cratering_fraction_slider, 2);
		self.__linked_rings_number = IntSlider(self.ui.ring_number, self.ui.ring_number_slider);
		self.__linked_moon_number = IntSlider(self.ui.moon_number, self.ui.moon_number_slider);
		self.__linked_moon_ratio = FloatSlider(self.ui.moon_ratio, self.ui.moon_ratio_slider, 2); 
		self.__linked_moon_depth = FloatSlider(self.ui.moon_depth, self.ui.moon_depth_slider, 1);
		self.__linked_moon_segments = IntSlider(self.ui.moon_segments, self.ui.moon_segments_slider);
		self.__linked_moon_fraction = FloatSlider(self.ui.moon_fraction, self.ui.moon_fraction_slider, 1);
		self.__linked_star_fields = IntSlider(self.ui.stars_fields, self.ui.stars_fields_slider);
		self.__linked_star_number = IntSlider(self.ui.stars_number, self.ui.stars_number_slider);
		self.ui.create_button.clicked.connect(self.onCreateClicked);
		self.ui.recommended_button.clicked.connect(self.onRecommendedClicked);
		self.ui.random_button.clicked.connect(self.onRandomClicked);
	#________________________________________________
	def onCreateClicked(self):
		self.__generator = PlanetarySystemGenerator(ui = self.ui);
	
	def onRandomClicked(self):
		
		seed(self.ui.random_seed.value());
		
		self.ui.planet_radius.setValue(uniform(self.ui.planet_radius.minimum(), self.ui.planet_radius.maximum()));
		self.ui.planet_cratering_depth.setValue(uniform(self.ui.planet_cratering_depth.minimum(), self.ui.planet_cratering_depth.maximum()));
		self.ui.planet_cratering_negative.setChecked(uniform(0, 1) > .5);
		self.ui.planet_cratering_segments.setValue(uniform(self.ui.planet_cratering_segments.minimum(), self.ui.planet_cratering_segments.maximum() + 1));
		self.ui.planet_cratering_fraction.setValue(uniform(self.ui.planet_cratering_fraction.minimum(), self.ui.planet_cratering_fraction.maximum()));
		self.ui.ring_number.setValue(uniform(self.ui.ring_number.minimum(), self.ui.ring_number.maximum() + 1));
		self.ui.moon_number.setValue(uniform(self.ui.moon_number.minimum(), self.ui.moon_number.maximum() + 1));
		self.ui.moon_ratio.setValue(uniform(self.ui.moon_ratio.minimum(), self.ui.moon_ratio.maximum()));
		self.ui.moon_depth.setValue(uniform(self.ui.moon_depth.minimum(), self.ui.moon_depth.maximum()));
		self.ui.moon_negative.setChecked(uniform(0, 1) > .5);
		self.ui.moon_segments.setValue(uniform(self.ui.moon_segments.minimum(), self.ui.moon_segments.maximum() + 1));
		self.ui.moon_fraction.setValue(uniform(self.ui.moon_fraction.minimum(), self.ui.moon_fraction.maximum()));
		self.ui.stars_fields.setValue(uniform(self.ui.stars_fields.minimum(), self.ui.stars_fields.maximum() + 1));
		self.ui.stars_number.setValue(uniform(self.ui.stars_number.minimum(), self.ui.stars_number.maximum() + 1));
	
	def onRecommendedClicked(self):
		self.ui.planet_radius.setValue(1.0);
		self.ui.planet_cratering_depth.setValue(1.0);
		self.ui.planet_cratering_negative.setChecked(True);
		self.ui.planet_cratering_segments.setValue(10);
		self.ui.planet_cratering_fraction.setValue(.75);
		self.ui.ring_number.setValue(3);
		self.ui.moon_number.setValue(10);
		self.ui.moon_ratio.setValue(.1);
		self.ui.moon_depth.setValue(1);
		self.ui.moon_negative.setChecked(True);
		self.ui.moon_segments.setValue(10);
		self.ui.moon_fraction.setValue(.75);
		self.ui.stars_fields.setValue(5);
		self.ui.stars_number.setValue(100);
		
		
#========================================================		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	dialog = SlidersDialog()
	dialog.show()
	sys.exit(app.exec_())
