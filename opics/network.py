import os
import binascii
from typing import List, Optional, Dict
from numpy import ndarray
from opics.sparam_ops import connect_s
from opics.components import componentModel
from opics.globals import F
import multiprocessing as mp


def solve_tasks(data: list):
    components, ntp, nets = data
    # If pin occurances are in the same component:
    if ntp[0] == ntp[2]:
        # print(t_components[ca].s.shape)
        new_s = connect_s(
            components[0].s,
            ntp[1],
            None,
            ntp[3],
            create_composite_matrix=False,
        )
        components[0].s = new_s
        new_component = components[0]

        new_net = nets[0]
        p1, p2 = new_net[ntp[1]], new_net[ntp[3]]

        # delete both port references
        new_net.remove(p1)
        new_net.remove(p2)

        return new_component, new_net

    # If pin occurances are in different components:
    else:
        combination_f = F
        combination_s = connect_s(components[0].s, ntp[1], components[1].s, ntp[3])

        # nets of the new component
        net1, net2 = nets[0], nets[1]
        del net1[ntp[1]], net2[ntp[3]]
        new_net = net1 + net2

        # create new component
        new_component = componentModel(f=combination_f, s=combination_s, nets=new_net)
        return new_component, new_net


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
        if "f" not in params:
            params["f"] = self.f

        temp_component = component(**params)

        temp_component.component_id = (
            temp_component.component_id
            + "_"
            + str(binascii.hexlify(os.urandom(4)))[2:-1]
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

        # create global netlist
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

        t_components = self.current_components
        t_nets = self.global_netlist
        t_connections = [i for i in set(sum(t_nets, [])) if i >= 0]

        _connections_in_use = set()
        while len(t_connections) > 0:

            # track components and connections in use
            _components_in_use = set()
            _nets_in_use = []
            _task_bundle = []

            # ------------ Step 1: Create Task Bundles------------------
            # for loop to iterate over connections
            for _connection in t_connections:
                if _connection not in _connections_in_use:
                    # get components and port indexes
                    net_to_port = self.global_to_local_ports(_connection, t_nets)

                    # components are already being used in another net, skip this connection
                    if (
                        t_components[net_to_port[0]].component_id in _components_in_use
                        or t_components[net_to_port[2]].component_id
                        in _components_in_use
                    ):
                        continue

                    # lock components, nets, and connections to prevent from being used in other threads
                    _connections_in_use.add(_connection)
                    _components_in_use.add(t_components[net_to_port[0]].component_id)
                    _components_in_use.add(t_components[net_to_port[2]].component_id)
                    _nets_in_use.append(t_nets[net_to_port[0]])
                    _nets_in_use.append(t_nets[net_to_port[2]])

                    # -------- Step 2: add components to tasks bundles -----------
                    if net_to_port[0] == net_to_port[2]:
                        # if the both components are the same
                        _task_bundle.append(
                            [
                                [t_components[net_to_port[0]], None],
                                net_to_port,
                                [t_nets[net_to_port[0]], t_nets[net_to_port[2]]],
                            ]
                        )

                        """
                        _task_bundle.append({"components": [t_components[net_to_port[0]],
                                                            None],
                                             "ntp": net_to_port,
                                             "nets": [t_nets[net_to_port[0]],
                                                      t_nets[net_to_port[2]]]
                                             })
                        """

                    else:
                        _task_bundle.append(
                            [
                                [
                                    t_components[net_to_port[0]],
                                    t_components[net_to_port[2]],
                                ],
                                net_to_port,
                                [t_nets[net_to_port[0]], t_nets[net_to_port[2]]],
                            ]
                        )
                        """
                        _task_bundle.append({"components": [t_components[net_to_port[0]],
                                                            t_components[net_to_port[2]]],
                                             "ntp": net_to_port,
                                             "nets": [t_nets[net_to_port[0]],
                                                      t_nets[net_to_port[2]]]})
                        """

            # ------- Step 3: Remove components, nets, connection ids ----------
            _temp_components = []

            for _ in range(len(t_components)):
                _each_components = t_components[_]
                if _each_components.component_id not in _components_in_use:
                    _temp_components.append(_each_components)
            t_components = _temp_components
            t_nets = [each_net for each_net in t_nets if each_net not in _nets_in_use]
            t_connections = [
                each_conn
                for each_conn in t_connections
                if each_conn not in _connections_in_use
            ]

            # ------- solve tasks and merge results -----------
            """
            for _each_task in _task_bundle:
                result = solve_tasks(**_each_task)
                t_components.append(result[0])
                t_nets.append(result[1])

            for _each_task in _task_bundle:
                result = solve_tasks(_each_task)
                t_components.append(result[0])
                t_nets.append(result[1])
            """
            with mp.Pool() as pool:
                results = pool.map(solve_tasks, _task_bundle)
            # merge results
            for each_result in results:
                t_components.append(each_result[0])
                t_nets.append(each_result[1])

        self.current_components = t_components
        self.sim_result = t_components[-1]
        self.current_connections = []
        self.global_netlist = t_nets
        return t_components[-1]
