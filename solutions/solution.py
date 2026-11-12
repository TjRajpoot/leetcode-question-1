class Solution:
    def isPlagiarized(self, code1: list[str], code2: list[str], k: int) -> bool:
        n, m = len(code1), len(code2)
        if k > min(n, m):
            return False

        # Shared coordinate compression: 0 = END, 1 = SEP.
        ids = {}
        next_id = 2
        s = []

        for token in code1:
            if token not in ids:
                ids[token] = next_id
                next_id += 1
            s.append(ids[token])

        s.append(1)

        for token in code2:
            if token not in ids:
                ids[token] = next_id
                next_id += 1
            s.append(ids[token])

        s.append(0)
        N = len(s)

        # Suffix array of cyclic shifts; the unique smallest terminal
        # sentinel makes this equivalent to suffix-array order.
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
                cls = c[x]
                cnt[cls] -= 1
                p[cnt[cls]] = x

            cn[p[0]] = 0
            new_classes = 1
            for i in range(1, N):
                cur = (c[p[i]], c[(p[i] + length) % N])
                prev = (c[p[i - 1]], c[(p[i - 1] + length) % N])
                if cur != prev:
                    new_classes += 1
                cn[p[i]] = new_classes - 1

            c, cn = cn, c
            classes = new_classes
            if classes == N:
                break
            length *= 2

        sa = p

        # Kasai LCP: lcp[r] is LCP(sa[r], sa[r - 1]).
        rank = [0] * N
        for i, pos in enumerate(sa):
            rank[pos] = i

        lcp = [0] * N
        h = 0
        for i in range(N):
            r = rank[i]
            if r == 0:
                h = 0
                continue
            j = sa[r - 1]
            while i + h < N and j + h < N and s[i + h] == s[j + h]:
                h += 1
            lcp[r] = h
            if h:
                h -= 1

        def source(pos: int) -> int:
            if pos < n:
                return 0
            if n < pos < n + m + 1:
                return 1
            return -1  # separator or terminal sentinel

        for r in range(1, N):
            if source(sa[r - 1]) != -1 and source(sa[r]) != -1:
                if source(sa[r - 1]) != source(sa[r]) and lcp[r] >= k:
                    return True
        return False
