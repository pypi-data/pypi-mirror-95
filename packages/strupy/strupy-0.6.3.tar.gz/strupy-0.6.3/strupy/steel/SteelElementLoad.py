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
from strupy.steel.SteelSectionLoad import SteelSectionLoad

class SteelElementLoad(SteelSectionLoad):

    def __init__(self):
        SteelSectionLoad.__init__(self)
        self.stabilitycheck=[False]
        self.deflectioncheck=[False]

    def add_loadcase(self, casevalue={  "Name": 'Noname',
                                        "M_yEd": 0*u.kNm, "M_zEd": 0*u.kNm, "T_Ed": 0*u.kNm, "N_Ed": 0*u.kN, "V_yEd": 0*u.kN, "V_zEd": 0*u.kN,
                                        "caseactiv": True, "stabilitycheck": False, "deflectioncheck": False}):
        SteelSectionLoad.add_loadcase(self, casevalue)
        #---
        if "stabilitycheck" in casevalue:
            self.stabilitycheck.append(casevalue["stabilitycheck"])
        else:
            self.stabilitycheck.append(False)
        #---
        if "deflectioncheck" in casevalue:
            self.deflectioncheck.append(casevalue["deflectioncheck"])
        else:
            self.deflectioncheck.append(False)

    def edit_loadcase(self, casenumber, newcasevalue={  "Name": 'Noname',
                                                        "M_yEd": 0*u.kNm, "M_zEd": 0*u.kNm, "T_Ed": 0*u.kNm, "N_Ed": 0*u.kN, "V_yEd": 0*u.kN, "V_zEd": 0*u.kN,
                                                        "caseactiv": True, "stabilitycheck": False, "deflectioncheck": False}):
        SteelSectionLoad.edit_loadcase(self, casenumber, newcasevalue)
        #---
        if "stabilitycheck" in newcasevalue:
            self.stabilitycheck[casenumber]=newcasevalue["stabilitycheck"]
        if "deflectioncheck" in newcasevalue:
            self.deflectioncheck[casenumber]=newcasevalue["deflectioncheck"]

    def delete_loadcase(self, casenumber):
        SteelSectionLoad.delete_loadcase(self, casenumber)
        self.stabilitycheck.pop(casenumber)
        self.deflectioncheck.pop(casenumber)

    def get_loadcases(self):
        out = SteelSectionLoad.get_loadcases(self)
        out["stabilitycheck"] = self.stabilitycheck
        out["deflectioncheck"] = self.deflectioncheck
        return out

# Test if main
if __name__ == '__main__':
    print ('test SteelElementLoad')
    # creating SteelSectionLoad object
    a=SteelElementLoad()
    print(a.get_loadcases())
    # adding lodacase to SteelSectionLoad object
    a.add_loadcase({"Name": 'ULS_case1', "M_yEd": 10*u.kNm, "M_zEd": 10*u.kNm, "T_Ed": 2*u.kNm, "N_Ed": 0*u.kN, "V_yEd": 9*u.kN, "V_zEd": 9*u.kN})
    a.add_loadcase({"Name": 'ULS_case2', "M_yEd": 10*u.kNm, "M_zEd": 10*u.kNm, "T_Ed": 2*u.kNm, "N_Ed": 0*u.kN, "V_yEd": 9*u.kN, "V_zEd": 9*u.kN, "caseactiv": True, "stabilitycheck": True})
    print(a.get_loadcases())
    # deleting lodacase number 0 from SteelSectionLoad object
    a.delete_loadcase(2)
    print(a.get_loadcases())
    # editing lodacase values number 0 in SteelSectionLoad object
    a.edit_loadcase(0, {"Name": 'ULS_changed', "M_yEd": 10*u.kNm, "M_zEd": 10*u.kNm, "T_Ed": 2*u.kNm, "N_Ed": 0*u.kN, "V_yEd": 9*u.kN, "V_zEd": 9*u.kN})
    a.edit_loadcase(1, {"Name": 'ULS_case2', "M_yEd": 10*u.kNm, "M_zEd": 10*u.kNm, "T_Ed": 2*u.kNm, "N_Ed": 0*u.kN, "V_yEd": 9*u.kN, "V_zEd": 9*u.kN, "caseactiv": False, "stabilitycheck": False})
    print(a.get_loadcases())
    # deactivating all load cases
    a.caseactiv_all()
    print(a.get_loadcases())
    # activating all load cases
    a.caseactiv_any()
    print(a.get_loadcases())
    # deactivating loadcase 0
    a.caseactiv_offcase(0)
    print(a.get_loadcases())
    # activating loadcase 0
    a.caseactiv_oncase(0)
    print(a.get_loadcases())
    # clearing lodacase in SteelSectionLoad object
    a.clear_loadcase()
    print(a.get_loadcases())