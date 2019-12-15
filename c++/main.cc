
#include "search.h"
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

    std::string instance = "2000_k2";
    auto input = parse_input("/home/mezpusz/tuwien/2019W/heuristic/programming1/instances/"+instance+".txt");
    Edgelist edgelist;
    int64_t k, L, M;
    std::tie(edgelist, k, L, M) = input;
    auto solution = construct_randomized_greedy(&edgelist, edgelist.size(), k, L, M, 0.1);
    // std::cout << "Best solution is: " << solution
    //           << "with obj: " << std::sqrt(solution.obj) << std::endl;
    // return 0;
    solution = local_search(solution, &edgelist);
    std::cout << "Best solution is: " << solution
              << "with obj: " << int(std::sqrt(solution.obj)) << std::endl;
    validate_solution(solution, &edgelist);
    write_solution_to_file("try.txt", solution, instance);
    return 0;
}
