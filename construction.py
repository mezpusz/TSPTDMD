from solution import Solution, Edge, insert_edge, add_loopback_edge, Chain, update_objective
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
    validate_solution(sol, edgelist)
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

# Takes the input to construct random and returns a function that
# generates new random solutions without having to resupply the arguments.
# Created so we don't have to supply the arguments to grasp as well
def construct_random_from_given_inputs(edgelist,n,k,L):
    return lambda: construct_random(edgelist,n,k,L)

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
