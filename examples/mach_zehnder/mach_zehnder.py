import time
import warnings
import numpy as np
from opics.globals import C
from opics import Network
import opics


if __name__ == "__main__":
    warnings.filterwarnings(
        "ignore"
    )  # ignore all/complex number warnings from numpy or scipy

    sim_start = time.time()

    # define frequency range and resolution
    freq = np.linspace(C * 1e6 / 1.5, C * 1e6 / 1.6, 2000)

    # import component library
    ebeam = opics.libraries.ebeam

    # initialize an empty circuit
    circuit = Network(f=freq)

    # define component instances
    gc = circuit.add_component(ebeam.GC)
    y = circuit.add_component(ebeam.Y)
    wg2 = circuit.add_component(ebeam.Waveguide, params={"length": 0e-6})
    wg1 = circuit.add_component(ebeam.Waveguide, params={"length": 15e-6})
    y2 = circuit.add_component(ebeam.Y)
    gc2 = circuit.add_component(ebeam.GC)

    # specify custom port names
    gc.set_port_reference(0, "input_port")
    gc2.set_port_reference(0, "output_port")

    # define circuit connectivity
    circuit.connect(gc, 1, y, 0)
    circuit.connect(y, 1, wg1, 0)
    circuit.connect(y, 2, wg2, 0)
    circuit.connect(y2, 0, gc2, 1)
    circuit.connect(wg1, 1, y2, 1)
    circuit.connect(wg2, 1, y2, 2)

    # simulate network
    circuit.simulate_network()

    print("simulation finished in %ss" % (str(round(time.time() - sim_start, 2))))

    circuit.sim_result.plot_sparameters(show_freq=False, scale="log")

    data1 = circuit.sim_result.get_data([[1, 0]])

    print("done")
