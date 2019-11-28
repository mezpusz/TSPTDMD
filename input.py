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

    # Seems to me it could be M = L - sum(weights)?
    M = L
    for i in range(n):
        M -= weights[i]

    # Let M be a value larger than any of the existing weights
    M = math.ceil((M ** 2 + (k-1)*L ** 2)/k)
    print("M=" + str(M))
    # and assign it to invalid edges:
    for u in vertices:
        for v in range(len(u)):
            if u[v] == -1:
                u[v] = M
    return vertices, k, L

def coords(lines):
    n, k, L = map(int, lines[0].split())
    coordinates = []
    vertices = [[-1 for j in range(n)] for i in range(n)]
    for i in range(n):
        x, y = map(int, lines[i+1].split())
        coordinates.append((x,y))
    for i in range(n):
        for j in range(i+1, n):
            dist_x = (coordinates[i][0] - coordinates[j][0])**2
            dist_y = (coordinates[i][1] - coordinates[j][1])**2
            dist = math.sqrt(dist_x+dist_y)
            #TODO: look out for rounding here
            vertices[i][j] = int(dist)
            vertices[i][j] = int(dist)
    return vertices, k, L
