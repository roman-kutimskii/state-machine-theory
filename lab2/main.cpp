#include <iostream>
#include <map>

#include "state-machine-utils.h"

std::unordered_map<std::string, MealyState> minimizeMealyMachine(std::unordered_map<std::string, MealyState>& mealy)
{
    removeUnreachableStatesMealy(mealy);

    std::unordered_map<std::string, std::map<std::string, std::string>> transitionMap;

    for (auto& [state, stateInfo] : mealy) {
        for (auto& [input, transition] : stateInfo.transitions) {
            transitionMap[state][input] = transition.second;
        }
    }

    std::unordered_map<std::string, std::string> outputMap;
    std::unordered_map<std::string, std::vector<std::string>> equivalenceClasses;
    bool changed = true;

    while (changed) {
        for (auto& [state, info] : transitionMap) {
            for (auto& [_, output] : info) {
                outputMap[state] += output;
            }
        }

        for (auto& [state, stateInfo] : mealy) {
            for (auto& [input, transition] : stateInfo.transitions) {
                transitionMap[state][input] = outputMap[transition.first];
            }
        }

        std::unordered_map<std::string, std::vector<std::string>> newEquivalenceClasses;
        for (auto& [state, info] : outputMap) {
            newEquivalenceClasses[info].push_back(state);
        }
        changed = newEquivalenceClasses.size() != equivalenceClasses.size();
        equivalenceClasses = newEquivalenceClasses;
    }

    std::unordered_map<std::string, MealyState> minimized;
    for (auto& [eqClass, states] : equivalenceClasses) {
        MealyState newState;
        newState.isInitial
            = std::ranges::any_of(states, [&](const std::string& state) { return mealy[state].isInitial; });
        for (const auto& state : states) {
            const auto transitions = mealy[state].transitions;
            for (const auto& [input, transition] : transitions) {
                newState.transitions[input] = { outputMap[transition.first], transition.second };
            }
        }
        minimized[eqClass] = newState;
    }

    return minimized;
}

std::unordered_map<std::string, MooreState> minimizeMooreMachine(std::unordered_map<std::string, MooreState>& moore)
{
    removeUnreachableStatesMoore(moore);

    std::unordered_map<std::string, std::map<std::string, std::string>> transitionMap;

    for (auto& [state, stateInfo] : moore) {
        for (const auto& [input, _] : stateInfo.transitions) {
            transitionMap[state][input] = stateInfo.output;
        }
    }

    std::unordered_map<std::string, std::string> outputMap;
    std::unordered_map<std::string, std::vector<std::string>> equivalenceClasses;
    bool changed = true;

    while (changed) {
        for (auto& [state, info] : transitionMap) {
            for (auto& [_, output] : info) {
                outputMap[state] += output;
            }
        }

        for (auto& [state, stateInfo] : moore) {
            for (auto& [input, transition] : stateInfo.transitions) {
                transitionMap[state][input] = outputMap[transition];
            }
        }

        std::unordered_map<std::string, std::vector<std::string>> newEquivalenceClasses;
        for (auto& [state, info] : outputMap) {
            newEquivalenceClasses[info].push_back(state);
        }
        changed = newEquivalenceClasses.size() != equivalenceClasses.size();
        equivalenceClasses = newEquivalenceClasses;
    }

    std::unordered_map<std::string, MooreState> minimized;
    for (auto& [eqClass, states] : equivalenceClasses) {
        MooreState newState;
        newState.isInitial
            = std::ranges::any_of(states, [&](const std::string& state) { return moore[state].isInitial; });
        newState.output = moore[states.at(0)].output;
        for (const auto& state : states) {
            const auto transitions = moore[state].transitions;
            for (const auto& [input, transition] : transitions) {
                newState.transitions[input] = outputMap[transition];
            }
        }
        minimized[eqClass] = newState;
    }

    return minimized;
}

int main(int argc, char* argv[])
{
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <machine-type> <input-file> <output-file>" << std::endl;
        return 1;
    }

    std::string machineType = argv[1];
    std::string inputFileName = argv[2];
    std::string outputFileName = argv[3];

    if (machineType == "mealy") {
        auto mealy = readMealyMachine(inputFileName);
        removeUnreachableStatesMealy(mealy);
        const auto minimized = minimizeMealyMachine(mealy);
        writeMealyMachine(minimized, outputFileName);
    } else if (machineType == "moore") {
        auto moore = readMooreMachine(inputFileName);
        const auto minimized = minimizeMooreMachine(moore);
        writeMooreMachine(minimized, outputFileName);
    } else {
        std::cerr << "Unknown machine type: " << machineType << std::endl;
        return 1;
    }

    return 0;
}
