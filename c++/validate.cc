#include "validate.h"
#include <cassert>
#include <set>

__int128_t diff2(__int128_t a, __int128_t b) {
    if (a < b) {
        return b-a;
    }
    return a-b;
}

void validate_solution(Solution solution, Edgelist* edgelist) {
    // std::cout << solution;
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
    std::set<__int128_t> vertices;
    assert(solution.chains.size()==1);
    auto x = solution.chains[0].edges.size();
    assert(x > 0);
    assert(solution.chains[0].edges.size()==solution.num_edges);
    assert(n==solution.num_edges);
    const auto& e = solution.chains[0].edges;
    for(__int128_t i = 0; i < e.size(); i++) {
        assert(e[i].w==edgelist->at(e[i].u)[e[i].v]);
        if (i == 0) {
            assert(e[i].u == e.back().v);
        } else {
            assert(e[i].u==e[i-1].v);
        }
        // drivers[e.driver]-=edgelist[e.u][e.v]
        vertices.insert(e[i].u);
    }
    __int128_t obj = 0;
    for (const auto& d : solution.drivers) {
        obj += d.obj;
    }
    for(__int128_t i = 0; i < n; i++) {
        assert(vertices.count(i) == 1);
    }
    obj /= k;
    if ((obj == 0 && solution.obj == 0) || (obj < 10 || solution.obj < 10)) {
        return;
    }
    assert(0.1 > diff2(obj,solution.obj)/std::max(obj, solution.obj));
}
