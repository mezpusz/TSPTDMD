import math

def validate_solution(solution, edgelist):
    # remove this to have validation 
    # return
    k = len(solution.drivers)
    L = solution.L
    assert(k > 0)
    assert(L > 0)
    drivers = [L for i in range(k)]
    vertices = [False for i in range(len(edgelist))]
    assert(len(solution.chains)==1)
    assert(len(solution.chains[0].edges)==solution.num_edges)
    assert(len(edgelist)==solution.num_edges)
    for i,e in enumerate(solution.chains[0].edges):
        assert(e.w==edgelist[e.u][e.v])
        assert(e.u==solution.chains[0].edges[i-1].v)
        drivers[e.driver]-=edgelist[e.u][e.v]
        vertices[e.u] = True
    obj = 0
    for d in drivers:
        obj += d**2
    for i,v in enumerate(vertices):
        assert(v)
    obj /= k
    calculated = int(obj)
    from_solution = solution.obj
    print("Objective in solution is: {}, calculated: {}".format(from_solution, calculated))
    if calculated == 0 and from_solution == 0 or calculated < 10 and from_solution < 10:
        return
    assert(0.1 > abs(calculated-from_solution)/max(calculated, from_solution))
