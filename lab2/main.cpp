#include <map>

#include "state-machine-utils.h"

std::unordered_map<std::string, MealyState> minimizeMealy(std::unordered_map<std::string, MealyState>& mealy)
{
    removeUnreachableStatesMealy(mealy);

    std::unordered_map<std::string, std::map<std::string, std::string>> a;

    for (auto& [state, stateInfo] : mealy) {
        for (auto& [input, transition] : stateInfo.transitions) {
            a[state][input] = transition.second;
        }
    }

    std::unordered_map<std::string, std::string> b;

    for (auto& [state, info] : a) {
        b[state] = "";
        for (auto& [_, output] : info) {
            b[state] += output;
        }
    }

    for (auto& [state, stateInfo] : mealy) {
        for (auto& [input, transition] : stateInfo.transitions) {
            a[state][input] = b[transition.first];
        }
    }

    for (auto& [state, info] : a) {
        for (auto& [input, output] : info) {
            b[state] += output;
        }
    }

    for (auto& [state, stateInfo] : mealy) {
        for (auto& [input, transition] : stateInfo.transitions) {
            a[state][input] = b[transition.first];
        }
    }

    for (auto& [state, info] : a) {
        for (auto& [input, output] : info) {
            b[state] += output;
        }
    }

    for (auto& [state, stateInfo] : mealy) {
        for (auto& [input, transition] : stateInfo.transitions) {
            a[state][input] = b[transition.first];
        }
    }

    for (auto& [state, info] : a) {
        for (auto& [input, output] : info) {
            b[state] += output;
        }
    }

    std::unordered_map<std::string, std::vector<std::string>> c;

    for (auto& [state, info] : b) {
        c[info].push_back(state);
    }

    std::unordered_map<std::string, MealyState> minimized;
    for (auto& [eqClass, states] : c) {
        minimized[eqClass] = {};
        for (const auto& state : states) {
            if (!minimized[eqClass].isInitial) {
                minimized[eqClass].isInitial = mealy[state].isInitial;
            }
        }
        auto state = states[0];
        auto transitions = mealy[state].transitions;
        for (const auto& [input, transition] : transitions) {
            minimized[eqClass].transitions[input] = {b[transition.first],transition.second};
        }
    }

    return minimized;
}

int main()
{
    auto mealy = readMealyMachine("mealy.csv");
    const auto minimized = minimizeMealy(mealy);
    writeMealyMachine(minimized, "output.csv");
    return 0;
}
