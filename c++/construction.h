#pragma once
#include "solution.h"

Solution construct_randomized_greedy(
    Edgelist* edgelist,
    __int128_t n, __int128_t k, __int128_t L, __int128_t M, float alpha
);
void add_loopback_edge(
    Edgelist* edgelist,
    Solution& solution,
    __int128_t driver
);
__int128_t find_inner_vertex(const Solution& solution, Edge edge);