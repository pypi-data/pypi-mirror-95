==========
StruPy 0.6
==========
Structural engineering design python package

Changelog
---------
StruPy 0.6.3
  - US imprial unit system updated
StruPy 0.6.2
  - port to python3, python 2 dropped
  - US imprial unit system updated
StruPy 0.5.8
  - US imprial unit system added
  - US and UK section datatase added
StruPy 0.5.7
  - steel.element_resistance hot fix
StruPy 0.5.6
  - steel.SteelSection added
StruPy 0.5.5
  - concrete.RcPanelDataLoader upgraded for Robot2016
StruPy 0.5.4
  - concrete.RcPanelDataLoader upgraded to Mecway7
StruPy 0.5.3
  - strupy.x_graphic package updated (caused by dxfstructure)
StruPy 0.5.2
  - concrete.RcPanelToolbox added (cut_peak, smooth and anchore inside)
  - concrete.RcPanel family updated
  - steel.SectionBase optimized (speedmode paremeter added)
  - steel profile class acc. EC3 implemented
StruPy 0.5.1
  - strupy.steel.Bolt modules created
  - strupy.x_graphic package updated
StruPy 0.4.7
  - strupy.concrete.RcRecSectSolver corrected
StruPy 0.4.6
  - concrete.RcPanelDataLoader upgraded (Mecway input interface)  
StruPy 0.4.5
  - concrete.RcPanel modules upgraded  
StruPy 0.4.4
  - concrete.RcPanelDataLoader upgraded  
StruPy 0.4.3
  - concrete.RcPanelDataLoader upgraded  
StruPy 0.4.2
  - concrete.RcPanel modules upgraded  
StruPy 0.4.1
  - some strupy.concrete modules optimized
  - concrete.RcPanel modules created  
StruPy 0.3.4
  - strupy.concrete.RcRecSectSolver corrected
StruPy 0.3.3
  - some strupy.concrete modules optimized  
StruPy 0.3.2
  - some strupy.concrete modules optimized  
StruPy 0.3.1
  - strupy.steel package upgraded
  - strupy.x_graphic package created  
StruPy 0.2
  - steel section database created (SectionBase class in strupy.steel)  
StruPy 0.1
  - some functionality for concrete deisgn added  

Requirements
------------
StruPy is based on Python 3.6 and few non-standard Python library:

  - Unum (https://pypi.python.org/pypi/Unum)
  - PyQt5 (https://www.riverbankcomputing.com/software/pyqt) - not necessary, only for strupy.x_graphic package needed
  - Matplotlib (http://matplotlib.org) - not necessary - only for a few ploting function needed
  - NumPy (http://www.numpy.org) - not necessary - for concret.RcPanel and steel.Bolt family needed
  - xlrd (https://pypi.python.org/pypi/xlrd) - not necessary - only for Concrete.RcPanelDataLoader needed
  - dxfwrite (https://pypi.python.org/pypi/dxfwrite) - not necessary - only for Concrete.RcPanelViewer needed
  - easygui (https://pypi.python.org/pypi/easygui) - not necessary - only for Concrete.RcPanelDataLoader
  - pyautocad (https://pypi.python.org/pypi/pyautocad) - not necessary - only for strupy.x_graphic package needed

How to install
--------------
After the Python and needed library was installed, install StruPy by typing::

    pip install strupy

You can also find more install information at project website.

Windows 7,10 and Linux Xubutu tested.

Licence
-------
StruPy is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Copyright (C) 2015-2020 Lukasz Laba <lukaszlaba@gmail.com>

Contributions
-------------
If you want to help out, create a pull request or write email.

More information
----------------
Project website: https://bitbucket.org/struthonteam/strupy

Code repository: https://bitbucket.org/struthonteam/strupy

PyPI package: https://pypi.python.org/pypi/strupy

Contact: Lukasz Laba <lukaszlaba@gmail.com>