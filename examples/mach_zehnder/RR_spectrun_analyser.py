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
    general = opics.libraries.general
    temporary = opics.libraries.temporary

    # initialize an empty circuit
    circuit = Network()

    wc = circuit.add_component(temporary.waveguide_coupler(freq))
    # wc.plot_sparameters(show_freq=False, scale="log")

    # define component instances
    tap = circuit.add_component(general.probe(freq))

    tap.port_references[1] = "output_a"
    tap.port_references[2] = "output_b"

    gc_ = circuit.add_component(ebeam.GC(freq))
    # gc_.plot_sparameters(show_freq=False, scale="log", ports=[[1, 0]])

    circuit.connect(tap, 0, gc_, 1)

    # simulate network
    circuit.simulate_network()

    print("simulation finished in %ss" % (str(round(time.time() - sim_start, 2))))
    print(circuit.sim_result.nets)
    print(circuit.port_references)

    circuit.sim_result.plot_sparameters(
        show_freq=False, scale="log", ports=[[1, 0], [2, 0]]
    )

print("done")
