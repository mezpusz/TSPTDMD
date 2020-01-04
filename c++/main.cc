
#include "search.h"
#include "genetic.h"
#include "construction.h"
#include "input.h"
#include "validate.h"
#include <random>
#include <fstream>
#include <chrono>

bool parse_args(int argc, char** argv,
    std::string& input_filename,
    std::string& solution_filename,
    std::string& result_filename)
{
    if (argc < 4) {
        std::cout << "Parameters: ./tsptdmd <input_filename> <solution_filename> <result_filename>" << std::endl;
        return false;
    }
    input_filename = argv[1];
    solution_filename = argv[2];
    result_filename = argv[3];
    return true;
}

void write_solution_to_file(const std::string& filename, Solution solution, const std::string& instance) {
    std::ofstream file(filename, std::ios_base::app);
    file << instance << std::endl;
    for (const auto& e : solution.chains[0].edges) {
        file << e.u << " ";
    }
    file << std::endl;
    for (const auto& e : solution.chains[0].edges) {
        file << e.driver << " ";
    }
    file << std::endl;
}

const __int128_t kLocalIter = 100;

int main(int argc, char** argv) {
    std::srand(time(nullptr));

    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    std::chrono::steady_clock::time_point best_end = std::chrono::steady_clock::now();

    std::string input_filename;
    std::string solution_filename;
    std::string result_filename;
    if (!parse_args(argc, argv, input_filename, solution_filename, result_filename)) {
        return -1;
    }
    std::string instance = input_filename;
    while(true) {
        auto index = instance.find('/');
        if (index == std::string::npos) {
            break;
        }
        instance = instance.substr(index+1);
    }
    instance = instance.substr(0, instance.find('.'));

    auto input = parse_input(input_filename);
    Edgelist edgelist;
    int64_t k, L, M;
    std::tie(edgelist, k, L, M) = input;
    bool local = true;
    __int128_t iter = 0;
    if (local) {
        auto solution = construct_randomized_greedy2(&edgelist, edgelist.size(), k, L, M);
        auto best = solution;
        while(iter < kLocalIter) {
            solution = local_search(solution, &edgelist);
            auto new_sol = make_feasible(&edgelist, solution, M);
            if (new_sol < solution) {
                std::cout << "Found a more feasible solution " << new_sol.obj
                          << " best is: " << best.obj << std::endl;
                solution = new_sol;
            } else {
                if (solution < best) {
                    best = solution;
                    best_end = std::chrono::steady_clock::now();
                }
                if (best.obj == 0) {
                    break;
                }
                std::cout << "Local optimum reached with current " << solution.obj
                          << " and best " << best.obj << ", generating random neighbor" << std::endl;
                solution = random_neighbor(&edgelist, solution, 4);
                solution = make_feasible(&edgelist, solution, M);
                iter++;
            }
        }
        std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
        write_solution_to_file(solution_filename, best, instance);
        std::ofstream file(result_filename, std::ios_base::app);
        file << instance << " best solution: " << best.obj << ", iterations: " << iter
             << " best time " << std::chrono::duration_cast<std::chrono::milliseconds>(best_end - begin).count() << " µs, total time "
             << std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count() << " µs"
             << std::endl;
    } else {
        auto p = genetic_algorithm(&edgelist, edgelist.size(), k, L, M, 0.1, 5, 1.5);
        std::cout << "Best solution is: " << p[0]
                << "with obj: " << p[0].obj << std::endl;
        validate_solution(p[0], &edgelist);
        write_solution_to_file(solution_filename, p[0], instance);
    }
    return 0;
}
