import pathlib
from opics import libraries
from opics.network import Network
from opics.utils import netlistParser, NetlistProcessor
from opics.globals import c as c_

# warnings.filterwarnings('ignore') #ignore all/complex number warnings from numpy or scipy


def test_read_netlist():

    # read netlist
    cwd = pathlib.Path(__file__).absolute().parent
    spice_filepath = cwd / "test_read_netlist" / "test_sample.spi"


    # get netlist data
    circuitData = netlistParser(spice_filepath).readfile()

    print(circuitData)
    print(type(circuitData))

    # process netlist data
    subckt = NetlistProcessor(spice_filepath, Network, libraries, c_, circuitData)

    # simulate network
    subckt.simulate_network()

    # get input and output net labels
    inp_idx = subckt.sim_result.nets[0].index(circuitData["inp_net"])
    out_idx = [subckt.sim_result.nets[0].index(each) for each in circuitData["out_net"]]

    ports = [[each_output, inp_idx] for each_output in out_idx]


if __name__ == "__main__": 
    test_read_netlist()
