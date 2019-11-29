from input import parse_input
from construction import construct_deterministic, construct_random, construct_random_from_given_inputs
from search import local_search, local_search_partially_applied, best_improvement, first_improvement, random, tabu_search
from neighborhood import NeighborhoodFactory
from grasp import grasp
from os.path import exists
from vn import vnd, gvns
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

local_iterations = 100
grasp_iterations = 100
gvns_iterations  = 10
tabu_iterations  = 100
tabu_length      = 10
delta_eval       = True

heuristic = sys.argv[3]

if heuristic == 'deterministic_construction' or heuristic == 'dc':
    heuristic = "deterministic_construction"
    solution = construct_deterministic(edgelist, sorted_edgelist, len(edgelist), k, L, M)

elif heuristic == 'random_construction' or heuristic == 'rc':
    heuristic   = "random_construction"
    solution = construct_random(sorted_edgelist, len(edgelist), k, L)

elif heuristic == "local_search" or heuristic == "ls":
    heuristic   = "local_search"
    solution = construct_deterministic(edgelist, sorted_edgelist, len(edgelist), k, L, M)
    solution = local_search(solution, best_improvement, neighborhood_factory, local_iterations, delta_eval)

elif heuristic == "grasp":
    random_constructor = construct_random_from_given_inputs(sorted_edgelist, len(edgelist), k, L)
    grasp_local_search = local_search_partially_applied(best_improvement, neighborhood_factory, local_iterations, delta_eval)
    solution = grasp(random_constructor, grasp_local_search, grasp_iterations)

elif heuristic == "vnd":
    # vnd_neighborhood_fac is reset, so the exact type is unimportant
    vnd_neighborhood_fac = NeighborhoodFactory(edgelist)
    solution = construct_deterministic(edgelist, sorted_edgelist, len(edgelist), k, L, M)
    solution = vnd(solution, vnd_neighborhood_fac, delta_eval)

elif heuristic == "gvns":
    if sys.argv[2] == "sbm" or sys.argv[2] == "ShortBlockMove" or sys.argv[2] == 'r' or sys.argv[2] == "Reversal":
        print("That neighborhood is not currently supported")
        exit()

    # vnd_neighborhood_fac is reset, so the exact type is unimportant
    vnd_neighborhood_fac = NeighborhoodFactory(edgelist)
    solution = construct_deterministic(edgelist, sorted_edgelist, len(edgelist), k, L, M)
    solution = gvns(solution, neighborhood_factory, vnd_neighborhood_fac, len(edgelist), gvns_iterations, delta_eval)

elif heuristic == "tabu_search" or heuristic == "ts":
    heuristic   = "tabu_search"
    solution = construct_deterministic(edgelist, sorted_edgelist, len(edgelist), k, L, M)
    solution = tabu_search(solution, neighborhood_factory, tabu_iterations, tabu_length, delta_eval)


basename = os.path.splitext(os.path.basename(filename))[0]
res = basename + '\n'
for e in solution.chains[0].edges:
    res += str(e.u) + ' '
res += '\n'
for e in solution.chains[0].edges:
    res += str(e.driver) + ' '
res += '\n'

print(res)
filename = 'results/'+heuristic+'/'+basename+'_'+heuristic+'_results.txt'
with open(filename, 'a') as f:
    f.write(res)
logging.debug(solution.obj)
logging.debug(math.sqrt(solution.obj))
