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

import strupy.units_pure as u
import strupy.concrete.fas as fas_clon
import strupy.concrete.ascomp_pure as ascomp_pure
import strupy.concrete.astens_pure as astens_pure

fas_clon.u = u
fas_clon.ascomp = ascomp_pure
fas_clon.astens = astens_pure

def calc (Nsd=10.0*u.kN, Msd=200.0*u.kNm, h=0.8*u.m, b=0.4*u.m, ap=5*u.cm, an=5*u.cm, fip=20*u.mm, fin=20*u.mm, rysAp=1.0, rysAn=1.0, wlimp=0.3*u.mm, wlimn=0.3*u.mm, fcd=16.7E6*u.Pa, fctm=2.2*u.MPa, fyd=420*u.MPa):
    return fas_clon.calc (Nsd, Msd, h, b, ap, an, fip, fin, rysAp, rysAn, wlimp, wlimn, fcd, fctm, fyd)

# Test if main
if __name__ == '__main__':
    print ('test Fas')
    print (calc())