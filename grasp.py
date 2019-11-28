def grasp(random_heuristic, local_search, stop):
    best_sol = local_search(random_heuristic())
    counter = 0
    while counter < stop:
        new_sol = local_search(random_heuristic())
        if new_sol < best_sol:
            best_sol = new_sol
    counter += 1
