
#include "neighborhood.h"
#include "validate.h"

void make_reversal(Edgelist* edgelist, Solution& sol, __int128_t i, __int128_t j) {
    auto& edges = sol.chains[0].edges;
    for(__int128_t k = i+1; k < j; k++) {
        std::swap(edges[k].u, edges[k].v);
    }
    for(__int128_t k = i+1; k < j-k+i; k++) {
        std::swap(edges[k], edges[j-k+i]);
    }
    std::swap(edges[i].v, edges[j].u);
    __int128_t i_w = edges[i].w;
    __int128_t j_w = edges[j].w;
    edges[i].update_weight(edgelist);
    edges[j].update_weight(edgelist);

    std::vector<std::pair<__int128_t, __int128_t>> driver_map;
    driver_map.push_back(std::make_pair(edges[i].driver, edges[i].w-i_w));
    driver_map.push_back(std::make_pair(edges[j].driver, edges[j].w-j_w));
    sol.update_objective(driver_map);
}

Reversal::Reversal(Solution& solution, Edgelist* edgelist)
    : solution(&solution), newsol(solution), edgelist(edgelist)
{}

Solution* Reversal::next() {
    if (solution == nullptr) {
        return nullptr;
    }
    __int128_t num_edges = solution->num_edges;
    const auto& orig_edges = solution->chains[0].edges;
    if (j == i + 2 && i > 0) {
        // newsol = *solution;
        // std::cout << *solution << std::endl;
        // std::cout << newsol << std::endl;
        for (__int128_t k = i-1; k < num_edges; k++) {
            newsol.chains[0].edges[k] = solution->chains[0].edges[k];
        }
        // std::cout << newsol << std::endl;
        newsol.drivers = solution->drivers;
        newsol.obj = solution->obj;
    }
    auto& newedges = newsol.chains[0].edges;
    if (j == i + 2) {
        for(__int128_t k = i+1; k < j; k++) {
            std::swap(newedges[k].u, newedges[k].v);
        }
        const auto& v_i = orig_edges[i];
        const auto& v_j = orig_edges[j];
        newedges[i].v = v_j.u;
        newedges[j].u = v_i.v;
        newedges[i].update_weight(edgelist);
        newedges[j].update_weight(edgelist);
        std::vector<std::pair<__int128_t, __int128_t>> driver_map;
        driver_map.push_back(std::make_pair(v_i.driver, newedges[i].w-v_i.w));
        driver_map.push_back(std::make_pair(v_j.driver, newedges[j].w-v_j.w));
        newsol.update_objective(driver_map);
    } else {
        __int128_t k=j-1;
        while (k>i+1) {
            newedges[k] = newedges[k-1];
            k--;
        }
        newedges[i+1] = orig_edges[j-1];
        newedges[i+1].u = orig_edges[j-1].v;
        newedges[i+1].v = orig_edges[j-1].u;
        const auto& v_i = orig_edges[i];
        const auto& v_j = orig_edges[j];
        newsol.obj = solution->obj;
        newsol.drivers = solution->drivers;
        newedges[i].v = v_j.u;
        newedges[j].u = v_i.v;
        newedges[i].update_weight(edgelist);
        newedges[j].update_weight(edgelist);
        std::vector<std::pair<__int128_t, __int128_t>> driver_map;
        driver_map.push_back(std::make_pair(v_i.driver, newedges[i].w-v_i.w));
        driver_map.push_back(std::make_pair(v_j.driver, newedges[j].w-v_j.w));
        newsol.update_objective(driver_map);
    }
    j++;
    if (j == num_edges) {
        i++;
        j = i+2;
        if (i == num_edges - 2) {
            solution = nullptr;
        }
    }
    // validate_solution(newsol, edgelist);
    return &newsol;
}

DriverExchange::DriverExchange(Solution& solution, Edgelist* edgelist)
    : solution(&solution), newsol(solution), edgelist(edgelist)
{}

Solution* DriverExchange::next() {
    if (solution == nullptr) {
        return nullptr;
    }
    auto num_edges = solution->num_edges;
    auto& newedges = newsol.chains[0].edges;
    newsol.drivers = solution->drivers;
    newsol.obj = solution->obj;
    if (i > 0 && j == i+1) {
        newedges[i-1] = solution->chains[0].edges[i-1];
        newedges.back() = solution->chains[0].edges.back();
    } else {
        newedges[i] = solution->chains[0].edges[i];
        newedges[j-1] = solution->chains[0].edges[j-1];
    }

    std::swap(newedges[i].driver, newedges[j].driver);
    std::vector<std::pair<__int128_t, __int128_t>> driver_map;
    driver_map.push_back(std::make_pair(newedges[i].driver, newedges[j].w-newedges[i].w));
    driver_map.push_back(std::make_pair(newedges[j].driver, newedges[i].w-newedges[j].w));
    newsol.update_objective(driver_map);
    j++;
    if (j == num_edges) {
        i++;
        j = i+1;
        if (i == num_edges - 1) {
            solution = nullptr;
        }
    }
    // validate_solution(newsol, edgelist);
    return &newsol;
}
