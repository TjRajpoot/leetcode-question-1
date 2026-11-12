# Contributing

Thanks for reviewing this proposed programming problem.

## Scope

The intended task is to compare two **already-normalized token sequences** and determine whether they share a contiguous fragment of length at least `k`.

Do not expand the judged task into parsing arbitrary programming languages. Normalization is explicitly outside the function contract.

## Before proposing a change

- Preserve the exact token-sequence definition.
- Add a public example for any newly clarified edge case.
- Add fixed tests for boundary conditions.
- Run the randomized differential test generator.
- If changing the algorithm, retain a brute-force oracle for small cases.

## Run tests

```bash
python3 tools/test_generator.py
python3 tools/test_generator.py --stress
```

## Reference implementations

Keep C++17, Java 17, and Python 3 implementations behaviorally equivalent. Any change to the statement or constraints must be reflected in all three.
