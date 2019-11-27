from neighborhood import Reversal, ShortBlockMove

def local_search(edgelist, solution, step_fnc, neighborhood_gen, stopping_criteria):
    neighborhood = ShortBlockMove(solution, edgelist)
    best = solution
    i = 0
    while i < 100 and not stopping_criteria:
        new_sol = step_fnc(best, neighborhood)
        if new_sol < best:
            best = new_sol
        else:
            return best
        neighborhood = ShortBlockMove(best, edgelist)
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
    neighborhood = neighborhood(solution)
    return neighborhood.random()
