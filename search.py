
def local_search(solution, step_fnc, neighborhood_factory, iterations):
    print('Running local search')
    best = solution
    i = 0
    while i < iterations:
        new_sol = step_fnc(best, neighborhood_factory.get(best))
        if new_sol < best:
            best = new_sol
        else:
            return best
        i += 1
    return best

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
    i = 0
    while True:
        new = neighborhood.next()
        i+=1
        if new == None:
            print("Found {} neighbors".format(i))
            return best
        elif new < best:
            best = new

def random(solution, neighborhood):
    return neighborhood.random()
