
#include "solution.h"

#include <algorithm>

bool kDebug = false;
std::ostream nullstr(0);

std::ostream& operator<<(std::ostream& out, const Solution& sol) {
    for (const auto& ch : sol.chains) {
        out << "chain: " << ch << std::endl;
    }
    return out;
}

std::ostream& operator<<(std::ostream& out, const Chain& ch) {
    for (const auto& e : ch.edges) {
        out << e << ";";
    }
    return out;
}

std::ostream& operator<<(std::ostream& out, const Edge& e) {
    out << "(" << e.u << "," << e.v << ")";
    return out;
}

std::ostream& debug() {
    if(kDebug) {
        return std::cout;
    } else {
        return nullstr;
    }
}

Solution::Solution(int64_t k, int64_t L, int64_t n)
    : chains()
    , num_edges(0)
    , drivers(k, L)
    , L(L)
    , obj(L*L)
    , n(n)
{}

Solution::Solution(const Solution& other)
    : Solution(other.drivers.size(), other.L, other.n)
{
    chains = other.chains;
    num_edges = other.num_edges;
    drivers = other.drivers;
    obj = other.obj;
}

Solution& Solution::operator=(const Solution& other)
{
    chains = other.chains;
    num_edges = other.num_edges;
    drivers = other.drivers;
    L = other.L;
    obj = other.obj;
    n = other.n;
    return *this;
}

bool Solution::operator<(const Solution& other) {
    return obj < other.obj;
}

Chain::Chain(int64_t n, Edge e)
    : edges()
{
    edges.reserve(n);
    edges.push_back(e);
}

Chain::Chain(const Chain& other)
    : edges(other.edges)
{}

Edge::Edge(int64_t u, int64_t v, int64_t d, int64_t w)
    : u(u), v(v), driver(d), w(w)
{}

void Edge::update_weight(Edgelist* edgelist) {
    w = edgelist->at(u)[v];
}

bool Edge::operator<(const Edge& other) const {
    return w < other.w;
}

Driver::Driver(int64_t L)
    : obj_squared(L*L)
    , obj(L)
{}

bool Solution::insert_edge(Edge edge) {
    debug() << "inserting edge " << edge.u << "," << edge.v << std::endl;
    if (num_edges == 0) {
        chains.push_back(Chain(n, edge));
    } else {
        std::pair<int64_t, int64_t> ch_pair;
        auto res = find_chains(edge, ch_pair);
        if (!res) {
            return false;
        }
        int64_t ch1 = ch_pair.first;
        int64_t ch2 = ch_pair.second;
        if (ch1 != -1) {
            if (ch2 == ch1) {
                return false;
            } else if (ch2 != -1) {
                merge_chains(ch1, ch2, edge);
            } else {
                add_chain_edge(ch1, edge);
            }
        } else {
            chains.push_back(Chain(n, edge));
        }
    }
    num_edges++;
    std::vector<std::pair<int64_t, int64_t>> driver_map;
    driver_map.push_back(std::make_pair(edge.driver, edge.w));
    update_objective(driver_map);
    return true;
}

bool Solution::find_chains(Edge edge, std::pair<int64_t, int64_t>& ch_pair) const {
    int64_t ch1 = -1;
    int64_t ch2 = -1;
    for(int64_t i = 0; i < chains.size(); i++) {
        const auto& ch = chains[i];
        for(int64_t j = 0; j < ch.edges.size(); j++) {
            if (ch.edges[j].u == edge.u || ch.edges[j].u == edge.v) {
                if (j == 0) {
                    if (ch1 == -1) {
                        ch1 = i;
                    } else {
                        ch2 = i;
                    }
                // edge endpoint64_t is inside chain, we cannot add it
                } else {
                    return false;
                }
            }
            if (ch.edges[j].v == edge.u || ch.edges[j].v == edge.v) {
                if (j == ch.edges.size()-1) {
                    if (ch1 == -1) {
                        ch1 = i;
                    } else {
                        ch2 = i;
                    }
                // edge endpoint64_t is inside chain, we cannot add it
                } else {
                    return false;
                }
            }
        }
    }
    ch_pair.first = ch1;
    ch_pair.second = ch2;
    debug() << "Find chains: edge " << edge << ", solution "
            << *this << ", result " << ch1 << "," << ch2 << std::endl;
    return true;
}

void Solution::merge_chains(int64_t ch1, int64_t ch2, Edge edge) {
    bool front = false;
    auto* e1 = &chains[ch1].edges;
    auto* e2 = &chains[ch2].edges;
    front = add_chain_edge(ch1, edge);

    if (front) {
        if (e2->back().v != e1->at(0).u) {
            if (e2->size() > e1->size()) {
                reverse_chain(ch1);
                std::swap(e1,e2);
            } else {
                reverse_chain(ch2);
            }
        }
        // review
        e2->insert(e2->end(), e1->begin(), e1->end());
        chains[ch1].edges = *e2;
    } else {
        if (e2->at(0).u != e1->back().v) {
            if (e2->size() > e1->size()) {
                reverse_chain(ch1);
                std::swap(e1, e2);
            } else {
                reverse_chain(ch2);
            }
        }
        e1->insert(e1->end(), e2->begin(), e2->end());
        chains[ch1].edges = *e1;
    }
    chains.erase(chains.begin() + ch2);
    debug() << "Merge chains: edge " << edge << ", solution "
            << *this << ", result " << ch1 << "," << ch2 << std::endl;
}

void Solution::reverse_chain(int64_t ch) {
    for(auto& e : chains[ch].edges) {
        std::swap(e.u, e.v);
    }
    std::reverse(chains[ch].edges.begin(), chains[ch].edges.end());
}

// Returns True if the edge is added to the front
// and false if it is added to the back
bool Solution::add_chain_edge(int64_t ch, Edge edge) {
    auto& e = chains[ch].edges;
    if (e[0].u == edge.u or e[0].u == edge.v) {
        if (e[0].u == edge.u) {
            std::swap(edge.u, edge.v);
        }
        e.insert(e.begin(), edge);
        return true;
    } else if (e.back().v == edge.v or e.back().v == edge.u) {
        if (e.back().v == edge.v) {
            std::swap(edge.u, edge.v);
        }
        e.push_back(edge);
        return false;
    }
    return false;
}

void Solution::add_loopback_edge(Edge edge) {
    if (chains[0].edges[-1].v == edge.v) {
        std::swap(edge.u, edge.v);
    }
    chains[0].edges.push_back(edge);
    num_edges++;
    std::vector<std::pair<int64_t, int64_t>> driver_map;
    driver_map.push_back(std::make_pair(edge.driver, edge.w));
    update_objective(driver_map);
}

bool Solution::can_edge_be_added(Edge edge) const {
    std::pair<int64_t, int64_t> chain_pair;
    auto res = find_chains(edge, chain_pair);
    if (!res) {
        return false;
    }
    if (chain_pair.first != -1 && chain_pair.second == chain_pair.first) {
        return false;
    } else {
        return true;
    }
}

int64_t Solution::calculate_objective_with_edge(Edge edge) const {
    int64_t k = drivers.size();
    const auto& driver = drivers[edge.driver];
    auto old_obj = driver.obj_squared;
    auto new_obj = (driver.obj-edge.w)*(driver.obj-edge.w);
    return obj + (new_obj-old_obj)/k;
}

void Solution::update_objective(std::vector<std::pair<int64_t, int64_t>> driver_map) {
    int64_t k = drivers.size();
    for(auto [d, change] : driver_map) {
        auto& driver = drivers[d];
        obj -= driver.obj_squared/k;
        driver.obj -= change;
        driver.obj_squared = driver.obj * driver.obj;
        obj += driver.obj_squared/k;
    }
}
