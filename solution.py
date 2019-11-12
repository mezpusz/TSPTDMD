
class Solution:
    def __init__(self, k):
        self.chains = []
        self.num_edges = 0
        self.drivers = [Driver() for i in range(k)]
        self.obj = 0

    def __str__(self):
        res = "Chains "
        for ch in self.chains:
            res += str(ch) + ";"
        return res

class Chain:
    def __init__(self, e):
        self.edges = [e]

    def __str__(self):
        res = ""
        for e in self.edges:
            res += str(e) + ","
        return res

class Edge:
    def __init__(self, u, v, d):
        self.u = u
        self.v = v
        self.driver = d

    def __str__(self):
        return "({},{})d={}".format(self.u, self.v, self.driver)

class Driver:
    def __init__(self):
        self.obj_squared = 0
        self.obj = 0

def insert_edge(solution, edge):
    if solution.num_edges == 0:
        solution.chains.append(Chain(edge))
    else:
        ch1 = -1
        ch2 = -1
        for i in range(len(solution.chains)):
            ch = solution.chains[i]
            for j in range(len(ch.edges)):
                if ch.edges[j].u == edge.u or ch.edges[j].u == edge.v:
                    if j == 0:
                        if ch1 == -1:
                            ch1 = i
                        else:
                            ch2 = i
                    # edge endpoint is inside chain, we cannot add it
                    else:
                        return False
                if ch.edges[j].v == edge.u or ch.edges[j].v == edge.v:
                    if j == len(ch.edges)-1:
                        if ch1 == -1:
                            ch1 = i
                        else:
                            ch2 = i
                    # edge endpoint is inside chain, we cannot add it
                    else:
                        return False
        if ch1 != -1:
            if ch2 == ch1:
                return False
            elif ch2 != -1:
                merge_chains(solution, ch1, ch2, edge)
            else:
                add_chain_edge(solution, ch1, edge)
        else:
            solution.chains.append(Chain(edge))
    solution.num_edges += 1
    return True

def merge_chains(solution, ch1, ch2, edge):
    front = False
    e1 = solution.chains[ch1].edges
    e2 = solution.chains[ch2].edges
    front = add_chain_edge(solution, ch1, edge)

    if front:
        if e2[0].u != edge.u:
            reverse_chain(solution, ch2)
        solution.chains[ch1].edges = e2 + e1
    else:
        if e2[0].u != edge.v:
            reverse_chain(solution, ch2)
        solution.chains[ch1].edges = e1 + e2
    del solution.chains[ch2]

def reverse_chain(solution, ch):
    for e in solution.chains[ch].edges:
        e.u, e.v = e.v, e.u
    solution.chains[ch].edges = solution.chains[ch].edges.reverse()

# returns whether the edge was added in
# front or to the back of the chain
def add_chain_edge(solution, ch, edge):
    e = solution.chains[ch].edges
    if e[0].u == edge.u or e[0].u == edge.v:
        if e[0].u == edge.u:
            edge.u, edge.v = edge.v, edge.u
        e.insert(0, edge)
        return True
    elif e[-1].v == edge.v or e[-1].v == edge.u:
        if e[-1].v == edge.v:
            edge.u, edge.v = edge.v, edge.u
        e.append(edge)
        return False