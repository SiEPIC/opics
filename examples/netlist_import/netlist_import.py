from opics.library import libraries
from opics.network import Network
from opics.utils import netlistParser, NetlistProcessor
from opics.globals import c_ 
import time, os
from pathlib import Path
#warnings.filterwarnings('ignore') #ignore all/complex number warnings from numpy or scipy

sim_start = time.time()

# read netlist
spice_filepath = Path(os.path.dirname(__file__) + r"\\spice_netlist.spi")

# get netlist data
circuitData = netlistParser(spice_filepath).readfile()

# process netlist data
subckt = NetlistProcessor(spice_filepath, Network, libraries, c_, circuitData)

#simulate network
subckt.simulate_network()

#get input and output net labels
inp_idx = subckt.sim_result.nets[0].index(circuitData["inp_net"])
out_idx = [subckt.sim_result.nets[0].index(each) for each in circuitData["out_net"]]

ports = [[each_output, inp_idx] for each_output in out_idx]

#plot results
subckt.sim_result.plot_sparameters(ports=ports)

