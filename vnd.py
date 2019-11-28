
from search import local_search, best_improvement

def vnd(solution, neighborhood_factory):
    print('Starting VND...')
    l = 0
    best = solution
    while l < 4:
        neighborhood_factory.set_index(l)
        new = local_search(best, best_improvement, neighborhood_factory, 1)
        if new < best:
            best = new
            print('New best solution found: {}'.format(best.obj))
            l = 0
        else:
            l += 1
    return best
