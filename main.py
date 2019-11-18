from input import parse_input
from construction import construct_deterministic
from search import local_search, first_improvement
import sys

if len(sys.argv) < 2:
    print('Filename should be given as first parameter!')
    exit(-1)

vertices, k, L = parse_input(sys.argv[1])
print("n={} k={} L={}".format(len(vertices), k, L))

edgelist = []
for u in range(len(vertices)):
    for v in range(u+1, len(vertices[u])):
        edgelist.append((u,v,vertices[u][v]))
edgelist = sorted(edgelist, key=lambda x: x[2])
print(edgelist)

solution = construct_deterministic(edgelist, len(vertices), k, L)
print("Result of local search: {}".format(local_search(vertices, solution, first_improvement, None, False)))
