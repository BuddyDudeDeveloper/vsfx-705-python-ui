# VSFX 705 Python UI
The repo for the Python UI assignment of the VSFX 705 course at SCAD.

## How to Run
1. Download the repository and put all files and folders into your Qt_Dev folder.
2. In Maya, run the following code in the script editor:

```python
import planetary_system_generator_ui
reload(planetary_system_generator_ui)
mayaWin = planetary_system_generator_ui.getMayaMainWindow()
dialog = planetary_system_generator_ui.PlanetarySystemGeneratorDialog(mayaWin) 
```
