from search import local_search, best_improvement
import copy
from neighborhood import n_step
import logging

def vnd(solution, neighborhood_factory):
    #print('Starting VND...')
    l = 0
    best = solution
    while l < 4:
        logging.debug("  l " + str(l))
        neighborhood_factory.set_index(l)
        new = local_search(best, best_improvement, neighborhood_factory, 1)
        if new < best:
            best = new
            #print('New best solution found: {}'.format(best.obj))
            l = 0
        else:
            l += 1
    return best


def gvns(init_sol,neighborhood_fac, vnd_neighborhood_fac, k_max, iter):
    best_sol = init_sol
    i = 0
    while i < iter:
        logging.debug("i " + str(i))
        k = 1
        while k < k_max:
            logging.debug(" k " + str(k))
            random_sol = n_step(best_sol, neighborhood_fac, k)
            vnd_sol = vnd(random_sol, vnd_neighborhood_fac)
            if vnd_sol < best_sol:
                best_sol = vnd_sol
                k = 1
            else:
                k = k+1
        i += 1
    return best_sol
