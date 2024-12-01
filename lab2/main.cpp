#include <map>

#include "state-machine-utils.h"

std::unordered_map<std::string, MealyState> minimizeMealy(const std::unordered_map<std::string, MealyState> &mealy) {
    auto minimized = mealy;
    removeUnreachableStatesMealy(minimized);

    return minimized;
}


int main() {
    const auto mealy = readMealyMachine("mealy.csv");
    const auto minimized = minimizeMealy(mealy);
    writeMealyMachine(minimized, "output.csv");
    return 0;
}
