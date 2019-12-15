

#pragma once
#include <vector>
#include <cstdint>
#include <iostream>

std::ostream& debug();

using Edgelist = std::vector<std::vector<int64_t>>;

struct Driver {
    int64_t obj_squared;
    int64_t obj;

    Driver(int64_t L);
};

struct Edge {
    int64_t u;
    int64_t v;
    int64_t driver;
    int64_t w;

    Edge(int64_t u, int64_t v, int64_t d, int64_t w);
    void update_weight(Edgelist* edgelist);
    bool operator<(const Edge& other) const;
};

struct Chain {
    std::vector<Edge> edges;

    Chain(int64_t n, Edge e);
    Chain(const Chain& other);
};

struct Solution {
    std::vector<Chain> chains;
    int64_t num_edges;
    std::vector<Driver> drivers;
    int64_t L;
    int64_t obj;
    int64_t n;

    Solution(int64_t k, int64_t L, int64_t n);
    Solution(const Solution& other);
    Solution& operator=(const Solution& other);
    bool operator<(const Solution& other);
    bool insert_edge(Edge edge);
    bool find_chains(Edge edge, std::pair<int64_t, int64_t>& chains) const;
    void merge_chains(int64_t ch1, int64_t ch2, Edge edge);
    void reverse_chain(int64_t ch);
    bool add_chain_edge(int64_t ch, Edge edge);
    void add_loopback_edge(Edge edge);
    bool can_edge_be_added(Edge edge) const;
    int64_t calculate_objective_with_edge(Edge edge) const;
    void update_objective(std::vector<std::pair<int64_t, int64_t>> driver_map);
};

std::ostream& operator<<(std::ostream& out, const Solution& sol);
std::ostream& operator<<(std::ostream& out, const Chain& ch);
std::ostream& operator<<(std::ostream& out, const Edge& e);