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
    source_node: Node
    destination_node: Node
    is_bidirectional: bool = False
    weighted_value: Optional[Union[int, float, Decimal]] = 0

class Graph:

    def __init__(self) -> None:
        """Initialises an empty graph."""
        self._nodes: dict[Union[str, int], Node] = {}
        self._edges: dict[int, Edge] = {}
    
    def add_nodes(self, *nodes: Type[Node]) -> None:
        """Adds one or more nodes to the graph.

        Args:
            *nodes (Type[Node]): Nodes to be added to the graph.
        
        Returns:
            None
        """
        if not self.check_node_exist(*nodes):
            for node in nodes:
                self._nodes[node.id] = node
    
    def create_node(
            self,
            new_node_id: Union[str, int, uuid.UUID] = uuid.uuid4(),
            initial_edges: list[Edge] = [],
            additional_parameters: Optional[Any] = None
        ) -> None:
        """Creates a Node object and adds it to the graph.
        
        Args:
            new_node_id (Union[str, int, uuid.UUID]): Unique identifier for a node in the graph.
            initial_edges (list[Edge]): List of edges that connect to the new node being created.
            additional_parameters (Optional[Any]): Additional properties to apply to a node being created.
        
        Returns:
            None
        """
        node = Node(id=new_node_id, connected_edges=initial_edges, additional_parameters=additional_parameters)
        self.add_nodes(node)  
    
    def remove_node(self, *nodes: Type[Node]) -> None:
        """Removes one or more nodes from the graph.
        
        Args:
            *nodes (Type[node]): Nodes to be removed from the graph.
        
        Returns:
            None
        """
        if self.check_node_exist(*nodes):
            for node in nodes:
                if node.id in self._nodes:
                    del self._nodes[node.id]
    
    def list_nodes(self) -> list[Node]:
        """Returns a list of all the nodes in the graph.
        
        Returns:
            list[Node]: A list of nodes in the graph.
        """
        return list(self._nodes.values())
    
    def get_node_by_id(
            self,
            node_id: Union[str, int, uuid.UUID],
            get_copy: bool = False
        ) -> Optional[Node]:
        """Returns a node instance of the node with the specified node_id, or returns None if the node does not exist in the graph.
        
        Args:
            node_id (Union[str, int, uuid.UUID]): Unique identifier to identify which node to return from the graph.
            get_copy (bool): Boolean value that will return the node as a reference if False and as a copy if True.
        
        Returns:
            Optional[Node]: Returns the node from the graph with the specified ID. Otherwise, returns None.
        """
        node = None
        if node_id in self._nodes:
            node = self._nodes[node_id] if not(get_copy) else deepcopy(self._nodes[node_id])
        return node

    def add_edges(self, *edges: Type[Edge]) -> None:
        """Adds one or more edges to the graph.
        
        Args:
            *edges (Tuple[Edge]): Edges to be added to the graph.
        
        Returns:
            None
        """
        if not self.check_edge_exist(*edges):
            for edge in edges:
                self._edges[edge.id] = edge
                self._nodes[edge.source_node.id].connected_edges.append(edge)
                if edge.is_bidirectional:
                    self._nodes[edge.destination_node.id].connected_edges.append(edge)
    
    def create_edge(
            self,
            source_node: Node,
            destination_node: Node,
            edge_id: Union[str, int, uuid.UUID] = uuid.uuid4(),
            is_bidirectional: bool = False,
            weighted_value: Optional[Union[int, float, Decimal]] = 0
        ) -> None:
        """Creates an Edge object between 2 nodes and adds it to the graph.
        
        Args:
            source_node (Node): The source node of the edge.
            destination_node (Node): The destination node of the edge.
            edge_id (Union[str, int, uuid.UUID]): Unique identifier for an edge in the graph.
            is_bidirectional (bool): Boolean to indicate if the edge is bidirectional.
            weighted_value (Optional[Union[int, float, Decimal]]): The weight/value assigned to an edge.
        
        Returns:
            None
        """
        edge = Edge(
            id=edge_id, source_node=source_node, destination_node=destination_node,
            is_bidirectional=is_bidirectional, weighted_value=weighted_value)
        self.add_edges(edge)
    
    def remove_edges(self, *edges: Type[Edge]) -> None:
        """Removes one or more edges from the graph.
        
        Args:
            *edges (Type[Edge]): Edges to be added to the graph.
        
        Returns:
            None
        """
        if self.check_edge_exist(*edges):
            for edge in edges:
                self._nodes[edge.source_node.id].connected_edges.remove(edge)
                if edge.is_bidirectional:
                    self._nodes[edge.destination_node.id].connected_edges.remove(edge)
                del self._edges[edge.id]
    
    def list_edges(self) -> list[Edge]:
        """Returns a list of all the edges in the graphs.
        
        Returns:
            list[Edge]: A list of edges in the graph.
        """
        return list(self._edges.values())
    
    def get_edge_by_id(
            self,
            edge_id: Union[str, int, uuid.UUID],
            get_copy: bool = False
        ) -> Optional[Edge]:
        """Returns an edge instance of the edge with the specified edge_id, or returns None if the edge does not exist in the graph.
        
        Args:
            edge_id (Union[str, int, uuid.UUID]): Unique identifier to identify which edge to return from the graph.
            get_copy (bool): Boolean value that will return the edge as a reference if False and as a copy if True.

        Returns:
            Optional[Edge]: Returns the edge from thr graph with the specified ID. Otherwise, returns None.
        """
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
        """Returns a boolean indicating if all the nodes specified are present in the graph.
        
        Args:
            *nodes (Node): The nodes to check if exist in the graph.
        
        Returns:
            bool: Returns True if all the nodes specified are present in the graph. Otherwise, returns False.
        """
        for node in nodes:
            if node.id not in self._nodes:
                return False
        return True
    
    def check_edge_exist(self, *edges: Edge) -> bool:
        """Returns a boolean indicating if all the edges specified are present in the graph.
        
        Args:
            *edges (Edge): The edges to check if exist in the graph.
        
        Returns:
            bool: Returns True if all the edges specified are present. Otherwise, returns False.
        """
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
    edge1 = Edge(source_node=alpha, destination_node=beta)
    edge2 = Edge(source_node=beta, destination_node=gamma, is_bidirectional=True)
    G.add_edges(edge1, edge2)
    G.create_edge(source_node=gamma, destination_node=alpha, weighted_value=5)
    print(G.list_nodes())
    print()
    print(G.list_edges())
    print()
    A = G.get_node_by_id("Alpha")
    print(A)

    