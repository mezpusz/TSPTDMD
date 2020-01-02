#include "genetic.h"
#include "validate.h"
#include "search.h"
#include <algorithm>
#include <cassert>

void validate_population(Edgelist* edgelist, const Population& p) {
    for (const auto& s : p) {
        validate_solution(s, edgelist);
    }
    for (auto i = 1; i < p.size(); i++) {
        assert(p[i-1] < p[i] || p[i-1].obj == p[i].obj);
    }
}

Population init_population(Edgelist* edgelist, __int128_t n,
    __int128_t k, __int128_t L, __int128_t M, double alpha, __int128_t size) {
    Population p;
    for (__int128_t i = 0; i < size; i++) {
        p.push_back(construct_randomized_greedy2(edgelist, n, k, L, M));
    }
    std::sort(p.begin(), p.end());
    return p;
}

Population do_selection(Population p, __int128_t n, double factor) {
    Population s;
    __int128_t last_specimen = std::min(n, (__int128_t)((n*factor)-1));
    for(__int128_t i = 0; i < n; i++) {
        __int128_t j = std::rand() % last_specimen;
        s.push_back(p[j]);
        p.erase(p.begin() + j);
        last_specimen--;
    }
    std::sort(s.begin(), s.end());
    return s;
}

Population recombine(Edgelist* edgelist, Population p, double alpha) {
    __int128_t last_specimen = (__int128_t)((p.size()*alpha)-1);
    for (__int128_t i = 0; i < last_specimen; i++) {
        for (__int128_t j = i+1; j < last_specimen+1; j++) {
            auto children = cross(edgelist, p[i], p[j]);
            // insert into already sorted population
            for (auto& ch : children) {
                p.insert(std::upper_bound(p.begin(), p.end(), ch), ch);
            }
        }
    }
    return p;
}

Population cross(Edgelist* edgelist, const Solution& spec1, const Solution& spec2) {
    Population p;
    p.push_back(spec1);
    p.push_back(spec2);
    __int128_t i = std::rand() % (spec1.num_edges-2);
    __int128_t j = (std::rand() % (spec1.num_edges-i-2)) + (i+1);
    auto order1 = get_order(spec1, i, j);
    auto order2 = get_order(spec2, i, j);
    rearrange_by_order(edgelist, p[0], spec1, order2, i, j);
    rearrange_by_order(edgelist, p[1], spec2, order1, i, j);
    return p;
}

std::vector<__int128_t> get_order(const Solution& specimen, __int128_t i, __int128_t j) {
    std::vector<__int128_t> order(j-i+1);
    for (__int128_t i = 0; i < order.size(); i++) {
        order[i] = i;
    }
    std::sort(order.begin(), order.end(),
        [&specimen, &i](const __int128_t& lhs, const __int128_t& rhs) {
            return specimen.chains[0].edges[lhs+i].u < specimen.chains[0].edges[rhs+i].u;
        });
    return order;
}

void rearrange_by_order(Edgelist* edgelist, Solution& specimen, const Solution& sample,
    std::vector<__int128_t> order, __int128_t i, __int128_t j) {
    std::vector<std::pair<__int128_t, __int128_t>> driver_map;
    std::vector<__int128_t> sorted(j-i+1);
    for (__int128_t i = 0; i < order.size(); i++) {
        sorted[i] = i;
    }
    if (sorted == order) {
        return;
    }
    auto& edges = specimen.chains[0].edges;
    const auto& old_edges = sample.chains[0].edges;
    for(__int128_t k = i; k < j+1; k++) {
        auto new_u = old_edges[order[k-i]+i].u;
        __int128_t prev = (k==0) ? edges.size()-1 : k-1;
        auto new_w = edgelist->at(edges[prev].u)[new_u];
        auto old_w = edgelist->at(old_edges[prev].u)[old_edges[prev].v];
        driver_map.push_back(std::make_pair(edges[prev].driver, new_w-old_w));
        edges[prev].v = new_u;
        edges[prev].update_weight(edgelist);
        edges[k].u = new_u;
    }
    edges[j].update_weight(edgelist);
    auto new_w = edgelist->at(edges[j].u)[edges[j].v];
    auto old_w = edgelist->at(old_edges[j].u)[old_edges[j].v];
    driver_map.push_back(std::make_pair(edges[j].driver, new_w-old_w));
    specimen.update_objective(driver_map);
    // validate_solution(specimen, edgelist);
}

Population mutate(Edgelist* edgelist, Population p) {
    Population m;
    for(const auto& s : p) {
        m.push_back(mutate_specimen(edgelist, s));
    }
    std::sort(m.begin(), m.end());
    return m;
}

Solution mutate_specimen(Edgelist* edgelist, const Solution& specimen) {
    Solution new_s = specimen;
    __int128_t i = std::rand() % (new_s.num_edges-2);
    __int128_t j = (std::rand() % (new_s.num_edges-i-2)) + (i+1);
    auto& edges = new_s.chains[0].edges;
    const auto& old_edges = specimen.chains[0].edges;
    __int128_t prev = (i==0) ? edges.size()-1 : i-1;
    edges[prev].v = old_edges[j].u;
    edges[prev].update_weight(edgelist);
    edges[i].u = old_edges[j].u;
    edges[i].update_weight(edgelist);
    edges[j-1].v = old_edges[i].u;
    edges[j-1].update_weight(edgelist);
    edges[j].u = old_edges[i].u;
    edges[j].update_weight(edgelist);

    std::vector<std::pair<__int128_t, __int128_t>> driver_map;
    driver_map.push_back(std::make_pair(edges[prev].driver, edgelist->at(edges[prev].u)[edges[prev].v]-edgelist->at(old_edges[prev].u)[old_edges[prev].v]));
    driver_map.push_back(std::make_pair(edges[i].driver, edgelist->at(edges[i].u)[edges[i].v]-edgelist->at(old_edges[i].u)[old_edges[i].v]));
    driver_map.push_back(std::make_pair(edges[j-1].driver, edgelist->at(edges[j-1].u)[edges[j-1].v]-edgelist->at(old_edges[j-1].u)[old_edges[j-1].v]));
    driver_map.push_back(std::make_pair(edges[j].driver, edgelist->at(edges[j].u)[edges[j].v]-edgelist->at(old_edges[j].u)[old_edges[j].v]));
    new_s.update_objective(driver_map);
    return new_s;
}

Population genetic_algorithm(
    Edgelist* edgelist,
    __int128_t n,
    __int128_t k,
    __int128_t L,
    __int128_t M,
    double alpha,
    __int128_t p_size, 
    double sel_factor,
    __int128_t iterations)
{
    std::cout << "Starting genetic algorithm" << std::endl;
    auto p = init_population(edgelist, n, k, L, M, alpha, p_size*2);
    // validate_population(edgelist, p);
    for(__int128_t i = 0; i < iterations; i++) {
        p = do_selection(p, p_size, sel_factor);
        // validate_population(edgelist, p);
        p = recombine(edgelist, p);
        // validate_population(edgelist, p);
        p = mutate(edgelist, p);
        validate_population(edgelist, p);
        std::cout << "population best solution is " << p[0].obj << std::endl;
    }
    p = do_selection(p, p_size, sel_factor);
    std::cout << "Refining final population" << std::endl;
    for(auto& s : p) {
        while(true) {
            s = local_search(s, edgelist);
            auto new_sol = make_feasible(edgelist, s, M);
            if (new_sol < s) {
                std::cout << "Found a more feasible solution " << new_sol.obj << std::endl;
                s = new_sol;
            } else {
                break;
            }
        }
    }
    std::sort(p.begin(), p.end());
    validate_population(edgelist, p);
    return p;
}