#ifndef STATE_MACHINE_UTILS_H
#define STATE_MACHINE_UTILS_H

#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

struct MealyState {
    std::unordered_map<std::string, std::pair<std::string, std::string>> transitions;
    bool isInitial = false;
};

struct MooreState {
    std::string output;
    std::unordered_map<std::string, std::string> transitions;
    bool isInitial = false;
};

inline std::unordered_map<std::string, MealyState> readMealyMachine(const std::string& fileName)
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

    mealy[states.front()].isInitial = true;

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

inline void writeMealyMachine(const std::unordered_map<std::string, MealyState>& mealy, const std::string& fileName)
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

inline std::unordered_map<std::string, MooreState> readMooreMachine(const std::string& fileName)
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

    moore[states.front()].isInitial = true;

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

inline void writeMooreMachine(const std::unordered_map<std::string, MooreState>& moore, const std::string& fileName)
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

inline void removeUnreachableStatesMealy(std::unordered_map<std::string, MealyState>& mealy)
{
    std::unordered_set<std::string> reachable;
    std::vector<std::string> toVisit;

    for (const auto& state : mealy) {
        if (state.second.isInitial) {
            toVisit.push_back(state.first);
            break;
        }
    }

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

inline void removeUnreachableStatesMoore(std::unordered_map<std::string, MooreState>& moore)
{
    std::unordered_set<std::string> reachable;
    std::vector<std::string> toVisit;

    for (const auto& state : moore) {
        if (state.second.isInitial) {
            toVisit.push_back(state.first);
            break;
        }
    }

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

#endif // STATE_MACHINE_UTILS_H
