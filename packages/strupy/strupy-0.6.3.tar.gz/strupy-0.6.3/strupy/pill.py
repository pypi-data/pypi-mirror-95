'''
--------------------------------------------------------------------------
Copyright (C) 2015-2020 Lukasz Laba <lukaszlaba@gmail.com>

This file is part of StruPy.
StruPy structural engineering design Python package.
https://bitbucket.org/struthonteam/strupy

StruPy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

StruPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with StruPy; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------

File changes:
- python3 compatibility checked
'''

import strupy.units as u
from strupy.steel.MaterialSteel import MaterialSteel as __MaterialSteel
from strupy.steel.SectionBase import SectionBase as __SectionBase
from strupy.concrete.MaterialConcrete import MaterialConcrete as __MaterialConcrete
from strupy.concrete.MaterialRcsteel import MaterialRcsteel as __MaterialRcsteel
import strupy.concrete.rcsteel_area as rcsteel_area

MaterialSteel = __MaterialSteel()
SectionBase = __SectionBase()
MaterialConcrete = __MaterialConcrete()
MaterialRcsteel = __MaterialRcsteel()

# Test if main
if __name__ == '__main__':
    pass