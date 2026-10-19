#!/usr/bin/env python3
"""Compile chapter C++ snippets and run focused regression checks (C++17)."""
from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = {
    "05": ROOT / "content/chapters/05-data-structures.md",
    "06": ROOT / "content/chapters/06-graph-theory.md",
    "07": ROOT / "content/chapters/07-mathematics.md",
    "08": ROOT / "content/chapters/08-strings.md",
    "09": ROOT / "content/chapters/09-computational-geometry.md",
}
PRELUDE = """#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using i128 = __int128_t;
"""


def snippets(path: Path) -> list[str]:
    return re.findall(r"```cpp\n(.*?)```", path.read_text(encoding="utf-8"), re.S)


def section_snippet(path: Path, heading: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"^{re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        raise RuntimeError(f"section not found: {heading}")
    blocks = snippets_from_text(match.group(1))
    if len(blocks) != 1:
        raise RuntimeError(f"expected one C++ block in {heading}, found {len(blocks)}")
    return blocks[0]


def snippets_from_text(text: str) -> list[str]:
    return re.findall(r"```cpp\n(.*?)```", text, re.S)


def compile_and_run(name: str, code: str, directory: Path, run: bool = False) -> None:
    source = directory / f"{name.replace(' ', '_')}.cpp"
    binary = source.with_suffix("")
    source.write_text(PRELUDE + code, encoding="utf-8")
    subprocess.run(["g++", "-std=c++17", "-fsyntax-only" if not run else "-O2", str(source), *([] if not run else ["-o", str(binary)])], check=True)
    if run:
        subprocess.run([str(binary)], check=True)


def main() -> None:
    content = {key: snippets(path) for key, path in CHAPTERS.items()}
    # Supplementary snippets explicitly reuse definitions in the same chapter.
    dependencies = {
        ("05", 10): content["05"][5],   # RangeFenwick uses the chapter's Fenwick.
        ("06", 14): content["06"][7],   # TwoSAT uses the chapter's TarjanSCC.
        ("05", 27): content["05"][14],  # Matrix composition uses PointSegmentTree.
        ("05", 31): content["05"][29],  # Offline connectivity uses RollbackDSU.
        ("06", 16): content["06"][9],   # TreePathDifference uses BinaryLiftingLCA.
        ("09", 9): content["09"][0],    # Circle routines use the shared Point helpers.
    }
    checked = 0
    for chapter in ("05", "06", "07", "08", "09"):
        file = next((ROOT / "content/chapters").glob(f"{chapter}-*.md"))
        blocks = snippets(file)
        for index, block in enumerate(blocks, 1):
            dependency = dependencies.get((chapter, index))
            compile_and_run(f"syntax_{chapter}_{index}", (dependency + "\n" if dependency else "") + block, Path(tmpdir))
            checked += 1

    runtime_cases = [
        ("bellman_ford", content["06"][2] + r'''
int main() {
    vector<DirectedEdge> edges{{1,2,4},{2,3,-2},{1,3,5},{4,5,-1},{5,4,0}};
    auto [dist, negative] = bellmanFord(5, 1, edges);
    assert(!negative && dist[3] == 2 && dist[4] == INF);
    edges.push_back({3,2,-3});
    assert(bellmanFord(5, 1, edges).second);
}
'''),
        ("segment_tree", content["05"][6] + r'''
int main() {
    vector<ll> a{0,1,2,3,4,5}; SegmentTree tree(5); tree.build(a);
    tree.rangeAdd(2,4,10);
    assert(tree.rangeSum(1,5) == 45 && tree.rangeSum(2,4) == 39);
}
'''),
        ("dinic", content["06"][11] + r'''
int main() {
    Dinic flow(4); flow.addEdge(1,1,8); flow.addEdge(1,2,3); flow.addEdge(1,3,2);
    flow.addEdge(2,4,3); flow.addEdge(3,4,4); assert(flow.maxFlow(1,4) == 5);
}
'''),
        ("min_cost_flow", content["06"][14] + r'''
int main() {
    MinCostMaxFlow flow(4); flow.addEdge(1,1,7,2); flow.addEdge(1,2,2,1);
    flow.addEdge(1,3,2,0); flow.addEdge(2,4,2,2); flow.addEdge(3,4,2,5);
    auto [amount,cost] = flow.run(1,4,3); assert(amount == 3 && cost == 11);
}
'''),
        ("range_assign_segment_tree", content["05"][12] + r'''
int main() {
    vector<ll> a{0,1,2,3,4,5}; AssignAddSegmentTree st(5); st.build(a);
    st.rangeSet(2,4,0); st.rangeAdd(3,5,2);
    assert(st.rangeSum(1,5) == 12 && st.rangeSum(2,4) == 4);
}
'''),
        ("suffix_array", content["08"][6] + r'''
int main() {
    string s="ababa"; auto sa=suffixArray(s);
    assert((sa == vector<int>{4,2,0,3,1}));
    assert((lcpArray(s,sa) == vector<int>{1,3,0,2}));
}
'''),
        ("circle_geometry", content["09"][0] + "\n" + content["09"][8] + r'''
int main() {
    Circle c{{0,0},1};
    auto tangent=lineCircleIntersections({-2,1},{1,0},c);
    assert(tangent.size()==1 && fabsl(tangent[0].x)<1e-9L);
    assert(circleIntersections(c,Circle{{1,0},1}).size()==2);
}
'''),
        ("dsu_on_tree", section_snippet(CHAPTERS["05"], "## 5.14 DSU on Tree（树上启发式合并）") + r'''
int main() {
    mt19937 rng(712367);
    auto check = [&](int n, int mode) {
        vector<vector<int>> tree(n + 1);
        for (int v = 2; v <= n; ++v) {
            int p = mode == 1 ? v - 1 : (mode == 2 ? 1 : int(rng() % (v - 1)) + 1);
            tree[p].push_back(v);
            tree[v].push_back(p);
        }
        vector<int> color(n + 1);
        for (int u = 1; u <= n; ++u) {
            if (mode == 3) color[u] = 17;
            else if (mode == 4) color[u] = u * 100003 - 900000;
            else color[u] = int(rng() % 9) - 4;
        }
        int root = mode == 0 ? int(rng() % n) + 1 : 1;
        DSUOnTree solver(tree, color, root);
        vector<int> got = solver.solve();
        assert(solver.solve() == got);

        vector<int> parent(n + 1), order{root};
        parent[root] = -1;
        for (size_t i = 0; i < order.size(); ++i) {
            int u = order[i];
            for (int v : tree[u]) if (v != parent[u]) {
                parent[v] = u;
                order.push_back(v);
            }
        }
        vector<set<int>> seen(n + 1);
        vector<int> want(n + 1);
        for (int i = n - 1; i >= 0; --i) {
            int u = order[i];
            seen[u].insert(color[u]);
            for (int v : tree[u]) if (parent[v] == u)
                seen[u].insert(seen[v].begin(), seen[v].end());
            want[u] = (int)seen[u].size();
        }
        for (int u = 1; u <= n; ++u) assert(got[u] == want[u]);
    };

    check(1, 0);
    check(80, 1);
    check(80, 2);
    check(80, 3);
    check(80, 4);
    for (int test = 0; test < 300; ++test) check(1 + int(rng() % 90), 0);
}
'''),
        ("point_segment_tree_custom_merge", section_snippet(CHAPTERS["05"], "## 5.15 单点修改线段树与自定义合并 {#point-segment-tree-custom-merge}") + r'''
int main() {
    vector<Affine> two(3);
    two[1] = makeAffine(2, 1);
    two[2] = makeAffine(3, 4);
    PointSegmentTree<Affine, ComposeAffine> ordered(two, makeAffine(1, 0), ComposeAffine{});
    Affine pair = ordered.rangeQuery(1, 2);
    assert((pair.a * 5 + pair.b) % MOD == 37); // f2(f1(5)); reversed order would be 39
    assert(affineExample() == 821);

    mt19937 rng(91237);
    for (int trial = 0; trial < 100; ++trial) {
        int n = 1 + int(rng() % 30);
        vector<Affine> functions(n + 1);
        for (int i = 1; i <= n; ++i)
            functions[i] = makeAffine(rng() % MOD, rng() % MOD);
        PointSegmentTree<Affine, ComposeAffine> st(functions, makeAffine(1, 0), ComposeAffine{});
        for (int step = 0; step < 80; ++step) {
            if (rng() % 3 == 0) {
                int pos = 1 + int(rng() % n);
                Affine f = makeAffine((ll)(rng() % MOD), (ll)(rng() % MOD));
                functions[pos] = f;
                st.pointSet(pos, f);
            }
            int l = 1 + int(rng() % n), r = 1 + int(rng() % n);
            if (l > r) swap(l, r);
            Affine want = makeAffine(1, 0);
            for (int i = l; i <= r; ++i) want = ComposeAffine{}(want, functions[i]);
            Affine got = st.rangeQuery(l, r);
            assert(got.a == want.a && got.b == want.b);
            ll x = rng() % MOD;
            assert((got.a * x + got.b) % MOD == (want.a * x + want.b) % MOD);
        }
    }

    vector<ll> sums{0, 4, -2, 7, 1};
    PointSegmentTree<ll, plus<ll>> sumTree(sums, 0, plus<ll>{});
    assert(sumTree.rangeQuery(2, 4) == 6);
    sumTree.pointSet(3, 10);
    assert(sumTree.rangeQuery(1, 4) == 13);

    vector<ll> mins{0, 8, -3, 5, 2};
    auto minMerge = [](ll a, ll b) { return min(a, b); };
    PointSegmentTree<ll, decltype(minMerge)> minTree(mins, LLONG_MAX, minMerge);
    assert(minTree.rangeQuery(1, 4) == -3);
    minTree.pointSet(2, 9);
    assert(minTree.rangeQuery(2, 4) == 2);
}
'''),
        ("sieve_divisor_counts", section_snippet(CHAPTERS["07"], "## 7.3 素数筛") + r'''
int main() {
    PrimeSieve empty(0);
    assert(empty.primes.empty() && empty.minPrime.size() == 1);
    PrimeSieve one(1);
    assert(one.primes.empty() && one.divisorCount[0] == 0 && one.countDivisors(1) == 1);

    const int n = 3000;
    PrimeSieve sieve(n);
    vector<int> expectedPrimes;
    for (int x = 2; x <= n; ++x) {
        int divisorCount = 0;
        for (int d = 1; d <= x; ++d) if (x % d == 0) ++divisorCount;
        int smallest = 0, exponent = 0;
        for (int p = 2; p <= x; ++p) if (x % p == 0) {
            smallest = p;
            int value = x;
            while (value % p == 0) { ++exponent; value /= p; }
            break;
        }
        assert(sieve.countDivisors(x) == divisorCount);
        assert(sieve.minPrime[x] == smallest);
        assert(sieve.minPrimeExponent[x] == exponent);
        assert(sieve.isPrime(x) == (divisorCount == 2));
        if (divisorCount == 2) expectedPrimes.push_back(x);
    }
    assert(sieve.divisorCount[0] == 0); // sentinel only; no mathematical meaning
    assert(sieve.divisorCount[1] == 1 && sieve.countDivisors(2) == 2);
    assert(sieve.primes == expectedPrimes);
    assert(!sieve.isPrime(-1) && !sieve.isPrime(0) && !sieve.isPrime(1) && !sieve.isPrime(n + 1));
    assert(sieve.countDivisors(1024) == 11); // 2^10
    assert(sieve.countDivisors(2187) == 8);  // 3^7
    assert(sieve.countDivisors(432) == 20);  // 2^4 * 3^3
    assert(sieve.countDivisors(1225) == 9);  // 5^2 * 7^2
}
'''),
    ]
    runtime_cases.append(("tree_path_difference", content["06"][9] + "\n" +
        section_snippet(CHAPTERS["06"], "## 6.16 树上差分 + LCA {#tree-difference}") + r'''
int main() {
    mt19937 rng(442037);
    for (int trial = 0; trial < 160; ++trial) {
        int n = 1 + rng() % 40, root = 1 + rng() % n;
        vector<vector<int>> g(n + 1);
        for (int v = 2; v <= n; ++v) {
            int p = 1 + rng() % (v - 1);
            g[p].push_back(v); g[v].push_back(p);
        }
        TreePathDifference solver(g, root);
        vector<int> parent(n + 1, -1), depth(n + 1), order{root};
        parent[root] = 0;
        for (size_t i = 0; i < order.size(); ++i) {
            int u = order[i];
            for (int v : g[u]) if (parent[v] == -1) {
                parent[v] = u; depth[v] = depth[u] + 1; order.push_back(v);
            }
        }
        vector<ll> wantNode(n + 1), wantEdge(n + 1);
        assert(solver.collect() == make_pair(wantNode, wantEdge));
        for (int step = 0; step < 100; ++step) {
            int u = 1 + rng() % n, v = 1 + rng() % n;
            ll weight = (int)(rng() % 15) - 7;
            bool nodes = rng() % 2;
            if (nodes) solver.addNodes(u, v, weight);
            else solver.addEdges(u, v, weight);
            while (u != v) {
                if (depth[u] < depth[v]) swap(u, v);
                if (nodes) wantNode[u] += weight;
                else wantEdge[u] += weight;
                u = parent[u];
            }
            if (nodes) wantNode[u] += weight;
            auto got = solver.collect();
            assert(got == make_pair(wantNode, wantEdge));
            assert(solver.collect() == got);
        }
    }
}
'''))
    # Intermediate topics: expected answers come from small brute-force models.
    runtime_cases.extend([
        ("small_to_large", section_snippet(CHAPTERS["05"], "## 5.16 启发式合并（Small-to-Large） {#small-to-large}") + r'''
int main() {
    mt19937 rng(712367);
    for (int trial=0; trial<250; ++trial) {
        int n=1+rng()%35; vector<vector<int>> g(n+1); vector<int> parent(n+1);
        for (int v=2; v<=n; ++v) { parent[v]=1+rng()%(v-1); g[parent[v]].push_back(v); g[v].push_back(parent[v]); }
        vector<int> color(n+1); for (int u=1; u<=n; ++u) color[u]=int(rng()%8)-3;
        SmallToLargeDistinct solver(g,color,1); auto got=solver.solve();
        vector<set<int>> want(n+1); for (int u=n;u>=1;--u) { want[u].insert(color[u]); for(int v:g[u]) if(parent[v]==u) want[u].insert(want[v].begin(),want[v].end()); assert(got[u]==(int)want[u].size()); }
        assert(solver.solve()==got);
    }
}
'''),
        ("segment_tree_merge", section_snippet(CHAPTERS["05"], "## 5.17 线段树合并（Segment Tree Merge） {#segment-tree-merge}") + r'''
int main() {
    mt19937 rng(91237);
    for (int trial=0; trial<250; ++trial) {
        int sigma=1+rng()%24; SegmentTreeMerge st(1,sigma); int a=0,b=0; vector<int> fa(sigma+1),fb(sigma+1);
        for(int i=0;i<1+rng()%40;++i){int x=1+rng()%sigma;a=st.add(a,x);++fa[x];}
        for(int i=0;i<1+rng()%40;++i){int x=1+rng()%sigma;b=st.add(b,x);++fb[x];}
        int merged=st.merge(a,b); b=0; // 合并后清除被消费的根引用
        vector<int> all; for(int x=1;x<=sigma;++x) for(int c=0;c<fa[x]+fb[x];++c) all.push_back(x);
        sort(all.begin(),all.end()); for(int x=1;x<=sigma;++x) assert(st.count(merged,x)==fa[x]+fb[x]);
        for(int k=1;k<=(int)all.size();++k) assert(st.kth(merged,k)==all[k-1]);
    }
}
'''),
        ("persistent_segment_tree", section_snippet(CHAPTERS["05"], "## 5.18 主席树（可持久化线段树） {#persistent-segment-tree}") + r'''
int main() {
    mt19937 rng(3319);
    for(int trial=0;trial<100;++trial){
        int n=1+rng()%35,sigma=1+rng()%12; PersistentSegmentTree st(1,sigma); vector<int>a(n+1),root(n+1);
        for(int i=1;i<=n;++i){a[i]=1+rng()%sigma;root[i]=st.add(root[i-1],a[i]);}
        for(int q=0;q<100;++q){int l=1+rng()%n,r=1+rng()%n;if(l>r)swap(l,r);vector<int>w(a.begin()+l,a.begin()+r+1);sort(w.begin(),w.end());int k=1+rng()%w.size();assert(st.kthRange(root[r],root[l-1],k)==w[k-1]);}
        vector<vector<int>> g(n+1); vector<int> par(n+1),dep(n+1),val(n+1); for(int u=2;u<=n;++u){par[u]=1+rng()%(u-1);dep[u]=dep[par[u]]+1;g[par[u]].push_back(u);g[u].push_back(par[u]);} for(int u=1;u<=n;++u)val[u]=1+rng()%sigma;
        vector<int> pathRoot(n+1); for(int u=1;u<=n;++u)pathRoot[u]=st.add(pathRoot[par[u]],val[u]);
        auto lca=[&](int u,int v){while(dep[u]>dep[v])u=par[u];while(dep[v]>dep[u])v=par[v];while(u!=v){u=par[u];v=par[v];}return u;};
        for(int q=0;q<80;++q){int u=1+rng()%n,v=1+rng()%n,w=lca(u,v);vector<int> vals;int x=u;while(x!=w){vals.push_back(val[x]);x=par[x];}vals.push_back(val[w]);x=v;vector<int> tail;while(x!=w){tail.push_back(val[x]);x=par[x];}vals.insert(vals.end(),tail.begin(),tail.end());sort(vals.begin(),vals.end());for(int k=1;k<=(int)vals.size();++k)assert(st.kthPath(pathRoot[u],pathRoot[v],pathRoot[w],pathRoot[par[w]],k)==vals[k-1]);}
    }
}
'''),
        ("virtual_tree", section_snippet(CHAPTERS["05"], "## 5.19 虚树 {#virtual-tree}") + r'''
int main() {
    mt19937 rng(611);
    for (int trial = 0; trial < 120; ++trial) {
        int n = 1 + rng() % 35;
        VirtualTree vt(n);
        vector<int> parent(n + 1), depth(n + 1);
        for (int v = 2; v <= n; ++v) {
            parent[v] = 1 + rng() % (v - 1);
            depth[v] = depth[parent[v]] + 1;
            vt.addEdge(v, parent[v]);
        }
        vt.build();
        auto naiveLca = [&](int u, int v) {
            while (depth[u] > depth[v]) u = parent[u];
            while (depth[v] > depth[u]) v = parent[v];
            while (u != v) { u = parent[u]; v = parent[v]; }
            return u;
        };
        vector<int> special;
        int k = rng() % (n + 1);
        for (int i = 0; i < k; ++i) special.push_back(1 + rng() % n);
        auto got = vt.buildVirtual(special);
        sort(special.begin(), special.end());
        special.erase(unique(special.begin(), special.end()), special.end());
        if (special.empty()) {
            assert(got.root == 0 && got.vertices.empty() && got.edges.empty());
            continue;
        }
        set<int> expected(special.begin(), special.end());
        for (int u : special) for (int v : special) {
            assert(vt.lca(u, v) == naiveLca(u, v));
            expected.insert(naiveLca(u, v));
        }
        assert(set<int>(got.vertices.begin(), got.vertices.end()) == expected);
        assert(got.vertices.size() <= 2 * special.size() - 1);
        assert(got.edges.size() + 1 == got.vertices.size());
        map<int, int> direct;
        for (auto [p, x, distance] : got.edges) {
            assert(naiveLca(p, x) == p);
            assert(distance == depth[x] - depth[p]);
            assert(!direct.count(x));
            direct[x] = p;
        }
        for (int x : got.vertices) {
            if (x == got.root) continue;
            int closest = parent[x];
            while (closest && !expected.count(closest)) closest = parent[closest];
            assert(closest && direct.at(x) == closest);
        }
    }
    VirtualTree chain(6);
    for (int i = 1; i < 6; ++i) chain.addEdge(i, i + 1);
    chain.build(1);
    assert(chain.buildVirtual({4, 4}).vertices == vector<int>({4}));
    assert(chain.buildVirtual({}).vertices.empty());
    chain.build(6);
    auto one = chain.buildVirtual({2, 2, 2});
    assert(one.vertices == vector<int>({2}) && one.edges.empty());
}
'''),
        ("hld_paths", section_snippet(CHAPTERS["05"], "## 5.12 树链剖分") + r'''
int main() {
    mt19937 rng(9921);
    for(int trial=0;trial<120;++trial){int n=1+rng()%40;HLD h(n);vector<vector<int>>g(n+1);for(int v=2;v<=n;++v){int p=1+rng()%(v-1);h.addEdge(p,v);g[p].push_back(v);g[v].push_back(p);}h.build(1);vector<int>par(n+1),dep(n+1);vector<int>ord{1};for(int i=0;i<(int)ord.size();++i){int u=ord[i];for(int v:g[u])if(v!=par[u])par[v]=u,dep[v]=dep[u]+1,ord.push_back(v);}for(int q=0;q<100;++q){int u=1+rng()%n,v=1+rng()%n;vector<int>want;int a=u,b=v;while(dep[a]>dep[b])want.push_back(a),a=par[a];while(dep[b]>dep[a])want.push_back(b),b=par[b];while(a!=b)want.push_back(a),a=par[a],want.push_back(b),b=par[b];want.push_back(a);set<int>got;h.forPath(u,v,[&](int l,int r){assert(1<=l&&l<=r&&r<=n);for(int p=l;p<=r;++p)for(int x=1;x<=n;++x)if(h.pos[x]==p)got.insert(x);});assert(got==set<int>(want.begin(),want.end()));}int old=h.timer;h.build(n);assert(h.timer==old&&h.timer==n);}
}
'''),
        ("weighted", section_snippet(CHAPTERS["05"], "## 5.20 带权并查集 {#weighted-dsu}") + r'''
int main() {
    WeightedDSU dsu(6);
    assert(dsu.unite(1, 2, 5));
    assert(dsu.unite(2, 3, 2));
    assert(dsu.relation(1, 3).value() == 7);
    assert(dsu.unite(1, 3, 7));
    assert(!dsu.unite(1, 3, 6));
    assert(!dsu.relation(1, 4));
    assert(dsu.unite(4, 5, -8));
    assert(dsu.relation(4, 5).value() == -8); // 覆盖另一种按大小方向。

    mt19937 rng(712367);
    const int n = 30;
    vector<long long> value(n + 1);
    for (int i = 1; i <= n; ++i) value[i] = int(rng() % 200) - 100;
    WeightedDSU randomDsu(n);
    for (int i = 2; i <= n; ++i)
        assert(randomDsu.unite(i - 1, i, value[i] - value[i - 1]));
    for (int trial = 0; trial < 300; ++trial) {
        int x = 1 + int(rng() % n), y = 1 + int(rng() % n);
        assert(randomDsu.relation(x, y).value() == value[y] - value[x]);
        assert(!randomDsu.unite(x, y, value[y] - value[x] + 1));
        assert(randomDsu.relation(x, y).value() == value[y] - value[x]);
    }
    WeightedDSU zero(0);
}
'''),
        ("offline", section_snippet(CHAPTERS["05"], "## 5.21 离线树状数组 {#offline-fenwick}") + r'''
int main() {
    vector<PointXY> points{{1, 5}, {2, 2}, {2, 2}, {4, 9}};
    vector<QueryXY> qs{{2, 2, 0}, {2, 8, 1}, {3, 1, 2}};
    auto got = countDominated(points, qs);
    assert((got == vector<ll>{2, 3, 0}));
    vector<int> a{0, 1, 2, 1, 3, 2};
    vector<RangeQuery> rq{{1, 3, 0}, {2, 5, 1}, {3, 3, 2}};
    assert((distinctInRanges(a, rq) == vector<int>{2, 3, 1}));
    assert(countInversions(vector<ll>{3, 1, 2, 1}) == 4);
    assert(countDominated(vector<PointXY>{}, vector<QueryXY>{}).empty());
    assert(distinctInRanges(a, vector<RangeQuery>{}).empty());
    assert(countInversions(vector<ll>{}) == 0);

    mt19937 rng(99123);
    for (int trial = 0; trial < 100; ++trial) {
        int p = int(rng() % 25), q = int(rng() % 25);
        vector<PointXY> ps(p);
        for (auto& point : ps) point = {int(rng() % 7) - 3, int(rng() % 7) - 3};
        vector<QueryXY> qs2(q);
        for (int i = 0; i < q; ++i) qs2[i] = {int(rng() % 7) - 3, int(rng() % 7) - 3, i};
        auto got = countDominated(ps, qs2);
        for (const auto& query : qs2) {
            ll want = 0;
            for (const auto& point : ps)
                want += point.x <= query.x && point.y <= query.y;
            assert(got[query.id] == want);
        }
        int n = 1 + int(rng() % 25);
        vector<int> arr(n + 1);
        for (int i = 1; i <= n; ++i) arr[i] = int(rng() % 6) - 3;
        int qr = int(rng() % 25);
        vector<RangeQuery> ranges(qr);
        for (int i = 0; i < qr; ++i) {
            ranges[i] = {1 + int(rng() % n), 1 + int(rng() % n), i};
            if (ranges[i].l > ranges[i].r) swap(ranges[i].l, ranges[i].r);
        }
        auto distinct = distinctInRanges(arr, ranges);
        for (const auto& range : ranges) {
            set<int> seen(arr.begin() + range.l, arr.begin() + range.r + 1);
            assert(distinct[range.id] == (int)seen.size());
        }
        vector<ll> inv(n);
        for (ll& x : inv) x = int(rng() % 10) - 5;
        ll wantInv = 0;
        for (int i = 0; i < n; ++i)
            for (int j = i + 1; j < n; ++j) wantInv += inv[i] > inv[j];
        assert(countInversions(inv) == wantInv);
    }
}
'''),
        ("mo", section_snippet(CHAPTERS["05"], "## 5.22 莫队算法 {#mo-algorithm}") + r'''
int main() {
    vector<int> a{0, 1, 2, 1, 3, 2};
    MoDistinct solver(a);
    vector<MoQuery> q{{1, 3, 0}, {2, 5, 1}, {3, 3, 2}, {1, 5, 3}};
    assert((solver.solve(q) == vector<int>{2, 3, 1, 3}));
    assert((solver.solve(q) == vector<int>{2, 3, 1, 3}));
    assert(solver.solve(vector<MoQuery>{}).empty());
    mt19937 rng(8137);
    for (int trial = 0; trial < 100; ++trial) {
        int n = 1 + int(rng() % 35), qn = int(rng() % 80);
        vector<int> arr(n + 1);
        for (int i = 1; i <= n; ++i) arr[i] = int(rng() % 8) - 4;
        vector<MoQuery> queries(qn);
        for (int i = 0; i < qn; ++i) {
            queries[i] = {1 + int(rng() % n), 1 + int(rng() % n), i};
            if (queries[i].l > queries[i].r) swap(queries[i].l, queries[i].r);
        }
        MoDistinct randomSolver(arr);
        auto got = randomSolver.solve(queries);
        for (const auto& query : queries) {
            set<int> seen(arr.begin() + query.l, arr.begin() + query.r + 1);
            assert(got[query.id] == (int)seen.size());
        }
    }
}
'''),
        ("cartesian", section_snippet(CHAPTERS["05"], "## 5.23 笛卡尔树 {#cartesian-tree}") + r'''
int main() {
    vector<ll> a{0, 3, 1, 4, 2};
    auto t = buildMinCartesian(a);
    assert(t.root == 2 && t.left[2] == 1 && t.right[2] == 4);
    assert(t.left[4] == 3 && t.parent[1] == 2);
    vector<ll> equal{0, 7, 7, 7, 7, 7};
    auto same = buildMinCartesian(equal);
    assert(same.root == 1);
    for (int i = 1; i <= 5; ++i) assert(same.left[i] == 0 && same.right[i] == (i == 5 ? 0 : i + 1));
    vector<ll> increasing{0, 1, 2, 3, 4, 5};
    auto inc = buildMinCartesian(increasing);
    assert(inc.root == 1);
    vector<ll> decreasing{0, 5, 4, 3, 2, 1};
    auto dec = buildMinCartesian(decreasing);
    assert(dec.root == 5);

    mt19937 rng(5501);
    for (int trial = 0; trial < 120; ++trial) {
        int n = 1 + int(rng() % 45);
        vector<ll> values(n + 1);
        for (int i = 1; i <= n; ++i) values[i] = int(rng() % 9) - 4;
        auto tree = buildMinCartesian(values);
        vector<int> order, stack;
        int u = tree.root;
        while (u || !stack.empty()) {
            while (u) { stack.push_back(u); u = tree.left[u]; }
            u = stack.back(); stack.pop_back(); order.push_back(u); u = tree.right[u];
        }
        assert((int)order.size() == n);
        for (int i = 1; i <= n; ++i) {
            if (tree.left[i]) assert(values[i] <= values[tree.left[i]] && tree.parent[tree.left[i]] == i);
            if (tree.right[i]) assert(values[i] <= values[tree.right[i]] && tree.parent[tree.right[i]] == i);
        }
        for (int i = 0; i < n; ++i) assert(order[i] == i + 1);
    }
}
'''),
        ("li_chao", section_snippet(CHAPTERS["05"], "## 5.24 李超线段树 {#li-chao-tree}") + r'''
int main() {
    LiChaoMax tree(vector<ll>{-1, 0, 2, 5});
    assert(!tree.query(0));
    tree.addLine(1, 0);
    tree.addLine(-1, 4);
    tree.addLine(1, 3); // parallel line dominates y=x
    assert(tree.query(-1).value() == 5);
    assert(tree.query(0).value() == 4);
    assert(tree.query(5).value() == 8);
    LiChaoMax empty({});
    empty.addLine(1, 2);
    assert(!empty.query(0));
    // 中点换线后，旧线在右端胜出；候选必须递归右子树。
    LiChaoMax midpoint(vector<ll>{0, 10, 20});
    midpoint.addLine(1, 0);
    midpoint.addLine(0, 15);
    assert(midpoint.query(0).value() == 15);
    assert(midpoint.query(10).value() == 15);
    assert(midpoint.query(20).value() == 20);
    mt19937 rng(12345);
    vector<ll> xs;
    for (int x = -20; x <= 20; ++x) xs.push_back(x);
    LiChaoMax randomTree(xs);
    vector<pair<ll, ll>> lines;
    for (int step = 0; step < 150; ++step) {
        ll k = int(rng() % 81) - 40, b = int(rng() % 161) - 80;
        randomTree.addLine(k, b);
        lines.push_back({k, b});
        for (ll x : xs) {
            i128 want = numeric_limits<i128>::min();
            for (auto [slope, intercept] : lines)
                want = max(want, (i128)slope * x + intercept);
            assert(randomTree.query(x).value() == want);
        }
    }
    const ll big = 4000000000000000000LL;
    LiChaoMax large(vector<ll>{big});
    large.addLine(big, big);
    assert(large.query(big).value() == (i128)big * big + big);
}
'''),
        ("difference_gcd", section_snippet(CHAPTERS["05"], "## 5.25 差分 + GCD 线段树 {#difference-gcd-tree}") + r'''
int main() {
    mt19937_64 rng(712367);
    for (int trial = 0; trial < 120; ++trial) {
        int n = 1 + rng() % 35;
        vector<ll> a(n + 1), brute(n + 1);
        for (int i = 1; i <= n; ++i) a[i] = brute[i] = (ll)(rng() % 31) - 15;
        DifferenceGcdTree tree(a);
        for (int step = 0; step < 90; ++step) {
            int l = 1 + rng() % n, r = 1 + rng() % n;
            if (l > r) swap(l, r);
            if (rng() % 2 == 0) {
                ll delta = (ll)(rng() % 21) - 10;
                tree.rangeAdd(l, r, delta);
                for (int i = l; i <= r; ++i) brute[i] += delta;
            } else {
                ll want = 0;
                for (int i = l; i <= r; ++i) want = gcd(want, llabs(brute[i]));
                assert(tree.rangeGcd(l, r) == want);
            }
        }
    }
}
'''),
        ("sweep_line", section_snippet(CHAPTERS["05"], "## 5.26 扫描线 + 线段树 {#sweep-line-segment-tree}") + r'''
int main() {
    assert(rectangleUnionArea({{0,0,2,2}}) == 4);
    assert(rectangleUnionArea({{0,0,2,2},{1,1,3,3}}) == 7);
    assert(rectangleUnionArea({{0,0,4,1},{1,-2,3,3},{2,0,5,2}}) == 15);
    assert(rectangleUnionArea({{4,0,1,2},{0,3,2,3}}) == 0);
    mt19937 rng(19237);
    for (int trial = 0; trial < 250; ++trial) {
        vector<Rectangle> rectangles;
        for (int i = 0; i < 5; ++i) {
            int x1 = int(rng() % 7) - 3, x2 = int(rng() % 7) - 3;
            int y1 = int(rng() % 7) - 3, y2 = int(rng() % 7) - 3;
            if (x1 > x2) swap(x1, x2);
            if (y1 > y2) swap(y1, y2);
            rectangles.push_back({x1, y1, x2, y2});
        }
        long long brute = 0;
        for (int x = -3; x < 3; ++x) for (int y = -3; y < 3; ++y) {
            bool covered = false;
            for (const Rectangle& rec : rectangles)
                covered |= rec.x1 <= x && x < rec.x2 && rec.y1 <= y && y < rec.y2;
            brute += covered;
        }
        assert(rectangleUnionArea(rectangles) == brute);
    }
}
'''),
        ("matrix_segment", content["05"][14] + "\n" + section_snippet(CHAPTERS["05"], "## 5.27 线段树 + 矩阵乘法 {#matrix-segment-tree}") + r'''
int main() {
    mt19937 rng(81723);
    for (int trial = 0; trial < 100; ++trial) {
        int n = 1 + rng() % 18;
        vector<Matrix> a(n + 1, Matrix(2));
        for (int i = 1; i <= n; ++i) for (int x = 0; x < 2; ++x)
            for (int y = 0; y < 2; ++y) a[i].a[x][y] = int(rng() % 19) - 9;
        vector<Matrix> normalized(a.size());
        for (int i = 1; i <= n; ++i) normalized[i] = normalizedMatrix(a[i]);
        MatrixSegmentTree tree(normalized, identityMatrix(2), MatrixCompose{});
        for (int step = 0; step < 40; ++step) {
            int pos = 1 + rng() % n;
            Matrix changed(2);
            for (auto& row : changed.a) for (ll& value : row) value = int(rng() % 19) - 9;
            normalized[pos] = normalizedMatrix(changed);
            int l = 1 + rng() % n, r = 1 + rng() % n;
            if (l > r) swap(l, r);
            Matrix want = identityMatrix(2);
            for (int i = l; i <= r; ++i) want = multiplyMatrix(normalized[i], want);
            assert(replaceAndQuery(tree, pos, changed, l, r).a == want.a);
        }
    }
}
'''),
        ("segment_tree_search", section_snippet(CHAPTERS["05"], "## 5.28 线段树上二分 {#segment-tree-search}") + r'''
int main() {
    FirstAtLeastTree tree(vector<ll>{0, 2, -4, 7, 1, 7});
    assert(tree.firstAtLeast(1, 5, 7) == 3);
    assert(tree.firstAtLeast(4, 5, 7) == 5);
    assert(tree.firstAtLeast(1, 5, 8) == -1);
    tree.pointSet(3, 9);
    assert(tree.firstAtLeast(1, 3, 8) == 3);
    mt19937 rng(511);
    for (int trial = 0; trial < 150; ++trial) {
        int n = 1 + rng() % 40;
        vector<ll> a(n + 1);
        for (int i = 1; i <= n; ++i) a[i] = int(rng() % 31) - 15;
        FirstAtLeastTree randomTree(a);
        for (int step = 0; step < 80; ++step) {
            int l = 1 + rng() % n, r = 1 + rng() % n;
            if (l > r) swap(l, r);
            ll need = int(rng() % 35) - 17;
            int want = -1;
            for (int i = l; i <= r; ++i) if (a[i] >= need) { want = i; break; }
            assert(randomTree.firstAtLeast(l, r, need) == want);
            int p = 1 + rng() % n; a[p] = int(rng() % 31) - 15;
            randomTree.pointSet(p, a[p]);
        }
    }
}
'''),
        ("doubling_monotone_stack", section_snippet(CHAPTERS["05"], "## 5.29 倍增 + 单调栈 {#doubling-monotone-stack}") + r'''
int main() {
    NextGreaterDoubling tree(vector<ll>{0, 2, 1, 4, 3, 5});
    assert(tree.kthGreater(1, 1) == 3);
    assert(tree.kthGreater(1, 2) == 5);
    assert(tree.kthGreater(1, 3) == 0);
    assert(tree.kthGreater(4, 1) == 5);
    assert(tree.kthGreater(5, 1) == 0);
    mt19937 rng(7109);
    for (int trial = 0; trial < 150; ++trial) {
        int n = 1 + rng() % 40;
        vector<ll> a(n + 1);
        for (int i = 1; i <= n; ++i) a[i] = int(rng() % 15) - 7;
        NextGreaterDoubling randomTree(a);
        for (int i = 1; i <= n; ++i) {
            vector<int> next;
            int cur = i;
            while (true) {
                int want = 0;
                for (int j = cur + 1; j <= n; ++j) if (a[j] > a[cur]) { want = j; break; }
                if (!want) break;
                next.push_back(want); cur = want;
            }
            for (int k = 1; k <= 45; ++k) {
                int want = k <= (int)next.size() ? next[k - 1] : 0;
                assert(randomTree.kthGreater(i, k) == want);
            }
            for (int right = i; right <= n; ++right) {
                int want = 0;
                for (int j = i + 1; j <= right; ++j) if (a[j] > a[i]) { want = j; break; }
                assert(randomTree.firstGreaterWithin(i, right) == want);
            }
        }
    }
}
'''),
        ("rollback_dsu", section_snippet(CHAPTERS["05"], "## 5.30 可撤销并查集 {#rollback-dsu}") + r'''
int main() {
    RollbackDSU dsu(5);
    int s0 = dsu.snapshot();
    assert(dsu.unite(1, 2));
    int s1 = dsu.snapshot();
    assert(dsu.unite(2, 3));
    assert(!dsu.unite(1, 3));
    assert(dsu.same(1, 3) && dsu.components == 3);
    dsu.rollback(s1);
    assert(!dsu.same(1, 3) && dsu.same(1, 2));
    dsu.rollback(s0);
    assert(dsu.components == 5 && !dsu.same(1, 2));
}
'''),
        ("segment_tree_offline", content["05"][29] + "\n" + section_snippet(CHAPTERS["05"], "## 5.31 线段树分治（动态连通性） {#segment-tree-offline}") + r'''
int main() {
    vector<Operation> ops{
        {'A',1,2}, {'?',1,2}, {'A',2,3}, {'?',1,3},
        {'A',1,2}, {'D',2,1}, {'?',1,2}, {'?',1,3},
        {'D',1,2}, {'?',1,2}, {'D',1,2}, {'?',1,3},
        {'D',1,2}, {'?',1,2}
    };
    OfflineDynamicConnectivity solver(3, ops);
    vector<int> want{1,1,1,1,0,0,0};
    assert(solver.run() == want);
    assert(solver.run() == want);
    assert(OfflineDynamicConnectivity(3, {}).run().empty());
    mt19937 rng(88123);
    for (int trial = 0; trial < 160; ++trial) {
        int n = 1 + rng() % 7, q = 1 + rng() % 45;
        vector<Operation> randomOps;
        map<pair<int,int>, vector<int>> active;
        vector<int> expected;
        for (int t = 0; t < q; ++t) {
            int u = 1 + rng() % n, v = 1 + rng() % n;
            int choice = rng() % 4;
            if (choice == 0) {
                randomOps.push_back({'A', u, v});
                auto key = minmax(u, v); active[{key.first, key.second}].push_back(t);
            } else if (choice == 1) {
                randomOps.push_back({'D', u, v});
                auto key = minmax(u, v); auto& stack = active[{key.first, key.second}];
                if (!stack.empty()) stack.pop_back();
            } else {
                randomOps.push_back({'?', u, v});
                vector<vector<int>> graph(n + 1);
                for (const auto& item : active) if (!item.second.empty()) {
                    graph[item.first.first].push_back(item.first.second);
                    graph[item.first.second].push_back(item.first.first);
                }
                vector<int> seen(n + 1); queue<int> bfs; bfs.push(u); seen[u] = 1;
                while (!bfs.empty()) { int x = bfs.front(); bfs.pop(); for (int y : graph[x]) if (!seen[y]) seen[y] = 1, bfs.push(y); }
                expected.push_back(seen[v]);
            }
        }
        OfflineDynamicConnectivity randomSolver(n, randomOps);
        assert(randomSolver.run() == expected);
    }
}
'''),
    ])
    # The guide examples are what readers copy into their own main function.
    # Execute them against the actual templates so API/return-value changes
    # cannot silently leave the explanatory text with stale examples.
    examples_checked = 0
    guide_sections = [("05", n) for n in (12, 14, *range(16, 32))] + [("06", 16)]
    guide_dependencies = {
        ("05", 12): content["05"][6],
        ("05", 27): content["05"][14],
        ("05", 31): content["05"][29],
        ("06", 16): content["06"][9],
    }
    for chapter, number in guide_sections:
        source = CHAPTERS[chapter].read_text(encoding="utf-8")
        section = re.search(
            rf"^## {int(chapter)}\.{number} [^\n]*\n(.*?)(?=^## |\Z)",
            source, re.M | re.S,
        )
        if section is None:
            raise RuntimeError(f"missing guide section: {chapter}.{number}")
        body = section.group(1)
        examples = re.findall(r"```text\n(.*?)```", body, re.S)
        if not examples:
            raise RuntimeError(f"missing guide invocation example: {chapter}.{number}")
        code = guide_dependencies.get((chapter, number), "") + "\n"
        code += "\n".join(snippets_from_text(body))
        code += "\nint main() {\n" + "\n".join(examples) + "\n}\n"
        runtime_cases.append((f"guide_example_{chapter}_{number}", code))
        examples_checked += 1
    for name, code in runtime_cases:
        compile_and_run(name, code, Path(tmpdir), run=True)
    print(f"PASS: {checked} chapter code blocks compile under C++17; {len(runtime_cases)} runtime checks pass ({examples_checked} guide invocation examples).")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="icpcboard-check-") as tmpdir:
        main()
