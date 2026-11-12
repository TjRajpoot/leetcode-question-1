# Detect Code Plagiarism

**Difficulty:** Hard (proposed)  
**Topics:** String, Suffix Array, Longest Common Prefix  
**Target interface:** C++17 / Java 17 / Python 3

## Problem

You are given two arrays of strings, `code1` and `code2`, and an integer `k`.

Each array represents a source-code submission as a sequence of normalized tokens. The same token is represented by the same string in both arrays.

The submissions are considered similar if there exists a contiguous sequence of at least `k` tokens that appears in both arrays.

Return `true` if such a sequence exists. Otherwise, return `false`.

### Normalized-token input contract

The input has already been tokenized and normalized. You do not need to parse source code or remove comments.

The normalization process is external to this problem. It may remove formatting, consistently rename identifiers, and map language-specific syntax to a shared vocabulary. The judged function compares the resulting token strings exactly.

**Important:** This problem detects shared normalized token fragments. It does not determine semantic equivalence or prove that plagiarism occurred.

## Examples

### Example 1

**Input**
```text
code1 = ["INT", "ID0", "=", "1", ";"]
code2 = ["INT", "ID0", "=", "1", ";"]
k = 4
```

**Output**
```text
true
```

**Explanation:** The two arrays share the same contiguous sequence of five tokens.

### Example 2

**Input**
```text
code1 = ["INT", "ID0", "=", "1", ";"]
code2 = ["INT", "ID0", "=", "2", ";"]
k = 4
```

**Output**
```text
false
```

**Explanation:** Their longest common contiguous token sequence has length three, which is less than `k`.

### Example 3

**Input**
```text
code1 = ["A", "B", "C", "D", "E", "F"]
code2 = ["X", "B", "C", "D", "E", "Y"]
k = 4
```

**Output**
```text
true
```

**Explanation:** Both arrays contain `["B", "C", "D", "E"]`.

### Example 4

**Input**
```text
code1 = ["A", "B", "C", "D"]
code2 = ["C", "D", "A", "B"]
k = 3
```

**Output**
```text
false
```

**Explanation:** The arrays contain the same tokens, but no contiguous sequence of length three is shared.

### Example 5

**Input**
```text
code1 = ["A", "B", "C", "D", "E"]
code2 = ["B", "C", "D"]
k = 3
```

**Output**
```text
true
```

**Explanation:** The entire second array appears contiguously in the first array.

## Constraints

```text
1 <= code1.length
1 <= code2.length
code1.length + code2.length <= 100000
1 <= k <= 100000
1 <= code1[i].length <= 20
1 <= code2[i].length <= 20
```

Tokens are case-sensitive, non-empty strings over a shared normalized vocabulary.

## Function signature

### C++

```cpp
class Solution {
public:
    bool isPlagiarized(vector<string>& code1,
                       vector<string>& code2,
                       int k);
};
```

### Java

```java
class Solution {
    public boolean isPlagiarized(String[] code1,
                                 String[] code2,
                                 int k);
}
```

### Python

```python
class Solution:
    def isPlagiarized(self, code1: List[str],
                      code2: List[str],
                      k: int) -> bool:
```
