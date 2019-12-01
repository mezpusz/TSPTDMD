from solution import *
from random import randint
import copy
from validate import validate_solution

# edgelist should be sorted
# n = nr. of vertices
# k = nr. of drivers
# L = desired travel distance for each driver
def construct_deterministic(edgelist, sorted_edgelist, n, k, L, M):
    print('Constructing solution deterministically')
    # A = desired average travel distance to each node
    A = int(L*k/n)
    i = 0

    # i is set to index of last edge with weight < A
    for j in range(len(sorted_edgelist)):
        if sorted_edgelist[j][2] >= A:
            i = j
            break
    print("A={},i={}".format(A,i))

    sol = Solution(k, L)

    # l is driver number
    l = 0

    # We add edges with weight closest to A
    # We alternate between adding the edge with weight just below A
    # and the edge with weight just above A.
    # As we add edges we iterate through the driver numbers.
    # Stop when still need to add the last edge that turns the graph into a cycle.
    while sol.num_edges < n-1:
        # Try to add edge with weight just below A
        index = -1
        if i >= 0 and j < len(sorted_edgelist):
            if abs(sorted_edgelist[i][2] - A) < abs(sorted_edgelist[j][2] - A):
                index = i
                i -= 1
            else:
                index = j
                j += 1
        elif i >= 0:
            index = i
            i -= 1
        else:
            index = j
            j += 1
        if insert_edge(sol, Edge(sorted_edgelist[index][0], sorted_edgelist[index][1], l, sorted_edgelist[index][2])):
            l = (l + 1) % k   # Next driver
        #print("i={},j={},obj={}".format(i,j,sol.obj))

    add_lookback_edge(sorted_edgelist, sol, l)

    # This part is based on the reversal neighborhood structure.
    # We would like to make sure that the constructed solution
    # is already feasible, thus eliminating all edges with M
    # weight. This can be done by searching for replacements and
    # changing two edges at a time, during which one part of the
    # chain is reversed. We do this until we run out of options
    # but with a maximum number of tries to avoid infinite loops

    #TODO: put this and the code in Reversal to a common place
    changed = True
    tries = 0
    while M != -1 and changed and tries < 1000000:
        if tries % 1000 == 0:
            print("Trying to improve solution, current iteration {}".format(tries))
        changed = False
        index = -1
        edges = sol.chains[0].edges
        for i in range(len(edges)):
            if edges[i].w == M:
                index = i
                break
        if index == -1:
            break
        index2 = (index + 2) % len(edges)
        v_i = edges[index]
        while (index2 + 2) % sol.num_edges != index:
            v_i2 = edges[index2]
            if edgelist[v_i.u][v_i2.u] < M and edgelist[v_i.v][v_i2.v] < M:
                # Break the chain into two by removing two edges
                # i and j are removed so the remaining are added
                chain1 = Chain(edges, index+1, index2-1)
                chain2 = Chain(edges, index2+1, index-1)
                newsol = sol.copy()
                newsol.chains = [chain1, chain2]
                # The number of edges is decreased by 2,
                # we later add these edges back
                newsol.num_edges = sol.num_edges-2
                update_objective(newsol, [(v_i.driver, -v_i.w), (v_i2.driver, -v_i2.w)])
                # Add the first cross edge, consisting of
                # the second vertices of the removed edges
                insert_edge(newsol, Edge(v_i.v, v_i2.v, v_i.driver, edgelist[v_i.v][v_i2.v]))
                # Add the second cross edge
                add_loopback_edge(newsol, Edge(v_i.u, v_i2.u, v_i2.driver, edgelist[v_i.u][v_i2.u]))
                changed = True
                tries += 1
                sol = newsol
                break
            else:
                index2 += 1
                index2 %= sol.num_edges
    # validate_solution(sol, edgelist)
    return sol

def construct_random(edgelist, n, k, L):
    print('Constructing solution randomly')
    sol = Solution(k, L)
    i = randint(0, len(edgelist)-1)
    l = randint(0, k-1)

    # insert random edge
    while sol.num_edges < n-1:
        insert_edge(sol, Edge(edgelist[i][0], edgelist[i][1], l, edgelist[i][2]))
        i = randint(0, len(edgelist)-1)
        l = randint(0, k-1)
    add_lookback_edge(edgelist, sol, randint(0, k-1))
    return sol

def construct_randomized_greedy(edgelist, sorted_edgelist, n, k, L, alpha):
    print('Constructing solution randomly with greedy approach')
    sol = Solution(k, L)

    # create candidate list
    candidate_list = []
    for e in sorted_edgelist:
        edge = Edge(e[0], e[1], 0, e[2])
        if can_edge_be_added(sol, edge):
            for l in range(len(sol.drivers)):
                # create edge with actual driver
                edge = Edge(e[0], e[1], l, e[2])
                obj = calculate_objective_with_edge(sol, edge)
                candidate_list.append((obj, edge))
    candidate_list = sorted(candidate_list, key=lambda x: x[0])

    while sol.num_edges < n-1:
        # insert first candidate
        min_cand = candidate_list[0]
        max_cand = candidate_list[-1]
        max_value = min_cand[0] + alpha * (max_cand[0]-min_cand[0])
        last_index = next((i for i,c in enumerate(candidate_list) if c[0] > max_value), len(candidate_list)-1)
        chosen = randint(0, last_index)
        chosen_e = candidate_list[chosen][1]
        if not insert_edge(sol, chosen_e):
            found = False
            for i in range(len(sol.chains)):
                if (sol.chains[i].edges[0].u == chosen_e.u and sol.chains[i].edges[-1].v == chosen_e.v
                    or sol.chains[i].edges[0].u == chosen_e.v and sol.chains[i].edges[-1].v == chosen_e.u):
                    found = True
                    break
            if not found:
                raise Exception('Could not insert candidate, this should not happen')
            else:
                del candidate_list[chosen]
                continue
        v = find_inner_vertex(sol, chosen_e)
        del candidate_list[chosen]

        # remove non-feasible edges
        if v == -2:
            candidate_list = list(filter((lambda c: c[1].u != chosen_e.u and c[1].v != chosen_e.u), candidate_list))
            candidate_list = list(filter((lambda c: c[1].u != chosen_e.v and c[1].v != chosen_e.v), candidate_list))
        elif v != -1:
            candidate_list = list(filter((lambda c: c[1].u != v and c[1].v != v), candidate_list))
        # recalculate edge objectives for edges
        # that are still feasible
        for c in candidate_list:
            obj = calculate_objective_with_edge(sol, edge)
            c = (obj, c[1])
        candidate_list = sorted(candidate_list, key=lambda x: x[0])

    # choose driver for last edge
    last_driver = (-1, 0)
    for l in range(len(sol.drivers)):
        last_u = sol.chains[0].edges[-1].v
        last_v = sol.chains[0].edges[0].u
        edge = Edge(last_u, last_v, l, edgelist[last_u][last_v])
        obj = calculate_objective_with_edge(sol, edge)
        if last_driver[0] == -1 or obj < last_driver[0]:
            last_driver = (obj, l)
    add_lookback_edge(sorted_edgelist, sol, last_driver[1])
    # validate_solution(sol, edgelist)
    return sol

# Takes the input to construct random and returns a function that
# generates new random solutions without having to resupply the arguments.
# Created so we don't have to supply the arguments to grasp as well
def construct_randomized_greedy_from_given_inputs(edgelist,sorted_edgelist,n,k,L,alpha):
    return lambda: construct_randomized_greedy(edgelist,sorted_edgelist,n,k,L,alpha)

def add_lookback_edge(edgelist, solution, driver):
    # The solution maintains a set of chains of edges
    # that should've consolidated into one single chain now.
    # ch is that chain of edges.
    ch = solution.chains[0].edges

    # g is the set of edges that will turn the chain into a cycle
    g = (e for i, e in enumerate(edgelist) if e[0] == ch[0].u and
        e[1] == ch[-1].v or e[1] == ch[0].u and
        e[0] == ch[-1].v)

    # We pick the first of those edges.
    loopback_edge = next(g, None)
    add_loopback_edge(solution, Edge(loopback_edge[0], loopback_edge[1], driver, loopback_edge[2]))

def find_inner_vertex(solution, edge):
    for i in range(len(solution.chains)):
        ch = solution.chains[i]
        if len(ch.edges) == 1 and (edge.u == ch.edges[0].u and edge.v == ch.edges[0].v or
            edge.u == ch.edges[0].v and edge.v == ch.edges[0].u):
                return -1
        elif edge.u == ch.edges[0].u:
            return edge.v
        elif edge.v == ch.edges[0].u:
            return edge.u
        elif edge.u == ch.edges[-1].v:
            return edge.v
        elif edge.v == ch.edges[-1].v:
            return edge.u
    return -2