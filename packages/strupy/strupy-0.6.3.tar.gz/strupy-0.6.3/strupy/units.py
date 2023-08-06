'''
--------------------------------------------------------------------------
Copyright (C) 2015-2021 Lukasz Laba <lukaszlaba@gmail.com>

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
- kg units added
- m3, cm3, mm3, m4, cm4, mm4 units added
- python3 compatibility checked
- um, rad added
- US imperial unit system added
- US imperial unit system updated
- US imperial unit system updated
'''

from unum import Unum as __Unum

# Unum customization
__Unum.UNIT_SEP = '.'
__Unum.UNIT_DIV_SEP = '/'
__Unum.UNIT_FORMAT = '[%s]'
__Unum.VALUE_FORMAT = '%5.2f'

#---------------------------------------------------------------------
# SI unit list used in StruPy pakage
from unum.units import s
from unum.units import h
from unum.units import km                      # [km] unit definition
from unum.units import mile                    # [mile] unit definition
from unum.units import m                       # [m] unit definition
from unum.units import cm                      # [cm] unit definition
from unum.units import dm                      # [dm] unit definition
from unum.units import mm                      # [mm] unit definition
from unum.units import um                      # [um] unit definition
from unum.units import kg                      # [kg] unit definition
from unum.units import t                       # [t] unit definition

m2=m**2                                        # [m2] unit definition
cm2=cm**2                                      # [cm2] unit definition
mm2=mm**2                                      # [mm2] unit definition
from unum.units import ha                      # [ha] unit definition

m3=m**3                                        # [m3] unit definition
dm3=dm**3                                      # [cm3] unit definition
cm3=cm**3                                      # [cm3] unit definition
mm3=mm**3                                      # [mm3] unit definition

m4=m**4                                        # [m4] unit definition
cm4=cm**4                                      # [cm4] unit definition
mm4=mm**4                                      # [mm4] unit definition

from unum.units import N                       # [N] unit definition
kN = __Unum.unit('kN', 1E3 * N)                # [kN] unit definition

Nm = __Unum.unit('Nm', N * m)                  # [Nm] unit definition
kNm = __Unum.unit('kNm', 1E3 * N * m)          # [kNm] unit definition

from unum.units import J                       # [J] unit definition

from unum.units import Pa as Pa                # [Pa] unit definition
from unum.units import bar                     # [bar] unit definition
kPa = __Unum.unit('kPa', 1E3 * Pa)             # [kPa] unit definition
MPa = __Unum.unit('MPa', 1E6 * Pa)             # [MPa] unit definition
GPa = __Unum.unit('GPa', 1E9 * Pa)             # [MPa] unit definition

#---------------------------------------------------------------------
#Imperial unit system for US calculacion

inch = __Unum.unit('inch', 0.0254 * m)          # [in] unit definition
ft = __Unum.unit('ft', 12. * inch)              # [ft] unit definition
yd = __Unum.unit('yd', 3. * ft)                 # [yd] unit definition

inch2 = inch**2                                 # [inch2] unit definition
ft2 = ft**2                                     # [ft2] unit definition
yd2 = yd**2                                     # [yrd2] unit definition

inch3 = inch**3                                 # [inch3] unit definition
ft3 = ft**3                                     # [ft3] unit definition

inch4 = inch**4                                 # [inch4] unit definition
ft4 = ft**4                                     # [inch4] unit definition

lb = __Unum.unit('lb', 0.45359237 * kg)         # [lb] unit definition
UKton = __Unum.unit('UKton', 2240. * lb)        # [UKton] unit definition
USton = __Unum.unit('USton', 2000. * lb)        # [USton] unit definition

lbf = __Unum.unit('lbf', 4.4482216152605 * N)   # [lbf] unit definition
kip = __Unum.unit('kip', 1E3 * lbf)             # [kip] unit definition

lbfinch = __Unum.unit('lbfinch', lbf * inch)    # [lbfinch] unit definition
lbfft = __Unum.unit('lbfft', lbf * ft)          # [lbfft] unit definition
kipft = __Unum.unit('kipft', kip * ft)          # [kipft] unit definition
kipinch = __Unum.unit('kipinch', kip * inch)    # [kipinch] unit definition

plf = __Unum.unit('plf', lbf / ft)              # [plf] unit definition
klf = __Unum.unit('klf', kip / ft)              # [plf] unit definition

psi = __Unum.unit('psi', lbf / inch2)           # [psi] unit definition
ksi = __Unum.unit('ksi', 1E3 * psi)             # [ksi] unit definition
psf = __Unum.unit('psf', lbf / ft2)             # [psf] unit definition
ksf = __Unum.unit('ksf', 1E3 * psf)             # [ksf] unit definition

pci = __Unum.unit('pci', lbf / inch3)           # [pci] unit definition
pcf = __Unum.unit('pcf', lbf / ft3)             # [pcf] unit definition
kcf = __Unum.unit('kcf', kip / ft3)             # [kcf] unit definition

#---------------------------------------------------------------------

# Extra useful function definition

def xvalueformat(format='%10.2f'):
    __Unum.VALUE_FORMAT=format

def xunumlistvalue(unumlist,unit=1):
    if type(unumlist[0]) is not type ([]):
        unumlist = [(i/unit).asNumber() for i in unumlist]
        return unumlist
    if type(unumlist[0]) is type ([]):
        for j in range(len(unumlist)):
            unumlist[j] = [(i/unit).asNumber() for i in unumlist[j]]
        return unumlist

# Test if main
if __name__ == '__main__':
    print ('units test')
    print (3.7*m*s**2)
    print (23.7*kN/m)
    print (2*kN/m)
    a=10*m
    b=10*m
    c=a+b
    print (c)
    c=c**2
    print (c)
    print ('xunumlistvalue test')
    a=[1*m, 3*m]
    b=[1*m, 3*m]
    print (a)
    print (b)
    print ('_unumlistvalue --->')
    a=xunumlistvalue(a, 0.01*m)
    b=xunumlistvalue(b, 0.01*m)
    print (a)
    print (b)
    k=[[m, m], [m, m]]
    k=xunumlistvalue(k, 0.01*m)
    print (k)