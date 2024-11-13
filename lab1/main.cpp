#include <iostream>

#include "state-machine-utils.h"

std::unordered_map<std::string, MooreState> mealyToMoore(const std::unordered_map<std::string, MealyState>& mealy)
{
    std::unordered_map<std::string, MooreState> moore;
    std::vector<std::string> states;

    for (const auto& state : mealy) {
        for (const auto& transition : state.second.transitions) {
            std::string newState = transition.second.first + "_" + transition.second.second;
            states.push_back(newState);
            moore[newState].output = transition.second.second;
        }
    }

    for (const auto& state : mealy) {
        for (const auto& transition : state.second.transitions) {
            for (const auto& mooreState : states) {
                size_t pos = mooreState.find('_');
                std::string sub = mooreState.substr(0, pos);
                if (sub == state.first) {
                    moore[mooreState].transitions[transition.first]
                        = transition.second.first + "_" + transition.second.second;
                }
            }
        }
    }

    return moore;
}

std::unordered_map<std::string, MealyState> mooreToMealy(const std::unordered_map<std::string, MooreState>& moore)
{
    std::unordered_map<std::string, MealyState> mealy;

    for (const auto& state : moore) {
        for (const auto& transition : state.second.transitions) {
            mealy[state.first].transitions[transition.first]
                = { transition.second, moore.at(transition.second).output };
        }
    }

    return mealy;
}

int main(int argc, char* argv[])
{
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <conversion-type> <input-file> <output-file>" << std::endl;
        return 1;
    }

    std::string conversionType = argv[1];
    std::string inputFileName = argv[2];
    std::string outputFileName = argv[3];

    if (conversionType == "mealy-to-moore") {
        std::string startState;
        auto mealy = readMealyMachine(inputFileName, startState);
        removeUnreachableStatesMealy(mealy, startState);
        auto moore = mealyToMoore(mealy);
        writeMooreMachine(moore, outputFileName);
    } else if (conversionType == "moore-to-mealy") {
        std::string startState;
        auto moore = readMooreMachine(inputFileName, startState);
        removeUnreachableStatesMoore(moore, startState);
        auto mealy = mooreToMealy(moore);
        writeMealyMachine(mealy, outputFileName);
    } else {
        std::cerr << "Unknown conversion type: " << conversionType << std::endl;
        return 1;
    }

    return 0;
}
