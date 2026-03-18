// dist02_load_balancing.rs
//
// Load Balancing distributes incoming requests across multiple servers to
// optimize resource utilization, minimize response time, and avoid overload.
//
// Common algorithms:
// - Round Robin: Distribute requests sequentially across servers
// - Weighted Round Robin: Assign more requests to more capable servers
// - Least Connections: Route to server with fewest active connections
// - Weighted Least Connections: Combine connection count with server capacity
//
// Your task: Implement multiple load balancing strategies.
//
// Key concepts:
// - Server health and availability
// - Connection tracking
// - Fair distribution vs. optimal distribution
// - Server weights/capacity

// I AM NOT DONE

use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub struct Server {
    pub id: usize,
    pub weight: usize,          // Capacity weight (higher = more capable)
    pub active_connections: usize,
    pub total_requests: usize,
    pub is_healthy: bool,
}

impl Server {
    pub fn new(id: usize, weight: usize) -> Self {
        Self {
            id,
            weight,
            active_connections: 0,
            total_requests: 0,
            is_healthy: true,
        }
    }

    pub fn add_connection(&mut self) {
        self.active_connections += 1;
        self.total_requests += 1;
    }

    pub fn remove_connection(&mut self) {
        if self.active_connections > 0 {
            self.active_connections -= 1;
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum LoadBalancingStrategy {
    RoundRobin,
    WeightedRoundRobin,
    LeastConnections,
    WeightedLeastConnections,
}

pub struct LoadBalancer {
    servers: Vec<Server>,
    strategy: LoadBalancingStrategy,
    round_robin_index: usize,
    weighted_rr_counter: HashMap<usize, usize>, // Track weighted distribution
}

impl LoadBalancer {
    pub fn new(strategy: LoadBalancingStrategy) -> Self {
        Self {
            servers: Vec::new(),
            strategy,
            round_robin_index: 0,
            weighted_rr_counter: HashMap::new(),
        }
    }

    pub fn add_server(&mut self, server: Server) {
        self.weighted_rr_counter.insert(server.id, 0);
        self.servers.push(server);
    }

    pub fn mark_server_unhealthy(&mut self, server_id: usize) {
        if let Some(server) = self.servers.iter_mut().find(|s| s.id == server_id) {
            server.is_healthy = false;
        }
    }

    pub fn mark_server_healthy(&mut self, server_id: usize) {
        if let Some(server) = self.servers.iter_mut().find(|s| s.id == server_id) {
            server.is_healthy = true;
        }
    }

    fn get_healthy_servers(&self) -> Vec<usize> {
        self.servers
            .iter()
            .enumerate()
            .filter(|(_, s)| s.is_healthy)
            .map(|(i, _)| i)
            .collect()
    }

    fn select_round_robin(&mut self) -> Option<usize> {
        // TODO: Implement round robin selection
        // - Find next healthy server starting from round_robin_index
        // - Update round_robin_index for next call
        // - Return server ID (not index)
        // - Return None if no healthy servers
        todo!()
    }

    fn select_weighted_round_robin(&mut self) -> Option<usize> {
        // TODO: Implement weighted round robin selection
        // - Each server should receive requests proportional to its weight
        // - For example, servers with weights [1, 2, 3] should receive
        //   requests in ratio 1:2:3
        // - Use weighted_rr_counter to track distribution
        // - Return server ID (not index)
        // - Return None if no healthy servers
        todo!()
    }

    fn select_least_connections(&self) -> Option<usize> {
        // TODO: Implement least connections selection
        // - Find healthy server with minimum active_connections
        // - If tie, choose the one with lower ID
        // - Return server ID (not index)
        // - Return None if no healthy servers
        todo!()
    }

    fn select_weighted_least_connections(&self) -> Option<usize> {
        // TODO: Implement weighted least connections selection
        // - Find healthy server with minimum (active_connections / weight) ratio
        // - This balances load relative to server capacity
        // - If tie, choose the one with lower ID
        // - Return server ID (not index)
        // - Return None if no healthy servers
        todo!()
    }

    pub fn select_server(&mut self) -> Option<usize> {
        match self.strategy {
            LoadBalancingStrategy::RoundRobin => self.select_round_robin(),
            LoadBalancingStrategy::WeightedRoundRobin => self.select_weighted_round_robin(),
            LoadBalancingStrategy::LeastConnections => self.select_least_connections(),
            LoadBalancingStrategy::WeightedLeastConnections => self.select_weighted_least_connections(),
        }
    }

    pub fn handle_request(&mut self) -> Option<usize> {
        // TODO: Select a server and add a connection to it
        // Return the server ID
        todo!()
    }

    pub fn complete_request(&mut self, server_id: usize) {
        // TODO: Remove a connection from the specified server
        todo!()
    }

    pub fn get_server(&self, server_id: usize) -> Option<&Server> {
        self.servers.iter().find(|s| s.id == server_id)
    }

    pub fn get_server_stats(&self) -> Vec<ServerStats> {
        self.servers
            .iter()
            .map(|s| ServerStats {
                server_id: s.id,
                weight: s.weight,
                active_connections: s.active_connections,
                total_requests: s.total_requests,
                is_healthy: s.is_healthy,
            })
            .collect()
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct ServerStats {
    pub server_id: usize,
    pub weight: usize,
    pub active_connections: usize,
    pub total_requests: usize,
    pub is_healthy: bool,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_round_robin_basic() {
        let mut lb = LoadBalancer::new(LoadBalancingStrategy::RoundRobin);
        lb.add_server(Server::new(0, 1));
        lb.add_server(Server::new(1, 1));
        lb.add_server(Server::new(2, 1));

        // Should cycle through servers
        assert_eq!(lb.select_server(), Some(0));
        assert_eq!(lb.select_server(), Some(1));
        assert_eq!(lb.select_server(), Some(2));
        assert_eq!(lb.select_server(), Some(0));
    }

    #[test]
    fn test_round_robin_skip_unhealthy() {
        let mut lb = LoadBalancer::new(LoadBalancingStrategy::RoundRobin);
        lb.add_server(Server::new(0, 1));
        lb.add_server(Server::new(1, 1));
        lb.add_server(Server::new(2, 1));

        lb.mark_server_unhealthy(1);

        // Should skip server 1
        assert_eq!(lb.select_server(), Some(0));
        assert_eq!(lb.select_server(), Some(2));
        assert_eq!(lb.select_server(), Some(0));
    }

    #[test]
    fn test_weighted_round_robin() {
        let mut lb = LoadBalancer::new(LoadBalancingStrategy::WeightedRoundRobin);
        lb.add_server(Server::new(0, 1));
        lb.add_server(Server::new(1, 2));

        // Collect 12 selections
        let mut selections = Vec::new();
        for _ in 0..12 {
            selections.push(lb.select_server().unwrap());
        }

        // Count occurrences
        let count_0 = selections.iter().filter(|&&id| id == 0).count();
        let count_1 = selections.iter().filter(|&&id| id == 1).count();

        // Should be roughly 1:2 ratio (4:8 in 12 requests)
        assert_eq!(count_0, 4);
        assert_eq!(count_1, 8);
    }

    #[test]
    fn test_least_connections_basic() {
        let mut lb = LoadBalancer::new(LoadBalancingStrategy::LeastConnections);
        lb.add_server(Server::new(0, 1));
        lb.add_server(Server::new(1, 1));

        // First request goes to server 0 (both have 0 connections, choose lower ID)
        let server = lb.handle_request().unwrap();
        assert_eq!(server, 0);

        // Second request should go to server 1 (has fewer connections)
        let server = lb.handle_request().unwrap();
        assert_eq!(server, 1);
    }

    #[test]
    fn test_least_connections_balancing() {
        let mut lb = LoadBalancer::new(LoadBalancingStrategy::LeastConnections);
        lb.add_server(Server::new(0, 1));
        lb.add_server(Server::new(1, 1));

        // Add 2 connections to server 0
        lb.handle_request();
        lb.handle_request();

        // Complete one request from server 0
        lb.complete_request(0);

        // Server 0 has 1 connection, server 1 has 0
        // Next should go to server 1
        let server = lb.select_server().unwrap();
        assert_eq!(server, 1);
    }

    #[test]
    fn test_weighted_least_connections() {
        let mut lb = LoadBalancer::new(LoadBalancingStrategy::WeightedLeastConnections);
        lb.add_server(Server::new(0, 1)); // Lower capacity
        lb.add_server(Server::new(1, 3)); // Higher capacity

        // Send requests
        for _ in 0..8 {
            lb.handle_request();
        }

        let stats = lb.get_server_stats();
        let s0 = stats.iter().find(|s| s.server_id == 0).unwrap();
        let s1 = stats.iter().find(|s| s.server_id == 1).unwrap();

        // Server 1 should handle more requests due to higher weight
        assert!(s1.active_connections > s0.active_connections);
    }

    #[test]
    fn test_no_healthy_servers() {
        let mut lb = LoadBalancer::new(LoadBalancingStrategy::RoundRobin);
        lb.add_server(Server::new(0, 1));
        lb.add_server(Server::new(1, 1));

        lb.mark_server_unhealthy(0);
        lb.mark_server_unhealthy(1);

        assert_eq!(lb.select_server(), None);
    }

    #[test]
    fn test_server_recovery() {
        let mut lb = LoadBalancer::new(LoadBalancingStrategy::RoundRobin);
        lb.add_server(Server::new(0, 1));
        lb.add_server(Server::new(1, 1));

        lb.mark_server_unhealthy(1);
        assert_eq!(lb.select_server(), Some(0));

        lb.mark_server_healthy(1);
        assert_eq!(lb.select_server(), Some(0));
        assert_eq!(lb.select_server(), Some(1));
    }

    #[test]
    fn test_connection_tracking() {
        let mut lb = LoadBalancer::new(LoadBalancingStrategy::RoundRobin);
        lb.add_server(Server::new(0, 1));

        lb.handle_request();
        lb.handle_request();

        let server = lb.get_server(0).unwrap();
        assert_eq!(server.active_connections, 2);
        assert_eq!(server.total_requests, 2);

        lb.complete_request(0);
        let server = lb.get_server(0).unwrap();
        assert_eq!(server.active_connections, 1);
        assert_eq!(server.total_requests, 2); // Total doesn't decrease
    }

    #[test]
    fn test_weighted_distribution_fairness() {
        let mut lb = LoadBalancer::new(LoadBalancingStrategy::WeightedRoundRobin);
        lb.add_server(Server::new(0, 1));
        lb.add_server(Server::new(1, 2));
        lb.add_server(Server::new(2, 3));

        // Send 60 requests (divisible by 1+2+3=6)
        let mut distribution = HashMap::new();
        for _ in 0..60 {
            let server_id = lb.select_server().unwrap();
            *distribution.entry(server_id).or_insert(0) += 1;
        }

        // Should distribute in ratio 1:2:3 = 10:20:30
        assert_eq!(distribution.get(&0), Some(&10));
        assert_eq!(distribution.get(&1), Some(&20));
        assert_eq!(distribution.get(&2), Some(&30));
    }

    #[test]
    fn test_statistics() {
        let mut lb = LoadBalancer::new(LoadBalancingStrategy::RoundRobin);
        lb.add_server(Server::new(0, 2));
        lb.add_server(Server::new(1, 3));

        lb.handle_request();
        lb.handle_request();

        let stats = lb.get_server_stats();
        assert_eq!(stats.len(), 2);

        let s0_stats = stats.iter().find(|s| s.server_id == 0).unwrap();
        assert_eq!(s0_stats.weight, 2);
        assert!(s0_stats.is_healthy);
    }

    #[test]
    fn test_least_connections_tie_breaking() {
        let mut lb = LoadBalancer::new(LoadBalancingStrategy::LeastConnections);
        lb.add_server(Server::new(5, 1));
        lb.add_server(Server::new(3, 1));
        lb.add_server(Server::new(7, 1));

        // All have 0 connections, should choose lowest ID (3)
        let server = lb.select_server().unwrap();
        assert_eq!(server, 3);
    }
}
