import copy

class Solution:
    def __init__(self, k, L):
        self.chains = []
        self.num_edges = 0
        self.drivers = [Driver(L) for i in range(k)]
        self.obj = L ** 2

    def __str__(self):
        res = "(objective=" + str(self.obj) + ",chains="
        for ch in self.chains:
            res += str(ch) + ";"
        res += ")"
        return res

    def __lt__(self, other):
        return self.obj < other.obj

class Chain:
    def __init__(self, edges, i, j):
        if i <= j:
            self.edges = copy.deepcopy(edges[i:j+1])
        else:
            self.edges = copy.deepcopy(edges[i:])
            if j >= 0:
                 self.edges = self.edges + copy.deepcopy(edges[:j+1])
            #reverse_edges(self)

    def __str__(self):
        res = ""
        for e in self.edges:
            res += str(e) + ","
        return res

class Edge:
    def __init__(self, u, v, d, w):
        self.u = u
        self.v = v
        self.driver = d
        self.w = w

    def __str__(self):
        return "({},{})d={},w={}".format(self.u, self.v, self.driver, self.w)

class Driver:
    def __init__(self, L):
        self.obj_squared = L ** 2
        self.obj = L

def insert_edge(solution, edge):
    if solution.num_edges == 0:
        solution.chains.append(Chain([edge], 0, 0))
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
            solution.chains.append(Chain([edge], 0, 0))
    solution.num_edges += 1
    update_objective(solution, [(edge.driver, -edge.w)])
    return True

def merge_chains(solution, ch1, ch2, edge):
    front = False
    e1 = solution.chains[ch1].edges
    e2 = solution.chains[ch2].edges
    front = add_chain_edge(solution, ch1, edge)

    if front:
        if e2[-1].v != e1[0].u:
            reverse_chain(solution, ch2)
        solution.chains[ch1].edges = e2 + e1
    else:
        if e2[0].u != e1[-1].v:
            reverse_chain(solution, ch2)
        solution.chains[ch1].edges = e1 + e2
    del solution.chains[ch2]

def reverse_chain(solution, ch):
    reverse_edges(solution.chains[ch])

def reverse_edges(ch):
    for e in ch.edges:
        e.u, e.v = e.v, e.u
    ch.edges.reverse()

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

def add_loopback_edge(solution, edge):
    if solution.chains[0].edges[-1].v == edge.v:
        edge.u, edge.v = edge.v, edge.u
    solution.chains[0].edges.append(edge)
    solution.num_edges += 1
    update_objective(solution, [(edge.driver, -edge.w)])

def update_objective(solution, driver_map):
    for d, change in driver_map:
        driver = solution.drivers[d]
        solution.obj -= driver.obj_squared
        driver.obj += change
        driver.obj_squared = driver.obj ** 2
        solution.obj += driver.obj_squared
