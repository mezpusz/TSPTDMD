from solution import Solution, Edge, insert_edge, add_loopback_edge
from random import randint

# edgelist should be sorted
# n = nr. of vertices
# k = nr. of drivers
# L = desired travel distance for each driver
def construct_deterministic(edgelist, n, k, L):
    print('Constructing solution deterministically')
    # A = desired average travel distance to each node
    A = int(L*k/n)
    i = 0

    # i is set to index of last edge with weight < A
    for j in range(len(edgelist)):
        if edgelist[j][2] < A:
            i = j
    print("A={},i={}".format(A,i))

    # j is set to index of first edge with weight >= A
    j = i + 1

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
        if i >= 0 and j < len(edgelist):
            if abs(edgelist[i][2] - A) < abs(edgelist[j][2] - A):
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
        if insert_edge(sol, Edge(edgelist[index][0], edgelist[index][1], l, edgelist[index][2])):
            l = (l + 1) % k   # Next driver
        #print("i={},j={},obj={}".format(i,j,sol.obj))

    add_lookback_edge(edgelist, sol, l)
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
