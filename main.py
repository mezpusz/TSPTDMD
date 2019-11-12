from input import parse_input
from construction import construct_deterministic
import sys

if len(sys.argv) < 2:
    print('Filename should be given as first parameter!')
    exit(-1)

vertices, k, L = parse_input(sys.argv[1])
print("n={} k={} L={}".format(len(vertices), k, L))

edgelist = []
for u in range(len(vertices)-1):
    for v, d in vertices[u]:
        edgelist.append((u,v,d))
edgelist = sorted(edgelist, key=lambda x: x[2])
print(edgelist)

construct_deterministic(edgelist, len(vertices), k, L)
