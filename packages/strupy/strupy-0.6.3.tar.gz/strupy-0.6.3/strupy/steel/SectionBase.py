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
- US database added
- python3 tested - ui_get_sectionparameters and find_withparameter() not work
- speedmode option added
- Iomega unit corected to cm6
- draw_sectiongeometry() metchod added
- get_sectioncontourpoints() method added
'''

import xml.etree.ElementTree as ET
import copy
import os
import math

import strupy.units as u
import strupy.steel.database_sections.sectiontypes as sectiontypes

class SectionBase():
    
    def __init__(self, speedmode=2, basename='EU'): #speedmode available - 1 or 2
        self.__speedmode = speedmode
        self.set_databasename(basename)

    def get_available_databasenames(self):
        return ['EU', 'US', 'UK']
        
    def set_databasename(self, basename):
        if basename == 'EU':
            self.__database='sectionbase_EuropeanSectionDatabase.xml'
            self.lu = u.m
            self.sdu = u.m.asUnit(u.cm)   
            self.wu = u.kg
            self.__load_data_from_xml()
            print(basename + ' base loaded')
        elif basename == 'US':
            self.__database='sectionbase_AmericanSectionDatabase.xml'
            self.lu = u.ft
            self.sdu = u.inch 
            self.wu = u.lb
            self.__load_data_from_xml()
            print(basename + ' base loaded')
        elif basename == 'UK':
            self.__database='sectionbase_BritishSectionDatabase.xml'
            self.lu = u.m
            self.sdu = u.m.asUnit(u.cm)   
            self.wu = u.kg
            self.__load_data_from_xml()
            print(basename + ' base loaded')
        else:
            print(basename + ' base not found !!')
        self.set_speedmode(self.__speedmode)

    
    def __load_data_from_xml(self):
        self.__package_dir = os.path.split(__file__)[0]
        self.__xmlbase_path = os.path.join(self.__package_dir, "database_sections", self.__database)
        self.__tree = ET.parse(self.__xmlbase_path)
        self.__root = self.__tree.getroot()        
        
    def set_speedmode(self, speedmode=2):
        self.__speedmode = speedmode
        if self.__speedmode == 1:
            self.__sectiondictwithparam=self.__get_database_sectiondictwithparam()
        else:
            self.__sectiondictwithparam = {}
            
    def __get_database_sectiondictwithparam(self):
        sectiondictwithpatam={}
        for item in self.__root.iter('sectionlist_item'):
            sectiondictwithpatam[item.attrib['sectionname']]=self.__sectionparameters_unitaplly(copy.deepcopy(item.attrib))
        for i in sectiondictwithpatam:
            sectiondictwithpatam[i]['Wy']=\
            sectiondictwithpatam[i]['Iy']/max(sectiondictwithpatam[i]['vz'],sectiondictwithpatam[i]['vpz']).normalize()
            sectiondictwithpatam[i]['Wz']=\
            sectiondictwithpatam[i]['Iz']/max(sectiondictwithpatam[i]['vy'],sectiondictwithpatam[i]['vpy']).normalize()
            sectiondictwithpatam[i]['figuregroup']=sectiontypes.FigureGroupName(sectiondictwithpatam[i]['figure'])
        return sectiondictwithpatam
    
    def __get_one_sectiondictwithparam(self, sectionname):
        sectiondictwithpatam={}
        for item in self.__root.iter('sectionlist_item'):
            if item.attrib['sectionname'] == sectionname:
                sectiondictwithpatam[item.attrib['sectionname']]=self.__sectionparameters_unitaplly(copy.deepcopy(item.attrib))
        for i in sectiondictwithpatam:
            sectiondictwithpatam[i]['Wy']=\
            sectiondictwithpatam[i]['Iy']/max(sectiondictwithpatam[i]['vz'],sectiondictwithpatam[i]['vpz']).normalize()
            sectiondictwithpatam[i]['Wz']=\
            sectiondictwithpatam[i]['Iz']/max(sectiondictwithpatam[i]['vy'],sectiondictwithpatam[i]['vpy']).normalize()
            sectiondictwithpatam[i]['figuregroup']=sectiontypes.FigureGroupName(sectiondictwithpatam[i]['figure'])
        return sectiondictwithpatam

    def get_database_name(self):
        name=[]
        for item in self.__root.iter('baseinformation'):
            name = item.attrib
        return name['basetitle']

    def get_database_sectiontypes(self):
        sectiontypes=[]
        for item in self.__root.iter('sectiontype_item'):
            sectiontypes.append(item.attrib ['figure'])
        return sectiontypes
        
    def get_database_sectiontypesdescription(self):
        description={}
        for item in self.__root.iter('sectiontype_item'):
            description[item.attrib ['figure']]=item.attrib ['description']
        return description
        
    def get_database_sectionlist(self):
        sectionlist=[]
        for item in self.__root.iter('sectionlist_item'):
            sectionlist.append(item.attrib ['sectionname'])
        return sectionlist
        
    def get_database_sectionlistwithtype(self, secttype='IPE'):
        sectionlistwithtype=[]
        for item in self.__root.iter('sectionlist_item'):
                if item.attrib['figure'] == secttype :
                    sectionlistwithtype.append(item.attrib ['sectionname'])
        return sectionlistwithtype
        
    def get_database_sectiongroups(self):
        return sectiontypes.sectiongroups
        
    def get_figuregroupid(self, figure):
        return sectiontypes.FigureGroupId(figure)
        
    def get_figuregroupname(self, figure):
        return sectiontypes.FigureGroupName(figure)

    def __sectionparameters_unitaplly(self, param):
        lu = self.lu      #long_unit
        sdu = self.sdu    #sectdim_unit
        wu = self.wu      #weight_unit
        #---------------------------------
        param['mass']=float(param['mass'])*wu/lu
        param['surf']=float(param['surf'])*sdu**2/lu
        param['h']=float(param['h'])*sdu
        param['b']=float(param['b'])*sdu
        param['ea']=float(param['ea'])*sdu
        param['es']=float(param['es'])*sdu
        param['ra']=float(param['ra'])*sdu
        param['rs']=float(param['rs'])*sdu
        param['gap']=float(param['gap'])*sdu
        param['Ax']=float(param['Ax'])*sdu**2
        param['Ay']=float(param['Ay'])*sdu**2
        param['Az']=float(param['Az'])*sdu**2
        param['Ix']=float(param['Ix'])*sdu**4
        param['Iy']=float(param['Iy'])*sdu**4
        param['Iz']=float(param['Iz'])*sdu**4
        param['Iomega']=float(param['Iomega'])*sdu**6
        param['vy']=float(param['vy'])*sdu
        param['vpy']=float(param['vpy'])*sdu
        param['vz']=float(param['vz'])*sdu
        param['vpz']=float(param['vpz'])*sdu
        param['Wply']=float(param['Wply'])*sdu**3
        param['Wplz']=float(param['Wplz'])*sdu**3
        param['Wtors']=float(param['Wtors'])*sdu**3
        param['Ayv']=float(param['Ayv'])*sdu**2
        param['Azv']=float(param['Azv'])*sdu**2
        param['gamma']=float(param['gamma'])
        #---------------------------------
        return  param

    def get_sectionparameters(self, sectname='IPE 270'):
        if self.__speedmode == 1:
            return self.__sectiondictwithparam[sectname]
        if self.__speedmode == 2:
            return self.__get_one_sectiondictwithparam(sectname)[sectname]
            
    def get_sectioncontourpoints(self, sectname='IPE 270'):
        param = self.get_sectionparameters(sectname)
        figure = param['figure']
        h = param['h']
        b = param['b']
        ea = param['ea']
        es = param['es']
        ra = param['ra']
        rs = param['rs']
        gap = param['gap']
        vy = param['vy']
        vpy = param['vpy']
        vz = param['vz']
        vpz = param['vpz']
        gamma = param['gamma']
        return sectiontypes.sectioncontourpoints(figure, h, b, ea, es, ra, rs, gap, vz, vpz, vy, vpy, gamma)
    
    def draw_sectiongeometry(self, SomeGeometryObiect, sectname='IPE 270', annotation=1):
        param = self.get_sectionparameters(sectname)
        figure = param['figure']
        h = param['h']
        b = param['b']
        ea = param['ea']
        es = param['es']
        ra = param['ra']
        rs = param['rs']
        gap = param['gap']
        vy = param['vy']
        vpy = param['vpy']
        vz = param['vz']
        vpz = param['vpz']
        gamma = param['gamma']
        sectiontypes.draw_geometry(SomeGeometryObiect, figure, sectname, h, b, ea, es, ra, rs, gap, vz, vpz, vy, vpy, gamma, annotation)
        return None    
        
    def ui_get_sectionparameters(self):
        import tkinter
        root=tkinter.Tk()
        root.title('StrupySteelSectionBrowser')
        def sectname_changed(e):
            if L1.curselection():
                global sectname
                sectname = L1.get(L1.curselection())
                t.delete(1.0,tkinter.END)
                param_tmp=self.get_sectionparameters(sectname)
                for key in param_tmp:
                    t.insert(tkinter.END, key + '=' + str(param_tmp[key]) +'\n')
        def close_dialog(e):
            root.quit()
            root.destroy()
        def sectype_changed(e):
            if L.curselection():
                L1.delete(0,L1.size())
                for item in self.get_database_sectionlistwithtype(L.get(L.curselection())):
                    L1.insert(tkinter.END, item)
                t.delete(1.0,tkinter.END)
        s = tkinter.Scrollbar()
        s1 = tkinter.Scrollbar()
        L = tkinter.Listbox()
        L1 = tkinter.Listbox()
        t=tkinter.Text()
        s.pack(side=tkinter.LEFT, fill=tkinter.Y)
        s1.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        L.pack(side=tkinter.LEFT, fill=tkinter.Y)
        L1.pack(side=tkinter.LEFT, fill=tkinter.Y)
        t.pack()
        L.bind('<<ListboxSelect>>', sectype_changed)
        L1.bind('<<ListboxSelect>>', sectname_changed)
        L1.bind('<Double-Button-1>', close_dialog)
        s.config(command=L.yview)
        s1.config(command=L1.yview)
        L.config(yscrollcommand=s.set)
        L1.config(yscrollcommand=s1.set)
        for item in self.get_database_sectiontypes():
            L.insert(tkinter.END, item)
        root.mainloop()
        return self.get_sectionparameters(sectname)

    def get_parameters_description(self):
        descriptiondir=[]
        for item in self.__root.iter('parameterdescription'):
            descriptiondir = item.attrib
        descriptiondir['Wy'] = 'Elastic section modulus about Y axis'
        descriptiondir['Wz'] = 'Elastic section modulus about Z axis'
        descriptiondir['figuretype'] = 'General type of section figure'
        return descriptiondir
    
    def find_withparameter(self, parameter='mass', value=40*u.kg/u.m, delta_n=-0.2, delta_p=0.2):
        sectionlist=[]
        for i in self.__sectiondictwithparam.keys():
            if value*(1+delta_n) <= self.__sectiondictwithparam[i][parameter] <= value*(1+delta_p):
                sectionlist.append(str(i))
        return sectionlist

# Test if main
if __name__ == '__main__':
    #----
    class ExampleGeometryObiectForTesting():
        def addLine(self, p1, p2):
            print ('line from ' + str(p1) + ' to ' + str(p2))
        def addText(self, text, p):
            print ('text ' + text + ' a t' + str(p))
    #----
    print ('test DataBaseBrowser')
    base=SectionBase(basename='EU')
    print (base.get_database_name())
    print (base.get_database_sectiontypes())
    print (base.get_database_sectiontypesdescription())
    print (base.get_database_sectionlist())
    print (base.get_database_sectionlistwithtype('HEA'))
    print (base.get_sectionparameters("IPE 330"))
    #print (base.ui_get_sectionparameters())
    print (base.get_parameters_description())
    print (base.find_withparameter())
    print (base.get_sectioncontourpoints('IPE 330'))
    geometry = ExampleGeometryObiectForTesting() 
    print (base.draw_sectiongeometry(geometry, 'IPE 200'))
    '''
    type_with_no_contour_list = [] 
    for type in base.get_database_sectiontypesdescription():
        type_list = base.get_database_sectionlistwithtype(type)
        print type + '  ' +base.get_database_sectiontypesdescription()[type]
        if base.get_sectioncontourpoints(type_list[0]) == []:
            print '!!!!!!!!!!!!!!!!'
            type_with_no_contour_list.append(type)
    print type_with_no_contour_list
    
    print '------------ Types with no conturpoint definded-----------'    
    for type in type_with_no_contour_list:
        print type + '  ' +base.get_database_sectiontypesdescription()[type]
    '''