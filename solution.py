import copy

class Solution:
    def __init__(self, k, L):
        # A list of chains of edges, since an unfinished solution
        # might not be constructed as one single continuous chain
        self.chains = []
        self.num_edges = 0
        self.drivers = [Driver(L) for i in range(k)]
        self.L = L
        self.obj = L ** 2

    def __str__(self):
        res = "(objective=" + str(self.obj) + ",chains="
        for ch in self.chains:
            res += str(ch) + ";"
        res += ")"
        return res

    def __lt__(self, other):
        return self.obj < other.obj

    def copy(self):
        new = Solution(len(self.drivers), self.L)
        new.num_edges = self.num_edges
        new.drivers = copy.deepcopy(self.drivers)
        new.obj = self.obj
        return new

class Chain:
    def __init__(self, edges, i, j):
        if i <= j:
            self.edges = copy.deepcopy(edges[i:j+1])
        else:
            self.edges = copy.deepcopy(edges[i:])
            if j >= 0:
                 self.edges += copy.deepcopy(edges[:j+1])

    def __eq__(self, other):
        return self.edges == other.edges

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

    def copy(self, other):
        self.u = other.u
        self.v = other.v
        self.driver = other.driver
        self.w = other.w

    def update_weight(self, edgelist):
        self.w = edgelist[self.u][self.v]

    def __eq__(self, other):
        return self.u == other.u and self.v == other.v and self.driver == other.driver and self.w == other.w

    def __str__(self):
        return "({},{})d={},w={}".format(self.u, self.v, self.driver, self.w)

class Driver:
    def __init__(self, L):
        self.obj_squared = L ** 2
        self.obj = L

    def __eq__(self, other):
        return self.obj == other.obj

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
    update_objective(solution, [(edge.driver, edge.w)])
    return True

def merge_chains(solution, ch1, ch2, edge):
    front = False
    e1 = solution.chains[ch1].edges
    e2 = solution.chains[ch2].edges
    front = add_chain_edge(solution, ch1, edge)

    if front:
        if e2[-1].v != e1[0].u:
            if len(e2) > len(e1):
                reverse_chain(solution, ch1)
                e1, e2 = e2, e1
            else:
                reverse_chain(solution, ch2)
        solution.chains[ch1].edges = e2 + e1
    else:
        if e2[0].u != e1[-1].v:
            if len(e2) > len(e1):
                reverse_chain(solution, ch1)
                e1, e2 = e2, e1
            else:
                reverse_chain(solution, ch2)
        solution.chains[ch1].edges = e1 + e2
    del solution.chains[ch2]

def reverse_chain(solution, ch):
    for e in solution.chains[ch].edges:
        e.u, e.v = e.v, e.u
    solution.chains[ch].edges.reverse()

# Returns True if the edge is added to the front
# and false if it is added to the back
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
    update_objective(solution, [(edge.driver, edge.w)])

def can_edge_be_added(solution, edge):
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
    if ch1 != -1 and ch2 == ch1:
        return False
    else:
        return True

def calculate_objective_with_edge(solution, edge):
    k = len(solution.drivers)
    driver = solution.drivers[edge.driver]
    return solution.obj - int(driver.obj_squared/k) + ((driver.obj+edge.w)**2)/k

def update_objective(solution, driver_map):
    k = len(solution.drivers)
    for d, change in driver_map:
        driver = solution.drivers[d]
        solution.obj -= int(driver.obj_squared/k)
        driver.obj -= change
        driver.obj_squared = driver.obj ** 2
        solution.obj += int(driver.obj_squared/k)

def monolithic_objective(solution):
    obj = solution.L**2
    k = len(solution.drivers)
    for driver in solution.drivers:
        obj += int(driver.obj_squared/k)
    return obj


def choose_obj(new, prev, delta_eval):
    if delta_eval:
        return new < prev
    else:
        return monolithic_objective(new) < prev.obj
