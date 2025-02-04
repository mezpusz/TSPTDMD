from solution import choose_obj
import logging
import copy

def local_search(solution, step_fnc, neighborhood_factory, iterations=100, delta_eval=True):
    print('Running local search')
    best = solution
    i = 0
    while i < iterations:
        print(i)
        new_sol = step_fnc(best, neighborhood_factory.get(best), delta_eval)

        if new_sol < best:
            best = new_sol
        else:
            break
        i += 1
    return best

# Take the last two arguments and return a function
# that only needs the solution to run local search.
def local_search_partially_applied (step_fnc, neighborhood_factory, iterations, delta_eval=True):
    return lambda solution: local_search(solution, step_fnc, neighborhood_factory, iterations, delta_eval)

def tabu_search(solution, neighborhood_factory, iterations=100, tabu_length=10,delta_eval=True):
    print("tabu!")
    best = solution
    tabu_list = [best]
    i = 0
    while i < iterations:
        print(i)
        new_sol = tabu_improvement(best, neighborhood_factory.get(best), tabu_list, delta_eval)
        tabu_list.append(new_sol)
        if len(tabu_list) > tabu_length:
            tabu_list.pop(0)

        if new_sol < best:
            best = new_sol
        i += 1
    return best

def tabu_improvement(solution, neighborhood,tabu_list, delta_eval=True):
    best = solution
    i = 0
    for new in neighborhood.next():
        i+=1
        if choose_obj(new, best, delta_eval):
            not_in_tabu_list = True
            for tabu_elm in tabu_list:
                not_in_tabu_list |= tabu_elm.chains == new.chains
            print(not_in_tabu_list)
            if not_in_tabu_list:
                best = copy.deepcopy(new)
    return best

# step functions

def first_improvement(solution, neighborhood, delta_eval=True):
    for new in neighborhood.next():
        if choose_obj(new,solution,delta_eval):
            return copy.deepcopy(new)
    return solution

def best_improvement(solution, neighborhood, delta_eval=True):
    best = solution
    i = 0
    for new in neighborhood.next():
        i+=1
        if i % 10000 == 0:
            print("Found {} neighbors so far, best is {}".format(i, best.obj))
        if choose_obj(new, best, delta_eval):
            best = copy.deepcopy(new)
    return best

def random(solution, neighborhood, delta_eval=True):
    return neighborhood.random()
