#include "validate.h"
#include <cassert>

void validate_solution(Solution solution, Edgelist* edgelist) {
    std::cout << solution;
    auto k = solution.drivers.size();
    auto L = solution.L;
    auto n = edgelist->size();
    assert(k > 0);
    assert(L > 0);
    for (const auto& e : solution.chains[0].edges) {
        assert(e.u >= 0 && e.u < n);
        assert(e.v >= 0 && e.v < n);
        assert(e.w >= 0);
        assert(e.driver >= 0 && e.driver < k);
    }
    // drivers = [L for i in range(k)]
    // vertices = [False for i in range(len(edgelist))]
    assert(solution.chains.size()==1);
    auto x = solution.chains[0].edges.size();
    assert(x > 0);
    assert(solution.chains[0].edges.size()==solution.num_edges);
    assert(n==solution.num_edges);
    // for i,e in enumerate(solution.chains[0].edges):
    //     assert(e.w==edgelist[e.u][e.v])
    //     assert(e.u==solution.chains[0].edges[i-1].v)
    //     drivers[e.driver]-=edgelist[e.u][e.v]
    //     vertices[e.u] = True
    // obj = 0
    // for d in drivers:
    //     obj += d**2
    // for i,v in enumerate(vertices):
    //     assert(v)
    // obj /= k
    // calculated = int64_t(obj)
    // from_solution = solution.obj
    // print("Objective in solution is: {}, calculated: {}".format(from_solution, calculated))
    // if calculated == 0 and from_solution == 0 or calculated < 10 and from_solution < 10:
    //     return
    // assert(0.1 > abs(calculated-from_solution)/max(calculated, from_solution))
}
