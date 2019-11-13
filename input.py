
import math

def parse_input(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        if str.startswith(lines[0], 'EDGELIST'):
            return edgelist(lines[1:])
        elif str.startswith(lines[0], 'COORDS'):
            return coords(lines[1:])
        else:
            pass

def edgelist(lines):
    n, m, k, L = map(int, lines[0].split())
    vertices = [[-1 for j in range(n)] for i in range(n)]
    weights = []
    for i in range(m):
        u, v, w = map(int, lines[i+1].split())
        vertices[u][v] = w
        vertices[v][u] = w
        weights.append(w)
    weights = sorted(weights, reverse=True)
    M = L
    for i in range(n):
        M -= weights[i]
    M = math.ceil((M ** 2 + (k-1)*L ** 2)/k)
    print("M=" + str(M))
    for u in vertices:
        for v in range(len(u)):
            if u[v] == -1:
                u[v] = M
    return vertices, k, L

def coords(lines):
    n, k, L = map(int, lines[0].split())
    vertices = [[] for i in range(n)]
    return vertices, k, L
