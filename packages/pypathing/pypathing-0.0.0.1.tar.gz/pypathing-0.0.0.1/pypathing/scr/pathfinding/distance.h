#pragma once
#include <vector>
#include <tuple>

class Cluster;
class PathNode;

namespace distance {
	float distance(PathNode* a, PathNode* b, int key);
	float diagonal(PathNode* a, PathNode* end);
	float fastDiagonal(PathNode* a, PathNode* end);
	float manhattan(PathNode* a, PathNode* end);
	template <typename T>
	int manhattan(std::vector<T> a, std::vector<T> b) {
		if (a.size() != b.size()) {
			return (int)1;
		}
		auto a_iter = a.begin();
		auto b_iter = b.begin();
		int distance = 0;
		for (; a_iter != a.end(); a_iter++) {
			distance = distance + abs((*a_iter) - (*b_iter));
			b_iter++;
		}
		return distance;
	}
}

namespace movements {
	std::vector<std::tuple<int, int, int>> movements(int key);
	std::vector<std::tuple<int, int, int>> noDiagonal();
	std::vector<std::tuple<int, int, int>> fullDiagonal();
	std::vector<std::tuple<int, int, int>> oneMovementDiagonal();
	std::vector<std::tuple<int, int, int>> towMovementDiagonal();

	std::pair<bool, short> furtherMovement(int key, std::vector<std::vector<std::vector<int>>> arr, std::tuple<int, int, int>pos, std::tuple<int, int, int> direction);
	std::pair<bool, short> noDiagonal(std::vector<std::vector<std::vector<int>>> arr, std::tuple<int, int, int>pos, std::tuple<int, int, int> direction);
	std::pair<bool, short> fullDiagonal(std::vector<std::vector<std::vector<int>>> arr, std::tuple<int, int, int>pos, std::tuple<int, int, int> direction);
	std::pair<bool, short> oneMovementDiagonal(std::vector<std::vector<std::vector<int>>> arr, std::tuple<int, int, int>pos, std::tuple<int, int, int> direction, int nums);
}