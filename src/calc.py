from itertools import combinations


def find_factors(N):
    factors = set()
    for i in range(1, int(N**0.5) + 1):
        if N % i == 0:
            factors.add(i)
            factors.add(N // i)
    return sorted(factors)


def find_subsets(elements, subset_sizes):
    subsets = list()
    for size in subset_sizes:
        for combo in combinations(elements, size):
            subsets.append(list(combo))
    return subsets