from construction import construct_randomized_greedy_from_given_inputs
from solution import update_objective
from random import randint
from bisect import insort
from validate import validate_solution
import copy

def init_population(random_heuristic, n):
    return sorted([random_heuristic() for i in range(n)])

def do_selection(population, n, factor):
    new = []
    last_specimen = int(n*factor)-1
    for i in range(n):
        j = randint(0, last_specimen)
        new.append(population[j])
        del population[j]
        last_specimen-=1
    return sorted(new)

def recombine(edgelist, population, alpha=0.8):
    last_specimen = int(len(population)*alpha)-1
    for i in range(last_specimen):
        for j in range(i+1,last_specimen+1):
            children = cross(edgelist, population[i], population[j])
            # insert into already sorted list
            insort(population, children[0])
            insort(population, children[1])
    return population

def cross(edgelist, spec1, spec2):
    new1 = copy.deepcopy(spec1)
    new2 = copy.deepcopy(spec2)
    i = randint(0, new1.num_edges-2)
    j = randint(i+1, new1.num_edges-1)
    order1 = get_order(spec1, i, j)
    order2 = get_order(spec2, i, j)
    rearrange_by_order(edgelist, new1, spec1, order2, i, j)
    rearrange_by_order(edgelist, new2, spec2, order1, i, j)
    return new1, new2

def get_order(specimen, i, j):
    order = sorted(range(j-i+1), key=lambda x: specimen.chains[0].edges[x+i].u)
    return order

def rearrange_by_order(edgelist, new, old, order, i, j):
    changes = []
    if (sorted(order) == order):
        return
    for k in range(i, j+1):
        edges = new.chains[0].edges
        old_edges = old.chains[0].edges
        new_u = old_edges[order[k-i]+i].u
        new_w = edgelist[edges[k-1].u][new_u]
        old_w = edgelist[old_edges[k-1].u][old_edges[k-1].v]
        changes.append((edges[k-1].driver, new_w-old_w))
        edges[k-1].v = new_u
        edges[k-1].update_weight(edgelist)
        edges[k].u = new_u
    edges[j].update_weight(edgelist)
    new_w = edgelist[edges[j].u][edges[j].v]
    old_w = edgelist[old_edges[j].u][old_edges[j].v]
    changes.append((edges[j].driver, new_w-old_w))
    update_objective(new, changes)
    # validate_solution(new, edgelist)

def mutate(edgelist, population):
    new = []
    for s in population:
        new.append(mutate_specimen(edgelist, s))
    return sorted(new + population)

def mutate_specimen(edgelist, specimen):
    new = copy.deepcopy(specimen)
    i = randint(0, new.num_edges-2)
    j = randint(i+1, new.num_edges-1)
    edges = new.chains[0].edges
    old_edges = specimen.chains[0].edges
    edges[i-1].v = old_edges[j].u
    edges[i-1].update_weight(edgelist)
    edges[i].u = old_edges[j].u
    edges[i].update_weight(edgelist)
    edges[j-1].v = old_edges[i].u
    edges[j-1].update_weight(edgelist)
    edges[j].u = old_edges[i].u
    edges[j].update_weight(edgelist)
    update_objective(new, [
        (edges[i-1].driver, edgelist[edges[i-1].u][edges[i-1].v]-edgelist[old_edges[i-1].u][old_edges[i-1].v]),
        (edges[i].driver, edgelist[edges[i].u][edges[i].v]-edgelist[old_edges[i].u][old_edges[i].v]),
        (edges[j-1].driver, edgelist[edges[j-1].u][edges[j-1].v]-edgelist[old_edges[j-1].u][old_edges[j-1].v]),
        (edges[j].driver, edgelist[edges[j].u][edges[j].v]-edgelist[old_edges[j].u][old_edges[j].v])
    ])
    return new

def genetic_algorithm(edgelist, random_heuristic, population_size, selection_factor, iterations):
    population = init_population(random_heuristic, population_size*2)
    for i in range(iterations):
        population = do_selection(population, population_size, selection_factor)
        population = recombine(edgelist, population)
        population = mutate(edgelist, population)
        print('population {} best solution is: {}'.format(i, population[0].obj))
    population = do_selection(population, population_size, selection_factor)
    return population
