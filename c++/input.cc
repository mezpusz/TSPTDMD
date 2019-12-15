#include "input.h"
#include <fstream>
#include <algorithm>
#include <cmath>

// float proper_round(num):
//     num_last = str(num)[:str(num).index('.')+2][-1]
//     if num_last>='5':
//         return int64_t(num)+1
//     return int64_t(num)

int64_t distance(int64_t a, int64_t b) {
    if (a == b) {
        return 0;
    } else if ((a < 0 && b < 0) || (a > 0 && b > 0)) {
        if (a < b) {
            return (abs(abs(a) - abs(b)));
        } else {
            return -(abs(abs(a) - abs(b)));
        }
    }
    return std::copysign((abs(a) + abs(b)),b);
}

std::tuple<Edgelist, int64_t, int64_t, int64_t> edgelist(std::ifstream& infile) {
    int64_t n, m, k, L;
    infile >> n >> m >> k >> L;
    Edgelist edgelist(n, std::vector<int64_t>(n, -1));
    std::vector<int64_t> weights;
    for(int64_t i = 0; i < m; i++) {
        int64_t u, v, w;
        infile >> u >> v >> w;
        edgelist[u][v] = w;
        edgelist[v][u] = w;
        weights.push_back(w);
    }
    std::sort(weights.begin(), weights.end(), std::greater<int64_t>());

    int64_t M = L;
    for(int64_t i = 0; i < n; i++) {
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
    return std::tuple<Edgelist, int64_t, int64_t, int64_t>(edgelist, k, L, M);
}

std::tuple<Edgelist, int64_t, int64_t, int64_t> coords(std::ifstream& infile) {
    int64_t n, k, L;
    infile >> n >> k >> L;
    Edgelist edgelist(n, std::vector<int64_t>(n, -1));
    std::vector<std::pair<int64_t, int64_t>> coordinates;
    for(int64_t i = 0; i < n; i++) {
        int64_t x, y;
        infile >> x >> y;
        coordinates.push_back(std::make_pair(x,y));
    }
    for(int64_t i = 0; i < n; i++) {
        for(int64_t j = i+1; j < n; j++) {
            auto dist_x = distance(coordinates[i].first, coordinates[j].first);
            dist_x *= dist_x;
            auto dist_y = distance(coordinates[i].second, coordinates[j].second);
            dist_y *= dist_y;
            auto dist = std::sqrt(dist_x+dist_y);
            // auto dist_rounded = proper_round(dist);
            auto dist_rounded = dist;
            edgelist[i][j] = dist_rounded;
            edgelist[j][i] = dist_rounded;
        }
    }
    return std::tuple<Edgelist, int64_t, int64_t, int64_t>(edgelist, k, L, -1);
}

std::tuple<Edgelist, int64_t, int64_t, int64_t> parse_input(std::string filename) {
    std::ifstream infile(filename);
    std::string format;
    infile >> format;
    if(format == "EDGELIST") {
        return edgelist(infile);
    } else if(format == "COORDS") {
        return coords(infile);
    }
}
