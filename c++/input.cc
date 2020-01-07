#include "input.h"
#include <fstream>
#include <algorithm>
#include <cmath>

__int128_t proper_round(double num) {
    __int128_t whole = num;
    num -= (double)whole;
    if (num >= 0.5) {
        return whole+1;
    }
    return whole;
}

__int128_t abs_m(__int128_t a) {
    if (a < 0) {
        return -a;
    }
    return a;
}

__int128_t distance(__int128_t a, __int128_t b) {
    if (a == b) {
        return 0;
    } else if ((a < 0 && b < 0) || (a > 0 && b > 0)) {
        if (a < b) {
            return (abs_m(abs_m(a) - abs_m(b)));
        } else {
            return -(abs_m(abs_m(a) - abs_m(b)));
        }
    }
    return std::copysign((int64_t)(abs_m(a) + abs_m(b)),(int64_t)b);
}

std::tuple<Edgelist, __int128_t, __int128_t, __int128_t> edgelist(std::ifstream& infile) {
    int64_t n, m, k, L;
    infile >> n >> m >> k >> L;
    Edgelist edgelist(n, std::vector<__int128_t>(n, -1));
    std::vector<__int128_t> weights;
    for(__int128_t i = 0; i < m; i++) {
        int64_t u, v, w;
        infile >> u >> v >> w;
        edgelist[u][v] = w;
        edgelist[v][u] = w;
        weights.push_back(w);
    }
    std::sort(weights.begin(), weights.end(), std::greater<__int128_t>());

    __int128_t M = L;
    for(__int128_t i = 0; i < n; i++) {
        M -= weights[i];
    }
    M = (M * M + (k-1)*(L * L))/k;
    M = sqrt(M);
    for(auto& u : edgelist) {
        for(auto& v : u) {
            if(v == -1) {
                v = M;
            }
        }
    }
    return std::tuple<Edgelist, __int128_t, __int128_t, __int128_t>(edgelist, k, L, M);
}

std::tuple<Edgelist, __int128_t, __int128_t, __int128_t> coords(std::ifstream& infile) {
    int64_t n, k, L;
    infile >> n >> k >> L;
    Edgelist edgelist(n, std::vector<__int128_t>(n, -1));
    std::vector<std::pair<__int128_t, __int128_t>> coordinates;
    for(__int128_t i = 0; i < n; i++) {
        int64_t x, y;
        infile >> x >> y;
        coordinates.push_back(std::make_pair(x,y));
    }
    for(__int128_t i = 0; i < n; i++) {
        for(__int128_t j = i+1; j < n; j++) {
            auto dist_x = distance(coordinates[i].first, coordinates[j].first);
            dist_x *= dist_x;
            auto dist_y = distance(coordinates[i].second, coordinates[j].second);
            dist_y *= dist_y;
            auto dist = std::sqrt((int64_t)(dist_x+dist_y));
            auto dist_rounded = proper_round(dist);
            // auto dist_rounded = dist;
            edgelist[i][j] = dist_rounded;
            edgelist[j][i] = dist_rounded;
        }
    }
    return std::tuple<Edgelist, __int128_t, __int128_t, __int128_t>(edgelist, k, L, -1);
}

std::tuple<Edgelist, __int128_t, __int128_t, __int128_t> parse_input(std::string filename) {
    std::ifstream infile(filename);
    std::string format;
    infile >> format;
    if(format == "EDGELIST") {
        return edgelist(infile);
    } else if(format == "COORDS") {
        return coords(infile);
    }
}
