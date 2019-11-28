
from search import local_search, best_improvement
from neighborhood import neighborhoods

def vnd(solution, neighborhood_factory):
    print('Starting VND...')
    l = 0
    best = solution
    while l < len(neighborhoods):
        neighborhood_factory.set_index(l)
        new = local_search(best, best_improvement, neighborhood_factory, 1)
        if new < best:
            best = new
            print('New best solution found: {}'.format(best.obj))
            l = 0
        else:
            l += 1
    return best
