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
        # Break the chain into two by removing two edges
        # i and j are removed so the remaining are added
        chain1 = Chain(orig_edges, self.i+1, self.j-1)
        chain2 = Chain(orig_edges, self.j+1, self.i-1)
        newsol = copy.deepcopy(self.solution)
        newsol.chains = [chain1, chain2]
        # The number of edges is decreased by 2,
        # we later add these edges back
        newsol.num_edges = self.solution.num_edges-2
        v_i = orig_edges[self.i]
        v_j = orig_edges[self.j]
        # Add the first cross edge, consisting of
        # the second vertices of the removed edges
        insert_edge(newsol, Edge(v_i.v, v_j.v, v_i.driver, self.edgelist[v_i.v][v_j.v]))
        # Add the second cross edge
        add_loopback_edge(newsol, Edge(v_i.u, v_j.u, v_j.driver, self.edgelist[v_i.u][v_j.u]))
        # Update values for next iteration:
        # * j should be always at least two positions away from i
        #   otherwise the operation doesn't make sense
        # * all operations are modulo the cycle length
        # * when the neighborhood is traversed, solution becomes
        #   None, so the next iteration won't give anything
        if (self.j + 2) % self.solution.num_edges == self.i:
            self.i += 1
            self.i %= self.solution.num_edges
            self.j = (self.i + 2) % self.solution.num_edges
            if self.i == 0 and self.j == 2:
                self.solution = None
        else:
            self.j = (self.j + 1) % self.solution.num_edges
        return newsol

class ExchangeDriver(Neighborhood):
    def __init__(self, solution, k):
        self.solution = solution
        self.i = 0
        self.j = 1

    def next(self):
        if self.solution == None:
            return None
        newsol = copy.deepcopy(self.solution)
        e_i = newsol.chains[0].edges[self.i]
        e_j = newsol.chains[0].edges[self.j]
        e_i.d, e_j.d = e_j.d, e_i.d
        # Update values for next iteration:
        # * when the neighborhood is traversed, solution becomes
        #   None, so the next iteration won't give anything
        if self.j + 1 == self.solution.num_edges:
            self.i += 1
            if self.i == self.solution.num_edges:
                self.solution = None
            self.j = self.i + 1
        else:
            self.j += 1
        return newsol
