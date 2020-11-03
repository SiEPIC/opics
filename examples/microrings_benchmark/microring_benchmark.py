# This example is a benchmark test to evaluate the runtime of OPICS
# Benchmark circuit is 100 microring resonators connected in series
from opics.network import Network
from opics.globals import c
import warnings
import numpy as np
import time, opics


warnings.filterwarnings("ignore")

benchmark = []

for i in range(10):

    sim_start = time.time()

    # define frequency range and resolution
    freq = np.linspace(c * 1e6 / 1.5, c * 1e6 / 1.6, 2000)

    components = opics.libraries.ebeam

    circuit = Network()

    input_gc = circuit.add_component(components.GC(freq))
    output_gc = circuit.add_component(components.GC(freq))
    count = 0

    n_rings = 200

    while count < n_rings:
        if count == 0:
            dc_halfring = circuit.add_component(components.DC_halfring(freq))
            wg = circuit.add_component(components.Waveguide(freq, np.pi * 5e-6))
            circuit.connect(input_gc, 1, dc_halfring, 0)
            circuit.connect(dc_halfring, 1, wg, 0)
            circuit.connect(wg, 1, dc_halfring, 3)
            prev_comp = dc_halfring

        elif count >= 1:
            dc_halfring = circuit.add_component(components.DC_halfring(freq))
            wg = circuit.add_component(components.Waveguide(freq, np.pi * 5e-6))
            circuit.connect(prev_comp, 2, dc_halfring, 0)
            circuit.connect(dc_halfring, 1, wg, 0)
            circuit.connect(wg, 1, dc_halfring, 3)
            prev_comp = dc_halfring

        count += 1
    # connect components

    circuit.connect(dc_halfring, 2, output_gc, 1)

    circuit.simulate_network()

    sim_time = round(time.time() - sim_start, 2)
    print("simulation finished in %ss" % (str(sim_time)))

    benchmark.append(sim_time)

# circuit.sim_result.plot_sparameters(show_freq = False, scale="log", ports = [[1,0], [0,0]])
"""
x = 0
for i in circuit.current_components:
    x+=1
print(x)"""
"""for each in circuit.current_components:
    each.plot_sparameters(show_freq=False, scale="abs_sq")"""

print(np.mean(benchmark), "s average time taken")
