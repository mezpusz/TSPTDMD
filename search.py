import logging

def local_search(solution, step_fnc, neighborhood_factory, iterations=100):
    #print('Running local search')
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

def tabu_search(solution, neighborhood_factory, iterations=100, tabu_length=10):
    best = solution
    tabu_list = [best]
    i = 0
    while i < iterations:
        new_sol = tabu_improvement(best, neighborhood_factory.get(best), tabu_list)

        tabu_list.append(new_sol)
        if len(tabu_list) > tabu_length:
            tabu_list.pop(0)

        if new_sol < best:
            best = new_sol
        else:
            break
        i += 1
    return best

def tabu_improvement(solution, neighborhood,tabu_list):
    best = solution
    i = 0
    while True:
        new = neighborhood.next()
        i+=1
        if new == None:
            break
        elif new < best:
            not_in_tabu_list = True
            for tabu_elm in tabu_list:
                not_in_tabu_list |= tabu_elm.chains == new.chains
            if not_in_tabu_list:
                best = new
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
        # logging.debug("best iter " + str(i))
        new = neighborhood.next()
        i+=1
        if new == None:
            #print("Found {} neighbors".format(i))
            break
        elif new < best:
            best = new
    return best

def random(solution, neighborhood):
    return neighborhood.random()
