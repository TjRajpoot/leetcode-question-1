#!/usr/bin/env python3
"""Differential and stress tests for Detect Code Plagiarism.

Run:
    python3 tools/test_generator.py
    python3 tools/test_generator.py --stress
"""
import argparse
import random
import time


def fast_is_plagiarized(code1, code2, k):
    n, m = len(code1), len(code2)
    if k > min(n, m):
        return False

    ids = {}
    nxt = 2
    s = []
    for token in code1:
        if token not in ids:
            ids[token] = nxt
            nxt += 1
        s.append(ids[token])
    s.append(1)
    for token in code2:
        if token not in ids:
            ids[token] = nxt
            nxt += 1
        s.append(ids[token])
    s.append(0)
    N = len(s)

    alphabet = max(N, max(s) + 1)
    cnt = [0] * alphabet
    for x in s:
        cnt[x] += 1
    for i in range(1, alphabet):
        cnt[i] += cnt[i - 1]

    p = [0] * N
    for i in range(N - 1, -1, -1):
        cnt[s[i]] -= 1
        p[cnt[s[i]]] = i

    c = [0] * N
    classes = 1
    c[p[0]] = 0
    for i in range(1, N):
        if s[p[i]] != s[p[i - 1]]:
            classes += 1
        c[p[i]] = classes - 1

    pn = [0] * N
    cn = [0] * N
    length = 1
    while length < N:
        for i in range(N):
            x = p[i] - length
            pn[i] = x if x >= 0 else x + N

        cnt = [0] * classes
        for x in pn:
            cnt[c[x]] += 1
        for i in range(1, classes):
            cnt[i] += cnt[i - 1]
        for i in range(N - 1, -1, -1):
            x = pn[i]
            cl = c[x]
            cnt[cl] -= 1
            p[cnt[cl]] = x

        cn[p[0]] = 0
        new_classes = 1
        for i in range(1, N):
            a = (c[p[i]], c[(p[i] + length) % N])
            b = (c[p[i - 1]], c[(p[i - 1] + length) % N])
            if a != b:
                new_classes += 1
            cn[p[i]] = new_classes - 1
        c, cn = cn, c
        classes = new_classes
        if classes == N:
            break
        length *= 2

    rank = [0] * N
    for r, pos in enumerate(p):
        rank[pos] = r
    lcp = [0] * N
    h = 0
    for i in range(N):
        r = rank[i]
        if r == 0:
            h = 0
            continue
        j = p[r - 1]
        while i + h < N and j + h < N and s[i + h] == s[j + h]:
            h += 1
        lcp[r] = h
        if h:
            h -= 1

    def src(pos):
        if pos < n:
            return 0
        if n < pos < n + m + 1:
            return 1
        return -1

    for r in range(1, N):
        x, y = src(p[r - 1]), src(p[r])
        if x != -1 and y != -1 and x != y and lcp[r] >= k:
            return True
    return False


def brute(code1, code2, k):
    n, m = len(code1), len(code2)
    for i in range(n - k + 1):
        for j in range(m - k + 1):
            if code1[i:i + k] == code2[j:j + k]:
                return True
    return False


def fixed_tests():
    cases = [
        (["A", "B", "C"], ["A", "B", "C"], 3, True),
        (["A", "B", "C"], ["X", "Y", "Z"], 1, False),
        (["A", "B", "C", "D"], ["X", "B", "C", "Y"], 2, True),
        (["A", "B", "C", "D"], ["X", "B", "C", "Y"], 3, False),
        (["A", "B", "C", "D"], ["C", "D", "A", "B"], 3, False),
        (["A"] * 5, ["A"] * 3, 3, True),
        (["A", "B"], ["B", "C"], 2, False),
        (["A", "B", "C", "D", "E"], ["B", "C", "D"], 3, True),
        (["A", "B", "C"], ["X", "Y", "Z"], 3, False),
        (["A", "B", "C", "D", "E"], ["X", "Y", "Z"], 1, False),
        (["A", "B", "C", "D"], ["A", "B", "C", "D"], 4, True),
        (["A", "B", "C", "D"], ["A", "B", "X", "D"], 2, True),
        (["A", "B", "C", "D"], ["A", "B", "X", "D"], 3, False),
    ]
    for idx, (a, b, k, expected) in enumerate(cases, 1):
        got = fast_is_plagiarized(a, b, k)
        assert got == expected, (idx, a, b, k, expected, got)
        assert brute(a, b, k) == expected, ("oracle", idx)
    return len(cases)


def randomized_tests(rounds=5000, seed=20261112):
    rng = random.Random(seed)
    alphabet = ["T0", "T1", "T2", "T3", "T4", "T5"]
    for case_id in range(rounds):
        n = rng.randint(1, 18)
        m = rng.randint(1, 18)
        a = [rng.choice(alphabet) for _ in range(n)]
        b = [rng.choice(alphabet) for _ in range(m)]
        k = rng.randint(1, min(n, m))
        expected = brute(a, b, k)
        got = fast_is_plagiarized(a, b, k)
        assert got == expected, {
            "case": case_id, "code1": a, "code2": b,
            "k": k, "expected": expected, "got": got
        }
    return rounds


def stress_test():
    n = 50000
    a = [f"T{i % 997}" for i in range(n)]
    b = [f"T{i % 997}" for i in range(n)]
    # A long shared fragment is guaranteed.
    start = time.perf_counter()
    result = fast_is_plagiarized(a, b, 40000)
    elapsed = time.perf_counter() - start
    assert result is True
    return n, elapsed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stress", action="store_true")
    parser.add_argument("--rounds", type=int, default=5000)
    args = parser.parse_args()

    fixed = fixed_tests()
    random_count = randomized_tests(args.rounds)
    print(f"PASS: {fixed} fixed tests")
    print(f"PASS: {random_count} randomized differential tests (seed=20261112)")

    if args.stress:
        n, seconds = stress_test()
        print(f"PASS: stress test with {n}+{n} tokens; {seconds:.3f}s")


if __name__ == "__main__":
    main()
