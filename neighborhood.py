import logging
from solution import Chain, Edge, insert_edge, add_loopback_edge, update_objective
import copy
from random import randint
from math import ceil

class NeighborhoodFactory():
    def __init__(self, edgelist, name='ExchangeDriver'):
        self.edgelist = edgelist
        if name == 'ExchangeDriver' or name == "ed":
            self.index = 0
        elif name == 'DriverReversal' or name == 'dr':
            self.index = 1
        elif name == 'ShortBlockMove' or name == 'sbm':
            self.index = 2
        elif name == 'Reversal' or name == 'r':
            self.index = 3
        else:
            raise Exception("No such neighborhood: {}".format(name))

    def set_index(self, i):
        self.index = i % 4


    def get(self, solution):
        if self.index == 0:
            return ExchangeDriver(solution)
        if self.index == 1:
            return DriverReversal(solution)
        elif self.index == 2:
            return ShortBlockMove(solution, self.edgelist)
        else:
            return Reversal(solution, self.edgelist)

class Neighborhood():
    def next(self):
        raise Exception("Not implemented")

    def random(self):
        raise Exception("Not implemented")

# reverses part of the route
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
        newsol = self.solution.copy()
        newsol.chains = [chain1, chain2]
        # The number of edges is decreased by 2,
        # we later add these edges back
        newsol.num_edges = self.solution.num_edges-2
        v_i = orig_edges[self.i]
        v_j = orig_edges[self.j]
        update_objective(newsol, [(v_i.driver, -v_i.w), (v_j.driver, -v_j.w)])
        # Add the first cross edge, consisting of
        # the second vertices of the removed edges
        insert_edge(newsol, Edge(v_i.v, v_j.v, v_i.driver, self.edgelist[v_i.v][v_j.v]))
        # Add the second cross edge
        add_loopback_edge(newsol, Edge(v_i.u, v_j.u, v_j.driver, self.edgelist[v_i.u][v_j.u]))
        # Update values for next iteration:
        # * j should be always at least two positions away from i
        #   otherwise the operation doesn't make sense
        # * j should not go above 2 when it goes around because
        #   those are duplicate solutions
        # * all operations are modulo the cycle length
        # * when the neighborhood is traversed, solution becomes
        #   None, so the next iteration won't give anything
        if (self.j + 2) % self.solution.num_edges == self.i or self.j == 2:
            self.i += 1
            self.i %= self.solution.num_edges
            self.j = (self.i + 2) % self.solution.num_edges
            if self.i == 0 and self.j == 2:
                self.solution = None
        else:
            self.j = (self.j + 1) % self.solution.num_edges
        return newsol

    def random(self):
        old_i = self.i
        old_j = self.j
        num_edges = self.solution.num_edges
        self.i = randint(0, num_edges-1)
        self.j = randint(0, num_edges-1)
        while (self.j + 1) % num_edges == self.i or (self.j - 1) % num_edges == self.i:
            self.i = randint(0, num_edges-1)
            self.j = randint(0, num_edges-1)
        newsol = self.next()
        self.i = old_i
        self.j = old_j
        return newsol

# Cuts out two parts of the route and exchanges them
class ShortBlockMove(Neighborhood):
    def __init__(self, solution, edgelist):
        self.solution = solution
        self.edgelist = edgelist
        self.i = 0
        self.j = 2
        self.l = 3
        # Sanity check to see whether the operation makes sense at all
        if (self.j + self.l + 1) >= self.solution.num_edges:
            self.solution = None

    def next(self):
        if self.solution == None:
            return None
        # logging.debug(str(self.i) + " " + str(self.j))
        orig_edges = self.solution.chains[0].edges
        num_edges = self.solution.num_edges
        # Break the chain into two by removing two edges
        # i and j are removed so the remaining are added
        chain1 = Chain(orig_edges, self.i+1, self.j-1)
        chain2 = Chain(orig_edges, self.j+1, (self.j+self.l-1) % num_edges)
        chain3 = Chain(orig_edges, (self.j+self.l+1) % num_edges, self.i-1)
        newsol = self.solution.copy()
        newsol.chains = [chain1, chain2, chain3]
        # The number of edges is decreased by 3,
        # we later add these edges back
        newsol.num_edges = num_edges-3
        v_i = orig_edges[self.i]
        v_j = orig_edges[self.j]
        v_k = orig_edges[(self.j+self.l) % num_edges]
        update_objective(newsol,
            [(v_i.driver, -v_i.w),
             (v_j.driver, -v_j.w),
             (v_k.driver, -v_k.w)])

        # Insert block at position i
        insert_edge(newsol, Edge(v_i.u, v_j.v, v_i.driver, self.edgelist[v_i.u][v_j.v]))
        insert_edge(newsol, Edge(v_k.u, v_i.v, v_k.driver, self.edgelist[v_k.u][v_i.v]))
        # Add missing edge where the block was before
        add_loopback_edge(newsol, Edge(v_j.u, v_k.v, v_j.driver, self.edgelist[v_j.u][v_k.v]))
        #print('next: i={},j={},sol={}'.format(self.i, self.j, newsol))
        # Update values for next iteration:
        # * j starts two positions away from i and it goes
        #   until the removed edge after the block is the
        #   same as i otherwise it doesn't make sense
        # * all operations are modulo the cycle length
        # * when the neighborhood is traversed, solution becomes
        #   None, so the next iteration won't give anything
        if (self.j + self.l + 2) % num_edges == self.i:
            self.i += 1
            self.i %= num_edges
            self.j = (self.i + 2) % num_edges
            if self.i == 0 and self.j == 2:
                self.solution = None
        else:
            self.j = (self.j + 1) % num_edges
        return newsol

    def random(self):
        old_i = self.i
        old_j = self.j
        num_edges = self.solution.num_edges
        self.i = randint(0, num_edges-1)
        self.j = randint(0, num_edges-1)
        while (self.j + self.l + 1) % num_edges == self.i or (self.j - 1) % num_edges == self.i:
            self.i = randint(0, num_edges-1)
            self.j = randint(0, num_edges-1)
        # logging.debug(str(self.i) + " " + str(self.j))
        newsol = self.next()
        self.i = old_i
        self.j = old_j
        return newsol

# The neighborhood consist of keeping the same route,
# but switching pairs of drivers
class ExchangeDriver(Neighborhood):
    def __init__(self, solution):
        self.solution = solution
        self.i = 0
        self.j = 1

    def next(self):
        if self.solution == None:
            return None
        newsol = copy.deepcopy(self.solution)
        e_i = newsol.chains[0].edges[self.i]
        e_j = newsol.chains[0].edges[self.j]
        update_objective(newsol, [(e_i.driver, e_j.w-e_i.w), (e_j.driver, e_i.w-e_j.w)])
        e_i.driver, e_j.driver = e_j.driver, e_i.driver
        # Update values for next iteration:
        # * when the neighborhood is traversed, solution becomes
        #   None, so the next iteration won't give anything
        if self.j + 1 == self.solution.num_edges:
            self.i += 1
            self.j = self.i + 1
            # I added + 1 because otherwise self.j would be self.solution.num_edges
            if self.i + 1 == self.solution.num_edges:
                self.solution = None
        else:
            self.j += 1

        return newsol

    def random(self):
        old_i = self.i
        old_j = self.j
        num_edges = self.solution.num_edges
        self.i = randint(0, num_edges-1)
        self.j = randint(0, num_edges-1)
        while self.j == self.i:
            self.i = randint(0, num_edges-1)
            self.j = randint(0, num_edges-1)
        newsol = self.next()
        self.i = old_i
        self.j = old_j
        return newsol

# Reverses the order of drivers in a part of the route
class DriverReversal(Neighborhood):
    def __init__(self, solution):
        self.solution = solution
        self.i = 0
        self.j = 2

    def next(self):
        if self.solution == None:
            return None
        newsol = copy.deepcopy(self.solution)
        k = self.i
        l = self.j
        while k < l:
            e_k = newsol.chains[0].edges[k]
            e_l = newsol.chains[0].edges[l]
            update_objective(newsol, [(e_k.driver, e_l.w-e_k.w), (e_l.driver, e_k.w-e_l.w)])
            e_k.driver, e_l.driver = e_l.driver, e_k.driver
            k+=1
            l-=1
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

    def random(self):
        old_i = self.i
        old_j = self.j
        num_edges = self.solution.num_edges
        self.i = randint(0, num_edges-1)
        self.j = randint(0, num_edges-1)
        while (self.j + 1) % num_edges == self.i or (self.j - 1) % num_edges == self.i:
            self.i = randint(0, num_edges-1)
            self.j = randint(0, num_edges-1)
        newsol = self.next()
        self.i = old_i
        self.j = old_j
        return newsol


# returns a solution n random steps away in the relevant neighborhood
def n_step(solution, neighborhood_fac, n):
    count = 1
    while count <= n:
        solution = neighborhood_fac.get(solution).random()
        count += 1
    return solution
