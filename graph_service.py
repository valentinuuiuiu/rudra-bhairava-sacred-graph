class GraphService:
    """
    Service for managing graph operations and algorithms
    """
    
    def __init__(self):
        self.graphs = {}  # Stores graph instances by id
        
    def create_graph(self, graph_id, graph_type='undirected'):
        """
        Create a new graph with given id and type
        Args:
            graph_id: Unique identifier for the graph
            graph_type: 'directed' or 'undirected' (default)
        Returns:
            The created graph instance
        """
        graph = {'id': graph_id, 'type': graph_type, 'nodes': {}, 'edges': []}
        self.graphs[graph_id] = graph
        return graph
        
    def add_node(self, graph_id, node_id, data=None):
        """
        Add a node to the specified graph
        Args:
            graph_id: ID of the graph
            node_id: Unique node identifier
            data: Optional node data
        """
        if graph_id not in self.graphs:
            raise ValueError(f"Graph {graph_id} not found")
            
        self.graphs[graph_id]['nodes'][node_id] = data or {}
        
    def add_edge(self, graph_id, source, target, weight=1):
        """
        Add an edge between two nodes
        Args:
            graph_id: ID of the graph
            source: Source node ID
            target: Target node ID
            weight: Edge weight (default 1)
        """
        if graph_id not in self.graphs:
            raise ValueError(f"Graph {graph_id} not found")
            
        graph = self.graphs[graph_id]
        if source not in graph['nodes'] or target not in graph['nodes']:
            raise ValueError("Source or target node not found")
            
        edge = {'source': source, 'target': target, 'weight': weight}
        graph['edges'].append(edge)
        
        if graph['type'] == 'undirected':
            reverse_edge = {'source': target, 'target': source, 'weight': weight}
            graph['edges'].append(reverse_edge)
            
    def get_shortest_path(self, graph_id, source, target):
        """
        Get shortest path between two nodes using Dijkstra's algorithm
        Args:
            graph_id: ID of the graph
            source: Starting node
            target: Destination node
        Returns:
            List of nodes representing the shortest path
        """
        # TODO: Implement Dijkstra's algorithm
        pass
        
    def get_graph_stats(self, graph_id):
        """
        Get statistics about the graph
        Args:
            graph_id: ID of the graph
        Returns:
            Dictionary with graph statistics
        """
        if graph_id not in self.graphs:
            raise ValueError(f"Graph {graph_id} not found")
            
        graph = self.graphs[graph_id]
        return {
            'node_count': len(graph['nodes']),
            'edge_count': len(graph['edges']),
            'density': self._calculate_density(graph)
        }
        
    def _calculate_density(self, graph):
        """Helper method to calculate graph density"""
        n = len(graph['nodes'])
        if n < 2:
            return 0
            
        max_edges = n * (n - 1)
        if graph['type'] == 'undirected':
            max_edges = max_edges // 2
            
        return len(graph['edges']) / max_edges