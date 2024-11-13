#include <fstream>
#include <iostream>
#include <unordered_map>
#include <sstream>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

struct MealyState {
    std::unordered_map<std::string, std::pair<std::string, std::string>> transitions;
};

struct MooreState {
    std::string output;
    std::unordered_map<std::string, std::string> transitions;
};

std::unordered_map<std::string, MealyState> readMealyMachine(const std::string& fileName, std::string& startState)
{
    std::ifstream file(fileName);
    std::string line;
    std::unordered_map<std::string, MealyState> mealy;
    std::vector<std::string> states;

    getline(file, line);
    std::stringstream ss(line);
    std::string state;
    getline(ss, state, ';');

    while (getline(ss, state, ';')) {
        states.push_back(state);
    }

    startState = states.front();

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

void writeMealyMachine(const std::unordered_map<std::string, MealyState>& mealy, const std::string& fileName)
{
    std::ofstream file(fileName);

    for (const auto& state : mealy) {
        file << ";" << state.first;
    }
    file << std::endl;

    std::unordered_map<std::string, std::vector<std::pair<std::string, std::string>>> transitions;
    for (const auto& state : mealy) {
        for (const auto& transition : state.second.transitions) {
            transitions[transition.first].emplace_back(transition.second.first, transition.second.second);
        }
    }

    for (const auto& transition : transitions) {
        file << transition.first;
        for (const auto& state : transition.second) {
            file << ";" << state.first << "/" << state.second;
        }
        file << std::endl;
    }
}

std::unordered_map<std::string, MooreState> readMooreMachine(const std::string& fileName, std::string& startState)
{
    std::ifstream file(fileName);
    std::string outputs;
    std::string line;
    std::unordered_map<std::string, MooreState> moore;
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

    startState = states.front();

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

void writeMooreMachine(const std::unordered_map<std::string, MooreState>& moore, const std::string& fileName)
{
    std::ofstream file(fileName);

    for (const auto& state : moore) {
        file << ";" << state.second.output;
    }
    file << std::endl;

    for (const auto& state : moore) {
        file << ";" << state.first;
    }
    file << std::endl;

    std::unordered_map<std::string, std::vector<std::string>> transitions;
    for (const auto& state : moore) {
        for (const auto& transition : state.second.transitions) {
            transitions[transition.first].push_back(transition.second);
        }
    }

    for (const auto& transition : transitions) {
        file << transition.first;
        for (const auto& state : transition.second) {
            file << ";" << state;
        }
        file << std::endl;
    }
}

void removeUnreachableStatesMealy(std::unordered_map<std::string, MealyState>& mealy, const std::string& startState)
{
    std::unordered_set<std::string> reachable;
    std::vector toVisit = { startState };

    while (!toVisit.empty()) {
        std::string current = toVisit.back();
        toVisit.pop_back();
        if (reachable.contains(current))
            continue;
        reachable.insert(current);

        for (const auto& transition : mealy[current].transitions) {
            toVisit.push_back(transition.second.first);
        }
    }

    for (auto it = mealy.begin(); it != mealy.end();) {
        if (!reachable.contains(it->first)) {
            it = mealy.erase(it);
        } else {
            ++it;
        }
    }
}

void removeUnreachableStatesMoore(std::unordered_map<std::string, MooreState>& moore, const std::string& startState)
{
    std::unordered_set<std::string> reachable;
    std::vector toVisit = { startState };

    while (!toVisit.empty()) {
        std::string current = toVisit.back();
        toVisit.pop_back();
        if (reachable.contains(current))
            continue;
        reachable.insert(current);

        for (const auto& transition : moore[current].transitions) {
            toVisit.push_back(transition.second);
        }
    }

    for (auto it = moore.begin(); it != moore.end();) {
        if (!reachable.contains(it->first)) {
            it = moore.erase(it);
        } else {
            ++it;
        }
    }
}

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
