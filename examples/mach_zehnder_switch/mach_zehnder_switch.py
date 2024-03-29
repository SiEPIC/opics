import time
import warnings
import numpy as np
import matplotlib.pyplot as plt
from opics import C
from opics import Network
import opics

warnings.filterwarnings("ignore")

# define frequency range and resolution
freq = np.linspace(C * 1e6 / 1.5, C * 1e6 / 1.6, 2000)

# import component library
library = opics.libraries.ebeam

power_values = [0, 3e-3, 9e-3, 12e-3]

for power_sweep in power_values:
    sim_start = time.time()

    # initialize an empty circuit
    circuit = Network()

    # define component instances
    gc_ = circuit.add_component(library.GC)
    y_ = circuit.add_component(library.Y)
    wg1 = circuit.add_component(library.Waveguide, params={"length": 50e-6})
    wg2 = circuit.add_component(
        library.TunableWG, params={"length": 150e-6, "power": power_sweep}
    )
    y2_ = circuit.add_component(library.Y)
    gc2_ = circuit.add_component(library.GC)

    # connect components
    circuit.connect(gc_, 1, y_, 0)
    circuit.connect(y_, 1, wg1, 0)
    circuit.connect(y_, 2, wg2, 0)
    circuit.connect(y2_, 0, gc2_, 1)
    circuit.connect(wg1, 1, y2_, 1)
    circuit.connect(wg2, 1, y2_, 2)

    # simulate network
    circuit.simulate_network()

    plt.plot(
        circuit.sim_result.C / circuit.sim_result.f * 1e6,
        20 * np.log10(circuit.sim_result.s[:, 1, 0]),
    )

plt.title("MZI power sweep w/ tunable WG component")
plt.legend(["%s W" % (each) for each in [0, 22e-3, 24e-3, 26e-3]])
plt.ylabel("dB")
plt.xlabel("um")
plt.xlim(
    np.min(circuit.sim_result.C / circuit.sim_result.f * 1e6),
    np.max(circuit.sim_result.C / circuit.sim_result.f * 1e6),
)
plt.show()
