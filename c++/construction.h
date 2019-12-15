#pragma once
#include "solution.h"

Solution construct_randomized_greedy(
    Edgelist* edgelist,
    int64_t n, int64_t k, int64_t L, int64_t M, float alpha
);
void add_loopback_edge(
    Edgelist* edgelist,
    Solution& solution,
    int64_t driver
);
int64_t find_inner_vertex(const Solution& solution, Edge edge);