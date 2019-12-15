#include "construction.h"
#include <map>

#include "validate.h"

__int128_t diff(__int128_t a, __int128_t b) {
    if (a < b) {
        return b-a;
    }
    return a-b;
}

Solution construct_randomized_greedy(
    Edgelist* edgelist,
    __int128_t n, __int128_t k, __int128_t L, __int128_t M, float alpha)
{
    std::cout << "Constructing solution with randomized greedy approach" << std::endl;
    Solution sol(k, L, n);

    __int128_t A = (L*k)/n;
    std::multimap<__int128_t, Edge> candidate_list;
    for (__int128_t u = 0; u < edgelist->size(); u++) {
        for (__int128_t v = u+1; v < edgelist->size(); v++) {
            Edge edge(u, v, 0, edgelist->at(u)[v]);
            __int128_t obj = diff(A,edge.w);
            candidate_list.insert(std::make_pair(obj, edge));
        }
    }

    while(sol.num_edges < n-1) {
        __int128_t min_cand = candidate_list.begin()->first;
        __int128_t max_cand = candidate_list.rbegin()->first;
        __int128_t max_value = min_cand + alpha * (max_cand-min_cand);
        __int128_t last_index = 0;
        for(auto& e : candidate_list) {
            if (e.first > max_value) {
                break;
            }
            last_index++;
        }
        __int128_t chosen = (last_index == 0) ? 0 : (std::rand() % last_index);
        auto chosen_c = candidate_list.begin();
        for(__int128_t i = 0; i < chosen; i++) {
            chosen_c++;
        }
        auto chosen_edge = chosen_c->second;
        auto driver = std::make_pair<__int128_t, __int128_t>(-1, 0);
        for(__int128_t l = 0; l < sol.drivers.size(); l++) {
            chosen_edge.driver = l;
            __int128_t obj = sol.calculate_objective_with_edge(chosen_edge);
            if (driver.first == -1 or obj < driver.first) {
                driver = std::make_pair(obj, l);
            }
        }
        chosen_edge.driver = driver.second;
        if(!sol.insert_edge(chosen_edge)) {
            std::cout << "Could not insert candidate, this should not happen" << std::endl;
            candidate_list.erase(chosen_c);
            continue;
#ifdef DEBUG
            bool found = false;
            std::cout << "Debug mode" << std::endl;
            for(int64_t i = 0; i < sol.chains.size(); i++) {
                if ((sol.chains[i].edges[0].u == chosen_edge.u && sol.chains[i].edges.back().v == chosen_edge.v)
                    || (sol.chains[i].edges[0].u == chosen_edge.v && sol.chains[i].edges.back().v == chosen_edge.u))
                {
                    found = true;
                    break;
                }
            }
            if (!found) {
                std::cout << "Could not insert candidate, this should not happen" << std::endl;
            } else {
                candidate_list.erase(chosen_c);
                continue;
            }
#endif
        }
        __int128_t v = find_inner_vertex(sol, chosen_edge);
        candidate_list.erase(chosen_c);

        if (v == -2) {
            for(auto c_it = candidate_list.begin(); c_it != candidate_list.end();) {
                if (c_it->second.u == chosen_edge.u || c_it->second.v == chosen_edge.u
                    || c_it->second.u == chosen_edge.v || c_it->second.v == chosen_edge.v) {
                    c_it = candidate_list.erase(c_it);
                } else {
                    ++c_it;
                }
            }
        } else if (v != -1) {
            for(auto c_it = candidate_list.begin(); c_it != candidate_list.end();) {
                if (c_it->second.u == v || c_it->second.v == v) {
                    c_it = candidate_list.erase(c_it);
                } else {
                    ++c_it;
                }
            }
        }
        // std::cout << candidate_list.size() << " candidates left" << std::endl;
        // std::multimap<int64_t, Edge> new_candidate_list;
        // for (auto c : candidate_list) {
        //     int64_t obj = sol.calculate_objective_with_edge(c.second);
        //     new_candidate_list.insert(std::make_pair(obj, c.second));
        // }
        // candidate_list = new_candidate_list;
    }

    auto last_driver = std::make_pair<__int128_t, __int128_t>(-1, 0);
    for(__int128_t l = 0; l < sol.drivers.size(); l++) {
        __int128_t last_u = sol.chains[0].edges.back().v;
        __int128_t last_v = sol.chains[0].edges[0].u;
        Edge edge(last_u, last_v, l, edgelist->at(last_u)[last_v]);
        __int128_t obj = sol.calculate_objective_with_edge(edge);
        if (last_driver.first == -1 or obj < last_driver.first) {
            last_driver = std::make_pair(obj, l);
        }
    }
    add_loopback_edge(edgelist, sol, last_driver.second);
    // validate_solution(sol, edgelist);
    return sol;
}

void add_loopback_edge(
    Edgelist* edgelist,
    Solution& solution,
    __int128_t driver)
{
    auto& ch = solution.chains[0].edges;
    auto w = edgelist->at(ch[0].u)[ch.back().v];
    solution.add_loopback_edge(Edge(ch.back().v, ch[0].u, driver, w));
}

__int128_t find_inner_vertex(const Solution& solution, Edge edge) {
    for(__int128_t i = 0; i < solution.chains.size(); i++) {
        const auto& ch = solution.chains[i];
        if(ch.edges.size() == 1 && ((edge.u == ch.edges[0].u && edge.v == ch.edges[0].v) ||
            (edge.u == ch.edges[0].v && edge.v == ch.edges[0].u))) {
            return -1;
        } else if(edge.u == ch.edges[0].u) {
            return edge.v;
        } else if(edge.v == ch.edges[0].u) {
            return edge.u;
        } else if(edge.u == ch.edges.back().v) {
            return edge.v;
        } else if(edge.v == ch.edges.back().v) {
            return edge.u;
        }
    }
    return -2;
}
