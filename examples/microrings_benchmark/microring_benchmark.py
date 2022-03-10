"""
This example is a benchmark test to evaluate the runtime of OPICS
Benchmark circuit is 100 microring resonators connected in series
"""

import time
import numpy as np
from opics.network import Network, bulk_add_component
import multiprocessing as mp
import opics


def routine():

    benchmark = []

    for i in range(1):

        components = opics.libraries.ebeam

        sim_start = time.perf_counter()
        circuit = Network(
            mp_config={
                "enabled": True,
                "proc_count": mp.cpu_count() - 1,
                "close_pool": False,
            }
        )

        count = 0

        n_rings = 100

        _components_data = []

        while count < n_rings:
            _components_data.append(
                {
                    "component": components.DC_halfring,
                    "params": {"f": circuit.f},
                    "component_id": f"dc_{count}",
                }
            )

            _components_data.append(
                {
                    "component": components.Waveguide,
                    "params": {"f": circuit.f, "length": np.pi * 5e-6},
                    "component_id": f"wg_{count}",
                }
            )
            count += 1

        bulk_add_component(circuit, _components_data)

        circuit.add_component(components.GC, component_id="input")
        circuit.add_component(components.GC, component_id="output")

        # bulk connect
        count = 0
        prev_comp = ""
        while count < n_rings:
            if count == 0:
                circuit.connect("input", 1, f"dc_{count}", 0)
                circuit.connect(f"dc_{count}", 1, f"wg_{count}", 0)
                circuit.connect(f"wg_{count}", 1, f"dc_{count}", 3)
                prev_comp = "dc_0"

            elif count >= 1:
                circuit.connect(prev_comp, 2, f"dc_{count}", 0)
                circuit.connect(f"dc_{count}", 1, f"wg_{count}", 0)
                circuit.connect(f"wg_{count}", 1, f"dc_{count}", 3)
                prev_comp = f"dc_{count}"
            count += 1

        circuit.connect(prev_comp, 2, "output", 1)

        circuit.simulate_network()
        sim_time = round(time.perf_counter() - sim_start, 2)
        benchmark.append(sim_time)
        circuit.sim_result.plot_sparameters(interactive=True, show_freq=False)
        print(f"simulation finished in {sim_time*1000} ms")

    print(np.mean(benchmark), "s average time taken")


if __name__ == "__main__":
    routine()
