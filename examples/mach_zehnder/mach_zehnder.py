import time, warnings
import numpy as np
import matplotlib.pyplot as plt
from opics import c_ as c
from opics import Network
import opics

warnings.filterwarnings('ignore') #ignore all/complex number warnings from numpy or scipy
sim_start = time.time()


#define frequency range and resolution
freq = np.linspace(c*1e6/1.5, c*1e6/1.6, 2000)

#import component library
ebeam = opics.libs.ebeam

#initialize an empty circuit
circuit = Network()

#define component instances
gc_  = circuit.add_component(ebeam.GC(freq))
y_ =   circuit.add_component(ebeam.Y(freq))
wg2 =  circuit.add_component(ebeam.Waveguide(freq, 150e-6))
wg1 =  circuit.add_component(ebeam.Waveguide(freq, 50e-6))
y2_ =  circuit.add_component(ebeam.Y(freq))
gc2_ = circuit.add_component(ebeam.GC(freq))

#define circuit connectivity
circuit.connect(gc_, 1, y_, 0)
circuit.connect(y_, 1, wg1, 0)
circuit.connect(y_, 2, wg2, 0)
circuit.connect(y2_, 0, gc2_, 1)
circuit.connect(wg1, 1, y2_, 1)
circuit.connect(wg2, 1, y2_, 2)

#simulate network
circuit.simulate_network()

print("simulation finished in %ss"%(str(round(time.time()-sim_start,2))))

circuit.sim_result.plot_sparameters(show_freq = False, scale="log")
