
#pragma once
#include "solution.h"

struct Neighborhood {
    virtual Solution* next() = 0;
};

struct Reversal : public Neighborhood {
    Solution* solution;
    Solution newsol;
    Edgelist* edgelist;
    __int128_t i = 0;
    __int128_t j = 2;

    Reversal(Solution& solution, Edgelist* edgelist);

    Solution* next() override;
};

struct DriverExchange : public Neighborhood {
    Solution* solution;
    Solution newsol;
    Edgelist* edgelist;
    __int128_t i = 0;
    __int128_t j = 1;

    DriverExchange(Solution& solution, Edgelist* edgelist);

    Solution* next() override;
};