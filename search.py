
def local_search(solution, step_fnc, neighborhood_factory):
    best = solution
    i = 0
    while i < 100:
        new_sol = step_fnc(best, neighborhood_factory.get_default(best))
        if new_sol < best:
            best = new_sol
        else:
            return best
        i += 1
    return solution

# step functions
def first_improvement(solution, neighborhood):
    while True:
        new = neighborhood.next()
        if new == None:
            return solution
        elif new < solution:
            return new

def best_improvement(solution, neighborhood):
    best = solution
    while True:
        new = neighborhood.next()
        if new == None:
            return best
        elif new < best:
            best = new

def random(solution, neighborhood):
    return neighborhood.random()
