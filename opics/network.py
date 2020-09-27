
from scipy.interpolate import interp1d
from copy import deepcopy
from .sparam_ops import connect_s, innerconnect_s
from .components import compoundElement
import os, binascii

def interpolate(output_freq = None, input_freq= None, s_parameters = None):
    """interpolates s-parameters"""
    func = interp1d(input_freq, s_parameters, kind='cubic', axis=0)
    return [output_freq, func(output_freq)]


class Network:
    """ specifies the network
    """
    def __init__(self, networkID = None):
        self.networkID = networkID if networkID != None else str(binascii.hexlify(os.urandom(4)))[2:-1]
        self.current_components = []
        self.current_connections = []
        self.global_netlist = []
        self.sim_result = None


    def add_component(self, cls, componentID = None):
        """add component to a network
        """
        count = 0
        for each in self.current_components:
            if type(cls) == type(each):
                count+=1
        
        cls.componentID = cls.componentID +"_"+str(count) if componentID==None else componentID
        self.current_components.append(cls)
        return cls

    def connect(self, component_A, port_A, component_B, port_B):
        """connect two components together
        """
        self.current_connections.append([self.current_components.index(component_A), port_A, self.current_components.index(component_B), port_B])


    def initiate_global_netlist(self):
        """initiates a global netlist with negative indices, overwrite indices that are used in the circuit with positive values
        """
        gnetlist = []
        net_start = 0
        for component_idx in range(len(self.current_components)):
            temp_net = []
            for i in range(self.current_components[component_idx].s.shape[-1]):
                net_start -=1
                temp_net.append(net_start)
            gnetlist.append(temp_net)

        for i in range(len(self.current_connections)):
            each_conn = self.current_connections[i]
            gnetlist[each_conn[0]][each_conn[1]] = i
            gnetlist[each_conn[2]][each_conn[3]] = i

        self.global_netlist =  gnetlist  

    
    def global_to_local_ports(self, net_id, nets):
        """
        returns which components the net_id refers to and their corresponding local ports
        """
        filtered_nets = [nets.index(each_net) for each_net in nets if net_id in each_net]
        net_idx = []
        for each_net in filtered_nets:
            net_idx += [i for i, x in enumerate(nets[each_net]) if x == net_id]
        if len(filtered_nets) == 1:
            filtered_nets += filtered_nets
        
        return [filtered_nets[0], net_idx[0], filtered_nets[1], net_idx[1]]

    def simulate_network(self):
        """ function to trigger the simulation of the network
        """

        if self.global_netlist == []:
            self.initiate_global_netlist()

        t_components = deepcopy(self.current_components)
        t_nets = deepcopy(self.global_netlist)
        t_connections = [i for i in set(sum(t_nets, [])) if i >=0]

        for n in t_connections:
            #print("sim_network current connection", self.current_connections)
            #component A id, port id, component B id, port id
            ntp = self.global_to_local_ports(n, t_nets) #nets to ports
        
            # If pin occurances are in the same component:
            if ntp[0] == ntp[2]:
                #print(t_components[ca].s.shape)
                new_s = innerconnect_s(t_components[ntp[0]].s, ntp[1], ntp[3])
                t_components[ntp[0]].s = new_s
                del t_nets[ntp[0]][ntp[1]]
                if(ntp[1] < ntp[3]): #if the current index occurs before the second one, shifting all nets to the left
                    del t_nets[ntp[2]][ntp[3]-1]
                else:
                    del t_nets[ntp[2]][ntp[3]]

            # If pin occurances are in different components:
            else:
                combination_f = t_components[0].f
                combination_s = connect_s(t_components[ntp[0]].s, ntp[1], t_components[ntp[2]].s, ntp[3])
                #nets of newest component
                del t_nets[ntp[0]][ntp[1]], t_nets[ntp[2]][ntp[3]]
                new_net = t_nets[ntp[0]] + t_nets[ntp[2]]

                del t_components[ntp[0]], t_nets[ntp[0]]
                if(ntp[0]<ntp[2]):
                    del t_components[ntp[2]-1], t_nets[ntp[2]-1]
                else:
                    del t_components[ntp[2]], t_nets[ntp[2]]
                
                t_components.append(compoundElement(combination_f, combination_s, t_nets))
                t_nets.append(new_net)

        self.sim_result = t_components[0]
        return t_components[0]
