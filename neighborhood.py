import logging
from solution import Chain, Edge, insert_edge, add_loopback_edge, update_objective
import copy
from random import randint
from math import ceil
from validate import validate_solution

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
            return ExchangeDriver(solution, self.edgelist)
        if self.index == 1:
            return DriverReversal(solution, self.edgelist)
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

    def next(self):
        if self.solution == None:
            return None
        num_edges = self.solution.num_edges
        orig_edges = self.solution.chains[0].edges
        for i in range(num_edges-2):
            newsol = copy.deepcopy(self.solution)
            newedges = newsol.chains[0].edges
            j = i+2
            for e in newedges[i+1:j]:
                e.u, e.v = e.v, e.u
            v_i = orig_edges[i]
            v_j = orig_edges[j]
            newedges[i].v = v_j.u
            newedges[j].u = v_i.v
            newedges[i].update_weight(self.edgelist)
            newedges[j].update_weight(self.edgelist)
            update_objective(newsol,
                [(v_i.driver, newedges[i].w-v_i.w),
                (v_j.driver, newedges[j].w-v_j.w)]
            )
            # validate_solution(newsol, self.edgelist)
            yield newsol
            while 1:
                j += 1
                if j == num_edges:
                    break
                k=j-1
                while k>i+1:
                    newedges[k].copy(newedges[k-1])
                    k-=1
                newedges[i+1].copy(orig_edges[j-1])
                newedges[i+1].u = orig_edges[j-1].v
                newedges[i+1].v = orig_edges[j-1].u
                v_j = orig_edges[j]
                newsol.obj = self.solution.obj
                newsol.drivers = copy.deepcopy(self.solution.drivers)
                newedges[i].v = v_j.u
                newedges[j].u = v_i.v
                newedges[i].update_weight(self.edgelist)
                newedges[j].update_weight(self.edgelist)
                update_objective(newsol,
                    [(v_i.driver, newedges[i].w-v_i.w),
                    (v_j.driver, newedges[j].w-v_j.w)]
                )
                # validate_solution(newsol, self.edgelist)
                yield newsol

    def random(self):
        if self.solution == None:
            return None
        num_edges = self.solution.num_edges
        i = randint(0, num_edges-1)
        j = randint(0, num_edges-1)
        while j <= i + 2:
            i = randint(0, num_edges-1)
            j = randint(0, num_edges-1)
        orig_edges = self.solution.chains[0].edges
        newsol = copy.deepcopy(self.solution)
        newedges = newsol.chains[0].edges
        for e in newedges[i+1:j]:
            e.u, e.v = e.v, e.u
        v_i = orig_edges[i]
        v_j = orig_edges[j]
        newedges[i].v = v_j.u
        newedges[j].u = v_i.v
        newedges[i].update_weight(self.edgelist)
        newedges[j].update_weight(self.edgelist)
        update_objective(newsol,
            [(v_i.driver, newedges[i].w-v_i.w),
            (v_j.driver, newedges[j].w-v_j.w)]
        )
        # validate_solution(newsol, self.edgelist)
        return newsol

# Cuts out two parts of the route and exchanges them
class ShortBlockMove(Neighborhood):
    def __init__(self, solution, edgelist):
        self.solution = solution
        self.edgelist = edgelist
        self.l = 3

    def next(self):
        if self.solution == None:
            return None
        num_edges = self.solution.num_edges
        orig_edges = self.solution.chains[0].edges
        for i in range(num_edges-2):
            newsol = copy.deepcopy(self.solution)
            newedges = newsol.chains[0].edges
            j = i+2
            # copy block edges to their positions
            for k in range(self.l):
                newedges[(i+k+1) % num_edges].copy(orig_edges[(j+k+1) % num_edges])
            # move edges that were before the block after the block
            for k in range(j-i):
                newedges[(i+self.l+k+1) % num_edges].copy(orig_edges[(i+k+1) % num_edges])
            v_i = orig_edges[i]
            v_j = orig_edges[j]
            v_k = orig_edges[(j+self.l) % num_edges]
            # update edge endpoints where the block has been copied
            newedges[i].v = v_j.v
            newedges[i].update_weight(self.edgelist)
            newedges[(i+self.l) % num_edges].v = v_i.v
            newedges[(i+self.l) % num_edges].update_weight(self.edgelist)
            # update edge endpoints where the block was
            newedges[(j+self.l) % num_edges].v = v_k.v
            newedges[(j+self.l) % num_edges].update_weight(self.edgelist)
            update_objective(newsol,
                [(v_i.driver, newedges[i].w-v_i.w),
                (v_j.driver, newedges[(j+self.l) % num_edges].w-v_j.w),
                (v_k.driver, newedges[(i+self.l) % num_edges].w-v_k.w)])
            # validate_solution(newsol, self.edgelist)
            yield newsol
            while 1:
                j += 1
                if j + self.l >= num_edges:
                    break
                # move all edges one down in new block position
                old_u = newedges[i+1%num_edges].u
                old_driver = newedges[i+1%num_edges].driver
                for k in range(i+1, i+self.l):
                    newedges[k%num_edges].copy(newedges[(k+1)%num_edges])
                # update edge before block
                newedges[i].v = newedges[i+1].u
                newedges[i].update_weight(self.edgelist)
                # update edges at the end of block
                newedges[(i+self.l-1)%num_edges].copy(orig_edges[(j+self.l-1)%num_edges])
                newedges[(i+self.l)%num_edges].copy(orig_edges[(j+self.l)%num_edges])
                newedges[(i+self.l)%num_edges].v = v_i.v
                newedges[(i+self.l)%num_edges].update_weight(self.edgelist)

                # update edges at where the block was
                newedges[(j+self.l-1)%num_edges].v = old_u
                newedges[(j+self.l-1)%num_edges].update_weight(self.edgelist)
                newedges[(j+self.l)%num_edges].u = old_u
                newedges[(j+self.l)%num_edges].driver = old_driver
                newedges[(j+self.l)%num_edges].update_weight(self.edgelist)

                # reset objective
                newsol.obj = self.solution.obj
                newsol.drivers = copy.deepcopy(self.solution.drivers)
                v_j = orig_edges[j]
                v_k = orig_edges[(j+self.l) % num_edges]
                update_objective(newsol,
                    [(v_i.driver, newedges[i].w-v_i.w),
                    (v_j.driver, newedges[(j+self.l) % num_edges].w-v_j.w),
                    (v_k.driver, newedges[(i+self.l) % num_edges].w-v_k.w)])
                # validate_solution(newsol, self.edgelist)
                yield newsol

    def random(self):
        if self.solution == None:
            return None
        num_edges = self.solution.num_edges
        i = randint(0, num_edges-1)
        j = randint(0, num_edges-1)
        while j + self.l >= num_edges or j <= i + 2:
            i = randint(0, num_edges-1)
            j = randint(0, num_edges-1)
        num_edges = self.solution.num_edges
        orig_edges = self.solution.chains[0].edges
        newsol = copy.deepcopy(self.solution)
        newedges = newsol.chains[0].edges
        # copy block edges to their positions
        for k in range(self.l):
            newedges[(i+k+1) % num_edges].copy(orig_edges[(j+k+1) % num_edges])
        # move edges that were before the block after the block
        for k in range(j-i):
            newedges[(i+self.l+k+1) % num_edges].copy(orig_edges[(i+k+1) % num_edges])
        v_i = orig_edges[i]
        v_j = orig_edges[j]
        v_k = orig_edges[(j+self.l) % num_edges]
        # update edge endpoints where the block has been copied
        newedges[i].v = v_j.v
        newedges[i].update_weight(self.edgelist)
        newedges[(i+self.l) % num_edges].v = v_i.v
        newedges[(i+self.l) % num_edges].update_weight(self.edgelist)
        # update edge endpoints where the block was
        newedges[(j+self.l) % num_edges].v = v_k.v
        newedges[(j+self.l) % num_edges].update_weight(self.edgelist)
        update_objective(newsol,
            [(v_i.driver, newedges[i].w-v_i.w),
            (v_j.driver, newedges[(j+self.l) % num_edges].w-v_j.w),
            (v_k.driver, newedges[(i+self.l) % num_edges].w-v_k.w)])
        # validate_solution(newsol, self.edgelist)
        return newsol

# The neighborhood consist of keeping the same route,
# but switching pairs of drivers
class ExchangeDriver(Neighborhood):
    def __init__(self, solution, edgelist):
        self.solution = solution
        self.edgelist = edgelist

    def next(self):
        if self.solution == None:
            return None
        for i in range(self.solution.num_edges-1):
            j = i+1
            newsol = copy.deepcopy(self.solution)
            newedges = newsol.chains[0].edges
            e_i = newedges[i]
            e_j = newedges[j]
            update_objective(newsol, [(e_i.driver, e_j.w-e_i.w), (e_j.driver, e_i.w-e_j.w)])
            e_i.driver, e_j.driver = e_j.driver, e_i.driver
            # validate_solution(newsol, self.edgelist)
            yield newsol
            while 1:
                j+=1
                if j == self.solution.num_edges:
                    break
                # change back drivers
                e_i.driver, e_j.driver = e_j.driver, e_i.driver
                e_j = newedges[j]
                # reset objective
                newsol.obj = self.solution.obj
                newsol.drivers = copy.deepcopy(self.solution.drivers)
                update_objective(newsol,
                    [(e_i.driver, e_j.w-e_i.w),
                    (e_j.driver, e_i.w-e_j.w)]
                )
                e_i.driver, e_j.driver = e_j.driver, e_i.driver
                # validate_solution(newsol, self.edgelist)
                yield newsol

    def random(self):
        if self.solution == None:
            return None
        num_edges = self.solution.num_edges
        i = randint(0, num_edges-1)
        j = randint(0, num_edges-1)
        newsol = copy.deepcopy(self.solution)
        newedges = newsol.chains[0].edges
        e_i = newedges[i]
        e_j = newedges[j]
        update_objective(newsol, [(e_i.driver, e_j.w-e_i.w), (e_j.driver, e_i.w-e_j.w)])
        e_i.driver, e_j.driver = e_j.driver, e_i.driver
        # validate_solution(newsol, self.edgelist)
        return newsol

# Reverses the order of drivers in a part of the route
class DriverReversal(Neighborhood):
    def __init__(self, solution, edgelist):
        self.solution = solution
        self.edgelist = edgelist
        self.i = 0
        self.j = 2

    def next(self):
        if self.solution == None:
            return None
        num_edges = self.solution.num_edges
        for i in range(num_edges-2):
            j = i+2
            newsol = copy.deepcopy(self.solution)
            newedges = newsol.chains[0].edges
            k = i
            l = j
            while k < l:
                e_k = newedges[k]
                e_l = newedges[l]
                update_objective(newsol, [(e_k.driver, e_l.w-e_k.w), (e_l.driver, e_k.w-e_l.w)])
                e_k.driver, e_l.driver = e_l.driver, e_k.driver
                k+=1
                l-=1
            # validate_solution(newsol, self.edgelist)
            yield newsol
            while 1:
                j+=1
                if j == num_edges:
                    break
                k=j
                driver_changes = [0 for d in newsol.drivers]
                while k>=i+1:
                    driver_changes[newedges[k].driver] -= newedges[k].w
                    driver_changes[newedges[k-1].driver] += newedges[k].w
                    newedges[k].driver = newedges[k-1].driver
                    k-=1
                new_j = self.solution.chains[0].edges[j]
                driver_changes[newedges[i].driver] -= newedges[i].w
                driver_changes[new_j.driver] += newedges[i].w
                newedges[i].driver = new_j.driver
                driver_map = [(i,v) for i,v in enumerate(driver_changes)]
                update_objective(newsol, driver_map)
                # validate_solution(newsol, self.edgelist)
                yield newsol

    def random(self):
        if self.solution == None:
            return None
        num_edges = self.solution.num_edges
        i = randint(0, num_edges-1)
        j = randint(0, num_edges-1)
        while (j + 1) % num_edges == i or (j - 1) % num_edges == i:
            i = randint(0, num_edges-1)
            j = randint(0, num_edges-1)
        newsol = copy.deepcopy(self.solution)
        k = i
        l = j
        while k < l:
            e_k = newsol.chains[0].edges[k]
            e_l = newsol.chains[0].edges[l]
            update_objective(newsol, [(e_k.driver, e_l.w-e_k.w), (e_l.driver, e_k.w-e_l.w)])
            e_k.driver, e_l.driver = e_l.driver, e_k.driver
            k+=1
            l-=1
        # validate_solution(newsol, self.edgelist)
        return newsol

# returns a solution n random steps away in the relevant neighborhood
def n_step(solution, neighborhood_fac, n):
    count = 1
    while count <= n:
        solution = neighborhood_fac.get(solution).random()
        count += 1
    return solution
