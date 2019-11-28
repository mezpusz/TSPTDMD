from input import parse_input
from construction import construct_deterministic, construct_random
from search import local_search, best_improvement
from neighborhood import NeighborhoodFactory
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from random import seed
seed()

if len(sys.argv) < 3:
    logging.error('Help: main.py [filename] [neighborhood]')
    exit(-1)

vertices, k, L = parse_input(sys.argv[1])
logging.debug("n={} k={} L={}".format(len(vertices), k, L))

edgelist = []
for u in range(len(vertices)):
    for v in range(u+1, len(vertices[u])):
        edgelist.append((u,v,vertices[u][v]))
edgelist = sorted(edgelist, key=lambda x: x[2])
logging.debug(edgelist)

solution = construct_deterministic(edgelist, len(vertices), k, L)
neighborhood_factory = NeighborhoodFactory(vertices, sys.argv[2])
solution = local_search(solution, best_improvement, neighborhood_factory)

res = ""
for e in solution.chains[0].edges:
    res += str(e.u) + " "
res += "\n"
for e in solution.chains[0].edges:
    res += str(e.driver) + " "

print(res)
logging.debug(solution.obj)