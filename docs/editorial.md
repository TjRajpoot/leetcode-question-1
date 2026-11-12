# Editorial — Detect Code Plagiarism

## Approach: Suffix Array + LCP

We need to determine whether two token arrays share a common contiguous substring of length at least `k`.

A direct comparison of every pair of starting positions is too slow for arrays with up to 100,000 combined tokens.

### 1. Coordinate-compress tokens

Map each distinct token string to an integer. Use the same mapping for both arrays so equal tokens receive equal integers.

Reserve two integer values:
- `0`: unique terminal sentinel;
- `1`: unique separator.

All ordinary token IDs must be greater than `1`.

Construct:

```text
S = code1 + [separator] + code2 + [terminal]
```

The separator prevents a common prefix from continuing across the boundary between the two source arrays. The terminal sentinel is unique and smaller than every other value.

### 2. Build the suffix array

Build the suffix array of `S` using the doubling algorithm with counting sort.

The unique smallest terminal sentinel lets us sort cyclic shifts and obtain suffix order.

At each doubling round, sort suffix positions by pairs of equivalence classes:

```text
(class[i], class[(i + length) mod N])
```

Counting sort keeps each round linear, giving `O(N log N)` total time.

### 3. Build the LCP array

Use Kasai's algorithm.

`lcp[r]` stores the longest common prefix of the suffix at `sa[r]` and the previous suffix at `sa[r - 1]`.

Kasai's algorithm takes `O(N)` time.

### 4. Check adjacent suffixes from different sources

A suffix starting at a position in `code1` belongs to source 1. A suffix starting after the separator and before the terminal sentinel belongs to source 2. The separator and terminal positions are ignored.

Inspect adjacent suffixes in suffix-array order. If they belong to different sources and their LCP is at least `k`, return `true`.

If no such pair exists, return `false`.

## Why adjacent suffixes are sufficient

All suffixes sharing a particular prefix form a contiguous interval in lexicographical suffix-array order.

Suppose a common token sequence of length at least `k` occurs in both input arrays. The suffixes beginning at those occurrences share a prefix of length at least `k`. The interval of suffixes with that prefix contains suffixes from both sources. Therefore, at least one adjacent pair in that interval must come from different sources, and that pair has LCP at least `k`.

Conversely, if adjacent suffixes from different sources have LCP at least `k`, their first `k` tokens are identical and occur contiguously in both arrays.

Thus, the algorithm returns `true` exactly when the required common sequence exists.

## Complexity

Let `N = n + m + 2`.

| Phase | Time |
|---|---:|
| Coordinate compression | Expected `O(N)` |
| Suffix array (doubling + counting sort) | `O(N log N)` |
| Kasai LCP | `O(N)` |
| Cross-source scan | `O(N)` |
| Total | Expected `O(N log N)` |

Auxiliary space: `O(N)`.

The expected qualifier comes from hash-map token compression. The suffix-array, LCP, and scan phases are deterministic.
