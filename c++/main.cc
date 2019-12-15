
#include "search.h"
#include "genetic.h"
#include "construction.h"
#include "input.h"
#include "validate.h"
#include <random>
#include <fstream>

void write_solution_to_file(const std::string& filename, Solution solution, const std::string& instance) {
    std::ofstream file(filename);
    file << instance << std::endl;
    for (const auto& e : solution.chains[0].edges) {
        file << e.u << " ";
    }
    file << std::endl;
    for (const auto& e : solution.chains[0].edges) {
        file << e.driver << " ";
    }
}

int main(int argc, char** argv) {
    std::srand(time(nullptr));

    std::string instance = "0010_k2";
    auto input = parse_input("/home/mezpusz/tuwien/2019W/heuristic/programming1/instances/"+instance+".txt");
    Edgelist edgelist;
    int64_t k, L, M;
    std::tie(edgelist, k, L, M) = input;
    auto p = genetic_algorithm(&edgelist, edgelist.size(), k, L, M, 0.1, 5, 1.5);
    // auto solution = construct_randomized_greedy(&edgelist, edgelist.size(), k, L, M, 0);
    // std::cout << "Best solution is: " << solution
    //           << "with obj: " << std::sqrt(solution.obj) << std::endl;
    // return 0;
    for (auto& s : p) {
        auto n = local_search(s, &edgelist);
        std::cout << "New solution has obj: " << n.obj << std::endl;
        p.push_back(n);
    }
    std::sort(p.begin(), p.end());
    std::cout << "Best solution has obj: " << p[0].obj << std::endl;
    validate_solution(p[0], &edgelist);
    write_solution_to_file("try.txt", p[0], instance);
    return 0;
}
