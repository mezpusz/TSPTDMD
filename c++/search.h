
#pragma once
#include "solution.h"
#include "neighborhood.h"
#include <functional>

Solution local_search(Solution solution, Edgelist* edgelist, __int128_t iterations=10);
Solution random_neighbor(Edgelist* edgelist, Solution sol, __int128_t dist);