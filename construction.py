from solution import Solution, Edge, insert_edge, add_loopback_edge
from random import randint

# edgelist should be sorted
# n = nr. of vertices
# k = nr. of drivers
# L = desired travel distance for each driver
def construct_deterministic(edgelist, n, k, L):
    # A = desired average travel distance to each node
    A = L*k/n
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
        if i >= 0 and insert_edge(sol, Edge(edgelist[i][0], edgelist[i][1], l, edgelist[i][2])):
            l = (l + 1) % k   # Next drier
        print("i={},j={},solution={}".format(i,j,sol))

        # Try to add the edge with weight just above A
        if j < len(edgelist) and insert_edge(sol, Edge(edgelist[j][0], edgelist[j][1], l, edgelist[i][2])):
            l = (l + 1) % k   # Next driver
        print("i={},j={},solution={}".format(i,j,sol))

        # update i and j to reflect that we've added 2 more edges to the solution
        # or that that edge is unable to be added anyway
        i = i-1
        j = j+1

    # The solution maintains a set of chains of edges
    # that should've consolidated into one single chain now.
    # ch is that chain of edges.
    ch = sol.chains[0].edges

    # g is the set of edges that will turn the chain into a cycle
    g = (e for i, e in enumerate(edgelist) if e[0] == ch[0].u and
        e[1] == ch[-1].v or e[1] == ch[0].u and
        e[0] == ch[-1].v)

    # We pick the first of those edges.
    loopback_edge = next(g, None)
    add_loopback_edge(sol, Edge(loopback_edge[0], loopback_edge[1], l, loopback_edge[2]))
    print("solution={}".format(sol))

# NOt working yet
def construct_random(edgelist, n, k, L):
    s = Solution(k, L)
    i = randint(0, len(edgelist)-1)

    # insert random edge
    while s.num_edges < n-1:
        if insert_edge(s, Edge(edgelist[i][0], edgelist[i][1], l, edgelist[i][2])):
            # evaluate here
            l = (l + 1) % k  # next driver
        i = randint(0, len(edgelist)-1)
