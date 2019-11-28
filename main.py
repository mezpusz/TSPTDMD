from input import parse_input
from construction import construct_deterministic, construct_random, construct_random_from_given_inputs
from search import local_search, local_search_partially_applied, best_improvement, first_improvement
from neighborhood import NeighborhoodFactory
from grasp import grasp
from vnd import vnd
import logging, sys, math, os.path
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from random import seed
seed()

if len(sys.argv) < 4:
    logging.error('Help: main.py [filename] [neighborhood] [heuristic]')
    exit(-1)

filename = sys.argv[1]
edgelist, k, L, M = parse_input(filename)
#logging.debug("n={} k={} L={}".format(len(vertices), k, L))

sorted_edgelist = []
for u in range(len(edgelist)):
    for v in range(u+1, len(edgelist[u])):
        sorted_edgelist.append((u,v,edgelist[u][v]))
sorted_edgelist = sorted(sorted_edgelist, key=lambda x: x[2])
#logging.debug(sorted_edgelist)

neighborhood_factory = NeighborhoodFactory(edgelist, sys.argv[2])

heuristic = sys.argv[3]
if heuristic == 'deterministic_construction' or heuristic == 'dc':
    solution = construct_deterministic(edgelist, sorted_edgelist, len(edgelist), k, L, M)
if heuristic == 'random_construction' or heuristic == 'rc':
    solution = construct_random(sorted_edgelist, len(edgelist), k, L)
elif heuristic == "local_search" or heuristic == "ls":
    solution = construct_deterministic(edgelist, sorted_edgelist, len(edgelist), k, L, M)
    solution = local_search(solution, best_improvement, neighborhood_factory, 100)
elif heuristic == "grasp":
    random_constructor = construct_random_from_given_inputs(sorted_edgelist, len(edgelist), k, L)
    grasp_local_search = local_search_partially_applied(best_improvement, neighborhood_factory, 100)
    solution = grasp(random_constructor, grasp_local_search, 500)
elif heuristic == "vnd":
    solution = construct_deterministic(edgelist, sorted_edgelist, len(edgelist), k, L, M)
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
with open('results/'+heuristic+'/'+basename+'_'+heuristic+'_results.txt', 'a') as f:
    f.write(res)
logging.debug(solution.obj)
logging.debug(math.sqrt(solution.obj))
