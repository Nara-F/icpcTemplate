
# 6. 图论

本章默认点编号为 `1..n`。无向边必须加入两个方向；权值和距离使用 `long long`。若题目允许重边，应保留全部边，或在矩阵建图时取最小权值。DFS 与 BFS 基础统一见第 3.8、3.9 节。

## 6.1 拓扑排序

**1. 它是做什么的**

对 1-based 有向图，拓扑排序返回一个排列，使每条边 `u -> v` 的 `u` 都排在 `v` 前面。适用于依赖顺序和 DAG 动态规划；若图有环则无拓扑序，函数返回空向量。邻接表存边数 `m`，运行时间为 $O(n+m)$，额外空间为 $O(n)$；连同输入图计算，存储为 $O(n+m)$。本实现用队列返回任意一个合法顺序，不保证字典序最小。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `graph[u]` | 从 `u` 出发的有向边终点列表；重边应逐条保留。 |
| `indegree[v]` | 输入中进入 `v` 的边数，包含重边。调用时传入副本，函数内部递减。 |
| `n` | `graph.size()-1`，点编号为 `1..n`，下标 0 不用。 |
| `q` | 当前剩余入度为 0、可加入结果的点。 |
| `order` | 已取出的拓扑序前缀；长度小于 `n` 表示有环。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `topologicalSort(graph, indegree)` | `graph` 是 1-based 邻接表，`indegree` 长度至少 `n+1` 且按每条边准确统计；返回含全部点的拓扑序，或有环时返回空向量。入度按值传递，不改调用者的向量；不校验端点与入度是否一致。 |

**4. 怎么调用**

建边时同时统计终点入度，再调用函数。示例边为 `1->2, 1->3, 2->3`，队列处理顺序固定为 `1,2,3`；另用自环检查环检测：

```text
vector<vector<int>> graph(4);
vector<int> indegree(4, 0);
graph[1].push_back(2); ++indegree[2];
graph[1].push_back(3); ++indegree[3];
graph[2].push_back(3); ++indegree[3];
vector<int> order = topologicalSort(graph, indegree);
assert(order == vector<int>({1, 2, 3}));

vector<vector<int>> cyclic(2);
cyclic[1].push_back(1);
vector<int> cyclicIndegree = {0, 1};
assert(topologicalSort(cyclic, cyclicIndegree).empty());
```

模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

// 参数 graph 为 1-based 有向邻接表，indegree 是逐边统计的入度副本；返回拓扑序，有环返回空表。
vector<int> topologicalSort(
    const vector<vector<int>>& graph,
    vector<int> indegree
) {
    // graph[u] 只保存有向出边 u->v；indegree 必须逐条统计所有入边（含重边）。
    int n = (int)graph.size() - 1;
    queue<int> q;
    for (int u = 1; u <= n; ++u) {
        if (indegree[u] == 0) q.push(u);
    }

    // 不变量：队列中的点在“删去已输出点及其出边后”入度为 0。
    vector<int> order;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (int v : graph[u]) {
            if (--indegree[v] == 0) q.push(v);
        }
    }

    if ((int)order.size() != n) return {};  // 有向环导致剩余点无法降至入度 0
    return order;
}
```

**5. 要改哪里**

- 若要求字典序最小拓扑序，将队列换为小根堆，其余入度处理不变，复杂度变为 $O((n+m)\log n)$。
- 若要计算 DAG 上的 DP，可在弹出 `u` 时处理 `u`，再沿出边更新后继状态；必须保持拓扑顺序。
- 重边需在建图和入度统计中都逐条处理；若输入图可能无效，应在调用前验证点编号和入度一致性。

**6. 自检**

三点 DAG 的答案应是 `[1,2,3]`，且每条边起点在终点之前。单点无边图返回 `[1]`；单点自环返回空向量。平行边 `1->2` 两次时，入度应为 2，处理 `1` 时也应递减两次。

**7. 坑**

- DAG 却返回空：入度漏算或与邻接表中的重边数量不符。
- 环图结果长度不足：这正是检测信号，不能把部分序列当作完整答案。
- 把出度当入度：入度为 0 的点才可先输出。
- 需要唯一顺序却直接使用结果：拓扑序可能不唯一；若要判唯一，应在每一步检查队列中是否恰有一个点。

**8. 一句话原理**

反复输出当前没有未处理前驱的点，并删去它的所有出边；剩余点无法继续时便含有环。

**参考：**

- [OI Wiki：拓扑排序](https://oi-wiki.org/graph/topo/)

## 6.2 Dijkstra 单源最短路

**1. 它是做什么的**

Dijkstra 求 1-based 有向或无向非负权图中，指定起点到各点的最短距离，并记录一组前驱以恢复一条最短路。不可达点距离为 `INF`，其 `previous` 为 `-1`；起点前驱也为 `-1`。负权边不适用。邻接表加堆实现的时间为 $O((n+m)\log(n+m))$，空间为 $O(n+m)$；堆中允许同一点存在多条旧记录，至多有 $O(m)$ 条成功松弛记录。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `Edge{to,weight}` | 邻接表项，表示当前点到 `to` 的有向边及非负权值。无向边要加入两个方向。 |
| `distance[v]` | 已知最短距离；初始为 `INF`，起点为 0。有限最短路必须小于 `INF`，计算时距离加边权不能溢出。 |
| `previous[v]` | 当前最短路树中的前驱点；不可达点和起点为 `-1`。 |
| `pq` | 小根堆，存入堆时的 `(距离,点)`；距离与当前 `distance` 不相同的记录已过期。 |
| `n` | `graph.size()-1`，有效点号为 `1..n`。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `dijkstra(graph,start)` | `graph` 为 1-based 邻接表，端点合法、权值非负，`start` 在 `1..n`；返回距离和前驱数组，不修改图。允许重边。 |
| `restorePath(start,target,previous)` | 使用同一次 Dijkstra 产生的前驱表和合法点号；返回起点到终点的点序列，不可达时返回空向量；不改 `previous`。 |

**4. 怎么调用**

有向图只加入给定方向；无向边要同时加入反向边。例中最短路为 `1->2->3->4`，长度 5，点 5 不可达：

```text
vector<vector<Edge>> graph(6);
graph[1].push_back({2, 2}); graph[1].push_back({3, 10});
graph[2].push_back({3, 1}); graph[3].push_back({4, 2});
DijkstraResult result = dijkstra(graph, 1);
assert(result.distance[4] == 5);
assert(result.distance[5] == INF);
assert(restorePath(1, 4, result.previous) == vector<int>({1, 2, 3, 4}));
assert(restorePath(1, 5, result.previous).empty());
```

模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = numeric_limits<ll>::max() / 4;

struct Edge {
    // 邻接表中的一项表示有向边“当前点 -> to”；无向边需手动加入反向项。
    int to;
    ll weight;
};

struct DijkstraResult {
    vector<ll> distance;  // INF 表示从 start 不可达
    vector<int> previous; // 最短路树中的前驱；start 和不可达点均为 -1
};

// 参数 graph 为 1-based 非负权邻接表、start 为合法起点；返回各点距离和前驱，不修改图。
DijkstraResult dijkstra(
    const vector<vector<Edge>>& graph,
    int start
) {
    // 仅适用于所有边权 >=0；允许重边。点编号为 1..n。
    int n = (int)graph.size() - 1;
    vector<ll> distance(n + 1, INF);
    vector<int> previous(n + 1, -1);
    // 小根堆保存“入堆时距离,点”；同一点可能有多条新旧记录。
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> pq;

    distance[start] = 0;
    pq.push({0, start});
    while (!pq.empty()) {
        auto [currentDistance, u] = pq.top();
        pq.pop();
        if (currentDistance != distance[u]) continue;  // 跳过已经失效的旧记录

        for (const Edge& edge : graph[u]) {
            int v = edge.to;
            // u 被取出时 distance[u] 已是当前最优；这里松弛一条出边 u->v。
            if (distance[v] > distance[u] + edge.weight) {
                distance[v] = distance[u] + edge.weight;
                previous[v] = u;
                pq.push({distance[v], v});
            }
        }
    }
    return {distance, previous};
}

// 参数 start/target 为点号，previous 是最短路前驱表；返回路径点序，不可达时空表；不改输入。
    vector<int> restorePath(int start, int target, const vector<int>& previous) {
    // 返回 start 到 target 的点序列；前驱链无法到 start 时返回空数组。
    vector<int> path;
    for (int v = target; v != -1; v = previous[v]) {
        path.push_back(v);
        if (v == start) break;
    }
    if (path.empty() || path.back() != start) return {};
    reverse(path.begin(), path.end());
    return path;
}
```

**5. 要改哪里**

- 无向图建边时为每条输入边插入两个 `Edge`；有向图只插入题面方向。
- 若要计算到某个终点，可在堆中取出终点的当前有效记录时提前结束；若还需要完整 `distance` 数组则不能提前停止。
- 存在负边时应改用 Bellman–Ford 或其他适用算法；仅过滤掉从起点暂时没走到的负边不够。
- 多源最短路可将所有源点以距离 0 入堆；前驱恢复需据题意处理多个起点。

**6. 自检**

示例距离 `distance[2..4]` 为 `2,3,5`，`distance[5]` 保持 `INF`，恢复路径应为 `[1,2,3,4]`。单点图起点距离为 0、路径为 `[1]`；零权边合法，重边保留也会由松弛选出较短结果。不可达距离不可直接参与普通加法。

**7. 坑**

- 有负权时答案错误：Dijkstra 的贪心确定性依赖所有边权非负，应换算法。
- 前驱链或距离异常：无向边只加了一个方向，或起点、终点编号越界。
- 堆反复处理旧状态：必须跳过 `currentDistance != distance[u]` 的记录。
- `INF` 输出成实际距离或参与加法：先判断是否等于 `INF`，且保证所有有限距离运算安全。

**8. 一句话原理**

每次确定当前距离最小的未过期堆记录，并用它松弛出边，非负权保证该距离不再变小。

**参考：**

- [OI Wiki：最短路](https://oi-wiki.org/graph/shortest-path/)

## 6.3 Bellman–Ford 与负环判断

**1. 它是做什么的**

Bellman–Ford 在有向带权图上求单源最短距离，允许负边，并检测从起点可达的负环。若检测到可达负环，返回布尔值 `true`，同时距离数组全部填为 `INF`；否则不可达点为 `INF`，其余为有限最短距离。时间最坏 $O(nm)$，空间为 $O(n)$（另有输入边表 $O(m)$）；无更新时提前结束。有限结果须能表示为 `long long` 且严格小于 `INF`。实现用 `__int128` 保存中间值，但其范围有限，输入仍须保证中间运算及 `BIG=2^120` 哨兵安全。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `DirectedEdge{from,to,weight}` | 一条有向边 `from -> to`；无向边要显式加入两个方向。 |
| `work[v]` | `__int128` 暂存距离；`BIG` 表示当前不可达。 |
| `distance[v]` | 最终 `long long` 距离；不可达或检测到负环时为 `INF`。 |
| `round` | 当前边表扫描轮次；至多扫描 `n` 次。 |
| `changed` | 本轮是否发生松弛；若为 false，算法可结束。 |
| `n`, `start` | 点数和起点；点编号为 `1..n`。 |

只有 `work[from]` 可达时才尝试松弛。第 `n` 轮仍有更新表示存在起点可达的负环；不保证报告与起点不连通的负环。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `bellmanFord(n,start,edges)` | `n>=1`，`start` 和所有边端点在 `1..n`；边表按有向边解释。返回 `{distance, hasReachableNegativeCycle}`，不修改 `edges`。若负环标志为真，距离数组全部为 `INF`；否则返回可达最短距离和不可达哨兵。 |

**4. 怎么调用**

准备点数、起点和有向边表；无向边按双向各放一条。示例中 `1->2->3->4` 的距离为 5，点 5 不可达；第二组边含起点可达负自环：

```text
vector<DirectedEdge> edges = {{1, 2, 4}, {1, 3, 5}, {2, 3, -2}, {3, 4, 3}};
auto result = bellmanFord(5, 1, edges);
assert(!result.second && result.first[4] == 5 && result.first[5] == INF);

vector<DirectedEdge> negative = {{1, 2, 1}, {2, 2, -1}};
auto cycle = bellmanFord(2, 1, negative);
assert(cycle.second && cycle.first[1] == INF && cycle.first[2] == INF);
```

模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = numeric_limits<ll>::max() / 4;

struct DirectedEdge {
    // 边方向固定为 from -> to；无向边若需要须显式加入两个方向。
    int from, to;
    ll weight;
};

// 参数 n/start/edges 为点数、起点和有向边表；返回距离及起点可达负环标志，不改边表。
pair<vector<ll>, bool> bellmanFord(
    int n,
    int start,
    const vector<DirectedEdge>& edges
) {
    // 用更宽的中间值避免 long long 松弛溢出；有限答案须能放入 ll 且小于 INF。
    const __int128_t BIG = (__int128_t)1 << 120;
    vector<__int128_t> work(n + 1, BIG);
    work[start] = 0;

    // 每轮扫描所有边；原地松弛可一次推进多条边，但 n 轮判环结论仍成立。
    for (int round = 1; round <= n; ++round) {
        bool changed = false;
        for (const auto& edge : edges) {
            if (work[edge.from] == BIG) continue; // 不可达点不能参与松弛
            __int128_t candidate = work[edge.from] + edge.weight;
            if (candidate < work[edge.to]) {
                work[edge.to] = candidate;
                changed = true;
                if (round == n) return {vector<ll>(n + 1, INF), true};
            }
        }
        if (!changed) break;
    }

    vector<ll> distance(n + 1, INF);
    for (int v = 1; v <= n; ++v) {
        if (work[v] != BIG) {
            // 调用方需保证所有可达最短距离均在 ll 范围内且严格小于 INF。
            distance[v] = (ll)work[v];
        }
    }
    return {distance, false};
}
```

**5. 要改哪里**

- 若需检测全图任意位置的负环，可新增超级源向所有原点连零权边，或改实现把所有初始距离设为 0；当前接口只判断 `start` 可达的负环。
- 若需输出负环影响的具体点或恢复路径，需要额外保存前驱并追踪第 `n` 轮更新；当前只返回布尔标志，且负环时抹去所有距离。
- 无向负边会形成可达的二向负环（同一边往返），应根据题目语义确认是否允许。
- 边权或路径极大时，调整数值类型与哨兵设计并证明中间值范围；`__int128` 也不是无限精度。

**6. 自检**

第一组中距离依次为 `dist[1]=0, dist[2]=4, dist[3]=2, dist[4]=5`，点 5 为 `INF`。第二组负自环可从 1 到达，返回负环标志且所有距离为 `INF`。负环若位于与起点断开的分量，不应触发该接口的标志；单点无边图返回距离 0 且无负环。

**7. 坑**

- `INF` 被负边松弛成有限值：跳过不可达的 `from`，不要对哨兵做加法。
- 把任意负环都当成检测结果：当前只检测从 `start` 可达的负环。
- 负环时读取部分距离：函数明确将整张距离数组置为 `INF`，此时只有布尔标志可用。
- 以为 `__int128` 无溢出风险：它只扩大范围，仍需约束点数、边权和累加值。

**8. 一句话原理**

反复松弛所有边至多 `n-1` 轮求有限最短路，第 `n` 轮仍能改进就说明起点可达负环。

**参考：**

- [OI Wiki：Bellman–Ford 算法](https://oi-wiki.org/graph/shortest-path/#bellmanford-%E7%AE%97%E6%B3%95)

## 6.4 Floyd 全源最短路

**1. 它是做什么的**

Floyd–Warshall 在点数较小的有向加权图上计算所有点对的最短距离，可含负边，但要求不存在负环。输入和结果都是 1-based 距离矩阵；`INF` 表示不可达。时间为 $O(n^3)$，矩阵空间为 $O(n^2)$。算法原地修改矩阵；每次只在两段都可达时相加，但仍要求有限边权及存储的有限距离小于 `INF`，所有候选加法不溢出 `long long`。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `distance[u][v]` | 当前已知 `u` 到 `v` 的最短距离；初值对角线为 0、其他为 `INF`。 |
| `k` | 当前允许作为中转点的编号；必须位于最外层循环。 |
| `i`, `j` | 当前尝试改进的起点和终点。 |
| `INF` | 不可达哨兵；不能直接参与加法。 |

每轮 `k` 后，`distance[i][j]` 已考虑编号不超过 `k` 的点作为中转。完成后若某个 `distance[i][i] < 0`，说明存在负环。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `makeDistanceMatrix(n)` | 为 `n` 个点创建 `(n+1)×(n+1)` 矩阵；点编号 `1..n`，对角线 0、其余 `INF`。返回新矩阵。 |
| `addDirectedEdge(distance,u,v,weight)` | 对矩阵单元取当前值与 `weight` 的较小值；原地修改 `distance[u][v]`，不自动添加反向边；端点须合法。 |
| `floydWarshall(distance)` | 参数为合法 1-based 方阵且无负环；原地覆盖所有点对距离，无返回值。调用后可检查对角线发现负环，但此时最短距离不具有限定义。 |

**4. 怎么调用**

先创建矩阵，再加入有向边；无向边对两个方向各调用一次。例中最短路 `1->2->3->4` 长度为 4，反向不可达：

```text
vector<vector<ll>> distance = makeDistanceMatrix(4);
addDirectedEdge(distance, 1, 2, 3);
addDirectedEdge(distance, 2, 3, -1);
addDirectedEdge(distance, 1, 3, 5);
addDirectedEdge(distance, 3, 4, 2);
floydWarshall(distance);
assert(distance[1][4] == 4);
assert(distance[1][3] == 2);
assert(distance[4][1] == INF);
assert(distance[2][2] == 0);
```

模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = numeric_limits<ll>::max() / 4;

// 参数 n 为点数；返回 n+1 方阵，1..n 对角为 0、其余 INF；分配新矩阵。
    vector<vector<ll>> makeDistanceMatrix(int n) {
    // 矩阵使用 1..n；distance[u][v] 表示有向距离，初始仅自身到自身为 0。
    vector<vector<ll>> distance(n + 1, vector<ll>(n + 1, INF));
    for (int i = 1; i <= n; ++i) distance[i][i] = 0;
    return distance;
}

// 参数为距离矩阵、端点和权值；返回 void，以较小权值写 distance[u][v]；不自动添加反向边。
    void addDirectedEdge(vector<vector<ll>>& distance, int u, int v, ll weight) {
    // 保留同方向重边中的最小值；无向边需再调用一次 (v,u,weight)。
    distance[u][v] = min(distance[u][v], weight);
}

// 参数是 1-based 方阵；返回 void，原地覆盖为全源最短距离，须无负环且加法不溢出。
    void floydWarshall(vector<vector<ll>>& distance) {
    int n = (int)distance.size() - 1;
    // k 必须最外层：完成第 k 轮后，只允许 1..k 作为内部中转点。
    for (int k = 1; k <= n; ++k) {
        for (int i = 1; i <= n; ++i) {
            if (distance[i][k] == INF) continue;
            for (int j = 1; j <= n; ++j) {
                if (distance[k][j] == INF) continue;
                // 两段都可达才相加，避免 INF 参与运算产生伪路径。
                distance[i][j] = min(
                    distance[i][j],
                    distance[i][k] + distance[k][j]
                );
            }
        }
    }
}
```

**5. 要改哪里**

- 无向边需调用两次 `addDirectedEdge`，并确保两个方向权值一致。
- 检测负环时在算法结束后检查所有 `distance[i][i] < 0`；存在负环的相关最短距离不能当作有限答案使用。
- 点数较大时，改用单源算法逐个起点运行；Floyd 的立方时间和平方空间增长很快。
- 若需记录路径，额外维护前驱或下一跳矩阵，并在每次成功松弛时同步更新；当前模板只返回距离。

**6. 自检**

示例中 `distance[1][4]` 应为 4，`distance[1][3]` 应为 2，`distance[4][1]` 保持 `INF`，对角线仍为 0。无边的单点图距离为 0；重边应保留较小权值。含负边但无负环的路径应正常缩短；增加可达负环后至少一个对角线会变为负数。

**7. 坑**

- 结果漏掉中转路径：`k` 不在最外层，破坏动态规划依赖顺序。
- `INF` 相加产生伪距离：相加前分别检查 `distance[i][k]`、`distance[k][j]` 可达。
- 平行边覆盖成较大权值：加边应取最小值。
- 有负环仍输出最短距离：负环可无限降低路径代价，检测到后距离不再有有限定义。

**8. 一句话原理**

逐步开放每个点作为中转，尝试用 `i->k->j` 改进所有点对距离。

**参考：**

- [OI Wiki：Floyd 算法](https://oi-wiki.org/graph/shortest-path/#floyd-%E7%AE%97%E6%B3%95)

## 6.5 Kruskal 最小生成树

**1. 它是做什么的**

Kruskal 为 1-based 连通无向加权图求最小生成树；若图不连通，则返回最小生成森林及其总权。每条无向边在输入边表中只出现一次，权值可为负，重边允许。排序时间为 $O(m\log m)$，并查集合并额外耗时 $O(m\alpha(n))$；整体为 $O(n+m\log(m+1))$，空间为 $O(n+m)$，含按值复制的边表和结果边集。至少要求 `n>=1` 且边端点合法。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `WeightedEdge{u,v,weight}` | 一条无向边；边表中只放一次。 |
| `DSU.parent`, `DSU.sizeOf` | 并查集父节点与根集合大小，用来判断加入边是否成环。 |
| `edges` | `kruskal` 按值接收并排序的边表副本；调用方原向量不变。 |
| `chosen` | 被选入生成树/森林的边；最多 `n-1` 条。 |
| `connected` | 是否选出 `n-1` 条边；`n=1` 时空边集也算连通生成树。 |
| `totalWeight` | `chosen` 中边权之和；不连通时是森林总权，不是生成树权。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `DSU(n)` | 初始化点 `1..n` 为单元素集合；内部用于 Kruskal。 |
| `find(x)` | 返回元素 `x` 的根并压缩路径；要求 `x` 在 `1..n`。 |
| `unite(a,b)` | 合并两点所在集合；成功返回 `true`，已连通返回 `false`，并更新根大小。 |
| `kruskal(n,edges)` | 参数为正点数和合法端点的无向边表，边只存一次；返回 `{connected,totalWeight,chosen}`，不修改调用方的 `edges`。同权边顺序任意。 |

内部排序比较器按 `weight` 升序排列；同权时不承诺选边顺序。

**4. 怎么调用**

准备边表后调用 `kruskal`，根据 `connected` 判断是否存在生成树。例中最轻边权为 -1、1、2，总权 2：

```text
vector<WeightedEdge> edges = {{1, 2, 1}, {2, 3, 2}, {1, 3, 4}, {3, 4, -1}};
KruskalResult result = kruskal(4, edges);
assert(result.connected && result.totalWeight == 2);
assert(result.chosen.size() == 3);
```

模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct DSU {
    // 只有根的 sizeOf 有效；路径压缩和按大小合并保证近常数均摊复杂度。
    vector<int> parent, sizeOf;
    // 参数 n 是点编号上界；建立 1..n 单元素集合并初始化内部父节点和大小。
    explicit DSU(int n) : parent(n + 1), sizeOf(n + 1, 1) {
        iota(parent.begin(), parent.end(), 0);
    }
    // 参数 x 是 1..n 元素；返回集合代表并压缩访问路径。
    int find(int x) {
        return parent[x] == x ? x : parent[x] = find(parent[x]);
    }
    // 参数 a/b 是 1..n 元素；成功合并返回 true，否则 false；修改代表和集合大小。
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (sizeOf[a] < sizeOf[b]) swap(a, b);
        parent[b] = a;
        sizeOf[a] += sizeOf[b];
        return true;
    }
};

struct WeightedEdge {
    // 无向边在边表中只保存一次；允许负权、重边和自环。
    int u, v;
    ll weight;
};

struct KruskalResult {
    bool connected;
    ll totalWeight;
    vector<WeightedEdge> chosen;
};

// 参数 n 为点数、edges 为每条无向边只存一次的边表副本；返回生成森林信息，不改调用者边表。
    KruskalResult kruskal(int n, vector<WeightedEdge> edges) {
    // 按权从小到大扫描；不成环的最轻边一定可安全加入当前生成森林。
// 比较器参数为两条边；权值较小者排前，同权顺序任意；不修改边对象。
        sort(edges.begin(), edges.end(), [](const auto& a, const auto& b) {
        return a.weight < b.weight;
    });

    DSU dsu(n);
    ll totalWeight = 0;
    vector<WeightedEdge> chosen;
    for (const auto& edge : edges) {
        if (!dsu.unite(edge.u, edge.v)) continue;  // 同一连通块：加入会成环
        totalWeight += edge.weight;
        chosen.push_back(edge);
        if ((int)chosen.size() == n - 1) break;
    }
    return {(int)chosen.size() == n - 1, totalWeight, chosen};
}
```

**5. 要改哪里**

- 只需要最小生成森林总权时，可不保存或返回 `chosen`，减少结果边集空间。
- 若要输出树边或计算其他边集合性质，可沿用 `chosen`；边权相同可能有多种合法最优树，不要依赖固定选边顺序。
- 有向图的最小生成树不是该问题定义，不能直接使用本算法。
- 若需要最大生成树，可按权值降序排序；其余并查集判环逻辑不变。

**6. 自检**

示例选中 `3-4(-1)`、`1-2(1)`、`2-3(2)`，总权为 2 且有 3 条边。单点无边图应连通且总权 0。四点仅有 `1-2(-2)`、`3-4(3)` 时，应返回不连通、两条森林边、总权 1。自环不会被选入；平行边只会选择更有利的连接。

**7. 坑**

- 把不连通结果当生成树：检查 `connected`；否则 `totalWeight` 只表示森林权值。
- 无向边重复放两个方向：边表要求每条无向边只保存一次，重复反向项会增加冗余但不会改变并查集正确性。
- 忽略负权：Kruskal 按升序照常处理负边。
- 自环被计入：两端根相同，`unite` 返回 `false`，该边跳过。

**8. 一句话原理**

从轻到重加入连接不同连通块的边，跳过会成环的边，直到得到生成树或扫描完边表。

**参考：**

- [OI Wiki：最小生成树](https://oi-wiki.org/graph/mst/)

## 6.6 二分图判定

**1. 它是做什么的**

二分图判定检查无向图的每条边能否连接两个不同组，等价于判断是否含奇环。模板逐个连通块做 BFS 染色，图可不连通；时间为 $O(n+m)$，额外空间为 $O(n)$（颜色与队列），输入邻接表另占 $O(n+m)$。成功时返回一组 `0/1` 染色；失败时立即返回 `false`，此时颜色可能只填了一部分。自环会判为非二分图。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `graph[u]` | 无向邻接表；每条边应在两个端点列表中各出现一次。 |
| `color[u]` | `-1` 表示未访问，`0` 或 `1` 表示所在组。函数会先清空并重新赋值。 |
| `start` | 当前尚未染色的连通块起点。 |
| `q` | 当前 BFS 队列；弹出 `u` 时为所有未染色邻点赋予 `color[u]^1`。 |
| `n` | `graph.size()-1`，点编号为 `1..n`。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `colorBipartite(graph,color)` | 参数为 1-based 无向图和颜色输出向量；返回是否二分图，并将 `color` 重置为长度 `n+1`。成功时每个点均为 0/1 且相邻点异色；失败时可能提前返回，颜色不保证完整。 |

**4. 怎么调用**

先将无向边双向加入邻接表，再调用并检查返回值。示例有两条非连通链，所有相邻点应异色；另以自环检查失败：

```text
vector<vector<int>> graph(6);
graph[1].push_back(2); graph[2].push_back(1);
graph[2].push_back(3); graph[3].push_back(2);
graph[4].push_back(5); graph[5].push_back(4);
vector<int> color;
assert(colorBipartite(graph, color));
assert(color[1] != color[2] && color[2] != color[3]);
assert(color[4] != color[5]);

vector<vector<int>> loopGraph(2);
loopGraph[1].push_back(1);
assert(!colorBipartite(loopGraph, color));
```

模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

// 参数 graph 为 1-based 无向邻接表；返回是否二分图，并覆盖 color 为染色结果（失败时可能不完整）。
    bool colorBipartite(const vector<vector<int>>& graph, vector<int>& color) {
    // graph 必须是无向图的双向邻接表；-1 未访问，0/1 表示两侧颜色。
    int n = (int)graph.size() - 1;
    color.assign(n + 1, -1);

    // 必须枚举所有起点，才能覆盖非连通图中的每个连通块。
    for (int start = 1; start <= n; ++start) {
        if (color[start] != -1) continue;
        queue<int> q;
        color[start] = 0;
        q.push(start);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (int v : graph[u]) {
                if (color[v] == -1) {
                    // 每条无向边两端必须异色；异或 1 得到另一种颜色。
                    color[v] = color[u] ^ 1;
                    q.push(v);
                } else if (color[v] == color[u]) {
                    return false;
                }
            }
        }
    }
    return true;
}
```

**5. 要改哪里**

- 若输入是有向图但问题问底层无向图是否二分，先按题意忽略方向并构造无向邻接表；若方向本身重要，本模板不适用。
- 若要恢复两侧顶点集合，成功后按 `color[u]` 分组即可。
- 若只需要奇环存在性，仍可使用返回值；要输出具体奇环则需额外记录 BFS 父节点并在冲突边处恢复环。

**6. 自检**

示例中两条链都可交替染色，函数返回 `true`。单点无边图也为二分图；三角形 `1-2-3-1` 返回 `false`；自环返回 `false`。重边两端仍须异色，不会改变结论。注意非连通图每个分量都必须处理。

**7. 坑**

- 只有部分分量被染色：只从一个点开始 BFS；应遍历所有 `color[start] == -1` 的点。
- 把 `color == 0` 当未访问：未访问标记是 `-1`。
- 有向边漏掉反向：接口要求无向邻接表双向存边。
- 失败后使用完整染色：发现冲突会立即返回，只有成功时颜色才是完整划分。

**8. 一句话原理**

从每个未染色分量起步，沿边交替染色；同一条边两端同色就存在奇环。

**参考：**

- [OI Wiki：二分图](https://oi-wiki.org/graph/bi-graph/)

## 6.7 二分图最大匹配（增广路）

**1. 它是做什么的**

给定左右两部和左点到右点的可选边，增广路算法求最大匹配，并在 `matchRight` 中记录每个右点的左搭档。左右点各自编号 `1..leftCount`、`1..rightCount`，两套编号独立。适合中等规模二分图；时间为 $O(L E)$，其中 `L=leftCount`、`E` 为邻接边数，空间为 $O(L+R+E)$。更大规模可考虑 Hopcroft–Karp。该对象应先建完图，再只调用一次 `maximumMatching()`；当前实现不支持安全地在同一对象上重复求解或增量加边后继续求解，应重新建对象。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `graphLeft[u]` | 左点 `u` 可连接的右点列表。 |
| `matchRight[v]` | 与右点 `v` 匹配的左点；0 表示未匹配。 |
| `seen[v]` | 右点在当前增广尝试中是否访问过，以 `visitToken` 区分轮次。 |
| `leftCount`, `rightCount` | 左右部点数；编号从 1 开始。 |
| `visitToken` | 每尝试一个新左点递增，避免每轮清空 `seen`。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `BipartiteMatcher(L,R)` | 创建有 `L` 个左点、`R` 个右点的空图和空匹配；点数应非负。 |
| `addEdge(left,right)` | 添加一条左到右的可匹配边，无返回值；参数需分别在 `1..L`、`1..R`。建图应在求解前完成。 |
| `augment(u)` | 递归尝试为左点 `u` 找增广路；成功时修改 `matchRight` 并返回 `true`，失败返回 `false`。内部辅助函数，不应由调用者单独启动。 |
| `maximumMatching()` | 返回最大匹配大小，并写入 `matchRight`。应在静态图上对新对象调用一次；重复调用会再次尝试已匹配左点，可能造成同一左点占据多个右点。 |

**4. 怎么调用**

先确定左右部、加入所有边，再调用一次匹配函数。下例中左点 1 可连两个右点，左点 2 只可连右点 1；算法会为左点 1 改配到右点 2：

```text
BipartiteMatcher matcher(2, 2);
matcher.addEdge(1, 1);
matcher.addEdge(1, 2);
matcher.addEdge(2, 1);
assert(matcher.maximumMatching() == 2);
assert(matcher.matchRight[1] == 2 && matcher.matchRight[2] == 1);
```

模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

struct BipartiteMatcher {
    int leftCount, rightCount;
    // graphLeft[u] 只存“左部 u -> 右部 v”，左右编号属于两个独立空间。
    vector<vector<int>> graphLeft;
    vector<int> matchRight; // matchRight[v]=u；0 表示右点 v 当前未匹配
    vector<int> seen;       // 时间戳：本轮增广中右点是否已尝试
    int visitToken = 0;

    // 参数 leftCount/rightCount 为左右部点数；创建空二分图并初始化匹配及访问时间戳。
    BipartiteMatcher(int leftCount, int rightCount)
        : leftCount(leftCount), rightCount(rightCount),
          graphLeft(leftCount + 1), matchRight(rightCount + 1, 0),
          seen(rightCount + 1, 0) {}

    // 参数 left/right 分别为左右部合法点号；返回 void，将兼容边加入 graphLeft。
    void addEdge(int left, int right) {
        graphLeft[left].push_back(right);
    }

    // 参数 u 是当前待匹配左点；返回是否找到增广路，成功时修改 matchRight 的匹配关系。
    bool augment(int u) {
        // 不变量：尝试为左点 u 找交错路；成功时沿递归链整体改配。
        for (int v : graphLeft[u]) {
            if (seen[v] == visitToken) continue;
            seen[v] = visitToken;
            // v 空闲，或能把 v 的旧搭档改配到别处，就可令 u 占用 v。
            if (matchRight[v] == 0 || augment(matchRight[v])) {
                matchRight[v] = u;
                return true;
            }
        }
        return false;
    }

    // 无参数；从新对象的空匹配求最大匹配数并写 matchRight；只调用一次，重算须重建对象。
    int maximumMatching() {
        int matching = 0;
        for (int u = 1; u <= leftCount; ++u) {
            ++visitToken; // 每个左点必须拥有独立访问轮次，不能共用 seen 状态
            if (augment(u)) ++matching;
        }
        return matching;
    }
};
```

**5. 要改哪里**

- 若左右两部点数不同，分别传入真实大小；编号都从 1 开始，不要把右部编号偏移后再传给 `addEdge`。
- 若要输出左点匹配，可遍历 `matchRight[v]`，反向构造左到右关系；当前没有单独的 `matchLeft` 数组。
- 若图在求解后还要修改，创建新对象并重新加入完整边集；当前匹配状态与递归访问状态没有重置接口。
- 极大图可换 Hopcroft–Karp，简单 DFS 增广的 $O(L E)$ 可能过慢。

**6. 自检**

示例最终匹配是 `1-2`、`2-1`，大小为 2；若只有边 `1-1`，匹配大小为 1；无边图大小为 0。验证每个非零 `matchRight[v]` 均为合法左点，且不同右点不应被误认为同一左点有多份匹配。求解后不要再次调用同一对象。

**7. 坑**

- 匹配数偏小：每个新左点前没有新的 `visitToken`，旧的 `seen` 阻断了重试。
- 左右编号混淆：`graphLeft` 的行号是左点，列表元素是右点。
- 重复调用后匹配非法：函数会重新尝试已有匹配的左点，但不先释放旧右点；每次求解使用新对象。
- 误以为 `matchRight[v]==0` 表示左点未匹配：它只描述右部状态，左侧匹配关系需从该数组反查。

**8. 一句话原理**

逐个尝试给左点找路，必要时沿交替路改配旧搭档，从而增加一个匹配边。

**参考：**

- [OI Wiki：二分图最大匹配](https://oi-wiki.org/graph/graph-matching/bigraph-match/)

## 6.8 强连通分量（Tarjan）

**1. 它是做什么的**

Tarjan 算法把 1-based 有向图划分成强连通分量：同一分量内任意两点互相可达，且该集合极大。模板为每个点赋 `component[u]` 编号并统计分量数，时间 $O(n+m)$，额外数组和递归栈空间 $O(n)$；邻接表另占 $O(n+m)$。结果可用于缩点，分量间有向边形成 DAG。递归深度最坏为 $n$。对象只可 `run()` 一次；图变更或需重新计算时创建新对象。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `graph[u]` | 从 `u` 出发的有向边列表；重边不影响分量划分。 |
| `dfn[u]` | 首次访问时间；0 表示尚未访问。 |
| `low[u]` | 从 DFS 子树沿树边和仍在栈中的返边可到达的最小 `dfn`。 |
| `st`, `inStack` | Tarjan 栈及成员标记；只存尚未归入分量的活跃点。 |
| `component[u]` | 点所属编号；初始 `-1`，最终范围 `0..componentCount-1`。具体编号顺序不应当作语义。 |
| `timer`, `componentCount` | DFS 时间计数及已弹出的分量数。 |

当 `low[u] == dfn[u]` 时，`u` 是一个分量的根；从栈顶弹到 `u` 的点属于同一分量。访问到已访问点时，只有它仍在栈中才更新 `low`，并使用 `dfn[v]`。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `TarjanSCC(graph)` | 接收 1-based 邻接表的常量引用并初始化状态；图必须比对象活得久，且构造后到 `run()` 前保持不变。 |
| `dfs(u)` | 内部递归处理尚未访问的点，写入 `dfn`、`low`、`component`、栈状态；通常不由调用者直接调用。 |
| `run()` | 无参数、无返回值；遍历所有未访问点并写入分量编号和数量。只能在对象尚未运行时调用；需重算时新建对象。 |

**4. 怎么调用**

先创建图并加入有向边，再构造 solver 并运行。示例中的 `{1,2}` 和 `{3,4}` 分别互相可达，点 5 独立：

```text
vector<vector<int>> graph(6);
graph[1].push_back(2); graph[2].push_back(1);
graph[2].push_back(3);
graph[3].push_back(4); graph[4].push_back(3);
TarjanSCC solver(graph);
solver.run();
assert(solver.componentCount == 3);
assert(solver.component[1] == solver.component[2]);
assert(solver.component[3] == solver.component[4]);
assert(solver.component[1] != solver.component[3]);
```

模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

struct TarjanSCC {
    // graph 是 1-based 有向邻接表；只按题目方向加边，重边不影响正确性。
    const vector<vector<int>>& graph;
    int n, timer = 0, componentCount = 0;
    // dfn：首次访问序；low：经 DFS 树边和栈内返边能到达的最小 dfn。
    vector<int> dfn, low, component, st;
    vector<char> inStack;

    // 参数 graph 是 1-based 有向邻接表；保存其引用并分配 SCC 工作数组，图须长于对象生命周期。
    explicit TarjanSCC(const vector<vector<int>>& graph)
        : graph(graph), n((int)graph.size() - 1),
          dfn(n + 1, 0), low(n + 1, 0), component(n + 1, -1),
          inStack(n + 1, false) {}

    // 参数 u 是未访问顶点；返回 void，递归遍历其可达区域并更新 dfn/low/栈/分量编号。
    void dfs(int u) {
        // st 只保存尚未归入任何 SCC 的活跃点，inStack 与之同步。
        dfn[u] = low[u] = ++timer;
        st.push_back(u);
        inStack[u] = true;

        for (int v : graph[u]) {
            if (dfn[v] == 0) {
                dfs(v);
                low[u] = min(low[u], low[v]);
            } else if (inStack[v]) {
                // 已访问且仍在栈中才可能属于当前 SCC；此处必须使用 dfn[v]。
                low[u] = min(low[u], dfn[v]);
            }
        }

        if (low[u] == dfn[u]) {
            // u 是一个 SCC 的 DFS 根，弹到 u 为止的点恰属于同一分量。
            while (true) {
                int v = st.back();
                st.pop_back();
                inStack[v] = false;
                component[v] = componentCount;
                if (v == u) break;
            }
            ++componentCount;
        }
    }

    // 无参数；从所有未访问点启动 DFS 并写 component/componentCount；对象仅应运行一次。
    // 无参数；遍历全部连通区域并填充 SCC 编号及数量；须在对象尚未运行时调用。
    void run() {
        for (int u = 1; u <= n; ++u) {
            if (dfn[u] == 0) dfs(u);
        }
    }
};
```

**5. 要改哪里**

- 缩点时遍历原边 `u->v`；当 `component[u] != component[v]` 时加入分量图边，按后续算法需要去重。
- 需要拓扑序或 DAG DP 时，在缩点图上处理；原图的分量编号只用于分组，不应假定编号本身就是可依赖的拓扑顺序。
- 图更新或换一张图后重新计算，创建新 solver 并传入新图；该类保存图引用，且 `run` 不清空时间戳、栈和分量状态。
- 若递归深度可能过大，应改成迭代 Tarjan 或选用适合环境的实现；当前函数是递归 DFS。

**6. 自检**

示例应得到 3 个分量：`{1,2}`、`{3,4}`、`{5}`；编号具体值不固定，只检查相等关系。单点无边图有一个分量；单向边 `1->2` 的两个点属于不同分量。每个点最终 `component[u] >= 0`，重边不改变结果。

**7. 坑**

- 不同分量被合并：遇到已访问且仍在栈中的点时错用 `low[v]`；应以 `dfn[v]` 更新。
- 已弹栈的点影响 `low`：只对 `inStack[v]` 为真的已访问邻点更新。
- 重新运行得到旧结果：`run()` 不重置状态；重算需新对象。
- solver 引用失效：传入的图对象必须在 solver 生命周期内保持存在。

**8. 一句话原理**

用 `low` 判断 DFS 子树能否回到更早的活跃点，无法回到时就从栈中切出一个完整强连通分量。

**参考：**

- [OI Wiki：强连通分量](https://oi-wiki.org/graph/scc/)

## 6.9 割点与桥（Tarjan）

**1. 它是做什么的**

在 1-based 无向图中，割点是删除后连通块数增加的顶点，桥是删除后连通块数增加的边。模板可处理非连通图、重边和自环；运行时间为 $O(n+m)$，额外数组和递归栈为 $O(n)$，邻接表为 $O(n+m)$。桥以端点对返回，平行边中只有真正会断开的边才被判为桥。DFS 递归深度最坏为 $n$。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `Edge{to,id}` | 邻接项；无向边的两个方向共用一个 `id`。 |
| `dfn[u]` | 点 `u` 的首次访问时间，0 表示未访问。 |
| `low[u]` | 从 `u` 的 DFS 子树经树边和返边能到达的最小访问时间。 |
| `isCutVertex[u]` | 是否为割点；根节点使用至少两个 DFS 子树的特殊条件。 |
| `bridges` | 桥端点对 `(u,v)`；方向取决于 DFS 父子关系。 |
| `parentEdge` | 进入当前点的边编号；只跳过这一条边，从而保留通向同一父点的平行边。 |
| `timer`, `edgeCount` | 访问时间计数和下一条无向边的编号。 |

非根点若存在孩子 `v` 满足 `low[v] >= dfn[u]`，则 `u` 是割点；若 `low[v] > dfn[u]`，父子边是桥。根点割点条件另算。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `UndirectedLowlink(n)` | 分配 `1..n` 的图和工作数组；点数应非负。 |
| `addEdge(u,v)` | 参数为合法点号；添加一条无向边并自动插入双向邻接项，共享边编号；无返回值。每条输入边只调用一次。 |
| `dfs(u,parentEdge)` | 内部递归填充 `dfn/low` 并追加割点、桥；根的边编号传 `-1`，通常不由调用者直接调用。 |
| `run()` | 无参数、无返回值；遍历所有连通块并写结果。须在加完边后对新对象调用一次；重算需新建对象。 |

**4. 怎么调用**

先加入所有无向边，再运行一次。例中三角形含一条平行边，尾部链上的两条边为桥，3 和 4 为割点，6 是孤立点：

```text
UndirectedLowlink solver(6);
solver.addEdge(1, 2); solver.addEdge(1, 2);
solver.addEdge(2, 3); solver.addEdge(3, 1);
solver.addEdge(3, 4); solver.addEdge(4, 5);
solver.run();
assert(solver.isCutVertex[3] && solver.isCutVertex[4]);
assert(!solver.isCutVertex[1] && !solver.isCutVertex[6]);
assert(solver.bridges.size() == 2);
bool has34 = false, has45 = false;
for (auto [u, v] : solver.bridges) {
    if ((u == 3 && v == 4) || (u == 4 && v == 3)) has34 = true;
    if ((u == 4 && v == 5) || (u == 5 && v == 4)) has45 = true;
}
assert(has34 && has45);
```

模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

struct UndirectedLowlink {
    // 同一条无向边的两个邻接项共享 id；这是正确处理父子重边的关键。
    struct Edge { int to, id; };

    int n, timer = 0, edgeCount = 0;
    vector<vector<Edge>> graph;
    vector<int> dfn, low;
    vector<char> isCutVertex;
    vector<pair<int, int>> bridges;

    // 参数 n 为点数；初始化无向邻接表及割点/桥工作数组。
    explicit UndirectedLowlink(int n)
        : n(n), graph(n + 1), dfn(n + 1), low(n + 1),
          isCutVertex(n + 1, false) {}

    // 参数 u/v 是 1..n 端点；返回 void，加入一条带共享边编号的无向边。
    void addEdge(int u, int v) {
        // 每条无向边只调用一次，内部自动加入 u->v 与 v->u 两个方向。
        graph[u].push_back({v, edgeCount});
        graph[v].push_back({u, edgeCount});
        ++edgeCount;
    }

    // 参数 u 为当前点、parentEdge 为进入该点的边 id（根传 -1）；返回 void，写 lowlink 并追加割点/桥。
    void dfs(int u, int parentEdge) {
        // low[u]：从 u 的 DFS 子树经至多一条非树边能到达的最小 dfn。
        dfn[u] = low[u] = ++timer;
        int childCount = 0;

        for (const Edge& edge : graph[u]) {
            int v = edge.to;
            if (edge.id == parentEdge) continue; // 只跳过来时那一条边，不跳所有父点边
            if (dfn[v] == 0) {
                ++childCount;
                dfs(v, edge.id);
                low[u] = min(low[u], low[v]);
                if (low[v] > dfn[u]) bridges.push_back({u, v}); // 子树无法绕回 u 或更高
                // 非根 u：v 子树无法越过 u 时，删除 u 会把 v 子树分离。
                if (parentEdge != -1 && low[v] >= dfn[u]) isCutVertex[u] = true;
            } else {
                low[u] = min(low[u], dfn[v]);
            }
        }

        // DFS 根没有父侧，只有至少两个独立 DFS 子树时才是割点。
        if (parentEdge == -1 && childCount >= 2) isCutVertex[u] = true;
    }

    // 无参数；遍历无向图所有连通块并追加割点/桥结果；请在 addEdge 完成后调用一次。
    void run() {
        for (int u = 1; u <= n; ++u) {
            if (dfn[u] == 0) dfs(u, -1);
        }
    }
};
```

**5. 要改哪里**

- 若要统计删除点后连通块数量，需另外累计各 DFS 子树的分离贡献；当前只给割点布尔标记。
- 若要按边编号输出桥，可在结果中同时保存树边 `id`；当前 `bridges` 仅保存端点。
- 若图会修改或要重新计算，创建新对象并重新加入边；`run()` 不清空 `timer`、结果数组或图。
- 有向图的强连通性不是本模板的问题，应改用 SCC 算法。

**6. 自检**

示例中平行的 `1-2` 边都不是桥，三角形任删一边仍连通；只有 `3-4` 和 `4-5` 是桥，删除 3 或 4 会使连通块增加。单独一条边的两端都不是割点但该边是桥；孤立点不是割点。重边测试可确认 DFS 只跳过父边编号。

**7. 坑**

- 割点或桥判定边界错：割点非根用 `>=`，桥用严格 `>`。
- 根节点误判：根至少有两个 DFS 树孩子才是割点。
- 平行边被误判为桥：只跳过进入点的父边 ID，不能跳过所有通向父节点的边。
- 非连通部分漏掉：`run()` 必须从每个未访问点启动 DFS。
- 重跑得到旧状态：添加边后重新计算应新建对象并重新加边。

**8. 一句话原理**

`low` 记录子树能否绕回祖先；无法绕回时，相应树边是桥，无法越过当前点时当前点是割点。

**参考：**

- [OI Wiki：割点和桥](https://oi-wiki.org/graph/cut/)

## 6.10 最近公共祖先（倍增 LCA）

**1. 它是做什么的**

倍增 LCA 在静态、连通、无向树上预处理祖先表，支持最近公共祖先查询及向上提升。点编号为 `1..n`，根深度为 0。预处理时间和空间均为 $O(n\log n)$；每次 `lca` 或 `lift` 为 $O(\log n)$。构造器通过常量引用读取邻接表，不修改也不保存输入图引用。输入必须是无环、无重边、无自环的单棵树；不支持森林中跨树查询。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `depth[u]` | 根到 `u` 的边数；根深度 0。 |
| `up[j][u]` | `u` 的第 `2^j` 个祖先；越过根统一到虚拟点 0。 |
| `levels` | 足以表示任意树内向上距离的祖先层数。 |
| `q` | 构造时 BFS 定根的队列。 |
| `root` | 调用者选择的合法根；更换根会改变深度和祖先关系。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `BinaryLiftingLCA(tree,root)` | `tree` 是 1-based 连通无向树，`root` 在 `1..n`；建立深度和祖先表，不改 `tree`。 |
| `lift(u,steps)` | 返回从 `u` 向上 `steps` 条边到达的祖先；要求 `steps` 在 `0..depth[u]`。 |
| `lca(u,v)` | 返回同一棵树中两点的最近公共祖先；不修改预处理表。 |

**4. 怎么调用**

先双向建树，再指定根构造对象；之后重复查询。示例中路径为 `1-2-4, 1-2-5, 1-3`：

```text
vector<vector<int>> tree(6);
tree[1] = {2, 3}; tree[2] = {1, 4, 5};
tree[3] = {1}; tree[4] = {2}; tree[5] = {2};
BinaryLiftingLCA lcaSolver(tree, 1);
assert(lcaSolver.lca(4, 5) == 2);
assert(lcaSolver.lca(4, 3) == 1);
assert(lcaSolver.lift(4, 1) == 2);
assert(lcaSolver.depth[4] + lcaSolver.depth[3] - 2 * lcaSolver.depth[lcaSolver.lca(4, 3)] == 3);
```

模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

struct BinaryLiftingLCA {
    int n, levels;
    vector<int> depth;       // depth[root]=0；模板只接受一棵连通树
    // up[j][u] 是 u 的第 2^j 个祖先；越过根后统一落到虚拟点 0。
    vector<vector<int>> up;

    // 参数 tree 为 1-based 连通无向树、root 为合法根；预处理祖先表/深度，不修改 tree。
    BinaryLiftingLCA(const vector<vector<int>>& tree, int root) {
        // tree 是 1-based 无向树，必须双向加边且不能含环、重边或自环。
        n = (int)tree.size() - 1;
        levels = 1;
        while ((1 << levels) <= n) ++levels;
        depth.assign(n + 1, -1);
        up.assign(levels, vector<int>(n + 1, 0));

        queue<int> q;
        depth[root] = 0;
        q.push(root);
        // BFS 定根：up[0][v] 保存父节点；这里只跳过父边，不是一般图的 visited 检查。
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (int v : tree[u]) {
                if (v == up[0][u]) continue; // 仅跳父边；因此输入必须真的是树
                up[0][v] = u;
                depth[v] = depth[u] + 1;
                q.push(v);
            }
        }

        for (int j = 1; j < levels; ++j) {
            for (int u = 1; u <= n; ++u) {
                // 先跳 2^(j-1)，再从中间祖先跳同样距离。
                up[j][u] = up[j - 1][up[j - 1][u]];
            }
        }
    }

    // 参数 u 为树点、steps 在 0..depth[u]；返回向上 steps 步的祖先，不改预处理表。
    int lift(int u, int steps) const {
        // 按 steps 的二进制位拆分向上跳；调用者应保证 steps<=depth[u]。
        for (int j = 0; j < levels; ++j) {
            if ((steps >> j) & 1) u = up[j][u];
        }
        return u;
    }

    // 参数 u/v 为同一棵树内的点；返回最近公共祖先点号，不修改预处理表。
    int lca(int u, int v) const {
        // 先对齐深度，再从最高位向下保持“两点祖先仍不同”。
        if (depth[u] < depth[v]) swap(u, v);
        u = lift(u, depth[u] - depth[v]);
        if (u == v) return u;
        for (int j = levels - 1; j >= 0; --j) {
            if (up[j][u] != up[j][v]) {
                u = up[j][u];
                v = up[j][v];
            }
        }
        // 此时 u、v 不同但父节点相同，该父节点就是最近公共祖先。
        return up[0][u];
    }
};
```

**5. 要改哪里**

- 计算无权路径边数可用 `depth[u]+depth[v]-2*depth[lca(u,v)]`；若要路径点数再加 1。
- 若需处理森林，可为每个连通块分别建根并记录所属分量，跨分量查询需定义失败状态；当前类假设单棵树。
- 若 `n` 可能接近 `int` 左移上界，构造 `levels` 时应使用足够宽的移位类型，避免 `1 << levels` 溢出。
- 更换根需重新构造对象和祖先表；旧表中的深度、父亲关系对应旧根。

**6. 自检**

示例中 `lca(4,5)=2`，`lca(4,3)=1`，`lift(4,1)=2`，4 到 3 的路径有 3 条边。单点树的 `lca(root,root)` 应为根，`lift(u,0)` 应返回 `u`；根自身不能向上提升正步数。确认所有输入点均与根连通。

**7. 坑**

- 输入有环导致重复入队：构造仅跳过父点，要求输入真的是树。
- 祖先跨过根后出现非法下标：虚拟点 0 的祖先表保持为 0。
- 深度差没先对齐：先提升较深点，再同步倍增。
- 用于森林或不同分量：接口没有分量标记，跨树 LCA 无定义。
- 极大 `n` 移位溢出：`1 << levels` 使用 `int`，需按规模改用 `1LL`。

**8. 一句话原理**

先把两点深度对齐，再从大步到小步同步上跳，停在最近公共祖先的下一层。

**参考：**

- [OI Wiki：最近公共祖先](https://oi-wiki.org/graph/lca/)

## 6.11 树的直径

**1. 它是做什么的**

树的直径是任意两点间最长简单路径的长度。本模板适用于 `n>=1` 的 1-based 连通无向树，边权须非负；无权树令每条边权为 1。两次从起点遍历找最远点，返回直径长度和一对端点。时间 $O(n)$，额外空间 $O(n)$；每次遍历树边一次。一般图或含负权的树不能直接套用。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `TreeEdge{to,weight}` | 邻接项，表示无向边一端及非负权值；每条边在两端都存一项。 |
| `distance[u]` | 当前遍历起点到 `u` 的唯一路径长度；`-1` 表示未访问，故边权必须非负。 |
| `vertex` | 当前发现的最远点；距离相同时返回哪个点取决于编号扫描顺序。 |
| `a`, `b` | 直径端点候选；从 1 找到 `a`，再从 `a` 找到 `b`。 |
| `diameter` | `a` 到最远点 `b` 的距离，即直径长度。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `farthestVertex(tree,start)` | `tree` 为 1-based 连通非负权树，`start` 是合法点；返回 `{最远点,距离}`。遍历数组为局部变量，不修改图。 |
| `treeDiameter(tree)` | 要求 `n>=1` 的 1-based 连通非负权树；返回 `{直径长度,端点a,端点b}`，不修改图。若存在并列直径，端点不保证唯一。 |

**4. 怎么调用**

将无向边双向加入邻接表，再调用 `treeDiameter`。示例中 1 到 3 距离为 7，是最长路径：

```text
vector<vector<TreeEdge>> tree(5);
tree[1].push_back({2, 3}); tree[2].push_back({1, 3});
tree[2].push_back({3, 4}); tree[3].push_back({2, 4});
tree[2].push_back({4, 2}); tree[4].push_back({2, 2});
auto [length, a, b] = treeDiameter(tree);
assert(length == 7);
assert((a == 1 && b == 3) || (a == 3 && b == 1));
```

模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct TreeEdge {
    // 无向树边需在两端邻接表各存一份；两次最远点法要求 weight>=0。
    int to;
    ll weight;
};

// 参数 tree 为 1-based 非负边权树、start 为树点；返回最远点及距离，使用局部遍历数组。
    // 参数 tree 为 1-based 非负权连通树、start 为合法点；返回最远点和距离，仅分配局部数组。
    // 参数 tree 为 1-based 非负权连通树、start 为合法点；返回最远点和距离，仅分配局部数组。
pair<int, ll> farthestVertex(
    const vector<vector<TreeEdge>>& tree,
    int start
) {
    // 点编号为 1..n；distance=-1 同时作为未访问标记，因此边权必须非负。
    int n = (int)tree.size() - 1;
    vector<ll> distance(n + 1, -1);
    stack<int> st; // 树上起点到每点路径唯一，无需 Dijkstra 即可累计带权距离
    st.push(start);
    distance[start] = 0;

    while (!st.empty()) {
        int u = st.top();
        st.pop();
        for (const auto& edge : tree[u]) {
            if (distance[edge.to] != -1) continue; // 跳过父节点，避免沿无向边返回
            distance[edge.to] = distance[u] + edge.weight;
            st.push(edge.to);
        }
    }

    int vertex = start;
    for (int u = 1; u <= n; ++u) {
        if (distance[u] > distance[vertex]) vertex = u;
    }
    return {vertex, distance[vertex]};
}

// 参数为 1-based 连通非负带权树且 n>=1；返回 {直径长度,端点a,端点b}，不改树。
    tuple<ll, int, int> treeDiameter(const vector<vector<TreeEdge>>& tree) {
    // 第一次找直径某端点 a，第二次从 a 找另一端 b；返回 {长度,a,b}。
    auto [a, ignored] = farthestVertex(tree, 1);
    auto [b, diameter] = farthestVertex(tree, a);
    return {diameter, a, b};
}
```

**5. 要改哪里**

- 无权树可把每条边的 `weight` 设为 1，返回长度即边数。
- 若需输出具体直径路径，在第二次遍历时记录父节点，再从 `b` 回溯到 `a`；当前只返回端点和长度。
- 若边权为负，两次最远点法及 `-1` 未访问标记均不适用，应根据题意改用其他树形 DP。
- 输入是森林时，先定义目标是最大分量直径还是全局路径；当前函数固定从点 1 出发且要求连通树。

**6. 自检**

示例直径长度为 `3+4=7`，端点为 1 和 3。单点树返回长度 0、两个端点均为 1；含零权边仍能正确遍历，零距离点也会标记为已访问。带负边时不要使用本模板。

**7. 坑**

- 把一般图交给两次遍历：树的路径唯一，带环图中该过程不再计算最短/最长简单路径。
- 负边或断开图导致错误：要求连通且所有权值非负。
- 无向边只存一个方向：每条树边须在两端邻接表都加入。
- 误认为端点唯一：存在多个等长直径时，遍历顺序会影响返回的端点。

**8. 一句话原理**

从任意点走到最远端点，再从该端点走到最远点，后一次距离就是树的直径。

**参考：**

- [OI Wiki：树的直径](https://oi-wiki.org/graph/tree-diameter/)

## 6.12 最大流（Dinic）

**1. 它是做什么的**

Dinic 在非负容量有向网络中求源点到汇点的最大流，支持以 `limit` 截断本次增广量。点号为 `1..n`，源汇必须不同。算法反复对正残量边 BFS 建层次图，再用当前弧 DFS 增广；一般上界为 $O(V^2E)$，残量图空间为 $O(V+E)$，DFS 递归深度可达 $O(V)$。默认 `limit=INF`，因此返回值至多为 `INF`；若真实最大流可能更大，应传入可表示且足够大的上限。每次调用返回本次新增的流量，残量图会被修改。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `Edge{to,reverseIndex,capacity}` | 残量边；`capacity` 是当前剩余容量，不是原始容量。正反边互相记录索引。 |
| `graph[u]` | 残量网络邻接表；每次 `addEdge` 增加一条正向边和一条初始容量 0 的反向边。 |
| `level[u]` | BFS 层数；`-1` 表示从当前源点在残量网络不可达。 |
| `current[u]` | 当前层次图中 `u` 尚未尝试的边位置，用于避免重复扫描失败边。 |
| `flow`, `limit` | 本次调用新增流量及上限。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `Dinic(n)` | 创建 `n` 个点的空残量网络；点号范围 `1..n`。 |
| `addEdge(from,to,capacity)` | 加一条有向边及反向残量边；容量须非负，端点合法；原地修改残量图。平行边与自环可加入。 |
| `buildLevelGraph(source,sink)` | 沿正残量边重建 `level`；返回汇点是否可达。会覆盖旧层次。 |
| `sendFlow(u,sink,pushed)` | 内部 DFS，至多发送 `pushed`，成功时修改正反残量；通常由 `maxFlow` 调用。 |
| `maxFlow(source,sink,limit)` | 要求源汇合法且不同、`limit>=0`；返回当前残量图上最多新增的流量，上限为 `limit`。残量状态被修改，可再次调用继续增广；重算新实例需重新加边。 |

**4. 怎么调用**

按题意加入有向容量边，再调用 `maxFlow`。下面网络最大流为 5；分两次限额增广分别得到 3 和 2，之后没有剩余增广量：

```text
Dinic flow(4);
flow.addEdge(1, 2, 3); flow.addEdge(1, 3, 2);
flow.addEdge(2, 3, 1); flow.addEdge(2, 4, 2);
flow.addEdge(3, 4, 3);
assert(flow.maxFlow(1, 4, 3) == 3);
assert(flow.maxFlow(1, 4) == 2);
assert(flow.maxFlow(1, 4) == 0);
assert(!flow.buildLevelGraph(1, 4));
```

模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = numeric_limits<ll>::max() / 4;

struct Dinic {
    struct Edge {
        int to, reverseIndex;
        ll capacity; // 当前残量，不是原始容量；必须始终非负
    };

    int n;
    vector<vector<Edge>> graph; // graph[u][i] 与其 reverseIndex 指向的残量边互为反边
    vector<int> level;          // 残量网络中从 source 出发的 BFS 层号，-1 为不可达
    vector<int> current;        // 当前弧：本轮分层图中每点尚未尝试的首条边

    // 参数 n 为点数；初始化空残量网络、层次和当前弧数组。
    explicit Dinic(int n)
        : n(n), graph(n + 1), level(n + 1), current(n + 1) {}

    // 参数为端点和非负容量；返回 void，加入正向边及零容量反向边，修改残量图。
    void addEdge(int from, int to, ll capacity) {
        // 加有向容量边 from->to；反向边初始容量为 0，只用于撤回已经发送的流。
        // 自环的两条边都进入同一 vector，正向边的反向下标要跳过自身。
        Edge forward{to, (int)graph[to].size() + (from == to), capacity};
        Edge backward{from, (int)graph[from].size(), 0};
        graph[from].push_back(forward);
        graph[to].push_back(backward);
    }

    // 参数 source/sink 为合法点号；返回汇点是否可达，并重建 level 数组。
    bool buildLevelGraph(int source, int sink) {
        // 只沿正残量边 BFS；后续 DFS 只能走 level 恰好增加 1 的边。
        fill(level.begin(), level.end(), -1);
        queue<int> q;
        level[source] = 0;
        q.push(source);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (const Edge& edge : graph[u]) {
                if (edge.capacity <= 0 || level[edge.to] != -1) continue;
                level[edge.to] = level[u] + 1;
                q.push(edge.to);
            }
        }
        return level[sink] != -1;
    }

    // 参数 u/sink 为点号、pushed 为非负上限；返回实际发送量，并原地修改正反残量边。
    ll sendFlow(int u, int sink, ll pushed) {
        // 返回本次从 u 实际送到 sink 的流量；pushed 是上游允许的上限。
        if (u == sink || pushed == 0) return pushed;
        // i 使用引用：失败边以后无需重扫，这就是当前弧优化的不变量。
        for (int& i = current[u]; i < (int)graph[u].size(); ++i) {
            Edge& edge = graph[u][i];
            if (edge.capacity <= 0 || level[edge.to] != level[u] + 1) continue;
            ll sent = sendFlow(edge.to, sink, min(pushed, edge.capacity));
            if (sent == 0) continue;
            // 正向残量减少、反向残量增加，保证之后可以撤销/改道这部分流。
            edge.capacity -= sent;
            graph[edge.to][edge.reverseIndex].capacity += sent;
            return sent;
        }
        return 0;
    }

    // 参数为不同源汇和非负流量上限；返回本次从当前残量网可增广流量，残量图被修改。
    ll maxFlow(int source, int sink, ll limit = INF) {
        // 要求 source!=sink、点编号 1..n；返回不超过 limit 的最大增广量。
        assert(source != sink);
        ll flow = 0;
        while (flow < limit && buildLevelGraph(source, sink)) {
            fill(current.begin(), current.end(), 0); // 新分层图必须重置当前弧
            while (flow < limit) {
                ll sent = sendFlow(source, sink, limit - flow);
                if (sent == 0) break;
                flow += sent;
            }
        }
        return flow;
    }
};
```

**5. 要改哪里**

- 无向容量关系通常需要按题意分别调用两次 `addEdge`；这表示两个独立方向各有容量，不能随意当成一条共享容量边。
- 二分图匹配可建超级源到左点、兼容边、右点到超级汇，容量均设为 1；匹配数等于最大流。
- 求最小割必须让流跑到无增广路，不能用有限 `limit` 提前截断。此时再次 `buildLevelGraph` 返回 false，`level[v]>=0` 是源侧；割容量应从原始输入边表统计，不能把残量反边当原边。
- 若要重算另一组网络，创建新对象并重新加边；重复 `maxFlow` 是在旧残量状态上求新增量。

**6. 自检**

示例总流为 5：源点两条出边容量和为 5，汇点两条入边容量和也为 5；三次调用新增量分别为 3、2、0。单边容量为 0 时流为 0；只有反向于源汇方向的边时也无可发送流。源汇相同时不满足接口前提，代码会触发断言。

**7. 坑**

- 反向边被当原始边：反向边初始容量为 0，只用于撤回或改道已发送的流。
- 更新正向残量却没更新反向：会破坏流量守恒及后续重路由。
- 认为每次调用返回累计流：函数返回当前调用新增量；多次调用需自行累加。
- 限额后直接取最小割：尚有可增广流时层次图仍可达，不能得到最小割。
- 边容量或总流超过类型/默认上限：使用 `long long` 且默认上限为 `INF`，需按约束检查。

**8. 一句话原理**

在残量网络中只沿层数递增的最短增广路推流，直到汇点不可达或达到调用上限。

**参考：**

- [OI Wiki：最大流](https://oi-wiki.org/graph/flow/max-flow/)

## 6.13 欧拉路径与回路

**1. 它是做什么的**

Hierholzer 算法为无向多重图构造一条每条边恰好使用一次的欧拉点序。输入边表中每条无向边只出现一次，点编号为 `1..n`；平行边用内部边编号区分，自环也按一条边计。若忽略孤立点后不连通，或奇度点数不是 0 或 2，函数返回空向量；无边图也按接口约定返回空向量。时间与空间均为 $O(n+m)$，返回序列成功时长 `m+1`。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `edges[id]` | 第 `id` 条输入无向边；每条边只有一个 ID。 |
| `g[u]` | `(邻点,边ID)` 邻接项；同一无向边在两端各存一次。 |
| `deg[u]` | 度数；自环会增加 2。 |
| `used[id]` | 该边是否已被消费，双向邻接项共享同一标记。 |
| `it[u]` | `u` 当前扫描到的邻接位置，跳过已用边避免反复检查。 |
| `st`, `path` | Hierholzer 显式栈及回退生成的逆序答案；返回前反转。 |

存在欧拉回路时从首个非孤立点出发；有两个奇度点时从扫描到的一个奇度点出发。具体点序依赖邻接顺序。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `eulerTrailUndirected(n,edges)` | `n` 为点数，端点须在 `1..n`，边表每条无向边只出现一次；返回覆盖全部边的点序，失败或无边时返回空向量，不改输入边表。 |

函数会检查度数条件，并在构造后核对 `path.size()==m+1`；长度不足表示有边未被连通遍历。

**4. 怎么调用**

准备无向边表，每条边写一次，再调用函数。三角形的插入顺序会得到点序 `1,2,3,1`：

```text
vector<pair<int, int>> edges = {{1, 2}, {2, 3}, {3, 1}};
vector<int> path = eulerTrailUndirected(3, edges);
assert(path == vector<int>({1, 2, 3, 1}));
assert(eulerTrailUndirected(3, {}).empty());
```

模板如下：

```cpp

// 参数 n 为点数、edges 为每条无向边一次的端点表；返回全边欧拉点序，无欧拉遍历或非连通时为空。
vector<int> eulerTrailUndirected(
    int n, const vector<pair<int, int>>& edges) {
    // Hierholzer 回溯入答案，末尾需 reverse；每条边只消费一次。
    vector<vector<pair<int, int>>> g(n + 1);
    vector<int> deg(n + 1), it(n + 1);
    vector<char>used(edges.size());
    for (int id = 0; id < (int)edges.size(); ++id) {
        auto [u, v] = edges[id];
        g[u].push_back({v,id});
        g[v].push_back({u,id});
        ++deg[u];
        ++deg[v];
    }
    int start = 0, odd = 0;
    for (int u = 1; u <= n; ++u) {
        if (deg[u] == 0) {
            continue;
        }
        if (!start) {
            start = u;
        }
        if (deg[u] & 1) {
            ++odd;
            start = u;
        }
    }
    if (!start || (odd != 0 && odd != 2)) {
        return {};
    }
    vector<int> st{start}, path;
    while (!st.empty()) {
        int u = st.back();
        while (it[u] < (int)g[u].size()
               && used[g[u][it[u]].second]) {
            ++it[u];
        }
        if (it[u] == (int)g[u].size()) {
            path.push_back(u);
            st.pop_back();
        } else {
            auto [v, id] = g[u][it[u]++];
            if (!used[id]) {
                used[id] = true;
                st.push_back(v);
            }
        }
    }
    if (path.size() != edges.size() + 1) {
        return {};
    }
    reverse(path.begin(), path.end());
    return path;
}
```

**5. 要改哪里**

- 有向图需要按每条边只加入一次，并改用入度/出度条件及有向 Hierholzer；不能把有向边当无向边重复加入。
- 若需返回边序而不只是点序，应在每次消费边时同时记录边 ID，并在回退时将边 ID 与点序同步整理。
- 若题目允许无边图输出单点路径，可修改空边处理；当前接口统一返回空向量。
- 若要指定起点，需检查起点满足欧拉路径端点条件，并从该点启动，而不是使用当前自动选点规则。

**6. 自检**

三角形中每个点度数为 2，返回 4 个点且首尾相同；空边表返回空。单边图有两个奇度点，返回两个端点构成的 2 点序列；两个互不相连的单边会因未覆盖全部边而返回空。自环度数按 2 计，并且边 ID 只消费一次。

**7. 坑**

- 欧拉条件满足但返回空：非孤立部分不连通，检查路径长度是否为 `m+1`。
- 平行边漏掉或重复使用：以边 ID 标记，不能仅按端点去重。
- 回溯顺序颠倒：`path` 是逆序生成，最终必须反转。
- 把点序长度当边数：成功时点数为 `m+1`，边数为 `m`。

**8. 一句话原理**

沿尚未使用的边不断深入，走不动时回退并记录节点，最后反转回退序列得到覆盖全部边的路线。

## 6.14 2-SAT

**1. 它是做什么的**

2-SAT 判断变量取真/假时，一组二文字析取约束是否可满足，并在有解时返回一组赋值。每个子句形如 `(x==xv) OR (y==yv)`；节点编号将变量 `1..n` 的假、真文字分别映射到 `1..2n`。建蕴含图后调用第 6.8 节的 Tarjan SCC，时间与空间均为 $O(n+m)$，其中 `m` 为子句数。无解返回 `nullopt`；有解返回长度 `n+1` 的 `vector<char>`，下标 1..n 为布尔值。代码依赖 6.8 的 `TarjanSCC` 实现。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `vars` | 布尔变量数，变量编号 `1..vars`。 |
| `g` | 蕴含图，文字节点编号为 `1..2*vars`。 |
| `node(x,value)` | 变量 `x` 的文字节点；false 为 `2*x-1`，true 为 `2*x`。 |
| `scc` | 引用成员 `g` 的 Tarjan 求解器；成员声明顺序保证先构造 `g` 再构造它。 |
| `answer[x]` | 有解时变量 `x` 的取值；`char` 的 0 表示 false，非 0 表示 true。 |

析取 `(x==xv) OR (y==yv)` 转成两条蕴含：`¬(x==xv) -> (y==yv)` 和 `¬(y==yv) -> (x==xv)`。若同一变量的真、假文字落在同一 SCC，则无解。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `TwoSAT(n)` | 创建 `n` 个变量及 `2n` 个文字节点；`n` 应非负。内部 `scc` 保存对 `g` 的引用，因此不要复制或移动构造后的对象。 |
| `node(x,value)` | 要求 `x` 在 `1..vars`；返回对应文字节点号，不修改状态。 |
| `imply(a,b)` | 参数是合法文字节点号；向 `g` 添加边 `a->b`，无返回值。若调用者以它表示逻辑约束 `a=>b`，还必须加入逆否边 `¬b=>¬a`；通常由 `addOr` 成对调用。 |
| `addOr(x,xv,y,yv)` | 加入一个二文字析取子句，更新蕴含图，无返回值；变量号须合法。所有子句应在 `solve` 前加入。 |
| `solve()` | 运行内部 Tarjan 并返回可满足赋值或 `nullopt`。求解后不要再添加约束；若要修改/重算，创建新对象。 |

**4. 怎么调用**

先添加全部子句，再调用 `solve()`；示例约束为 `x OR y` 与 `¬x OR y`，因此 `y` 必须为真。该片段依赖 6.8 节的 `TarjanSCC`：

```text
TwoSAT solver(2);
solver.addOr(1, true, 2, true);
solver.addOr(1, false, 2, true);
auto answer = solver.solve();
assert(answer.has_value());
assert((*answer)[1] || (*answer)[2]);
assert(!(*answer)[1] || (*answer)[2]);
```

模板如下：

```cpp

struct TwoSAT {
    // 每个变量 x 有 false/true 两个文字节点；蕴含边记在 g 中。
    int vars;
    vector<vector<int>> g;
    TarjanSCC scc; // 复用 6.8 节实现；它保存 g 的引用，故 g 必须先声明

    // 参数 n 为变量数；分配文字蕴含图及引用该图的 SCC 求解器。
    explicit TwoSAT(int n) : vars(n), g(2 * n + 1), scc(g) {}

    // 参数 x 属于 1..vars、value 指定真假文字；返回对应 1-based 蕴含图节点号。
    int node(int x, bool value) const {
        return 2 * (x - 1) + (value ? 1 : 0) + 1;
    }
    // 参数 a/b 为文字节点号；返回 void，向蕴含图添加有向边 a->b。
    void imply(int a, int b) {
        g[a].push_back(b);
    }
    // 参数给出两个变量及各自文字真假值；返回 void，加入析取子句对应的两条蕴含边。
    void addOr(int x, bool xv, int y, bool yv) {
        // (x==xv) OR (y==yv) 等价于 ¬x->y 与 ¬y->x。
        int a = node(x, xv), b = node(y, yv);
        imply(node(x, !xv), b);
        imply(node(y, !yv), a);
    }
    // 无参数；返回可满足赋值（下标 1..vars）或 nullopt；运行 SCC 并写内部分量状态，仅可运行一次。
    optional<vector<char>> solve() {
        scc.run();
        vector<char> answer(vars + 1);
        for (int x = 1; x <= vars; ++x) {
            int f = node(x, false), t = node(x, true);
            if (scc.component[f] == scc.component[t]) return nullopt;
            // TarjanSCC 按弹栈顺序编号，较小分量先赋值为 true。
            answer[x] = scc.component[t] < scc.component[f];
        }
        return answer;
    }
};
```

**5. 要改哪里**

- 单文字约束 `x` 可写成 `addOr(x,true,x,true)`；`¬x` 可写成 `addOr(x,false,x,false)`。
- 若输入是一般三文字子句（3-SAT），本模板不适用；只有题目结构能化成二文字约束时才可使用。
- 若换用不同 SCC 实现，必须根据其分量编号方向重新核对 `component[t] < component[f]` 的赋值比较。
- 修改约束后需用新 `TwoSAT` 实例重新建图；内部 SCC 状态不会因新增边而重置。

**6. 自检**

示例的两个子句共同强制 `y=true`，返回赋值须满足两式。单变量 `x OR x` 可满足且要求 `x=true`；同时加入 `x OR x` 与 `¬x OR ¬x` 则应返回 `nullopt`。变量下标 0 不属于输出赋值范围；检查时读取 `answer[1..vars]`。

**7. 坑**

- 文字节点偏一位：假文字为 `2*x-1`，真文字为 `2*x`，图节点从 1 开始。
- 蕴含边方向反了：子句 `a OR b` 要加 `¬a->b` 与 `¬b->a`；单加逻辑蕴含 `a=>b` 时还要加逆否边。
- 改用 SCC 后赋值取反：分量编号顺序由实现决定，需验证比较方向。
- 求解后继续加子句：SCC 缓存已完成状态，不会重新处理新边。
- 复制/移动 `TwoSAT`：`scc` 的引用不会自动改指向副本的 `g`；直接在原对象中建图和求解。

**8. 一句话原理**

把每个析取转成两条蕴含，再用 SCC 判断真假文字是否矛盾并据分量顺序构造赋值。

**参考：**

- 依赖第 6.8 节的 Tarjan 强连通分量模板。

## 6.15 最小费用最大流

**1. 它是做什么的**

最小费用最大流在容量网络中，按最小单位费用发送尽可能多的流；`run(s,t,limit)` 最多新增 `limit` 单位并返回本次 `{flow,cost}`。点号为 `1..n`，容量非负，源汇不同。每次用 SPFA 在残量图中找最短增广路；SPFA 单次最坏可达 $O(VE)$，整体由增广次数和每次最短路成本决定，没有固定的 $O(m\log n)$ 保证，适合中小规模。空间为 $O(V+E)$。要求过程中不存在从源点可达的负费用环，且距离、反向费用、`add*distance` 及总代价均能安全表示为 `long long`；`cost` 不能是无法取负的最小整数。用于最短路的有限费用距离还须小于内部 `INF`。代码使用别名 `ll`，需在定义前声明 `using ll = long long;`。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `E{to,rev,cap,cost}` | 残量边；`cap` 为剩余容量，`cost` 为单位费用。正反边费用互为相反数。 |
| `g[u]` | 残量邻接表；`rev` 指向目标点邻接表中对应反边。 |
| `d[v]` | 本轮从 `s` 到 `v` 的最短费用距离；不可达为 `INF`。 |
| `pv[v]`, `pe[v]` | 最短路前驱点和前驱边下标，用于回溯增广路径。 |
| `in[v]` | 当前是否在 SPFA 队列中，避免重复入队。 |
| `flow`, `cost` | 本次调用新增的流量和费用；重复调用从当前残量状态继续，返回本次增量。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `MinCostMaxFlow(nodeCount)` | 创建 `1..nodeCount` 的空网络；点数应为正。 |
| `addEdge(u,v,cap,cost)` | 加入有向容量边及容量 0、费用 `-cost` 的反向残量边；容量非负、端点合法，且 `-cost` 可表示；原地修改 `g`。 |
| `run(s,t,limit)` | 要求 `s!=t`、端点合法、`limit>=0` 且无可达负费用环；返回本次新增流量和费用，修改残量图。若流量不足上限，返回实际流量，不另设失败标记。 |

**4. 怎么调用**

先定义 `ll` 别名、建图，再按所需上限调用。示例先发送两单位走低费用通道，第二次在残量图上继续发送剩余一单位：

```text
MinCostMaxFlow flow(4);
flow.addEdge(1, 2, 2, 1); flow.addEdge(2, 4, 2, 1);
flow.addEdge(1, 3, 1, 0); flow.addEdge(3, 4, 1, 5);
auto first = flow.run(1, 4, 2);
assert(first.first == 2 && first.second == 4);
auto second = flow.run(1, 4);
assert(second.first == 1 && second.second == 5);
auto exhausted = flow.run(1, 4);
assert(exhausted.first == 0 && exhausted.second == 0);
```

模板如下：

```cpp

struct MinCostMaxFlow {
    // 残量网络逐次找最短路，parent 回溯增广；反向边费用为负。
    struct E {
        int to, rev;
        ll cap, cost;
    };
    int n;
    vector<vector<E>> g;
    // 参数 nodeCount 为点数；初始化空残量网络。
    explicit MinCostMaxFlow(int nodeCount)
        : n(nodeCount), g(nodeCount + 1) {
    }
    // 参数为端点、非负容量和单位费用；返回 void，加入正向边与负费用反向残量边。
    void addEdge(int u, int v, ll cap, ll cost) {
        E a{v, (int)g[v].size() + (u == v), cap, cost};
        E b{u, (int)g[u].size(), 0, -cost};
        g[u].push_back(a);
        g[v].push_back(b);
    }
    // 参数 s/t 为不同源汇、limit 为非负流量上限；返回本次 {流量,费用}，并修改残量图；须无可达负费用环。
    pair<ll, ll> run(int s, int t, ll limit = LLONG_MAX / 4) {
        assert(s != t);
        ll flow = 0;
        ll cost = 0;
        const ll INF = numeric_limits<ll>::max() / 4;
        while (flow < limit) {
            vector<ll> d(n + 1, INF);
            vector<int> pv(n + 1), pe(n + 1);
            vector<char> in(n + 1);
            queue<int> q;
            d[s]=0;
            q.push(s);
            in[s]=1;
            while (!q.empty()) {
                int u = q.front();
                q.pop();
                in[u]=0;
                for (int i = 0; i < (int)g[u].size(); ++i) {
                    auto& e = g[u][i];
                    if (e.cap && d[e.to] > d[u] + e.cost) {
                        d[e.to] = d[u] + e.cost;
                        pv[e.to] = u;
                        pe[e.to] = i;
                        if (!in[e.to]) {
                            in[e.to] = 1;
                            q.push(e.to);
                        }
                    }
                }
            }
            if (d[t] == INF) break;
            ll add = limit - flow;
            for (int v = t; v != s; v = pv[v]) add = min(add, g[pv[v]][pe[v]].cap);
            flow += add;
            cost += add * d[t];
            for (int v = t; v != s; v = pv[v]) {
                auto& e = g[pv[v]][pe[v]];
                e.cap -= add;
                g[v][e.rev].cap += add;
            }
        }
        return {flow,cost};
    }
};
```

**5. 要改哪里**

- 若只允许发送指定流量 `F`，调用 `run(s,t,F)` 后检查返回的 `flow==F`；不足时网络无法满足需求。
- 若有可达负费用环，应先按题意处理环流，或换用能处理负环的建模/算法；当前 SPFA 增广过程可能无法终止。
- 大网络可改用势能配合 Dijkstra 的实现；势能初始化仍需正确处理负费用边。
- 多次调用可逐步追加流量，但返回的是本次增量；要从头重算应新建对象并重新加边。

**6. 自检**

示例第一次发送 2 单位，每单位费用 2，费用为 4；第二次发送剩余 1 单位，费用为 5；第三次无路可增，返回 `{0,0}`。若只有容量 1、费用 3 的单边且请求上限 2，应返回 `{1,3}`，调用方需识别未满足全部需求。容量 0 的边不可用；自环和反向残量边不能误当成独立原始容量。

**7. 坑**

- 反向边费用符号错误：撤回一单位流要抵消原费用，因此费用为 `-cost`。
- 把返回流量当累计总流：每次 `run` 的局部计数从 0 开始，结果仅是本次增量。
- 请求固定流量却不检查返回值：算法可能因无增广路提前停止，需比较实际流量和目标。
- 有可达负费用环：SPFA 会持续改进距离，违反算法前提，可能不终止。
- 溢出：检查负费用取反、最短距离、`add*d[t]` 和总费用的范围；`long long` 不是无限精度。

**8. 一句话原理**

每次在残量图中找费用最低的增广路并推送瓶颈流量，同时用反向边保留改道能力。

## 6.16 树上差分 + LCA {#tree-difference}

**1. 它是做什么的**

 一棵静态连通树，多次给路径上的所有点或边增加权值，最后统一读取各点或各边的总增量。

将每次路径修改变成常数个差分标记，最后一次自底向上汇总。

输入 1-based 无向树、根和若干 `(u,v,w)`；输出 `node[u]` 为点 `u` 总增量，`edge[u]` 为父边 `(parent[u],u)` 总增量，根的父边值为 0。允许负增量和重复路径；不改变原始权值。

复杂度：预处理时间、空间 $O(n\log n)$，每次加路径 $O(\log n)$，一次汇总 $O(n)$；$q$ 次更新再统一汇总共 $O((n+q)\log n)$。逐次汇总查询会增加到 $O(nq)$，不适用于高频在线查询。

**从数组差分开始。** 数组区间加可以只在左端点记开始、右端点之后记结束，最后前缀和还原。树没有唯一的“右端点”，但每个非根节点都有唯一父亲。我们改为让标记向父亲汇总：在 `u` 记 `+w`，就会让 `u` 到根的整条祖先链收到 `w`。负标记负责抵消不应该被修改的祖先。

**为什么要用 LCA。** 记 $z=\operatorname{lca}(u,v)$。分别在 `u`、`v` 加 `w`，上行到 `z` 时两路汇合，`z` 及其以上祖先暂时收到两份贡献。对点路径，`z` 应收到一份而其父亲以上应收到零份，所以：

$$
d_u\mathrel{+}=w,\quad d_v\mathrel{+}=w,\quad d_z\mathrel{-}=w,\quad d_{\operatorname{parent}(z)}\mathrel{-}=w.
$$

父亲为虚拟点 0 时，最后一项直接跳过。对边路径，把每条边寄存在较深端点：路径上不包含 `z` 的父边，故在 `z` 减去两份：

$$
e_u\mathrel{+}=w,\quad e_v\mathrel{+}=w,\quad e_z\mathrel{-}=2w.
$$

最后按孩子先于父亲的顺序执行 `d[parent[u]] += d[u]`。它是在计算每个点的差分子树和，不是沿 DFS 序直接做数组前缀和。点和边要用两套公式，不能混用。

**手算。** 树边为 `1-2, 1-3, 2-4, 2-5`。给路径 `4→2→5` 加 3，LCA 为 2。点差分先记 `d[4]=3,d[5]=3,d[2]=-3,d[1]=-3`；汇总后点 4、5、2 都是 3，点 1、3 是 0。边差分在点 2 记 -6，汇总后 `e[4]=e[5]=3,e[2]=0`，因此父边 `1-2` 没有被误加。若 `u=v`，点路径只含一个点，边路径为空，公式仍成立。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `lca` | 6.10 节的倍增 LCA，`up[0][u]` 为父亲；根的父亲为 0。 |
| `order` | 从根开始、父亲先于孩子的遍历序；逆序汇总时孩子已完成计算。 |
| `nodeDiff[u]` | 点路径的差分标记，尚未汇总时不能当作节点答案。 |
| `edgeDiff[u]` | 边路径的差分标记，汇总后由较深端点代表父边。 |
| `node[u]`、`edge[u]` | `collect()` 返回的总增量副本；根对应的 `edge` 值为 0。 |
| `z`、`p` | 更新路径的 LCA 及其父亲；点差分在 `p=0` 时跳过抵消。 |

**3. 函数在做什么**

| 函数 | 参数、返回与作用 |
|---|---|
| `TreePathDifference(tree,root)` | 输入非空的 1-based 连通无向树及合法根，建立 LCA、遍历序，清零两套差分，不修改原树。 |
| `addNodes(u,v,w)` | 给包含两端的点路径记录增量 `w`，返回 `void`，只改 `nodeDiff`。 |
| `addEdges(u,v,w)` | 给路径上的边记录增量 `w`，返回 `void`，只改 `edgeDiff`；同点路径没有边。 |
| `collect()` | 无参数，返回两套 1-based 总增量数组；在副本上汇总，不清空原标记，可重复调用或继续更新。 |

**4. 怎么调用**

下方复用 6.10 节的 `BinaryLiftingLCA`，先复制其定义。输入须为非空的合法树。所有差分值、子树累计值与 `2*w` 均须能放入 `long long`。构造时 BFS 得到父先于子的序列，反向处理即可避免这部分的递归栈。

```cpp
// 依赖：6.10 的 BinaryLiftingLCA，以及 <bits/stdc++.h> 和 using namespace std。
struct TreePathDifference {
    BinaryLiftingLCA lca;
    vector<int> order;
    vector<long long> nodeDiff, edgeDiff;

    // tree 为 1-based 非空连通无向树，root 在 1..n；建立 LCA/遍历序并清零差分，不修改 tree。
    TreePathDifference(const vector<vector<int>>& tree, int root = 1)
        : lca(tree, root), nodeDiff(tree.size()), edgeDiff(tree.size()) {
        order.push_back(root);
        for (size_t i = 0; i < order.size(); ++i) {
            int u = order[i];
            for (int v : tree[u]) if (v != lca.up[0][u]) order.push_back(v);
        }
    }

    // u,v 为 1..n 点号，w 为增量；返回 void，记录点路径（包含两端）的加法，暂不汇总。
    void addNodes(int u, int v, long long w) {
        int z = lca.lca(u, v), p = lca.up[0][z];
        nodeDiff[u] += w;
        nodeDiff[v] += w;
        nodeDiff[z] -= w;
        if (p) nodeDiff[p] -= w;
    }

    // u,v 为 1..n 点号，w 为增量；返回 void，记录路径所有边的加法；u==v 时总效果为零。
    void addEdges(int u, int v, long long w) {
        int z = lca.lca(u, v);
        edgeDiff[u] += w;
        edgeDiff[v] += w;
        edgeDiff[z] -= 2 * w;
    }

    // 无参数；返回 {点增量数组,父边增量数组}，均 1-based；不修改差分，可重复调用或继续添加路径。
    pair<vector<long long>, vector<long long>> collect() const {
        auto node = nodeDiff, edge = edgeDiff;
        for (int i = (int)order.size() - 1; i > 0; --i) {
            int u = order[i], p = lca.up[0][u];
            node[p] += node[u];
            edge[p] += edge[u];
        }
        edge[order[0]] = 0;
        return {node, edge};
    }
};
```

下面对树 `1-2,1-3,2-4,2-5` 的路径 `4→2→5` 分别增加点、边贡献。两套标记互不影响，需要两类结果时分别调用。

```text
vector<vector<int>> tree = {{}, {2,3}, {1,4,5}, {1}, {2}, {2}};
TreePathDifference solver(tree, 1);
solver.addNodes(4, 5, 3);
solver.addEdges(4, 5, 3);
auto [node, edge] = solver.collect();
assert((node == vector<long long>{0,0,3,0,3,3}));
assert((edge == vector<long long>{0,0,0,0,3,3}));
assert(solver.collect() == make_pair(node, edge));
```

**5. 要改哪里**

- 原始点权或边权非零时，在最终增量上叠加原值；模板不会替调用者保存原权值。
- 统计路径经过次数时令 `w=1`，再找经过次数最多的边；若要求总运输成本，可将父边权乘以 `edge[u]` 后求和。
- 路径拥堵次数、批量负载累加适合本法；每次修改后立即查询任意路径和，应改用 HLD 等动态维护方法。差分不能直接维护路径最小值。
- 改根或换树时新建对象；`collect()` 允许重复调用，但每次都是 $O(n)$，不能据此把批量算法当成高效在线算法。

**6. 自检**

基础：按上例手算差分与子树和，再检查链、星形树、根为 LCA 的情况。`u=v` 时，点更新只影响一个点，边更新总效果为零。

实现：将随机路径逐点枚举的暴力结果与模板比较；检查负增量、重复路径、没有更新、重复汇总以及汇总后再更新。组合：计算所有路径的总边权贡献，并与逐条路径暴力求和比较。

**7. 坑**

1. 点路径沿用边差分公式，会把 LCA 的点贡献减掉；先明确维护点还是边。
2. 将 DFS 序做前缀和不能恢复树上差分；应按孩子先于父亲的顺序累计子树和。
3. 调用 `addNodes` 不会更新边标记；两类操作与结果分别维护。
4. 根没有父边，不能把 `edge[root]` 当成真实边答案。
5. `2*w`、差分和累计值都可能溢出，须分别检查 `long long` 范围。

**8. 一句话原理**

端点标记产生向根传播的贡献，在 LCA 及其父亲处抵消多余部分，再用一次子树汇总还原整批路径增量。

**参考：** [OI Wiki：前缀和与差分（含树上差分）](https://oi-wiki.org/basic/prefix-sum/)。
