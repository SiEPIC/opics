from opics.library import libraries
from opics.network import Network
from opics.globals import c_ as c
import warnings
import numpy as np

warnings.filterwarnings('ignore')


#define frequency range and resolution
freq = np.linspace(c*1e6/1.5, c*1e6/1.6, 2000)

library = libraries['ebeam']
components = library['components']
print(components)

circuit = Network()

input_gc = circuit.add_component(components['GC'](freq))
output_gc = circuit.add_component(components['GC'](freq))
dc_halfring = circuit.add_component(components['DC'](freq))
wg = circuit.add_component(components['Waveguide'](freq, np.pi*5e-6))

#connect components
circuit.connect(input_gc, 1, dc_halfring, 0)
circuit.connect(dc_halfring, 1, wg, 0)
circuit.connect(wg, 1, dc_halfring, 3)
circuit.connect(dc_halfring,2, output_gc,1)

circuit.simulate_network()

circuit.sim_result.plot_sparameters(show_freq = False, scale="log", ports = [[1,0], [0,0]])
