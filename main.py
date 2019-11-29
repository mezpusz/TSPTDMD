from input import parse_input
from construction import construct_deterministic, construct_random, construct_random_from_given_inputs
from search import local_search, local_search_partially_applied, best_improvement, first_improvement
from neighborhood import NeighborhoodFactory
from grasp import grasp
from vn import vnd, gvns
import logging, sys, math, os.path
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from random import seed
seed()

if len(sys.argv) < 4:
    logging.error('Help: main.py [filename] [neighborhood] [heuristic]')
    exit(-1)

filename = sys.argv[1]
vertices, k, L = parse_input(filename)
#logging.debug("n={} k={} L={}".format(len(vertices), k, L))

edgelist = []
for u in range(len(vertices)):
    for v in range(u+1, len(vertices[u])):
        edgelist.append((u,v,vertices[u][v]))
edgelist = sorted(edgelist, key=lambda x: x[2])
#logging.debug(edgelist)

neighborhood_factory = NeighborhoodFactory(vertices, sys.argv[2])

local_iterations = 100
grasp_iterations = 100
gvns_iterations  = 10

heuristic = sys.argv[3]
if heuristic == "local_search" or heuristic == "ls":
    solution = construct_deterministic(edgelist, len(vertices), k, L)
    solution = local_search(solution, best_improvement, neighborhood_factory, local_iterations)
elif heuristic == "grasp":
    random_constructor = construct_random_from_given_inputs(edgelist, len(vertices), k, L)
    grasp_local_search = local_search_partially_applied(best_improvement, neighborhood_factory, local_iterations)
    solution = grasp(random_constructor, grasp_local_search, grasp_iterations)
elif heuristic == "vnd":
    # vnd_neighborhood_fac is reset, so the exact type is unimportant
    vnd_neighborhood_fac = NeighborhoodFactory(vertices)
    solution = construct_deterministic(edgelist, len(vertices), k, L)
    solution = vnd(solution, vnd_neighborhood_fac)
elif heuristic == "gvns":
    # vnd_neighborhood_fac is reset, so the exact type is unimportant
    vnd_neighborhood_fac = NeighborhoodFactory(vertices)
    solution = construct_deterministic(edgelist, len(vertices), k, L)
    solution = gvns(solution, neighborhood_factory, vnd_neighborhood_fac, len(vertices), gvns_iterations)

basename = os.path.splitext(os.path.basename(filename))[0]
res = basename + '\n'
for e in solution.chains[0].edges:
    res += str(e.u) + ' '
res += '\n'
for e in solution.chains[0].edges:
    res += str(e.driver) + ' '
res += '\n'

print(res)
with open(basename+'_'+heuristic+'_results.txt', 'a') as f:
    f.write(res)
logging.debug(solution.obj)
logging.debug(math.sqrt(solution.obj))
