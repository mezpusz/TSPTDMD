
#include "search.h"
#include "neighborhood.h"

auto best_improvement = [](Solution& solution, Neighborhood& neighborhood) {
    auto best = solution;
    __int128_t i = 0;
    while (true) {
        auto new_sol = neighborhood.next();
        i++;
        if (new_sol == nullptr) {
            break;
        }
        if (*new_sol < best) {
            debug() << "Found new best with obj " << new_sol->obj
                    << " (old is " << best.obj << ")" << std::endl;
            best = *new_sol;
        }
    }
    // std::cout << "Neighborhood is traversed, best obj was " << best.obj << std::endl;
    return best;
};

Solution random_neighbor(Edgelist* edgelist, Solution sol, __int128_t dist) {
    for (int d = 0; d < dist; d++) {
        __int128_t i = std::rand() % (sol.num_edges-2);
        __int128_t j = i + 2 + (std::rand() % (sol.num_edges - i - 2));
        make_reversal(edgelist, sol, i, j);
    }
    return sol;
}

Solution search_reversal(Edgelist* edgelist, Solution sol) {
    auto& e = sol.chains[0].edges;
    __int128_t min = sol.obj;
    std::pair<__int128_t, __int128_t> min_pair = std::make_pair<__int128_t, __int128_t>(-1,-1); 
    for (__int128_t i = 0; i < e.size(); i++) {
        for (__int128_t j = i+2; j < e.size(); j++) {
            std::vector<std::pair<__int128_t, __int128_t>> driver_map;
            driver_map.push_back(std::make_pair(e[i].driver, edgelist->at(e[i].u)[e[j].u]-e[i].w));
            driver_map.push_back(std::make_pair(e[j].driver, edgelist->at(e[i].v)[e[j].v]-e[j].w));
            __int128_t k = sol.drivers.size();
            __int128_t obj = sol.obj;
            auto drivers = sol.drivers;
            for(auto [d, change] : driver_map) {
                auto& driver = drivers[d];
                obj -= driver.obj_squared/k;
                driver.obj -= change;
                driver.obj_squared = driver.obj * driver.obj;
                obj += driver.obj_squared/k;
            }
            if (obj < min) {
                min = obj;
                min_pair.first = i;
                min_pair.second = j;
            }
        }
    }
    __int128_t i = min_pair.first;
    __int128_t j = min_pair.second;
    if (i != -1)
    {
        make_reversal(edgelist, sol, i, j);
    }
    // std::cout << "Neighborhood is traversed, best obj was " << sol.obj << std::endl;
    return sol;
}

Solution local_search(Solution solution, Edgelist* edgelist, __int128_t iterations)
{
    std::cout << "Starting local search" << std::endl;
    Solution best = solution;
    __int128_t i = 0;
    while(i < iterations) {
        auto current = best.obj;
        // Reversal reversal(best, edgelist);
        // Solution new_sol = best_improvement(best, reversal);
        Solution new_sol = search_reversal(edgelist, best);

        if (new_sol < best) {
            debug() << "Best improvement returned new solution with obj "
                    << new_sol.obj << " (old is " << best.obj << ")" << std::endl;
            best = new_sol;
        }

        DriverExchange driverExchange(best, edgelist);
        new_sol = best_improvement(best, driverExchange);

        if (new_sol < best) {
            debug() << "Best improvement returned new solution with obj "
                    << new_sol.obj << " (old is " << best.obj << ")" << std::endl;
            best = new_sol;
        }
        if (current == best.obj) {
            break;
        }
        i += 1;
    }
    return best;
}
