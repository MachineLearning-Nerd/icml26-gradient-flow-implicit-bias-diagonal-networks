"""Run the paper's four-feature Algorithm 1 appendix fixture exactly."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path


F = Fraction
ROOT = Path(__file__).parents[1]
OUTPUT = ROOT / "outputs/claim1_algorithm1_toy/trace.json"

X = [
    [F(1), F(1, 2), F(7, 10), F(0)],
    [F(1, 2), F(1), F(1, 10), F(7, 10)],
]
Y = [F(1), F(0)]
T_PLUS = [F(1)] * 4
T_MINUS = [F(1)] * 4


def mat_vec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum(value * weight for value, weight in zip(row, vector)) for row in matrix]


def transpose_mat_vec(matrix: list[list[Fraction]], vector: list[Fraction]) -> list[Fraction]:
    return [sum(row[index] * value for row, value in zip(matrix, vector)) for index in range(len(matrix[0]))]


def solve(square: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction] | None:
    augmented = [row[:] + [value] for row, value in zip(square, rhs)]
    size = len(square)

    for column in range(size):
        pivot = next((row for row in range(column, size) if augmented[row][column]), None)
        if pivot is None:
            return None
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                left - scale * right
                for left, right in zip(augmented[row], augmented[column])
            ]

    return [augmented[row][-1] for row in range(size)]


def squared_residual(vector: list[Fraction]) -> Fraction:
    residual = [target - value for target, value in zip(Y, mat_vec(X, vector))]
    return sum(value * value for value in residual)


def constrained_least_squares(
    positive: list[int], negative: list[int], selected: int
) -> list[Fraction]:
    constrained = positive + negative
    best: tuple[Fraction, tuple[int, ...], list[Fraction]] | None = None

    for free_count in range(len(constrained) + 1):
        for free_constrained in combinations(constrained, free_count):
            free = [selected, *free_constrained]
            normal = [
                [sum(X[row][left] * X[row][right] for row in range(len(X))) for right in free]
                for left in free
            ]
            rhs = [sum(X[row][index] * Y[row] for row in range(len(X))) for index in free]
            coefficients = solve(normal, rhs)
            if coefficients is None:
                continue

            candidate = [F(0)] * len(X[0])
            for index, coefficient in zip(free, coefficients):
                candidate[index] = coefficient
            if any(candidate[index] < 0 for index in positive):
                continue
            if any(candidate[index] > 0 for index in negative):
                continue

            score = squared_residual(candidate)
            key = tuple(free)
            if best is None or (score, key) < (best[0], best[1]):
                best = (score, key, candidate)

    if best is None:
        raise RuntimeError("No feasible constrained least-squares solution")
    return best[2]


def fraction(value: Fraction) -> str:
    return str(value)


def vector(values: list[Fraction]) -> dict[str, list[float] | list[str]]:
    return {"fraction": [fraction(value) for value in values], "float": [float(value) for value in values]}


def run() -> dict[str, object]:
    k = [F(0)] * 4
    s = [F(0)] * 4
    iterations: list[dict[str, object]] = []

    for _ in range(4):
        prediction = mat_vec(X, k)
        if prediction == Y:
            break

        u = [target - value for target, value in zip(Y, prediction)]
        correlation = transpose_mat_vec(X, u)
        positive = [index for index, value in enumerate(k) if value > 0]
        negative = [index for index, value in enumerate(k) if value < 0]
        inactive = [index for index, value in enumerate(k) if value == 0]
        deltas: dict[str, str] = {}
        finite: list[tuple[Fraction, int]] = []

        for index in inactive:
            if correlation[index] > 0:
                delta = (T_PLUS[index] - s[index]) / correlation[index]
            elif correlation[index] < 0:
                delta = (T_MINUS[index] + s[index]) / abs(correlation[index])
            else:
                deltas[str(index + 1)] = "inf"
                continue
            deltas[str(index + 1)] = fraction(delta)
            finite.append((delta, index))

        if not finite:
            raise RuntimeError("Algorithm 1 has no finite inactive-feature time")
        _, selected = min(finite)
        delta = next(value for value, index in finite if index == selected)
        next_s = [value + delta * speed for value, speed in zip(s, correlation)]
        next_k = constrained_least_squares(positive, negative, selected)

        iterations.append(
            {
                "p": len(iterations),
                "k_before": vector(k),
                "s_before": vector(s),
                "u": vector(correlation),
                "delta_by_feature": deltas,
                "selected_feature": selected + 1,
                "selected_delta": fraction(delta),
                "s_after": vector(next_s),
                "k_after": vector(next_k),
                "squared_residual_after": fraction(squared_residual(next_k)),
            }
        )
        k, s = next_k, next_s

    result = {
        "paper_fixture": {
            "arxiv": "2607.12332",
            "title": "Gradient Flow Dynamics and Implicit Bias of Diagonal Linear Networks under Infinitesimal Initialization",
            "source_section": "Appendix, Details of Figure experiment",
        },
        "inputs": {"X": vector([value for row in X for value in row]), "y": vector(Y), "t_plus": vector(T_PLUS), "t_minus": vector(T_MINUS)},
        "algorithm": "Algorithm 1: feature-selection time update followed by sign-constrained least squares",
        "iterations": iterations,
        "selected_features": [step["selected_feature"] for step in iterations],
        "final_k": vector(k),
        "final_prediction": vector(mat_vec(X, k)),
        "final_squared_residual": fraction(squared_residual(k)),
        "paper_comparison": {
            "paper_selected_features": [1, 3, 4],
            "paper_final_k": ["0", "0", "10/7", "-10/49"],
            "printed_delta_feature_1_at_p_3": "20",
            "algorithm_delta_feature_1_at_p_3": "40",
            "delta_discrepancy_changes_selection": False,
        },
        "scope": "This validates the appendix recursion and its arithmetic on the supplied fixture. It does not reproduce continuous-time gradient flow, the infinitesimal limit, or the paper's theorem.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    result = run()
    print(json.dumps({"output": str(OUTPUT), "selected_features": result["selected_features"], "final_k": result["final_k"], "final_squared_residual": result["final_squared_residual"]}, indent=2))
