from input import parse_input
from solution import Solution, Chain, Edge, update_objective
from validate import validate_solution
import sys
import math

result_file = sys.argv[1]
with open(result_file, 'r') as f:
    lines = f.readlines()
    filename = lines[0].split()[0]
    edgelist, k, L, M = parse_input('../programming1/instances/' + filename + '.txt')
    sol = Solution(k, L)
    sol.num_edges = len(edgelist)
    sol.chains.append(Chain([], 0, 0))
    edges = sol.chains[0].edges
    for e in lines[1].split():
        edges.append(Edge(int(e), -1, -1, -1))
    driver_map = []
    for i,d in enumerate(lines[2].split()):
        edges[i].driver = int(d)
    for i,e in enumerate(edges):
        edges[i-1].v = edges[i].u
        edges[i-1].w = edgelist[edges[i-1].u][edges[i-1].v]
        driver_map.append((edges[i-1].driver, edges[i-1].w))
    update_objective(sol, driver_map)
    invalids = 0
    for e in edges:
        if e.w == M:
            print('invalid edge: {},{}'.format(e.u, e.v))
            invalids+=1
    print('There are {} invalid edges in the solution'.format(invalids))
    print(int(math.sqrt(sol.obj)))
    validate_solution(sol, edgelist)
