This module contains rgb tuples for some colors.
Running e.g. 'easycolors.red' will return the rgb tuple for red. 
Running e.g. 'easycolors.transform(easycolors.red, (0,0,10))' will return the rgb tuple for red, but with its blue value incremented by 10. 
The first arg can also be a 3-value tuple, and the second arg can also be an int (which will in- or decrement all values in the given rgb-tuple).
Running 'easycolors.help()' will print some information that might be usefull.

example code:
-----------------------------------
import easycolors

easycolors.red
"(255,0,0)"

easycolors.transform(easycolors.red, (-10,0,0))
"(215,0,0)"

easycolors.transform((10,10,20), 5)
"(15,15,25)"