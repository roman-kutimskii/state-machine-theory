#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

struct MealyState {
    std::map<std::string, std::pair<std::string, std::string>> transitions;
};

struct MooreState {
    std::string output;
    std::map<std::string, std::string> transitions;
};

std::map<std::string, MealyState> readMealyMachine(const std::string& fileName)
{
    std::ifstream file(fileName);
    std::string line;
    std::map<std::string, MealyState> mealy;
    std::vector<std::string> states;

    getline(file, line);
    std::stringstream ss(line);
    std::string state;
    getline(ss, state, ';');

    while (getline(ss, state, ';')) {
        states.push_back(state);
    }

    while (getline(file, line)) {
        std::stringstream ssLine(line);
        std::string input, transition;
        getline(ssLine, input, ';');

        for (const auto& stateName : states) {
            getline(ssLine, transition, ';');
            size_t slashPos = transition.find('/');
            std::string nextState = transition.substr(0, slashPos);
            std::string output = transition.substr(slashPos + 1, transition.size());
            mealy[stateName].transitions[input] = { nextState, output };
        }
    }

    return mealy;
}

std::map<std::string, MooreState> readMooreMachine(const std::string& fileName)
{
    std::ifstream file(fileName);
    std::string outputs;
    std::string line;
    std::map<std::string, MooreState> moore;
    std::vector<std::string> states;

    getline(file, outputs);
    getline(file, line);
    std::stringstream ssOutputs(outputs);
    std::stringstream ss(line);
    std::string output;
    std::string state;
    getline(ssOutputs, output, ';');
    getline(ss, state, ';');

    while (getline(ss, state, ';')) {
        getline(ssOutputs, output, ';');
        states.push_back(state);
        moore[state].output = output;
    }

    while (getline(file, line)) {
        std::stringstream ssLine(line);
        std::string input, transition;
        getline(ssLine, input, ';');

        for (const auto& stateName : states) {
            getline(ssLine, transition, ';');
            moore[stateName].transitions[input] = transition;
        }
    }

    return moore;
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
        auto mealy = readMealyMachine(inputFileName);
        for (const auto& state : mealy) {
            std::cout << state.first << std::endl;
            for (const auto& transition : state.second.transitions) {
                std::cout << transition.first << " " << transition.second.first << "/" << transition.second.second
                          << std::endl;
            }
            std::cout << std::endl;
        }
    } else if (conversionType == "moore-to-mealy") {
        auto moore = readMooreMachine(inputFileName);
        for (const auto& state : moore) {
            std::cout << state.first << " " << state.second.output << std::endl;
            for (const auto& transition : state.second.transitions) {
                std::cout << transition.first << " " << transition.second << std::endl;
            }
            std::cout << std::endl;
        }
    } else {
        std::cerr << "Unknown conversion type: " << conversionType << std::endl;
        return 1;
    }

    return 0;
}
