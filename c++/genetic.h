#pragma once
#include "solution.h"
#include "construction.h"

using Population = std::vector<Solution>;

Population init_population(
    Edgelist* edgelist,
    __int128_t n,
    __int128_t k,
    __int128_t L,
    __int128_t M,
    double alpha,
    __int128_t size
);
Population do_selection(Population p, __int128_t n, double factor);
Population recombine(Edgelist* edgelist, Population p, double alpha=0.8);
Population cross(Edgelist* edgelist, const Solution& spec1, const Solution& spec2);
std::vector<__int128_t> get_order(const Solution& specimen, __int128_t i, __int128_t j);
void rearrange_by_order(Edgelist* edgelist, Solution& specimen, const Solution& sample,
    std::vector<__int128_t> order, __int128_t i, __int128_t j);
Population mutate(Edgelist* edgelist, Population p);
Solution mutate_specimen(Edgelist* edgelist, const Solution& specimen);
Population genetic_algorithm(
    Edgelist* edgelist,
    __int128_t n,
    __int128_t k,
    __int128_t L,
    __int128_t M,
    double alpha,
    __int128_t p_size, 
    double sel_factor,
    __int128_t iterations=100);
