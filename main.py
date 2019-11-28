from input import parse_input
from construction import construct_deterministic, construct_random, construct_random_from_given_inputs
from search import local_search, local_search_partially_applied, best_improvement, first_improvement
from neighborhood import NeighborhoodFactory
from grasp import grasp
from vnd import vnd
<<<<<<< Updated upstream
import logging, sys

=======
import logging, sys, math, os.path
>>>>>>> Stashed changes
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

heuristic = sys.argv[3]
if heuristic == "local_search" or heuristic == "ls":
    solution = construct_deterministic(edgelist, len(vertices), k, L)
    solution = local_search(solution, best_improvement, neighborhood_factory, 100)
elif heuristic == "grasp":
    random_constructor = construct_random_from_given_inputs(edgelist, len(vertices), k, L)
    grasp_local_search = local_search_partially_applied(best_improvement, neighborhood_factory, 100)
    solution = grasp(random_constructor, grasp_local_search, 500)
elif heuristic == "vnd":
    solution = construct_deterministic(edgelist, len(vertices), k, L)
    solution = vnd(solution, neighborhood_factory)

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
with open(basename+'_'+heuristic+'_results-full.txt', 'a') as f:
    f.write(res+'\n'+str(int(math.sqrt(solution.obj)))+'\n')
logging.debug(solution.obj)
logging.debug(math.sqrt(solution.obj))
