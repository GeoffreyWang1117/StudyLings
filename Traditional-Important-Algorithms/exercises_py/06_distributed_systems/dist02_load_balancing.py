# I AM NOT DONE

"""
dist02_load_balancing.py

Load Balancing distributes incoming requests across multiple servers to
optimize resource utilization, minimize response time, and avoid overload.

Common algorithms:
- Round Robin: Distribute requests sequentially across servers
- Weighted Round Robin: Assign more requests to more capable servers
- Least Connections: Route to server with fewest active connections
- Weighted Least Connections: Combine connection count with server capacity

Your task: Implement multiple load balancing strategies.

Key concepts:
- Server health and availability
- Connection tracking
- Fair distribution vs. optimal distribution
- Server weights/capacity
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional
import unittest


class LoadBalancingStrategy(Enum):
    """Load balancing strategy types."""
    ROUND_ROBIN = auto()
    WEIGHTED_ROUND_ROBIN = auto()
    LEAST_CONNECTIONS = auto()
    WEIGHTED_LEAST_CONNECTIONS = auto()


@dataclass
class Server:
    """Server representation."""
    id: int
    weight: int
    active_connections: int = 0
    total_requests: int = 0
    is_healthy: bool = True

    def add_connection(self):
        """Add a connection to this server."""
        self.active_connections += 1
        self.total_requests += 1

    def remove_connection(self):
        """Remove a connection from this server."""
        if self.active_connections > 0:
            self.active_connections -= 1


@dataclass
class ServerStats:
    """Statistics for a server."""
    server_id: int
    weight: int
    active_connections: int
    total_requests: int
    is_healthy: bool


class LoadBalancer:
    """Load balancer implementing multiple strategies."""

    def __init__(self, strategy: LoadBalancingStrategy):
        """Initialize load balancer with a strategy."""
        self.servers: List[Server] = []
        self.strategy = strategy
        self.round_robin_index = 0
        self.weighted_rr_counter: Dict[int, int] = {}

    def add_server(self, server: Server):
        """Add a server to the load balancer."""
        self.weighted_rr_counter[server.id] = 0
        self.servers.append(server)

    def mark_server_unhealthy(self, server_id: int):
        """Mark a server as unhealthy."""
        for server in self.servers:
            if server.id == server_id:
                server.is_healthy = False
                break

    def mark_server_healthy(self, server_id: int):
        """Mark a server as healthy."""
        for server in self.servers:
            if server.id == server_id:
                server.is_healthy = True
                break

    def _get_healthy_servers(self) -> List[int]:
        """Get indices of healthy servers."""
        return [i for i, s in enumerate(self.servers) if s.is_healthy]

    def _select_round_robin(self) -> Optional[int]:
        """
        TODO: Implement round robin selection.

        - Find next healthy server starting from round_robin_index
        - Update round_robin_index for next call
        - Return server ID (not index)
        - Return None if no healthy servers
        """
        pass  # TODO: Implement this

    def _select_weighted_round_robin(self) -> Optional[int]:
        """
        TODO: Implement weighted round robin selection.

        - Each server should receive requests proportional to its weight
        - For example, servers with weights [1, 2, 3] should receive
          requests in ratio 1:2:3
        - Use weighted_rr_counter to track distribution
        - Return server ID (not index)
        - Return None if no healthy servers
        """
        pass  # TODO: Implement this

    def _select_least_connections(self) -> Optional[int]:
        """
        TODO: Implement least connections selection.

        - Find healthy server with minimum active_connections
        - If tie, choose the one with lower ID
        - Return server ID (not index)
        - Return None if no healthy servers
        """
        pass  # TODO: Implement this

    def _select_weighted_least_connections(self) -> Optional[int]:
        """
        TODO: Implement weighted least connections selection.

        - Find healthy server with minimum (active_connections / weight) ratio
        - This balances load relative to server capacity
        - If tie, choose the one with lower ID
        - Return server ID (not index)
        - Return None if no healthy servers
        """
        pass  # TODO: Implement this

    def select_server(self) -> Optional[int]:
        """Select a server based on the configured strategy."""
        if self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            return self._select_round_robin()
        elif self.strategy == LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN:
            return self._select_weighted_round_robin()
        elif self.strategy == LoadBalancingStrategy.LEAST_CONNECTIONS:
            return self._select_least_connections()
        elif self.strategy == LoadBalancingStrategy.WEIGHTED_LEAST_CONNECTIONS:
            return self._select_weighted_least_connections()

    def handle_request(self) -> Optional[int]:
        """
        TODO: Select a server and add a connection to it.

        Return the server ID.
        """
        pass  # TODO: Implement this

    def complete_request(self, server_id: int):
        """
        TODO: Remove a connection from the specified server.
        """
        pass  # TODO: Implement this

    def get_server(self, server_id: int) -> Optional[Server]:
        """Get a server by ID."""
        for server in self.servers:
            if server.id == server_id:
                return server
        return None

    def get_server_stats(self) -> List[ServerStats]:
        """Get statistics for all servers."""
        return [
            ServerStats(
                server_id=s.id,
                weight=s.weight,
                active_connections=s.active_connections,
                total_requests=s.total_requests,
                is_healthy=s.is_healthy
            )
            for s in self.servers
        ]


# Unit Tests
class TestLoadBalancing(unittest.TestCase):

    def test_round_robin_basic(self):
        lb = LoadBalancer(LoadBalancingStrategy.ROUND_ROBIN)
        lb.add_server(Server(0, 1))
        lb.add_server(Server(1, 1))
        lb.add_server(Server(2, 1))

        # Should cycle through servers
        self.assertEqual(lb.select_server(), 0)
        self.assertEqual(lb.select_server(), 1)
        self.assertEqual(lb.select_server(), 2)
        self.assertEqual(lb.select_server(), 0)

    def test_round_robin_skip_unhealthy(self):
        lb = LoadBalancer(LoadBalancingStrategy.ROUND_ROBIN)
        lb.add_server(Server(0, 1))
        lb.add_server(Server(1, 1))
        lb.add_server(Server(2, 1))

        lb.mark_server_unhealthy(1)

        # Should skip server 1
        self.assertEqual(lb.select_server(), 0)
        self.assertEqual(lb.select_server(), 2)
        self.assertEqual(lb.select_server(), 0)

    def test_weighted_round_robin(self):
        lb = LoadBalancer(LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN)
        lb.add_server(Server(0, 1))
        lb.add_server(Server(1, 2))

        # Collect 12 selections
        selections = []
        for _ in range(12):
            selections.append(lb.select_server())

        # Count occurrences
        count_0 = selections.count(0)
        count_1 = selections.count(1)

        # Should be roughly 1:2 ratio (4:8 in 12 requests)
        self.assertEqual(count_0, 4)
        self.assertEqual(count_1, 8)

    def test_least_connections_basic(self):
        lb = LoadBalancer(LoadBalancingStrategy.LEAST_CONNECTIONS)
        lb.add_server(Server(0, 1))
        lb.add_server(Server(1, 1))

        # First request goes to server 0 (both have 0 connections, choose lower ID)
        server = lb.handle_request()
        self.assertEqual(server, 0)

        # Second request should go to server 1 (has fewer connections)
        server = lb.handle_request()
        self.assertEqual(server, 1)

    def test_least_connections_balancing(self):
        lb = LoadBalancer(LoadBalancingStrategy.LEAST_CONNECTIONS)
        lb.add_server(Server(0, 1))
        lb.add_server(Server(1, 1))

        # Add 2 connections to server 0
        lb.handle_request()
        lb.handle_request()

        # Complete one request from server 0
        lb.complete_request(0)

        # Server 0 has 1 connection, server 1 has 0
        # Next should go to server 1
        server = lb.select_server()
        self.assertEqual(server, 1)

    def test_weighted_least_connections(self):
        lb = LoadBalancer(LoadBalancingStrategy.WEIGHTED_LEAST_CONNECTIONS)
        lb.add_server(Server(0, 1))  # Lower capacity
        lb.add_server(Server(1, 3))  # Higher capacity

        # Send requests
        for _ in range(8):
            lb.handle_request()

        stats = lb.get_server_stats()
        s0 = next(s for s in stats if s.server_id == 0)
        s1 = next(s for s in stats if s.server_id == 1)

        # Server 1 should handle more requests due to higher weight
        self.assertGreater(s1.active_connections, s0.active_connections)

    def test_no_healthy_servers(self):
        lb = LoadBalancer(LoadBalancingStrategy.ROUND_ROBIN)
        lb.add_server(Server(0, 1))
        lb.add_server(Server(1, 1))

        lb.mark_server_unhealthy(0)
        lb.mark_server_unhealthy(1)

        self.assertIsNone(lb.select_server())

    def test_server_recovery(self):
        lb = LoadBalancer(LoadBalancingStrategy.ROUND_ROBIN)
        lb.add_server(Server(0, 1))
        lb.add_server(Server(1, 1))

        lb.mark_server_unhealthy(1)
        self.assertEqual(lb.select_server(), 0)

        lb.mark_server_healthy(1)
        self.assertEqual(lb.select_server(), 0)
        self.assertEqual(lb.select_server(), 1)

    def test_connection_tracking(self):
        lb = LoadBalancer(LoadBalancingStrategy.ROUND_ROBIN)
        lb.add_server(Server(0, 1))

        lb.handle_request()
        lb.handle_request()

        server = lb.get_server(0)
        self.assertEqual(server.active_connections, 2)
        self.assertEqual(server.total_requests, 2)

        lb.complete_request(0)
        server = lb.get_server(0)
        self.assertEqual(server.active_connections, 1)
        self.assertEqual(server.total_requests, 2)  # Total doesn't decrease

    def test_weighted_distribution_fairness(self):
        lb = LoadBalancer(LoadBalancingStrategy.WEIGHTED_ROUND_ROBIN)
        lb.add_server(Server(0, 1))
        lb.add_server(Server(1, 2))
        lb.add_server(Server(2, 3))

        # Send 60 requests (divisible by 1+2+3=6)
        distribution = {}
        for _ in range(60):
            server_id = lb.select_server()
            distribution[server_id] = distribution.get(server_id, 0) + 1

        # Should distribute in ratio 1:2:3 = 10:20:30
        self.assertEqual(distribution.get(0), 10)
        self.assertEqual(distribution.get(1), 20)
        self.assertEqual(distribution.get(2), 30)

    def test_statistics(self):
        lb = LoadBalancer(LoadBalancingStrategy.ROUND_ROBIN)
        lb.add_server(Server(0, 2))
        lb.add_server(Server(1, 3))

        lb.handle_request()
        lb.handle_request()

        stats = lb.get_server_stats()
        self.assertEqual(len(stats), 2)

        s0_stats = next(s for s in stats if s.server_id == 0)
        self.assertEqual(s0_stats.weight, 2)
        self.assertTrue(s0_stats.is_healthy)

    def test_least_connections_tie_breaking(self):
        lb = LoadBalancer(LoadBalancingStrategy.LEAST_CONNECTIONS)
        lb.add_server(Server(5, 1))
        lb.add_server(Server(3, 1))
        lb.add_server(Server(7, 1))

        # All have 0 connections, should choose lowest ID (3)
        server = lb.select_server()
        self.assertEqual(server, 3)


if __name__ == '__main__':
    unittest.main()
