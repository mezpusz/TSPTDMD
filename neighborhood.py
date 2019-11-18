from solution import Chain, Edge, insert_edge, add_loopback_edge
import copy

class Neighborhood():
    def next(self):
        raise Exception("Not implemented")

    def random(self):
        raise Exception("Not implemented")

class Reversal(Neighborhood):
    def __init__(self, solution, edgelist):
        self.solution = solution
        self.edgelist = edgelist
        self.i = 0
        self.j = 2

    def next(self):
        if self.solution == None:
            return None
        orig_edges = self.solution.chains[0].edges
        chain1 = Chain(orig_edges, self.i+1, self.j-1)
        chain2 = Chain(orig_edges, self.j+1, self.i-1)
        newsol = copy.deepcopy(self.solution)
        newsol.chains = [chain1, chain2]
        newsol.num_edges = self.solution.num_edges-2
        v_i = orig_edges[self.i]
        v_j = orig_edges[self.j]
        #print("i={},j={}".format(self.i, self.j))
        #print("Before next: "+str(v_i)+str(v_j)+"  "+str(newsol))
        insert_edge(newsol, Edge(v_i.v, v_j.v, v_i.driver, self.edgelist[v_i.v][v_j.v]))
        #print("During next: "+str(newsol))
        add_loopback_edge(newsol, Edge(v_i.u, v_j.u, v_j.driver, self.edgelist[v_i.u][v_j.u]))
        #print("next: " + str(newsol))
        if (self.j + 2) % self.solution.num_edges == self.i:
            self.i += 1
            self.i %= self.solution.num_edges
            self.j = (self.i + 2) % self.solution.num_edges
            if self.i == 0 and self.j == 2:
                self.solution = None
        else:
            self.j = (self.j + 1) % self.solution.num_edges
        return newsol