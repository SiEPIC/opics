import time, warnings, sys
from opics import c
from opics import Network
import opics, warnings
import numpy as np

warnings.filterwarnings('ignore')


#define frequency range and resolution
freq = np.linspace(c*1e6/1.5, c*1e6/1.6, 2000)

ebeam = opics.libraries.ebeam

circuit = Network()

input_gc = circuit.add_component(ebeam.GC(freq))
output_gc = circuit.add_component(ebeam.GC(freq))
wg = circuit.add_component(ebeam.Waveguide(freq, np.pi*5e-6))
dc_halfring = circuit.add_component(ebeam.DC_halfring(freq))


#connect components
circuit.connect(input_gc, 1, dc_halfring, 0)
circuit.connect(dc_halfring, 1, wg, 0)
circuit.connect(wg, 1, dc_halfring, 3)
circuit.connect(dc_halfring,2, output_gc,1)

circuit.simulate_network()

circuit.sim_result.plot_sparameters(show_freq = False, scale="abs_sq", ports = [[1,0], [0,0]])
