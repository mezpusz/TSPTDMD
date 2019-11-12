
from solution import Solution, Edge, insert_edge
from random import randint

def construct_deterministic(edgelist, n, k, L):
    A = L*k/n
    i = 0
    for j in range(len(edgelist)):
        if edgelist[j][2] < A:
            i = j
    print("A={},i={}".format(A,i))
    sol = Solution(k)
    j = i + 1
    l = 0
    while sol.num_edges < n-1:
        if i >= 0 and insert_edge(sol, Edge(edgelist[i][0], edgelist[i][1], l)):
            # evaluate here
            l = (l + 1) % k
        print("i={},j={},solution={}".format(i,j,sol))
        if j < len(edgelist) and insert_edge(sol, Edge(edgelist[j][0], edgelist[j][1], l)):
            # evaluate here
            l = (l + 1) % k
        print("i={},j={},solution={}".format(i,j,sol))
        i = i-1
        j = j+1

def construct_random(edgelist, n, k, L):
    s = Solution(k)
    i = randint(0, len(edgelist)-1)
    while s.num_edges < n-1:
        if insert_edge(s, Edge(edgelist[i][0], edgelist[i][1], l)):
            # evaluate here
            l = (l + 1) % k
        i = randint(0, len(edgelist)-1)
