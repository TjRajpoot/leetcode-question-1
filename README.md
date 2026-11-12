# Detect Code Plagiarism

A proposed algorithmic problem about finding a common contiguous fragment in two normalized token sequences.

![Language](https://img.shields.io/badge/languages-C%2B%2B17%20%7C%20Java17%20%7C%20Python3-blue)
![Algorithm](https://img.shields.io/badge/algorithm-Suffix%20Array-orange)
![Status](https://img.shields.io/badge/status-proposal-yellow)

> **Status: independent problem proposal — not affiliated with or accepted by LeetCode.**

## Problem at a glance

Given two arrays of normalized code tokens and an integer `k`, return `true` if they share a contiguous sequence of at least `k` identical tokens. Otherwise, return `false`.

This is a token-sequence matching problem. It does **not** parse source code, prove semantic equivalence, or establish intent to plagiarize.

## Repository layout

```text
.
├── README.md
├── problem.md
├── CONTRIBUTING.md
├── docs/
│   └── editorial.md
├── solutions/
│   ├── solution.cpp
│   ├── Solution.java
│   └── solution.py
├── tests/
│   └── public_examples.json
├── tools/
│   └── test_generator.py
└── .github/
    ├── ISSUE_TEMPLATE/
    │   └── problem-review.md
    └── workflows/
        └── validate.yml
```

## Reference algorithm

The optimized solutions use:

1. Shared coordinate compression of token strings.
2. A suffix array built by doubling and counting sort.
3. Kasai's algorithm to compute the LCP array.
4. A scan of adjacent suffixes that originate from different input arrays.

For `N = len(code1) + len(code2) + 2`:

- Expected time: `O(N log N)` (hash-map compression plus suffix-array construction).
- Auxiliary space: `O(N)`.

See [`problem.md`](problem.md) for the full statement and [`docs/editorial.md`](docs/editorial.md) for the proof and explanation.

## Run the tests

```bash
python3 tools/test_generator.py
```

Run the optional large stress test:

```bash
python3 tools/test_generator.py --stress
```

The generator compares the optimized Python implementation against a brute-force oracle on reproducible random inputs.

## Reference implementations

- [C++17](solutions/solution.cpp)
- [Java 17](solutions/Solution.java)
- [Python 3](solutions/solution.py)

## Contribution status

This repository is a prepared problem proposal. It has not been submitted to or approved by LeetCode. The problem's relationship to existing longest-common-substring and suffix-array exercises should be reviewed before presenting it as an original platform contribution.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for review guidelines.

## License

No license has been selected yet. Until one is added, the repository should be treated as all rights reserved by its author.
# leetcode-question-1
