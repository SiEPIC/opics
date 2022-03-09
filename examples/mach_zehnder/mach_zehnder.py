import time
import warnings
import numpy as np
from opics.globals import C
from opics import Network

# from opics.libraries import ebeam

import sys

sys.path.append(r"C:\Users\jeida\Desktop\delete\opics_ebeam-0.3.34")


def mzi_example():
    import ebeam

    # define frequency range and resolution
    freq = np.linspace(C * 1e6 / 1.5, C * 1e6 / 1.6, 2000)

    # import component library

    # initialize an empty circuit
    circuit = Network(f=freq)

    # define component instances
    input_gc = circuit.add_component(ebeam.GC)
    y1 = circuit.add_component(ebeam.Y)
    wg2 = circuit.add_component(ebeam.Waveguide, params={"length": 0e-6})
    wg1 = circuit.add_component(ebeam.Waveguide, params={"length": 15e-6})
    y2 = circuit.add_component(ebeam.Y)
    output_gc = circuit.add_component(ebeam.GC)

    # specify custom port names
    input_gc.set_port_reference(0, "input_port")
    output_gc.set_port_reference(0, "output_port")

    # define circuit connectivity
    circuit.connect(input_gc, 1, y1, 0)
    circuit.connect(y1, 1, wg1, 0)
    circuit.connect(y1, 2, wg2, 0)
    circuit.connect(y2, 0, output_gc, 1)
    circuit.connect(wg1, 1, y2, 1)
    circuit.connect(wg2, 1, y2, 2)

    sim_start = time.perf_counter()
    # simulate network

    circuit.simulate_network()

    print("simulation finished in %ss" % (str(time.perf_counter() - sim_start)))

    circuit.sim_result.plot_sparameters(show_freq=False, scale="log")

    print("done")


if __name__ == "__main__":
    warnings.filterwarnings(
        "ignore"
    )  # ignore all/complex number warnings from numpy or scipy

    mzi_example()
