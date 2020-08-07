
from opics.library import libraries
from opics.network import Network
import time, warnings
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore') #ignore all/complex number warnings from numpy or scipy
sim_start = time.time()

#define frequency range and resolution
freq = np.linspace(299792458*1e6/1.5, 299792458*1e6/1.6, 2000)

#import component library
library = libraries['ebeam']
library_components = library['components']

#initialize an empty circuit
circuit = Network()

#define component instances
gc_  = circuit.add_component(library_components['GC'](freq))
y_ =   circuit.add_component(library_components['Y'](freq))
wg2 =  circuit.add_component(library_components['Waveguide'](freq, 150e-6))
wg1 =  circuit.add_component(library_components['Waveguide'](freq, 50e-6))
y2_ =  circuit.add_component(library_components['Y'](freq))
gc2_ = circuit.add_component(library_components['GC'](freq))

#print(circuit.current_components)
#port_dic= {'port1': 0}

#connect components

print(circuit.current_connections)
print(circuit.global_netlist)

circuit.connect(gc_, 1, y_, 0)
circuit.connect(y_, 1, wg1, 0)
circuit.connect(y_, 2, wg2, 0)
circuit.connect(y2_, 0, gc2_, 1)
circuit.connect(wg1, 1, y2_, 1)
circuit.connect(wg2, 1, y2_, 2)

#print(circuit.global_to_local_ports(3))

#simulate network
circuit.simulate_network()

print("simulation finished in %ss"%(str(round(time.time()-sim_start,2))))


circuit.sim_result.plot_sparameters(show_freq = False, scale="log")

#gc_.plot_sparameters(show_freq=False, scale="log", port=[1,0])

print(circuit.global_netlist)


#print(circuit.sim_result.nets[0])
#y_.plot_sparameters(show_freq=False, scale="abs_sq")

# log scale optional
# add lookup table based solution
# add DC component, which parses another variable to optical components
# electrical netlist"""

