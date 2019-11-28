def local_search(solution, step_fnc, neighborhood_factory, iterations):
    print('Running local search')
    best = solution
    i = 0
    while i < iterations:
        new_sol = step_fnc(best, neighborhood_factory.get(best))
        if new_sol < best:
            best = new_sol
        else:
            break
        i += 1
    return best

# Take the last two arguments and return a function
# that only needs the solution to run local search.
def local_search_partially_applied (step_fnc, neighborhood_factory, iterations):
    return lambda solution: local_search(solution, step_fnc, neighborhood_factory, iterations)

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
            break
        elif new < best:
            best = new
    return best

def random(solution, neighborhood):
    return neighborhood.random()
