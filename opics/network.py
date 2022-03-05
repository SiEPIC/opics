import os
import binascii
from copy import deepcopy
from typing import List, Optional, Dict
from numpy import ndarray
from opics.sparam_ops import connect_s
from opics.components import componentModel
from opics.globals import F


class Network:
    """
    Specifies the network.

    Args:
        network_id: Define the network name.
        f: frequency data points.
    """

    def __init__(
        self, network_id: Optional[str] = None, f: Optional[ndarray] = None
    ) -> None:
        self.f = f
        if self.f is None:
            self.f = F

        self.network_id = (
            network_id if network_id else str(binascii.hexlify(os.urandom(4)))[2:-1]
        )
        self.current_components = []
        self.current_connections = []
        self.global_netlist = []
        self.port_references = {}
        self.idx_to_references = {}
        self.sim_result = None

    def add_component(
        self,
        component: componentModel,
        params: Dict = {},
        component_id: Optional[str] = None,
    ):
        """
        Adds component to a network.

        Args:
            component: An instance of componentModel class.
            params: Component parameter values.
            component_id: Custom component id tag.
        """
        count = 0
        for each in self.current_components:
            if type(component) == type(each):
                count += 1

        if "f" not in params:
            params["f"] = self.f

        temp_component = component(**params)

        temp_component.component_id = (
            temp_component.component_id + "_" + str(count)
            if component_id is None
            else component_id
        )

        self.current_components.append(temp_component)

        return temp_component

    def connect(
        self,
        component_A: componentModel,
        port_A: int,
        component_B: componentModel,
        port_B: int,
    ):
        """
        Connects two components together.

        Args:
            component_A: An instance of componentModel class.
            port_A: Port number of component_A
            component_B: An instance of componentModel class.
            port_B: Port number of component_B
        """
        if type(port_A) == str:
            port_A = self.current_components.index(component_A)[port_A]
        if type(port_B) == str:
            port_B = self.current_components.index(component_B)[port_B]

        self.current_connections.append(
            [
                self.current_components.index(component_A),
                port_A,
                self.current_components.index(component_B),
                port_B,
            ]
        )

    def initiate_global_netlist(self):
        """
        Initiates a global netlist with negative indices, \
            overwrite indices that are used in the circuit\
                 with positive values.
        """

        gnetlist = []
        net_start = 0
        for component_idx in range(len(self.current_components)):
            temp_net = []
            for each_port in range(self.current_components[component_idx].s.shape[-1]):
                net_start -= 1
                temp_net.append(net_start)
                if (
                    self.current_components[component_idx].port_references[each_port]
                    != each_port
                ):
                    self.port_references[net_start] = self.current_components[
                        component_idx
                    ].port_references[each_port]
            gnetlist.append(temp_net)

        for i in range(len(self.current_connections)):
            each_conn = self.current_connections[i]
            gnetlist[each_conn[0]][each_conn[1]] = i
            gnetlist[each_conn[2]][each_conn[3]] = i

        self.global_netlist = gnetlist

    def global_to_local_ports(self, net_id: int, nets: List[List[int]]) -> List[int]:
        """
        Maps the net_id to components and their local port numbers.

        Args:
            net_id: Net id reference.
            nets: Nets
        """
        filtered_nets = [
            nets.index(each_net) for each_net in nets if net_id in each_net
        ]
        net_idx = []
        for each_net in filtered_nets:
            net_idx += [i for i, x in enumerate(nets[each_net]) if x == net_id]
        if len(filtered_nets) == 1:
            filtered_nets += filtered_nets

        return [filtered_nets[0], net_idx[0], filtered_nets[1], net_idx[1]]

    def simulate_network(self) -> componentModel:
        """
        Triggers the simulation

        """

        if self.global_netlist == []:
            self.initiate_global_netlist()

        # check if all the components are connected
        _not_connected = set()
        for i, each_net in enumerate(self.global_netlist):
            if sum(each_net) < min(each_net):
                _not_connected.add(self.current_components[i])

        if bool(_not_connected):
            self.global_netlist = []
            raise RuntimeError("Some components are not connected.")

        t_components = deepcopy(self.current_components)
        t_nets = deepcopy(self.global_netlist)
        t_connections = [i for i in set(sum(t_nets, [])) if i >= 0]

        for n in t_connections:
            # print("sim_network current connection", self.current_connections)
            # component A id, port id, component B id, port id
            ntp = self.global_to_local_ports(n, t_nets)  # nets to ports

            # If pin occurances are in the same component:
            if ntp[0] == ntp[2]:
                # print(t_components[ca].s.shape)
                new_s = connect_s(
                    t_components[ntp[0]].s,
                    ntp[1],
                    None,
                    ntp[3],
                    create_composite_matrix=False,
                )
                t_components[ntp[0]].s = new_s
                del t_nets[ntp[0]][ntp[1]]
                if (
                    ntp[1] < ntp[3]
                ):  # if the current index occurs before the second one, shifting all nets to the left
                    del t_nets[ntp[2]][ntp[3] - 1]
                else:
                    del t_nets[ntp[2]][ntp[3]]

            # If pin occurances are in different components:
            else:
                combination_f = t_components[0].f
                combination_s = connect_s(
                    t_components[ntp[0]].s, ntp[1], t_components[ntp[2]].s, ntp[3]
                )
                # nets of newest component
                del t_nets[ntp[0]][ntp[1]], t_nets[ntp[2]][ntp[3]]
                new_net = t_nets[ntp[0]] + t_nets[ntp[2]]

                del t_components[ntp[0]], t_nets[ntp[0]]
                if ntp[0] < ntp[2]:
                    del t_components[ntp[2] - 1], t_nets[ntp[2] - 1]
                else:
                    del t_components[ntp[2]], t_nets[ntp[2]]

                t_components.append(
                    componentModel(f=combination_f, s=combination_s, nets=t_nets)
                )
                t_nets.append(new_net)

        if len(t_nets) == 1:

            self.sim_result = t_components[-1]
            self.current_components.clear()
            self.current_components = t_components
            self.global_netlist = t_nets

            for each_net in t_nets:
                i = 0
                for each_port in each_net:
                    self.idx_to_references[i] = each_port
                    i += 1

            return t_components[-1]

        else:
            self.current_components = t_components
            self.current_connections = []
            self.global_netlist = t_nets
            return t_components
