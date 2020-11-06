from opics import c
from opics import Network
import opics, time, warnings
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# define frequency range and resolution
freq = np.linspace(c * 1e6 / 1.5, c * 1e6 / 1.6, 2000)

# import component library
library = opics.libs.ebeam

power_values = [0, 3e-3, 9e-3, 12e-3]

for power_sweep in power_values:
    sim_start = time.time()

    # initialize an empty circuit
    circuit = Network()

    # define component instances
    gc_ = circuit.add_component(library.GC(freq))
    y_ = circuit.add_component(library.Y(freq))
    wg2 = circuit.add_component(library.TunableWG(freq, 150e-6, power_sweep))
    wg1 = circuit.add_component(library.Waveguide(freq, 50e-6))
    y2_ = circuit.add_component(library.Y(freq))
    gc2_ = circuit.add_component(library.GC(freq))

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
        circuit.sim_result.c / circuit.sim_result.f_ * 1e6,
        20 * np.log10(circuit.sim_result.s_[:, 1, 0]),
    )

plt.title("MZI power sweep w/ tunable WG component")
plt.legend(["%s W" % (each) for each in [0, 22e-3, 24e-3, 26e-3]])
plt.ylabel("dB")
plt.xlabel("um")
plt.xlim(
    np.min(circuit.sim_result.c / circuit.sim_result.f_ * 1e6),
    np.max(circuit.sim_result.c / circuit.sim_result.f_ * 1e6),
)
plt.show()
