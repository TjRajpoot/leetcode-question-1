import java.util.*;

class Solution {
    private int[] buildSuffixArray(int[] s) {
        int n = s.length;
        int maxValue = 0;
        for (int x : s) maxValue = Math.max(maxValue, x);
        int alphabet = Math.max(n, maxValue + 1);

        int[] p = new int[n];
        int[] c = new int[n];
        int[] cnt = new int[alphabet];

        for (int x : s) cnt[x]++;
        for (int i = 1; i < alphabet; i++) cnt[i] += cnt[i - 1];

        for (int i = n - 1; i >= 0; i--) {
            p[--cnt[s[i]]] = i;
        }

        int classes = 1;
        c[p[0]] = 0;
        for (int i = 1; i < n; i++) {
            if (s[p[i]] != s[p[i - 1]]) classes++;
            c[p[i]] = classes - 1;
        }

        int[] pn = new int[n];
        int[] cn = new int[n];

        for (int len = 1; len < n; len *= 2) {
            for (int i = 0; i < n; i++) {
                pn[i] = p[i] - len;
                if (pn[i] < 0) pn[i] += n;
            }

            Arrays.fill(cnt, 0, classes, 0);
            for (int x : pn) cnt[c[x]]++;
            for (int i = 1; i < classes; i++) cnt[i] += cnt[i - 1];

            for (int i = n - 1; i >= 0; i--) {
                int x = pn[i];
                p[--cnt[c[x]]] = x;
            }

            cn[p[0]] = 0;
            int newClasses = 1;

            for (int i = 1; i < n; i++) {
                int cur1 = c[p[i]];
                int cur2 = c[(p[i] + len) % n];
                int prev1 = c[p[i - 1]];
                int prev2 = c[(p[i - 1] + len) % n];

                if (cur1 != prev1 || cur2 != prev2) newClasses++;
                cn[p[i]] = newClasses - 1;
            }

            int[] swap = c;
            c = cn;
            cn = swap;
            classes = newClasses;

            if (classes == n) break;
        }
        return p;
    }

    public boolean isPlagiarized(String[] code1, String[] code2, int k) {
        int n = code1.length;
        int m = code2.length;

        if (k > Math.min(n, m)) return false;

        HashMap<String, Integer> ids = new HashMap<>();
        int nextId = 2; // 0 = END, 1 = SEP

        int[] s = new int[n + m + 2];

        for (int i = 0; i < n; i++) {
            Integer value = ids.get(code1[i]);
            if (value == null) {
                value = nextId++;
                ids.put(code1[i], value);
            }
            s[i] = value;
        }

        s[n] = 1; // unique separator

        for (int j = 0; j < m; j++) {
            Integer value = ids.get(code2[j]);
            if (value == null) {
                value = nextId++;
                ids.put(code2[j], value);
            }
            s[n + 1 + j] = value;
        }

        s[n + m + 1] = 0; // unique terminal sentinel

        int N = s.length;
        int[] sa = buildSuffixArray(s);
        int[] rank = new int[N];
        int[] lcp = new int[N];

        for (int i = 0; i < N; i++) rank[sa[i]] = i;

        int h = 0;
        for (int i = 0; i < N; i++) {
            int r = rank[i];
            if (r == 0) {
                h = 0;
                continue;
            }

            int j = sa[r - 1];
            while (i + h < N && j + h < N && s[i + h] == s[j + h]) h++;
            lcp[r] = h;
            if (h > 0) h--;
        }

        for (int i = 1; i < N; i++) {
            int a = sa[i - 1];
            int b = sa[i];

            boolean aFirst = a < n;
            boolean bFirst = b < n;
            boolean aSecond = a > n && a < n + m + 1;
            boolean bSecond = b > n && b < n + m + 1;

            if (((aFirst && bSecond) || (aSecond && bFirst)) && lcp[i] >= k) {
                return true;
            }
        }
        return false;
    }
}
