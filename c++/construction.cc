#include "construction.h"
#include <map>
#include <set>

#include "validate.h"

__int128_t diff(__int128_t a, __int128_t b) {
    if (a < b) {
        return b-a;
    }
    return a-b;
}

Solution make_feasible(Edgelist* edgelist, Solution sol, __int128_t M) {
    if (M == -1) {
        return sol;
    }
    Solution new_sol = sol;
    std::set<std::tuple<__int128_t, __int128_t, __int128_t, __int128_t>> tried;
    while (true) {
        // auto changes = 0;
        auto& e = new_sol.chains[0].edges;
        auto found = false;
        for (__int128_t i = 0; i < e.size(); i++) {
            if (e[i].w == M) {
                for (__int128_t j = i+2; j < e.size(); j++) {
                    if ((edgelist->at(e[j].u)[e[i].u] < M ||
                        edgelist->at(e[j].v)[e[i].v] < M) &&
                        tried.count(std::make_tuple(
                            std::min(e[i].u, e[j].u),
                            std::max(e[i].u, e[j].u),
                            std::min(e[i].v, e[j].v),
                            std::max(e[i].v, e[j].v))) == 0) {
                        found = true;
                        tried.insert(std::make_tuple(
                            std::min(e[i].u, e[j].u),
                            std::max(e[i].u, e[j].u),
                            std::min(e[i].v, e[j].v),
                            std::max(e[i].v, e[j].v)));
                        for(__int128_t k = i+1; k < j; k++) {
                            std::swap(e[k].u, e[k].v);
                        }
                        for(__int128_t k = i+1; k < j-k+i; k++) {
                            std::swap(e[k], e[j-k+i]);
                        }
                        std::swap(e[i].v, e[j].u);
                        __int128_t i_w = e[i].w;
                        __int128_t j_w = e[j].w;
                        e[i].update_weight(edgelist);
                        e[j].update_weight(edgelist);
                     
                        std::vector<std::pair<__int128_t, __int128_t>> driver_map;
                        driver_map.push_back(std::make_pair(e[i].driver, e[i].w-i_w));
                        driver_map.push_back(std::make_pair(e[j].driver, e[j].w-j_w));
                        new_sol.update_objective(driver_map);
                        break;
                    }
                }
            }
        }
        // std::cout << new_sol << std::endl;
        // validate_solution(new_sol, edgelist);
        // std::cout << changes << std::endl;
        __int128_t count = 0;
        for (__int128_t i = 0; i < e.size(); i++) {
            if (e[i].w == M) {
                count++;
            }
        }
        // std::cout << "Invalid edges: " << count
        //           << " obj " << new_sol.obj << std::endl;
        if (count == 0 || !found) {
            std::cout << "Infeasible edges remaining: " << count << std::endl;
            break;
        }
    }
    return new_sol;
}

Solution construct_randomized_greedy2(
    Edgelist* edgelist,
    __int128_t n, __int128_t k, __int128_t L, __int128_t M)
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
    std::set<__int128_t> nope;
    auto chosen_c = candidate_list.begin();

    while(sol.num_edges < n-1) {
        __int128_t last_index = 10;
        __int128_t chosen = (last_index == 0) ? 0 : (std::rand() % last_index);
        for(__int128_t i = 0; i < chosen; i++) {
            auto next = chosen_c;
            next++;
            if (next == candidate_list.end()) {
                break;
            }
            chosen_c++;
        }
        if (nope.count(chosen_c->second.u) == 0 &&
            nope.count(chosen_c->second.v) == 0) {
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
            if(sol.insert_edge(chosen_edge)) {
                __int128_t v = find_inner_vertex(sol, chosen_edge);
                if (v == -2) {
                    nope.insert(chosen_edge.u);
                    nope.insert(chosen_edge.v);
                } else if (v != -1) {
                    nope.insert(v);
                }
            }
        }
        chosen_c++;
        if (chosen_c == candidate_list.end()) {
            for(auto c_it = candidate_list.begin(); c_it != candidate_list.end();) {
                if (nope.count(c_it->second.u) > 0 || nope.count(c_it->second.v) > 0) {
                    c_it = candidate_list.erase(c_it);
                } else {
                    ++c_it;
                }
            }
            if (candidate_list.size() == 0) {
                std::cout << "Error: no more candidates" << std::endl;
                break;
            }
            std::cout << "End of list, edges needed " << (n-1-sol.num_edges)
                      << " excluded nodes " << nope.size()
                      << " remaining candidates " << candidate_list.size() << std::endl;
            chosen_c = candidate_list.begin();
        }
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
    sol = make_feasible(edgelist, sol, M);
    return sol;
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
    sol = make_feasible(edgelist, sol, M);
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
