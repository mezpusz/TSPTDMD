
from construction import construct_randomized_greedy_from_given_inputs
from genetic import genetic_algorithm
from search import local_search, best_improvement
from neighborhood import NeighborhoodFactory

def genetic_with_local_search(random_constructor, edgelist):
    population = genetic_algorithm(edgelist, random_constructor, 5, 1.2, 10)
    neighborhood_factory = NeighborhoodFactory(edgelist, 'Reversal')
    best = None
    for p in population:
        new = local_search(p, best_improvement, neighborhood_factory)
        if best == None or new < best:
            best = new
            print('New best is {}'.format(best.obj))
    return best