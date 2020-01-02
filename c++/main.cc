
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

    std::string instance = "rl5915_k2_1";
    // std::string instance = "2000_k2";
    auto input = parse_input("/home/mezpusz/tuwien/2019W/heuristic/programming1/instances/"+instance+".txt");
    Edgelist edgelist;
    int64_t k, L, M;
    std::tie(edgelist, k, L, M) = input;
    bool local = false;
    if (local) {
        auto solution = construct_randomized_greedy2(&edgelist, edgelist.size(), k, L, M);
        while(true) {
            solution = local_search(solution, &edgelist);
            auto new_sol = make_feasible(&edgelist, solution, M);
            if (new_sol < solution) {
                std::cout << "Found a more feasible solution " << new_sol.obj << std::endl;
                solution = new_sol;
            } else {
                break;
            }
        }
        write_solution_to_file("try.txt", solution, instance);
    } else {
        auto p = genetic_algorithm(&edgelist, edgelist.size(), k, L, M, 0.1, 5, 1.5);
        std::cout << "Best solution is: " << p[0]
                << "with obj: " << p[0].obj << std::endl;
        validate_solution(p[0], &edgelist);
        write_solution_to_file("try.txt", p[0], instance);
    }
    return 0;
}
