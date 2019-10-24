# Malcolm Kesson
# 27 Aug 2019
#
# A couple of classes intended to make is slightly easier to connect
# a spinbox to a slider so that editing the text of the spinbox alters
# it's slider and, conversely, changes to the slider continuously 
# updates the text of the spinbox.
# Save this file as:
#		maya/Qt_Dev/connection_utils.py

import math

#______________________________________________________________
class IntSlider(object):
	def __init__(self, spinbox, slider):
		self.spinbox = spinbox
		self.slider  = slider
		self.slider.valueChanged.connect(self.update_spinbox)
		self.spinbox.valueChanged.connect(self.update_slider)
	def update_spinbox(self):
		value = self.slider.value()
		self.spinbox.setValue( value )
	def update_slider(self):
		value = self.spinbox.value()
		self.slider.setValue( value )
	def getValue(self):
		return self.spinbox.value() 

#______________________________________________________________
class FloatSlider(IntSlider):
	def __init__(self, spinbox, slider, decimal_places = 2):
		# Calling the base class constructor can be done as follows:
		#	 super(FloatSlider, self).__init__(spinbox, slider)
		# or more "directly" as shown next.
		IntSlider.__init__(self, spinbox, slider)
		
		self.decimal_places = decimal_places
		self.spinbox.setDecimals(decimal_places)
		
	def update_spinbox(self):
		value = float(self.slider.value())/math.pow(10, self.decimal_places)
		self.spinbox.setValue( value )
	def update_slider(self):
		value = self.spinbox.value() * math.pow(10, self.decimal_places)
		self.slider.setValue( value )
	def getValue(self):
		return self.spinbox.value() * math.pow(10, self.decimal_places) 
#______________________________________________________________
	
