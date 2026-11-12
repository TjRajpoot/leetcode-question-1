#include <bits/stdc++.h>
using namespace std;

class Solution {
    static vector<int> buildSuffixArray(const vector<int>& s) {
        int n = (int)s.size();
        int alphabet = max(n, *max_element(s.begin(), s.end()) + 1);

        vector<int> p(n), c(n), cnt(alphabet, 0);
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

        vector<int> pn(n), cn(n);
        for (int len = 1; len < n; len *= 2) {
            for (int i = 0; i < n; i++) {
                pn[i] = p[i] - len;
                if (pn[i] < 0) pn[i] += n;
            }

            fill(cnt.begin(), cnt.begin() + classes, 0);
            for (int x : pn) cnt[c[x]]++;
            for (int i = 1; i < classes; i++) cnt[i] += cnt[i - 1];

            for (int i = n - 1; i >= 0; i--) {
                int x = pn[i];
                p[--cnt[c[x]]] = x;
            }

            cn[p[0]] = 0;
            int newClasses = 1;

            for (int i = 1; i < n; i++) {
                pair<int, int> cur = {c[p[i]], c[(p[i] + len) % n]};
                pair<int, int> prev = {c[p[i - 1]], c[(p[i - 1] + len) % n]};
                if (cur != prev) newClasses++;
                cn[p[i]] = newClasses - 1;
            }

            c.swap(cn);
            classes = newClasses;
            if (classes == n) break;
        }
        return p;
    }

public:
    bool isPlagiarized(vector<string>& code1,
                       vector<string>& code2,
                       int k) {
        int n = (int)code1.size();
        int m = (int)code2.size();

        if (k > min(n, m)) return false;

        unordered_map<string, int> id;
        id.reserve(n + m);
        int nextId = 2; // 0 = END, 1 = SEP

        vector<int> s;
        s.reserve(n + m + 2);

        for (const string& token : code1) {
            auto it = id.find(token);
            if (it == id.end()) it = id.emplace(token, nextId++).first;
            s.push_back(it->second);
        }

        s.push_back(1); // unique separator

        for (const string& token : code2) {
            auto it = id.find(token);
            if (it == id.end()) it = id.emplace(token, nextId++).first;
            s.push_back(it->second);
        }

        s.push_back(0); // unique terminal sentinel

        int N = (int)s.size();
        vector<int> sa = buildSuffixArray(s);

        vector<int> rank(N), lcp(N, 0);
        for (int i = 0; i < N; i++) rank[sa[i]] = i;

        int h = 0;
        for (int i = 0; i < N; i++) {
            int r = rank[i];
            if (r == 0) {
                h = 0;
                continue;
            }

            int j = sa[r - 1];
            while (i + h < N && j + h < N && s[i + h] == s[j + h]) {
                h++;
            }
            lcp[r] = h;
            if (h > 0) h--;
        }

        auto source = [&](int pos) {
            if (pos < n) return 0;
            if (pos > n && pos < n + m + 1) return 1;
            return -1; // separator or terminal sentinel
        };

        for (int i = 1; i < N; i++) {
            int a = source(sa[i - 1]);
            int b = source(sa[i]);
            if (a != -1 && b != -1 && a != b && lcp[i] >= k) {
                return true;
            }
        }
        return false;
    }
};
