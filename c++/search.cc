
#include "search.h"

auto best_improvement = [](Solution& solution, Neighborhood& neighborhood) {
    auto best = solution;
    int64_t i = 0;
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
    std::cout << "Neighborhood is traversed, best obj was " << best.obj << std::endl;
    return best;
};

Solution local_search(Solution solution, Edgelist* edgelist, int64_t iterations)
{
    std::cout << "Starting local search" << std::endl;
    Solution best = solution;
    int64_t i = 0;
    while(i < iterations) {
        auto current = best.obj;
        Reversal reversal(best, edgelist);
        Solution new_sol = best_improvement(best, reversal);

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
