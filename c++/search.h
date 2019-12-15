
#pragma once
#include "solution.h"
#include "neighborhood.h"
#include <functional>

Solution local_search(Solution solution, Edgelist* edgelist, int64_t iterations=100);