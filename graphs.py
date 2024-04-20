from abc import abstractmethod, ABC
from typing import Type, Any, Optional, Union
import pydantic
from decimal import Decimal

import uuid
from copy import deepcopy

class Node(pydantic.BaseModel):
    id: Union[str, int, uuid.UUID] = uuid.uuid4()
    connected_edges: list['Edge'] = []
    additional_parameters: Optional[Any] = None

class Edge(pydantic.BaseModel):
    id: Union[str, int, uuid.UUID] = uuid.uuid4()
    from_node: Node
    to_node: Node
    is_bidirectional: bool = False
    weighted_value: Optional[Union[int, float, Decimal]] = 0

class Graph:

    def __init__(self) -> None:
        self._nodes: dict[Union[str, int], Node] = {}
        self._edges: dict[int, Edge] = {}
    
    def add_nodes(self, *nodes: Type[Node]) -> None:
        if not self.check_node_exist(*nodes):
            for node in nodes:
                self._nodes[node.id] = node
    
    def create_node(self, new_node_id: Union[str, int, uuid.UUID] = uuid.uuid4(), initial_edges: list[Edge] = [], additional_parameters: Optional[Any] = None):
        node = Node(id=new_node_id, connected_edges=initial_edges, additional_parameters=additional_parameters)
        self.add_nodes(node)  
    
    def remove_node(self, *nodes: Type[Node]) -> None:
        if self.check_node_exist(*nodes):
            for node in nodes:
                if node.id in self._nodes:
                    del self._nodes[node.id]
    
    def list_nodes(self) -> list[Node]:
        return list(self._nodes.values())
    
    def get_node_by_id(self, node_id: Union[str, int, uuid.UUID], get_copy: bool = False) -> Optional[Node]:
        node = None
        if node_id in self._nodes:
            node = self._nodes[node_id] if not(get_copy) else deepcopy(self._nodes[node_id])
        return node

    def add_edges(self, *edges: Type[Edge]) -> None:
        if not self.check_edge_exist(*edges):
            for edge in edges:
                self._edges[edge.id] = edge
                self._nodes[edge.from_node.id].connected_edges.append(edge)
                if edge.is_bidirectional:
                    self._nodes[edge.to_node.id].connected_edges.append(edge)
    
    def create_edge(
            self,
            from_node: Node,
            to_node: Node,
            edge_id: Union[str, int, uuid.UUID] = uuid.uuid4(),
            is_bidirectional: bool = False,
            weighted_value: Optional[Union[int, float, Decimal]] = 0
        ) -> None:
        edge = Edge(
            id=edge_id, from_node=from_node, to_node=to_node,
            is_bidirectional=is_bidirectional, weighted_value=weighted_value)
        self.add_edges(edge)
    
    def remove_edges(self, *edges: Type[Edge]) -> None:
        if self.check_edge_exist(*edges):
            for edge in edges:
                self._nodes[edge.from_node.id].connected_edges.remove(edge)
                if edge.is_bidirectional:
                    self._nodes[edge.to_node.id].connected_edges.remove(edge)
                del self._edges[edge.id]
    
    def list_edges(self) -> list[Edge]:
        return list(self._edges.values())
    
    def get_edge_by_id(self, edge_id: Union[str, int, uuid.UUID], get_copy: bool = False) -> Optional[Edge]:
        edge = None
        if edge_id in self._edges:
            edge = self._edges[edge_id] if not(get_copy) else deepcopy(self._edges[edge_id])
        return edge
        
    def export_graph(self, export_file_location: str) -> None:
        pass

    @classmethod
    def import_graph(cls, graph_file_location: str) -> None:
        pass

    def check_node_exist(self, *nodes: Node) -> bool:
        for node in nodes:
            if node.id not in self._nodes:
                return False
        return True
    
    def check_edge_exist(self, *edges: Edge) -> bool:
        for edge in edges:
            if edge.id not in self._edges:
                return False
        return True

if __name__ == "__main__":
    print("New One")
    G = Graph()
    alpha = Node(id="Alpha")
    beta = Node(id="Beta")
    gamma = Node(id="Gamma")
    G.add_nodes(alpha, beta, gamma)
    G.create_node("Delta")
    edge1 = Edge(from_node=alpha, to_node=beta)
    edge2 = Edge(from_node=beta, to_node=gamma, is_bidirectional=True)
    G.add_edges(edge1, edge2)
    G.create_edge(from_node=gamma, to_node=alpha, weighted_value=5)
    print(G.list_nodes())
    print()
    print(G.list_edges())
    print()
    A = G.get_node_by_id("Alpha")
    print(A)

    