""" OID: orthogonal ID for polarization
"""

from copy import deepcopy
from pathlib import Path
import numpy as np
from opics.globals import f
from opics.components import componentModel, Waveguide

datadir = Path(str(Path(__file__).parent)) / "data"


class BDC(componentModel):
    """50/50% broadband directional 3-dB couplers. Two 3-dB couplers can be used to make an unbalanced Mach-Zehnder Interferometer (MZI), \
        showing a large extinction ratio. The advantage of this device compared to the Y-Branch is that it has 2x2 ports, \
        thus the MZI has two outputs. Compared to the directional coupler, it is less wavelength sensitive.

    """

    cls_attrs = {"height": 0, "width": 0}
    valid_OID = [1]
    ports = 4

    def __init__(self, f=f, height=220e-9, width=500e-9, OID=1):
        data_folder = datadir / "bdc_TE_source"
        filename = "bdc_lookup_table.xml"

        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["height"] = height
        LUT_attrs_["width"] = width
        super().__init__(f, data_folder, filename, 4, "bdc_sparam", **LUT_attrs_)
        if OID in self.valid_OID:
            self.s = self.load_sparameters(data_folder, filename)
        else:
            self.s = np.zeros((self.f.shape[0], self.ports, self.ports))
        self.componentID = "Ebeam_BDC"


class DC_temp(componentModel):
    """The directional coupler is commonly used for splitting and combining light in photonics. \
        It consists of two parallel waveguides where the coupling coefficient is influenced by the \
            waveguide length and the distance between waveguides.

    """

    cls_attrs = {"Lc": 0}
    valid_OID = [1]
    ports = 4

    def __init__(self, f=f, Lc=0, OID=1):
        data_folder = datadir / "ebeam_dc_te1550"
        filename = "dc_map.xml"

        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["Lc"] = Lc
        super().__init__(f, data_folder, filename, 4, "s-param", **LUT_attrs_)
        if OID in self.valid_OID:
            self.s = self.load_sparameters(data_folder, filename)
        else:
            self.s = np.zeros((self.f.shape[0], self.ports, self.ports))
        self.componentID = "Ebeam_DC"


class DC_halfring(componentModel):
    """Models evanescent coupling region between a straight waveguide and a bent radius of length pi*radius um. Useful for filters, sensors."""

    cls_attrs = {
        "CoupleLength": 0,
        "gap": 100e-9,
        "radius": 5e-6,
        "thickness": 220e-9,
        "width": 500e-9,
    }
    valid_OID = [1]
    ports = 4

    def __init__(
        self,
        f=f,
        CoupleLength=0,
        gap=100e-9,
        radius=5e-6,
        thickness=220e-9,
        width=500e-9,
        OID=1,
    ):
        data_folder = datadir / "ebeam_dc_halfring_straight"
        filename = "te_ebeam_dc_halfring_straight.xml"

        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["CoupleLength"] = CoupleLength
        LUT_attrs_["gap"] = gap
        LUT_attrs_["radius"] = radius
        LUT_attrs_["thickness"] = thickness
        LUT_attrs_["width"] = width

        super().__init__(f, data_folder, filename, 4, "s-param", **LUT_attrs_)
        if OID in self.valid_OID:
            self.s = self.load_sparameters(data_folder, filename)
        else:
            self.s = np.zeros((self.f.shape[0], self.ports, self.ports))
        self.componentID = "Ebeam_DC_halfring"


class GC(componentModel):
    """Fully-etched fibre-waveguide grating couplers with sub-wavelength gratings showing high coupling efficiency as well as low \
        back reflections for both transverse electric (TE) and transverse magnetic (TM) modes. EBeam fabrication cost is reduced \
            by ~2-3X when eliminating the shallow etch.
    """

    cls_attrs = {"deltaw": 0, "height": 2.2e-07}
    valid_OID = [1]
    ports = 2

    def __init__(self, f=f, deltaw=0, height=2.2e-07, OID=1):

        data_folder = datadir / "gc_source"
        filename = "GC_TE_lookup_table.xml"

        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["deltaw"] = deltaw
        LUT_attrs_["height"] = height
        super().__init__(f, data_folder, filename, 2, "gc_sparam", **LUT_attrs_)
        if OID in self.valid_OID:
            self.s = self.load_sparameters(data_folder, filename)
        else:
            self.s = np.zeros((self.f.shape[0], self.ports, self.ports))

        self.componentID = "Ebeam_GC"


class Multimode(componentModel):
    valid_OID = [1, 2]
    ports = 2

    def __init__(self, f=f, OID=1):
        super().__init__(f, "", "")
        if OID in self.valid_OID and OID == 1:
            self.s = np.zeros((self.f.shape[0], self.ports, self.ports))
            self.s[1, 0] = self.s[0, 1] = -2 * np.ones((self.f.shape[0]))
        elif OID in self.valid_OID and OID == 2:
            self.s = np.zeros((self.f.shape[0], self.ports, self.ports))
            self.s[1, 0] = self.s[0, 1] = -5 * np.ones((self.f.shape[0]))
        self.componentID = "Ebeam_multimode"


class Terminator(componentModel):
    """This component is used to terminate a waveguide. This terminator is a nano-taper that spreads \
        the light into the oxide and is used for efficient edge coupling. Even if a waveguide crosses near\
             this taper end, the reflection is minimal. This is included in this model, 1 µm away, therefore, \
                 the model is a worst-case reflection. To terminate unused ports on components to avoid reflections,\
                      refer to Disconnected Waveguides.

    """

    valid_OID = [1]
    ports = 1

    def __init__(self, f=f, OID=1):
        data_folder = datadir / "ebeam_terminator_te1550"
        filename = "ebeam_terminator_te1550.npz"
        super().__init__(f, data_folder, filename)
        if OID in self.valid_OID:
            self.s = self.load_sparameters(data_folder, filename)
        else:
            self.s = np.zeros((self.f.shape[0], self.ports, self.ports))
        self.componentID = "Ebeam_Terminator"


class TunableWG(Waveguide):
    cls_attrs = {"power": 0}
    valid_OID = [1, 2]
    ports = 2

    def __init__(self, length=5e-6, f=f, power=0e-3, TE_loss=700, OID=1):
        data_folder = datadir / "tunable_wg"
        filename = "wg_strip_tunable.xml"
        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["power"] = power

        super().__init__(f, length, data_folder, filename, TE_loss, **LUT_attrs_)
        if OID in self.valid_OID:
            self.s = self.load_sparameters(length, data_folder, filename, TE_loss)
        else:
            self.s = np.zeros((self.f.shape[0], self.ports, self.ports))
        self.componentID = "Ebeam_TunableWG"


class Waveguide(Waveguide):
    """Waveguides are components that guide waves. Although these are individual components that can\
         be adjusted for use, it is recommended to draw paths in KLayout and convert them to waveguides\
              using the built-in SiEPIC features.
    """

    cls_attrs = {"wg_length": 0e-6, "height": 220e-9, "width": 500e-9}
    valid_OID = [1, 2]
    ports = 2

    def __init__(
        self, f=f, wg_length=5e-6, height=220e-9, width=500e-9, TE_loss=700, OID=1
    ):
        data_folder = datadir / "wg_integral_source"
        filename = "wg_strip_lookup_table.xml"

        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["height"] = height
        LUT_attrs_["width"] = width

        # length is not part of LUT attributes
        del LUT_attrs_["wg_length"]

        super().__init__(
            f,
            length=wg_length,
            data_folder=data_folder,
            filename=filename,
            TE_loss=TE_loss,
            **LUT_attrs_
        )
        if OID in self.valid_OID:
            self.s = self.load_sparameters(wg_length, data_folder, filename, TE_loss)
        else:
            self.s = np.zeros((self.f.shape[0], self.ports, self.ports))

        self.componentID = "Ebeam_WG"


class Y(componentModel):
    """50/50 3dB splitter. Useful for splitting light, Mach-Zehner Interferometers, etc.\
         The layout parameters for the device were taken from the journal paper below, and implemented in EBeam lithography.
    """

    cls_attrs = {"height": 220e-9, "width": 500e-9}
    valid_OID = [1]
    ports = 3

    def __init__(self, f=f, height=220e-9, width=500e-9, OID=1):

        data_folder = datadir / "y_branch_source"
        filename = "y_lookup_table.xml"
        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["height"] = height
        LUT_attrs_["width"] = width

        # print(LUT_attrs_)
        super().__init__(f, data_folder, filename, 3, "y_sparam", **LUT_attrs_)
        if OID in self.valid_OID:
            self.s = self.load_sparameters(data_folder, filename)
        else:
            self.s = np.zeros((self.f.shape[0], self.ports, self.ports))
        self.componentID = "Ebeam_Y"


class Switch(componentModel):
    """2x2 tunable optical switch component. Useful for switching the input optical power between two output ports."""

    cls_attrs = {"power": 0}
    valid_OID = [1]
    ports = 4

    def __init__(self, f=f, power=0e-3, OID=1):
        data_folder = datadir / "2x2_switch"
        filename = "2x2_switch.xml"

        LUT_attrs_ = deepcopy(self.cls_attrs)
        LUT_attrs_["power"] = power
        super().__init__(f, data_folder, filename, 4, "switch_sparam", **LUT_attrs_)
        if OID in self.valid_OID:
            self.s = self.load_sparameters(data_folder, filename)
        else:
            self.s = np.zeros((self.f.shape[0], self.ports, self.ports))
        self.componentID = "Ebeam_switch"


component_factory = dict(
    BDC=BDC,
    DC_halfring=DC_halfring,
    DC_temp=DC_temp,
    GC=GC,
    Multimode=Multimode,
    Path=Path,
    Switch=Switch,
    Terminator=Terminator,
    TunableWG=TunableWG,
    Waveguide=Waveguide,
    Y=Y,
)

components = list(component_factory.keys())
__all__ = components


if __name__ == "__main__":
    import numpy as np
    import opics as op

    w = np.linspace(1.52, 1.58, 3) * 1e-6
    f = op.c / w
    c = BDC(f=f)
    s = c.get_data()
