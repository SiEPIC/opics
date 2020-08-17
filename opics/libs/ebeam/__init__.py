from ...components import componentModel,Waveguide
import numpy as np
from pathlib import Path
from copy import deepcopy
datadir =  Path(str(Path(__file__).parent)) / "data"


class BDC(componentModel):
    cls_attrs = {"height":0, "width":0}
    valid_OID = [1]
    ports = 4
    def __init__(self, f_, height = 220e-9, width = 500e-9, OID = 1):
        data_folder=datadir
        filename="bdc_lookup_table.xml"

        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["height"] = height
        LUT_attrs_["width"] = width
        super().__init__(f_, data_folder, filename, 4, "bdc_sparam", **LUT_attrs_)
        if(OID in self.valid_OID):
            self.s_ = self.load_sparameters(data_folder, filename)
        else:
            self.s_ = np.zeros((self.f_.shape[0], self.ports, self.ports))
        self.componentID = "Ebeam_BDC"


class DC(componentModel):
    cls_attrs = {"Lc":0}
    valid_OID = [1]
    ports = 4
    def __init__(self, f_, Lc = 0, OID = 1):
        data_folder = datadir/ 'ebeam_dc_te1550'
        filename="dc_map.xml"

        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["Lc"] = Lc
        super().__init__(f_, data_folder, filename, 4, "s-param", **LUT_attrs_)
        if(OID in self.valid_OID):
            self.s_ = self.load_sparameters(data_folder, filename)
        else:
            self.s_ = np.zeros((self.f_.shape[0], self.ports, self.ports))
        self.componentID = "Ebeam_DC"


class DC_halfring(componentModel):
    cls_attrs = {"CoupleLength" : 0, "gap" : 100e-9, "radius" : 5e-6, "thickness" : 220e-9, "width" : 500e-9}
    valid_OID = [1]
    ports = 4
    def __init__(self, f_, CoupleLength = 0, gap = 100e-9, radius = 5e-6, thickness = 220e-9, width = 500e-9, OID = 1):
        data_folder = datadir / 'ebeam_dc_halfring_straight'
        filename="te_ebeam_dc_halfring_straight.xml"

        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["CoupleLength"] = CoupleLength
        LUT_attrs_["gap"] = gap
        LUT_attrs_["radius"] = radius
        LUT_attrs_["thickness"] = thickness
        LUT_attrs_["width"] = width

        super().__init__(f_, data_folder, filename, 4, "s-param", **LUT_attrs_)
        if(OID in self.valid_OID):
            self.s_ = self.load_sparameters(data_folder, filename)
        else:
            self.s_ = np.zeros((self.f_.shape[0], self.ports, self.ports))
        self.componentID = "Ebeam_DC_halfring"




class GC(componentModel):
    cls_attrs = {"deltaw" : 0, "height" : 2.2e-07}
    valid_OID = [1]
    ports = 2
    def __init__(self, f_, deltaw = 0, height = 2.2e-07, OID = 1):

        data_folder= datadir / "gc_source"
        filename="GC_TE_lookup_table.xml"

        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["deltaw"] = deltaw
        LUT_attrs_["height"] = height
        super().__init__(f_, data_folder, filename, 2, "gc_sparam", **LUT_attrs_)
        if(OID in self.valid_OID):
            self.s_ = self.load_sparameters(data_folder, filename)
        else:
            self.s_ = np.zeros((self.f_.shape[0], self.ports, self.ports))

        self.componentID = "Ebeam_GC"



class Multimode(componentModel):
    valid_OID = [1,2]
    ports = 2
    def __init__(self, f_, OID=1):
        super().__init__(f_, "", "")
        if(OID in self.valid_OID and OID == 1):
            self.s_ = np.zeros((self.f_.shape[0], self.ports, self.ports))
            self.s_[1,0] = self.s_[0,1] = -2*np.ones((self.f_.shape[0]))
        elif(OID in self.valid_OID and OID == 2):
            self.s_ = np.zeros((self.f_.shape[0], self.ports, self.ports))
            self.s_[1,0] = self.s_[0,1] = -5*np.ones((self.f_.shape[0]))
        self.componentID = "Ebeam_multimode"


class Terminator(componentModel):
    valid_OID = [1]
    ports  = 1
    def __init__(self, f_, OID=1):
        data_folder = datadir / 'ebeam_terminator_te1550'
        filename="ebeam_terminator_te1550.npz"
        super().__init__(f_, data_folder, filename)
        if(OID in self.valid_OID):
            self.s_ = self.load_sparameters(data_folder, filename)
        else:
            self.s_ = np.zeros((self.f_.shape[0], self.ports, self.ports))
        self.componentID = "Ebeam_Terminator"



class TunableWG(Waveguide):
    cls_attrs = {"power": 0}
    valid_OID = [1,2]
    ports = 2
    def __init__(self, f_, length, power = 0e-3, TE_loss = 700, OID = 1):
        data_folder=datadir /'tunable_wg'
        filename="wg_strip_tunable.xml"
        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["power"] = power

        super().__init__(f_, length, data_folder, filename, TE_loss, **LUT_attrs_)
        if(OID in self.valid_OID):
            self.s_ = self.load_sparameters(length, data_folder, filename, TE_loss)
        else:
            self.s_ = np.zeros((self.f_.shape[0], self.ports, self.ports))
        self.componentID = "Ebeam_TunableWG"



class Waveguide(Waveguide):
    cls_attrs = {"length":0e-6, "height":220e-9, "width":500e-9}
    valid_OID = [1,2]
    ports = 2
    def __init__(self, f_, length = 0e-6, height = 220e-9, width=500e-9, TE_loss = 700, OID=1):
        data_folder=datadir / "wg_integral_source"
        filename="wg_strip_lookup_table.xml"

        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["height"] = height
        LUT_attrs_["width"] = width

        #length is not part of LUT attributes
        del LUT_attrs_["length"]

        super().__init__(f_, length = length, data_folder= data_folder, filename= filename, TE_loss= TE_loss, **LUT_attrs_)
        if(OID in self.valid_OID):
            self.s_ = self.load_sparameters(length, data_folder, filename, TE_loss)
        else:
            self.s_ = np.zeros((self.f_.shape[0], self.ports, self.ports))
        
        self.componentID = "Ebeam_WG"


class Y(componentModel):
    cls_attrs = {"height":220e-9, "width":500e-9}
    valid_OID = [1]
    ports = 3
    def __init__(self, f_, height= 220e-9, width= 500e-9, OID=1):
        
        data_folder = datadir/ 'y_branch_source'
        filename="y_lookup_table.xml"
        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["height"] = height
        LUT_attrs_["width"] =  width

        #print(LUT_attrs_)
        super().__init__(f_, data_folder, filename, 3, "y_sparam", **LUT_attrs_)
        if(OID in self.valid_OID):
            self.s_ = self.load_sparameters(data_folder, filename)
        else:
            self.s_ = np.zeros((self.f_.shape[0], self.ports, self.ports))
        self.componentID = "Ebeam_Y"


