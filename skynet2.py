from collections import deque
from typing import Deque, List

class Node:
    def __init__(self, index: int):
        self.index = index
        self.links: List[Node] = []
        self.is_gateway = False
        self.is_closed = False

    @property #getters
    def nb_gateway_links(self) -> int:
        return sum(link.is_gateway for link in self.links)

    def get_gateway_link(self):
        return next((link for link in self.links if link.is_gateway), None)

class Graph:
    def __init__(self):
        self.nodes: List[Node] = []
        self.target_gateways: List[Node] = []

    def update_targets(self, gateway: Node):
        if not gateway.links:
            self.target_gateways.remove(gateway)

    def reset(self):
        for node in self.nodes:
            node.is_closed = False

    def sever(self, node1: Node, node2: Node):
        print(f"{node1.index} {node2.index}")

    def block_agent(self, agent_index: int) -> bool:
        agent_node: Node = self.nodes[agent_index]
        for node in agent_node.links:
            if node.is_gateway:
                self.sever(agent_node, node)
                agent_node.links.remove(node)
                node.links.remove(agent_node)
                self.update_targets(node)
                return True
        return False

    def block_double_gateway(self, agent_index: int) -> bool:
        agent_node = self.nodes[agent_index]
        queue: Deque[Node] = deque()
        self.reset()
        agent_node.is_closed = True
        queue.append(agent_node)

        while queue:
            atual_node: Node = queue.popleft() #remove o objeto mais a esquerda do deque
            for aux in atual_node.links:
                nb_gateway_links = aux.nb_gateway_links
                if not aux.is_gateway and nb_gateway_links >= 1 and not aux.is_closed:
                    aux.is_closed = True
                    if nb_gateway_links == 2:
                        gateway = aux.get_gateway_link()
                        self.sever(aux, gateway)
                        aux.links.remove(gateway)
                        gateway.links.remove(aux)
                        self.update_targets(gateway)
                        return True
                    else:
                        queue.append(aux)
        return False

    def block_gateway(self):
        gateway = self.target_gateways[0]
        node = gateway.links[0]
        self.sever(gateway, node)
        gateway.links.remove(node)
        node.links.remove(gateway)
        self.update_targets(gateway)


graph = Graph()
graph.nb_nodes, nb_links, graph.nb_gateways = map(int, input().split())

for index in range(graph.nb_nodes):
    graph.nodes.append(Node(index))

for _ in range(nb_links):
    n1, n2 = map(int, input().split())
    node1: Node = graph.nodes[n1]
    node2: Node = graph.nodes[n2]
    node1.links.append(node2)
    node2.links.append(node1)

for _ in range(graph.nb_gateways):
    index = int(input())
    gateway = graph.nodes[index]
    gateway.is_gateway = True
    graph.target_gateways.append(gateway)


while True:
    agent_index = int(input())
    if not graph.block_agent(agent_index):
        if not graph.block_double_gateway(agent_index):
            graph.block_gateway()
