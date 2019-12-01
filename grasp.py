import logging

def grasp(random_heuristic, local_search, stop):
    best_sol = local_search(random_heuristic())
    counter = 1
    while counter < stop:
        new_sol = local_search(random_heuristic())
        logging.debug('{}: {}'.format(counter, new_sol.obj))
        if new_sol < best_sol:
            best_sol = new_sol
        counter += 1

    return best_sol
