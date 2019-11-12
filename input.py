
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
    vertices = [[] for i in range(n)]
    for i in range(m):
        i, j, w = map(int, lines[i+1].split())
        vertices[i].append((j, w))
        vertices[j].append((i, w))
    return vertices, k, L

def coords(lines):
    n, k, L = map(int, lines[0].split())
    vertices = [[] for i in range(n)]
    return vertices, k, L
