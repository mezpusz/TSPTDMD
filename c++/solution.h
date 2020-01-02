

#pragma once
#include <vector>
#include <cstdint>
#include <iostream>

std::ostream& debug();

inline std::ostream& operator<<(std::ostream& out, __int128_t val) {
    std::string str;
    do {
        int digit = val % 10;
        str = std::to_string(digit) + str;
        val = (val - digit) / 10;
    } while (val != 0);
    out << str;
    return out;
}

using Edgelist = std::vector<std::vector<__int128_t>>;

struct Driver {
    __int128_t obj_squared;
    __int128_t obj;

    Driver(__int128_t L);
};

struct Edge {
    __int128_t u;
    __int128_t v;
    __int128_t driver;
    __int128_t w;

    Edge(__int128_t u, __int128_t v, __int128_t d, __int128_t w);
    void update_weight(Edgelist* edgelist);
    bool operator<(const Edge& other) const;
};

struct Chain {
    std::vector<Edge> edges;

    Chain(__int128_t n, Edge e);
    Chain(const Chain& other);
};

struct Solution {
    std::vector<Chain> chains;
    __int128_t num_edges;
    std::vector<Driver> drivers;
    __int128_t L;
    __int128_t obj;
    __int128_t n;

    Solution(__int128_t k, __int128_t L, __int128_t n);
    bool operator<(const Solution& other) const;
    bool insert_edge(Edge edge);
    bool find_chains(Edge edge, std::pair<__int128_t, __int128_t>& chains) const;
    void merge_chains(__int128_t ch1, __int128_t ch2, Edge edge);
    void reverse_chain(__int128_t ch);
    bool add_chain_edge(__int128_t ch, Edge edge);
    void add_loopback_edge(Edge edge);
    bool can_edge_be_added(Edge edge) const;
    __int128_t calculate_objective_with_edge(Edge edge) const;
    void update_objective(std::vector<std::pair<__int128_t, __int128_t>> driver_map);
};

std::ostream& operator<<(std::ostream& out, const Solution& sol);
std::ostream& operator<<(std::ostream& out, const Chain& ch);
std::ostream& operator<<(std::ostream& out, const Edge& e);