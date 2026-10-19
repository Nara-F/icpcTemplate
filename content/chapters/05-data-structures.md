
# 5. 数据结构

本章代码默认使用 C++17。除特别说明外，数组下标从 1 开始；调用查询、删除操作前应保证容器非空、区间合法。字典树统一收录在第 8 章字符串中。

## 5.1 栈与队列

**1. 它是做什么的**

栈、队列和双端队列是按位置约束插入、删除顺序的序列容器：栈后进先出，队列先进先出，双端队列允许在两端操作。括号匹配、撤销操作常用栈；广度优先搜索和按到达顺序处理任务常用队列；需要两端进出时用 `deque`。

本例接收整数序列 `a`，分别将其压入局部栈和队列，再逐个读取并弹出；它还演示向双端队列两端插入和从前端删除。函数返回 `void`，不修改 `a`，也不输出数据；读取出的值目前被丢弃，实际题目要在取值处加入处理逻辑。三种容器在本例中均不要求元素有序或互异。

复杂度：构造容器并处理长度为 `k` 的序列，整体时间 $O(k)$；一次 `push`、`pop`、`top`、`front`、`back` 或 `empty` 均为 $O(1)$。`deque` 两端插入和删除为 $O(1)$。存放 `k` 个元素需要 $O(k)$ 空间；这里统计额外空间的渐进量级。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `a` | 只读输入序列；按从前到后的顺序依次入栈、入队。 |
| `st` | `stack<int>` 栈适配器；只能查看和删除栈顶，先入的元素后取出。 |
| `q` | `queue<int>` 队列适配器；从队首查看和删除，先入的元素先取出。 |
| `dq` | `deque<int>` 双端队列；示例先在前端放 `1`、再在后端放 `2`，随后从前端删除 `1`。 |
| `x` | 每轮取出的元素；必须在 `pop()` 前读取，当前示例没有保留或输出它。 |

这些容器按元素顺序工作，没有节点编号或自定义下标。`stack` 和 `queue` 不提供迭代器，也不支持随机访问；若需要遍历全部元素，应逐次读取并弹出，或选择适合的其他容器。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `stackQueueExample(const vector<int>& a)` | 接收整数向量常量引用；返回 `void`。 | 创建三个局部容器并演示入栈、入队和双端队列操作；不改变 `a`，函数结束时容器销毁。当前取出的值被丢弃，没有可见输出。 |
| `push` | 插入一个元素；返回 `void`。 | 栈和队列从各自的后端加入；`deque` 可用 `push_front` 或 `push_back` 指定一端。 |
| `top` / `front` / `back` | 无参数；返回相应端元素的引用。 | 只能在容器非空时读取；示例将元素复制到 `x` 后再弹出。 |
| `pop` / `pop_front` / `pop_back` | 无参数；返回 `void`。 | 删除指定端元素，不返回被删值；调用前必须确认非空。 |
| `empty` / `size` | 无参数；分别返回是否为空、元素个数。 | 可用于安全循环和检查容器状态。 |

题目通常不需要调用演示函数；直接在自己的逻辑中声明并使用相应容器即可。若调用本例函数，`a` 中的元素只会被消费演示，不会产生答案。

**4. 怎么调用**

先选符合处理顺序的容器；插入元素；每轮先判断非空，再读取对应端并处理元素，最后调用 `pop` 删除。若要两端操作，使用 `deque`。本例完整模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

// 参数 a 是待演示的整数序列；返回 void，局部容器消费并展示栈/队列/双端队列顺序，不改 a。
    void stackQueueExample(const vector<int>& a) {
    // 适配器不暴露迭代器；以下循环都先读顶端/队首，再 pop。
    stack<int> st;
    for (int x : a) st.push(x); // 入栈顺序与 a 相同，弹出顺序因此相反
    while (!st.empty()) {
        int x = st.top();
        st.pop();
        (void)x;  // 在此处理：顺序与 a 相反
    }

    queue<int> q;
    for (int x : a) q.push(x); // 队列按到达顺序服务
    while (!q.empty()) {
        int x = q.front();
        q.pop();
        (void)x;  // 在此处理：顺序与 a 相同
    }

    deque<int> dq;
    dq.push_front(1);
    dq.push_back(2);
    if (!dq.empty()) dq.pop_front();
}
```

下面的片段可放在业务函数内。对序列 `4 7 9`，栈依次取出 `9 7 4`，队列依次取出 `4 7 9`；两端队列操作后剩余 `[2]`：

```text
vector<int> a = {4, 7, 9};
stack<int> st;
for (int x : a) st.push(x);
while (!st.empty()) {
    int x = st.top();
    // 处理 x
    st.pop();
}

queue<int> q;
for (int x : a) q.push(x);
while (!q.empty()) {
    int x = q.front();
    // 处理 x
    q.pop();
}

deque<int> dq;
dq.push_front(1);
dq.push_back(2);
dq.pop_front();
// 结果：dq 中只剩 2
```

**5. 要改哪里**

- 需要后进先出时保留 `stack`，处理逻辑放在读取 `top()` 之后、`pop()` 之前；例如括号匹配时在这里检查并配对。
- 需要先进先出时保留 `queue`，在读取 `front()` 后处理；广度优先搜索通常在入队时标记节点已发现，避免重复入队。
- 需要从两端插入或删除时改用 `deque` 的 `push_front`、`push_back`、`pop_front`、`pop_back`。栈和队列适配器不提供另一端接口。
- 若需要按下标读取、排序或遍历而不消费元素，换用 `vector` 或 `deque` 等支持相应操作的容器；`stack` / `queue` 不适合这些需求。
- 多组数据时，局部容器在函数结束时自动销毁；若容器定义在外层并跨组复用，每组开始前需清空，避免残留元素。

**6. 自检**

取 `a = [4, 7, 9]`：逐个压入栈后，弹出顺序应为 `9, 7, 4`；逐个入队后，出队顺序应为 `4, 7, 9`。对双端队列先执行 `push_front(1)`、`push_back(2)`，再执行 `pop_front()`，应只剩 `2`。单元素序列压入任一容器后只读取一次；空序列则两个处理循环都不进入。重复值（如 `[5, 5]`）仍按位置入出，结果仍各有两个 `5`，容器不会自动去重。

**7. 坑**

1. 空容器调用 `top()`、`front()`、`back()` 或 `pop()` 会导致未定义行为；先用 `empty()` 检查，或在 `while (!empty())` 中操作。
2. 先 `pop()` 再读取会丢失待处理元素；先复制/处理 `top()` 或 `front()`，再删除。
3. 误以为 `pop()` 会返回元素；它只负责删除，需先用 `top()`、`front()` 或 `back()` 取值。
4. 需要遍历或随机访问时使用 `stack` / `queue`；它们是适配器，只暴露受限接口，应改选支持目标操作的容器。
5. 显式栈模拟 DFS 时，子节点的入栈次序会影响弹出访问次序；若要维持递归 DFS 的访问顺序，通常按期望访问顺序的反向压入。

**8. 一句话原理**

栈、队列和双端队列通过限制允许操作的端点，分别实现后进先出、先进先出和两端进出。

**参考：**

- [OI Wiki：栈](https://oi-wiki.org/ds/stack/)
- [OI Wiki：队列](https://oi-wiki.org/ds/queue/)

## 5.2 单调栈

**1. 它是做什么的**

给定一个静态整数数组，若要对每个位置找右侧第一个严格更小的元素，可以从左向右扫描并用单调栈在线性时间内完成。模板返回的是元素的下标；找不到时为 `-1`。它不修改输入数组，也不处理动态插入、删除或区间更新。

预处理：无。单次调用时间：$O(n)$，其中 $n$ 是数组长度；每个下标只入栈、出栈各至多一次。额外空间：$O(n)$，用于答案和栈。每次入栈、出栈本身为 $O(1)$。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `a` | 只读输入数组，位置从 `0` 到 `n-1`。 |
| `n` | `a.size()` 转成的整数，表示元素个数。 |
| `answer` | 与 `a` 等长；`answer[j]` 存位置 `j` 右侧首个严格更小元素的位置，暂时未找到或最终不存在时为 `-1`。 |
| `st` | 保存尚未找到答案的位置下标。栈中下标从底到顶递增，对应的数组值单调不减。 |
| `i` | 当前扫描到的下标；`st.top()` 是当前正在等待答案的位置。 |

例如 `a = [3, 1, 2, 1, 4]`。扫描到位置 `1` 的值 `1` 时，位置 `0` 的值 `3` 被弹出并得到答案 `1`。值相等时不弹出，所以位置 `1` 不会把位置 `3` 当作“严格更小”；结束后 `answer = [1, -1, 3, -1, -1]`。

**3. 函数在做什么**

| 函数 | 参数与返回 | 作用和前提 |
|---|---|---|
| `firstSmallerOnRight(const vector<int>& a)` | 参数是任意长度的只读整数数组；返回等长 `vector<int>`。 | 从左向右扫描。每当 `a[i] < a[st.top()]`，位置 `i` 就是栈顶下标右侧第一个严格更小的位置，记录后弹栈；最后仍在栈中的下标没有答案，保留 `-1`。可直接处理空数组。 |

没有需要调用者自行实现的辅助函数；通常只需调用公开函数并读取返回数组。函数不保留跨调用状态，同一输入可重复调用。

**4. 怎么调用**

先准备数组，再调用函数；返回数组与输入逐项对应。下例可放在业务函数中：

```text
vector<int> a = {3, 1, 2, 1, 4};
vector<int> next = firstSmallerOnRight(a);
// next 为 {1, -1, 3, -1, -1}
```

模板代码如下，代码片段本身不含 `main`，需要在调用处提供数组：

```cpp

#include <bits/stdc++.h>
using namespace std;

// 参数 a 为 0-based 数组；返回每项右侧首个严格更小位置的下标，不存在为 -1；不改 a。
    vector<int> firstSmallerOnRight(const vector<int>& a) {
    // a 与答案均为 0-based；answer[i] 是右侧首个严格更小值的下标。
    int n = (int)a.size();
    vector<int> answer(n, -1);
    stack<int> st;  // 栈中下标递增，且对应值从栈底到栈顶单调不减

    for (int i = 0; i < n; ++i) {
        // 严格更小才弹；改成 <= 即改为“右侧首个小于等于”。
        while (!st.empty() && a[i] < a[st.top()]) {
            answer[st.top()] = i;
            st.pop();
        }
        st.push(i);
    }
    return answer;
}
```

**5. 要改哪里**

- 求右侧首个严格更大位置：把弹栈条件改为 `a[i] > a[st.top()]`。
- 求右侧首个小于或等于的位置：把条件改为 `a[i] <= a[st.top()]`。相等值会在此时被弹出，因此较早位置会把当前相等位置记为答案。
- 求左侧最近元素：反向扫描，并相应调整栈中下标顺序与答案定义；不能只改一个比较符号。
- 需要返回元素值而不是位置时，可在确定答案处使用 `a[i]`；若要计算距离，则用 `i - j`（当前下标减去被弹出下标 `j`），并先判断答案是否为 `-1`。

**6. 自检**

对 `a = [2, 2, 1]`，结果应为 `[2, 2, -1]`：相等的 `2` 不算严格更小，而 `1` 是前两个位置的答案。对单元素 `[7]`，结果为 `[-1]`；空数组返回空数组。扫描结束时栈中每个下标右侧都没有更小值，这些位置的答案应继续为 `-1`。

**7. 坑**

- 重复值答案不对：严格与非严格条件混淆。严格更小用 `<`，小于等于用 `<=`。
- 得到的是值却拿来当位置：栈中保存的是下标，确定答案时记录的也是下标。
- `-1` 被用于计算距离或访问数组：先判断该位置是否存在答案，再计算 `answer[j] - j`。
- 误以为栈里最终只剩最小值：栈保存的是尚未找到右侧更小值的候选位置，多个位置可以同时留在栈中。

**8. 一句话原理**

从左向右扫描时，新位置一旦比栈顶位置的值小，就成为该栈顶位置等待已久的第一个严格更小元素。

**参考：**

- [OI Wiki：单调栈](https://oi-wiki.org/ds/monotonous-stack/)

## 5.3 单调队列

**1. 它是做什么的**

给定长度为 `n` 的整数数组 `a` 和窗口长度 `k`，本模板返回每个连续长度为 `k` 的闭区间最小值。仅当 `1 <= k <= n` 时有答案，结果长度为 `n-k+1`；否则返回空数组。对固定窗口，时间复杂度为 $O(n)$，队列辅助空间为 $O(k)$，另需 $O(n-k+1)$ 保存返回结果。初始化没有独立预处理阶段，单次调用处理每个元素一次；每个下标最多入队、出队各一次，所以摊还总操作数为 $O(n)$，单次循环可能弹出多个元素。

它也可用于某些 DP：当每个状态只需查询一段随状态移动的候选区间最优值，且候选值能按下标顺序维护时，可用单调队列代替逐项扫描。若候选区间不单调移动，或候选优劣不能由队尾淘汰规则保证，则不能直接套用。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `a` | 输入数组，0-based；函数不会修改它。 |
| `k` | 窗口长度，合法范围是 `1..n`。 |
| `i` | 当前扫描到的数组下标，也是当前窗口的右端点。 |
| `dq` | 候选下标的双端队列；下标递增，对应值严格递增。队首是当前窗口最小值候选。 |
| `answer` | 按窗口右端点递增收集的结果；`answer[j]` 对应闭区间 `[j, j+k-1]`。 |

处理到 `i` 时，当前窗口是 `[i-k+1, i]`。队首下标不大于 `i-k` 就已过期；从队尾删除值大于或等于 `a[i]` 的下标，因为新元素更靠右且不大于旧元素，旧元素之后不可能再成为最小值。相等时保留较新的下标，它能留在窗口更久。

**3. 函数在做什么**

| 函数 | 参数、返回与作用 |
|---|---|
| `slidingWindowMinimum(a, k)` | 参数为 0-based 整数数组和窗口长度；返回各合法窗口的最小值，不修改 `a`。`k <= 0` 或 `k > a.size()` 时返回空数组。队列在调用内创建，不保留跨调用状态。 |

**4. 怎么调用**

调用时传入数组和窗口长度，直接使用返回数组；数组为空或窗口不合法时，结果为空。下面片段可放在业务函数内：

```text
vector<int> a = {4, 2, 2, 5, 1};
vector<int> ans = slidingWindowMinimum(a, 3);
// ans 为 {2, 2, 1}，依次对应 [4,2,2]、[2,2,5]、[2,5,1]
```

模板代码如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

// 参数 a 为 0-based 数组、k 为窗口长度；返回各窗口最小值，k<=0 或 k>n 时返回空表；不改 a。
    vector<int> slidingWindowMinimum(const vector<int>& a, int k) {
    // a 为 0-based；每个答案对应闭区间 [i-k+1, i]。
    int n = (int)a.size();
    vector<int> answer;
    if (k <= 0 || k > n) return answer;

    // dq 保存候选下标：下标递增，对应值严格递增，队首永远是窗口最小值。
    deque<int> dq;
    for (int i = 0; i < n; ++i) {
        while (!dq.empty() && dq.front() <= i - k) dq.pop_front();  // 移出窗口
        // 相等也弹出旧下标，保留有效期更长的新下标；求最大值时反转不等号。
        while (!dq.empty() && a[dq.back()] >= a[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1) answer.push_back(a[dq.front()]);
    }
    return answer;
}
```

**5. 要改哪里**

- 求窗口最大值：队列对应值改为严格递减，把队尾条件 `a[dq.back()] >= a[i]` 改为 `a[dq.back()] <= a[i]`，队首读取方式不变。
- 若要保留相等值中较早的下标，可将最小值的队尾条件改成 `>`；此时队列值非递减，答案仍正确，但可能多保留候选。
- 变长窗口或其他 DP 候选区间，需要按题目定义修改过期条件和队尾淘汰条件；只有当淘汰后旧候选永远不可能胜出时，才能删除它。若需要同时查询多个不同窗口且窗口端点不按顺序前进，应换用适合的数据结构。

**6. 自检**

对 `a = {4,2,2,5,1}`、`k = 3`，答案应为 `{2,2,1}`；第二个窗口出现重复最小值，队列会舍弃较早的 `2`，但最小值仍为 `2`。`k=1` 时结果应逐项等于原数组；`k=n` 时只返回全数组最小值；空数组、`k=0` 或 `k>n` 均返回空数组。扫描过程中可检查队列下标递增、所有下标均在当前窗口内、对应值严格递增。

**7. 坑**

- 结果少一个或区间错位：窗口是闭区间，只有 `i >= k-1` 才产生答案；第 `j` 项对应 `[j,j+k-1]`。
- 最小值偶尔错误：队尾条件方向写反，导致队首不再是窗口最小值候选；最小值应弹出所有值大于或等于当前值的候选。
- 旧元素影响当前答案：先移除所有过期下标，再读取队首。
- 用值而非下标入队：无法判断候选何时离开窗口；队列应保存数组下标，取值时再访问 `a[dq.front()]`。

**8. 一句话原理**

每个新元素淘汰它之后永远不可能更优的旧候选，队首因此始终给出当前窗口最小值。

**参考：**

- [OI Wiki：单调队列](https://oi-wiki.org/ds/monotonous-queue/)

## 5.4 堆与优先队列

**1. 它是做什么的**

堆适合在一批候选元素中反复取得当前优先级最高或最低者，同时允许新元素加入。C++ `priority_queue` 默认是大根堆，`top()` 返回最大值；指定 `greater<T>` 后成为小根堆。常用于贪心选择、Dijkstra 和 Top-K。它支持查看堆顶、插入和删除堆顶，不支持高效删除任意元素或直接修改堆中元素。

本模板把输入向量中的整数依次放入小根堆，再按从小到大顺序取出，返回一个新向量，不修改输入。初始化采用逐个 `push`，因此处理 `n` 个元素整体为 $O(n\log n)$；不能把此实现的建堆成本写成线性。单次 `top()` 为 $O(1)$，`push` / `pop` 为 $O(\log n)$，空间为 $O(n)$。若使用支持范围建堆的接口，复杂度会不同，但本模板没有这样做。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `a` | 输入整数序列，以常量引用传入，函数不改它。 |
| `minHeap` | 小根优先队列；每次 `top()` 是尚未取出的最小值。 |
| `sorted` | 新建的结果向量，按弹出次序收集所有元素。 |
| `x` | 当前从 `a` 读入并加入堆的整数。 |

堆不暴露元素下标，也不保证除堆顶外的元素有序。相同值可以重复存在；弹出的值按非降序排列，但相等元素之间没有可观察的先后差异。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `heapOrder(const vector<int>& a)` | 接收只读整数向量；返回 `vector<int>`。 | 将所有值压入局部小根堆，逐个弹出并返回升序副本；空输入返回空向量。 |
| `push(x)` | 插入一个元素，返回 `void`。 | 堆调整后仍保持比较器定义的优先级关系。 |
| `top()` | 无参数；返回堆顶元素的常量引用。 | 仅堆非空时可调用。 |
| `pop()` | 无参数；返回 `void`。 | 删除堆顶，不返回其值；需要该值时先保存 `top()`。 |
| `empty()` / `size()` | 无参数；分别返回空状态和元素数量。 | 可用于安全取堆顶的循环条件。 |

**4. 怎么调用**

需要最小值优先时声明 `priority_queue<T, vector<T>, greater<T>>`；最大值优先可用默认 `priority_queue<T>`。循环中先保存 `top()`，再 `pop()`。本模板代码如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

// 参数 a 为待排序整数序列；返回按升序弹出的副本，不改 a。
    vector<int> heapOrder(const vector<int>& a) {
    // greater<int> 使 top() 为当前最小值；若去掉则默认是大根堆。
    priority_queue<int, vector<int>, greater<int>> minHeap;
    for (int x : a) minHeap.push(x);

    vector<int> sorted;
    while (!minHeap.empty()) {
        sorted.push_back(minHeap.top());
        minHeap.pop();
    }
    return sorted;
}
```

片段可放在业务函数内。输入 `[8, 3, 5, 3]` 时，返回值为 `[3, 3, 5, 8]`：

```text
vector<int> a = {8, 3, 5, 3};
vector<int> result = heapOrder(a);
// result: 3 3 5 8；a 仍为 8 3 5 3
```

**5. 要改哪里**

- 要取最大值，改用默认大根堆；要按其他优先级排序，换元素类型或提供比较器，并明确比较器定义的“优先”方向。
- 要处理 `(距离, 点编号)` 等状态，可存 `pair`；`greater<pair<...>>` 按字典序比较，先比较距离，再比较点编号。
- 若在 Dijkstra 等算法中更新同一状态，不能原地修改堆内记录。可把新状态再次 `push`，取出时与当前最佳状态比较，跳过过期项；注意这种懒删除可能让堆暂时大于有效状态数。
- 要删除任意元素或频繁修改优先级，考虑维护索引的堆或其他数据结构；普通 `priority_queue` 没有对应接口。
- 若只想取得前 `k` 个值，可在读取至多 `k` 次后停止，不必把剩余元素全部弹出；堆仍需先容纳本模板插入的全部 `n` 个元素。

**6. 自检**

对 `[8, 3, 5, 3]`，小根堆连续弹出应为 `3, 3, 5, 8`，元素总数保持为 4，重复的 `3` 不会丢失。单元素 `[6]` 返回 `[6]`；空向量返回空向量。若去掉 `greater<int>`，同一输入应按 `8, 5, 3, 3` 弹出，借此确认比较器方向。

**7. 坑**

1. 默认 `priority_queue` 是大根堆；求最小值时忘记 `greater<T>` 会让结果顺序反过来。
2. 对空堆调用 `top()` 或 `pop()` 会导致未定义行为；先检查 `empty()`。
3. `pop()` 只删除，不返回元素；在删除前保存 `top()`。
4. 误以为堆内所有元素都已排序；只有堆顶有优先级保证，完整排序需反复弹出或使用排序算法。
5. 自定义比较器方向弄反会改变堆顶含义；用两个可区分元素手动核对比较关系。

**8. 一句话原理**

堆只维护最高优先级元素位于顶端，因此能快速查看它，并在每次插入或删除后用对数时间恢复这一结构。

**参考：**

- [OI Wiki：堆](https://oi-wiki.org/ds/heap/)

## 5.5 并查集

**1. 它是做什么的**

并查集维护元素只合并、不拆分的分组关系，支持判断是否同组、查询代表元和集合大小。元素编号为 `1..n`。构造初始化时间与空间为 $O(n)$；路径压缩配合按大小合并后，`find`、`unite`、`same`、`size` 的均摊时间为 $O(\alpha(n))$，其中 $\alpha$ 是反 Ackermann 函数。它不能任意拆分集合，也不直接维护集合内部路径等信息。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `parent[x]` | 元素 `x` 的父节点；根满足 `parent[x] == x`。 |
| `sizeOf[x]` | 仅当 `x` 是根时有效，表示该根代表的集合大小。 |
| `n` | 构造参数和最大合法编号；底层数组长为 `n+1`，下标 0 不作为元素使用。 |
| `a`, `b`, `x` | 操作涉及的元素编号，必须在 `1..n`。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `DSU(n)` | 初始化 `1..n` 为 `n` 个单元素集合；构造参数应为非负数。 |
| `find(x)` | 要求 `x` 在 `1..n`；返回所在集合的根，并通过路径压缩修改访问路径上的 `parent`。 |
| `unite(a,b)` | 要求两参数均在 `1..n`；合并所在集合，成功返回 `true`，原已连通返回 `false`；成功时修改根的 `parent` 和 `sizeOf`。 |
| `same(a,b)` | 返回两元素是否同组；查询会调用 `find`，因此可能压缩路径。 |
| `size(x)` | 返回 `x` 所在集合大小；查询会调用 `find` 并可能压缩路径。 |

**4. 怎么调用**

创建对象后，对每条需要加入连通关系的边调用 `unite`；再用 `same` 或 `size` 查询：

```text
DSU dsu(4);
dsu.unite(1, 2);
dsu.unite(2, 3);
// dsu.same(1, 3) 为 true；dsu.size(2) 为 3
// dsu.unite(1, 3) 返回 false，因为二者已经连通
```

原模板：

```cpp

#include <bits/stdc++.h>
using namespace std;

struct DSU {
    // parent[x] 指向父节点；仅根满足 parent[x]==x，且只有根的 sizeOf 有效。
    vector<int> parent, sizeOf;

    // 参数 n 是元素上界；建立编号 1..n 的单元素集合，初始化内部 parent/sizeOf。
    explicit DSU(int n) : parent(n + 1), sizeOf(n + 1, 1) {
        iota(parent.begin(), parent.end(), 0);
    }

    // 参数 x 是 1..n 的元素；返回其集合根，并对访问路径做路径压缩。
    int find(int x) {
        if (parent[x] == x) return x;
        // 路径压缩保持集合不变，只把查询路径上的点直接挂到根。
        return parent[x] = find(parent[x]);
    }

    // 参数 a、b 是 1..n 的元素；合并两集合，成功返回 true、原已连通返回 false；修改根和集合大小。
    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (sizeOf[a] < sizeOf[b]) swap(a, b);  // 始终把小树挂到大树
        parent[b] = a;
        sizeOf[a] += sizeOf[b];
        return true;
    }

    // 所有公开查询都先压到根，避免调用方误把非根当代表。
    // 参数 a、b 是 1..n 元素；返回是否同属一集合，查询会通过 find 压缩路径。
    bool same(int a, int b) { return find(a) == find(b); }
    // 参数 x 是 1..n 元素；返回其所在集合大小，查询会通过 find 压缩路径。
    int size(int x) { return sizeOf[find(x)]; }
};
```

**5. 要改哪里**

- 若改成 0-based 编号，需同步调整数组长度、初始化范围和每个接口的合法下标。
- 若需维护集合聚合信息，在成功合并时将两个根的状态合并到新根；非根上的旧聚合值不再有效。
- 若需要按后进先出顺序撤销已记录的合并，可使用回滚并查集并记录每次修改；它只能按操作历史撤销，不能任意拆分某个集合。常见回滚实现不做路径压缩，以便恢复修改。
- 多组数据可每组重新构造对象；普通并查集不提供清空或撤销接口。

**6. 自检**

初始 `DSU(3)` 中 `same(1,2)` 为 `false`、`size(1)` 为 1。`unite(1,2)` 返回 `true` 后两点同组且大小为 2；再次 `unite(2,1)` 返回 `false`，大小仍为 2。再合并 2 和 3 后，三个元素应同组、`size(3)` 为 3。

**7. 坑**

- 直接改 `parent[a]`：`a` 可能不是根；先用 `find` 取得两个根。
- 读取非根的 `sizeOf`：集合大小只保证存于根节点。
- 把 `unite` 的返回值当新根：它只表示本次是否真正合并。
- 需要拆分却使用普通并查集：已合并的信息无法恢复；回滚也只支持按记录顺序撤销，不支持任意拆分。

**8. 一句话原理**

每个集合由根代表，合并时小树挂到大树上，查询时压缩访问路径。

**参考：**

- [OI Wiki：并查集](https://oi-wiki.org/ds/dsu/)

## 5.6 树状数组

**1. 它是做什么的**

树状数组维护长度 `n>=1` 的 1-based 数组的可加减信息，支持单点增加、前缀和与区间和。本模板另提供 `lowerBound`：在每个位置的频次非负时，找前缀和首次达到目标的位置。更新与每次查询均为 $O(\log n)$，空间为 $O(n)$；构造全零结构的初始化为 $O(n)$，若逐点插入初始值则为 $O(n\log n)$。它适合和、频次等可做加减的量，不直接支持任意区间最值或区间赋值。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `n` | 最大有效下标；合法位置为 `1..n`。 |
| `tree[i]` | Fenwick 分块和，覆盖 `(i-lowbit(i), i]`，其中 `lowbit(i) = i & -i`。 |
| `index` | `add` 的更新位置，或 `prefixSum` 的查询右端点；前者必须至少为 1，后者可为 0。 |
| `left`, `right` | `rangeSum` 的闭区间端点。若 `left > right`，实现返回 0。 |
| `target` | `lowerBound` 要达到的前缀和目标。 |
| `accumulated` | `lowerBound` 二进制提升过程中，已确认小于 `target` 的前缀和。 |

下标从 1 开始；`tree[0]` 不参与更新。`lowerBound(target)` 返回最小的 `i`，使 `prefixSum(i) >= target`；没有满足位置时返回 `n+1`。本实现对 `target <= 0` 返回 1。

**3. 函数在做什么**

| 函数 | 参数、返回与作用 |
|---|---|
| `Fenwick(n)` | 创建最大下标为 `n` 的全零结构，内部数组长度为 `n+1`。 |
| `add(index, delta)` | 将位置 `index` 增加 `delta`，修改覆盖该位置的分块；要求 `1 <= index <= n`。 |
| `prefixSum(index)` | 返回闭区间 `[1,index]` 的和，`index` 可为 `0..n`；不修改结构。 |
| `rangeSum(left, right)` | 返回闭区间和 `prefixSum(right)-prefixSum(left-1)`；要求端点在有效范围内，空区间返回 0。 |
| `lowerBound(target)` | 在各点值非负时返回最小满足前缀和至少为 `target` 的下标；无解为 `n+1`。不修改结构。 |

**4. 怎么调用**

先构造容量，再用 `add` 记录每个位置的增量；前缀和与区间和可以随时查询。`lowerBound` 只适用于各点频次非负的情形，例如频次统计：

```text
Fenwick fw(5);
fw.add(1, 2);
fw.add(3, 1);
fw.add(5, 2);
// fw.prefixSum(3) == 3，fw.rangeSum(2, 5) == 3
// fw.lowerBound(4) == 5，fw.lowerBound(6) == 6（无解，n+1）
```

模板代码如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Fenwick {
    int n;
    // 仅使用 1..n；tree[i] 保存 (i-lowbit(i), i] 这一段的和。
    vector<ll> tree;

    // 参数 n 是正的最大下标；创建全零 1-based 树状数组，初始化内部 tree。
    explicit Fenwick(int n) : n(n), tree(n + 1, 0) {}

    // 参数 index 属于 1..n、delta 为增量；返回 void，修改覆盖 index 的 Fenwick 节点。
    void add(int index, ll delta) {
        // index 必须 >=1；向父区间跳转，直到超过 n。
        for (int i = index; i <= n; i += i & -i) tree[i] += delta;
    }

    // 参数 index 属于 0..n；返回原数组闭区间 [1,index] 的和，不改结构。
    ll prefixSum(int index) const {
        // 查询闭区间 [1,index]；每次删掉当前下标最低位的 1。
        ll result = 0;
        for (int i = index; i > 0; i -= i & -i) result += tree[i];
        return result;
    }

    // 参数 left/right 为合法 1-based 闭区间；返回当前区间和，不修改结构。
    ll rangeSum(int left, int right) const {
        if (left > right) return 0;
        return prefixSum(right) - prefixSum(left - 1);
    }

    // 频次数组非负时，返回最小 i 使 prefixSum(i)>=target；无解返回 n+1。
    // 参数 target 为目标前缀频次；要求各点频次非负，返回最小满足前缀和>=target 的下标，无解为 n+1。
    int lowerBound(ll target) const {
        int index = 0;
        ll accumulated = 0;
        int step = 1;
        while ((step << 1) <= n) step <<= 1;
        // 二进制提升：index 始终是“前缀和仍小于 target”的最大已知下标。
        for (; step; step >>= 1) {
            int next = index + step;
            if (next <= n && accumulated + tree[next] < target) {
                index = next;
                accumulated += tree[next];
            }
        }
        return index + 1;
    }
};
```

**5. 要改哪里**

- 单点赋值需先保存旧值，再调用 `add(index, newValue-oldValue)`；直接把新值作为增量会把旧值重复计入。
- 若要维护频次并按累计频次定位，保证每次更新后每个位置的频次仍非负，再调用 `lowerBound`。普通数组值可以为负，但此时前缀和不再单调，不能用该函数二进制提升。
- 想从一组初始值建树，当前结构没有批量 `build` 接口；可逐点 `add`，时间为 $O(n\log n)$，或另行实现线性建树。
- 区间加、区间和等需求通常需要两棵树状数组并重新推导更新公式；区间最值或任意赋值应换用支持相应操作的数据结构。

**6. 自检**

上面的示例各点值为 `[2,0,1,0,2]`，所以前三项和为 `3`，区间 `[2,5]` 和为 `3`。累计和首次达到 4 的位置是 5；目标 6 大于总和 5，返回 `n+1=6`。单位置更新后可用 `rangeSum(i,i)` 核对；目标为 1 时应返回第一个正频次位置。更新下标 0 会导致循环无法前进，必须始终使用 `1..n`。

**7. 坑**

- 更新后程序卡住：`add(0, delta)` 中 `i & -i` 为 0，循环不前进；更新位置必须至少为 1。
- 区间和差一位：区间是闭区间，公式要减去 `prefixSum(left-1)`。
- `lowerBound` 给出错误位置：某次减量让某个点频次变成负数，前缀和不再单调；保持所有点频次非负。
- 无解时访问数组越界：目标超过总频次会返回 `n+1`，调用方要先处理这个哨兵值。
- `target <= 0` 的边界与直觉不同：本实现仍返回 1；若题意需要空前缀下标 0，需调整接口约定和实现。

**8. 一句话原理**

用 `i & -i` 把前缀拆成少量不重叠分块，并在二进制提升时跳过仍达不到目标的整段。

**参考：**

- [OI Wiki：树状数组](https://oi-wiki.org/ds/fenwick/)

## 5.7 线段树（区间加、区间和）

**1. 它是做什么的**

这棵线段树维护一个长度为 `n` 的 1-based 数组，支持把闭区间 `[l,r]` 每个数加上 `delta`，以及查询该区间的元素和。两种操作可以交错进行；单点加是 `rangeAdd(i,i,delta)`。适合区间更新和区间查询混合出现的场景，不能直接支持区间赋值或任意其他统计量。

构造对象及开辟数组空间为 $O(n)$；对初值建树为 $O(n)$；一次合法区间加或区间和查询为 $O(\log n)$。空间为 $O(n)$，本实现使用约 `4n` 个节点槽位。每个值及区间和均使用 `long long`，题目数据仍须保证乘法和总和不溢出。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `n` | 数组长度，必须大于 0。有效位置为 `1..n`。 |
| `sum[p]` | 线段树节点 `p` 所管理闭区间的当前总和，已计入该节点上的整段修改。 |
| `lazy[p]` | 已计入 `sum[p]`、但尚未传给孩子的每项增量。下传后必须清零，避免重复应用。 |
| `p, left, right` | 递归内部使用的节点编号和当前闭区间；不是使用者传入数组的零基下标。 |
| `ql, qr` | 查询或更新的目标闭区间，要求 `1 <= ql <= qr <= n`。 |
| `delta` | 对目标区间每个元素增加的值。 |
| `a` | 初始值向量；`a[1]` 到 `a[n]` 对应数组位置，`a[0]` 不参与构建。 |

内部节点的左右孩子分别代表 `[left,mid]` 和 `[mid+1,right]`。`sum[p]` 已计入本节点收到的更新；祖先尚未下传的标记可能还未反映在子节点中。访问子节点前必须先下传。若整段加 `delta`，总和应增加 `delta * (right-left+1)`。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及调用条件 |
|---|---|---|
| `SegmentTree(int n)` | 长度 `n`；构造对象。 | 分配并将 `sum`、`lazy` 初始化为零；要求 `n > 0`。 |
| `build(a)` | 1-based 初值向量；返回 `void`。 | 初始化节点和。仅应在刚构造的新对象上调用一次；它不清除已有 `lazy` 标记，带更新状态的对象不能靠再次 `build` 重置，应重新构造对象。 |
| 内部 `build(a,p,left,right)` | 初值及当前节点区间；返回 `void`。 | 递归建立 `sum`，不触碰 `lazy`，使用者无需直接调用。 |
| `apply(p,left,right,delta)` | 节点区间和增量；返回 `void`。 | 更新本段和与本段懒标记，供内部调用。 |
| `pushDown(p,left,right)` | 当前节点及其区间；返回 `void`。 | 将增量按左右子区间的实际长度下传并清空父标记；叶节点无需下传。 |
| `rangeAdd(l,r,delta)` | 合法 1-based 闭区间和增量；返回 `void`。 | 修改区间内所有元素。 |
| `rangeSum(l,r)` | 合法 1-based 闭区间；返回 `long long`。 | 查询区间和；查询时可能下传懒标记，但不改变逻辑数组的值。 |
| 内部重载 `rangeAdd` / `rangeSum` | 额外接收 `p,left,right`；更新返回 `void`，查询返回和。 | 递归实现，使用者调用公开的三参数或双参数接口即可。 |

**4. 怎么调用**

令 `n >= 1`，准备长度至少 `n+1` 的向量，使初值放在 `a[1..n]`；构造一个新对象并调用一次 `build(a)`。之后对所有操作使用合法闭区间。模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct SegmentTree {
    int n;
    // 节点 p 管理闭区间 [left,right]。
    // sum[p] 已含本节点全部修改；lazy[p] 表示尚未下传给子节点的“每项增量”。
    vector<ll> sum, lazy;

    // 参数 n 为正数组长度；分配区间和与懒标记空间，初始值均为 0。
    explicit SegmentTree(int n) : n(n), sum(4 * n + 4), lazy(4 * n + 4) {}

    // 参数 a 为 1-based 初值；p 管理闭区间 [left,right]，递归写入 sum、不触碰 lazy；区间合法且非空，只应对全零新对象构建。
    void build(const vector<ll>& a, int p, int left, int right) {
        // 输入 a 使用 1-based；递归区间始终是闭区间。
        if (left == right) {
            sum[p] = a[left];
            return;
        }
        int mid = (left + right) / 2;
        build(a, p * 2, left, mid);
        build(a, p * 2 + 1, mid + 1, right);
        sum[p] = sum[p * 2] + sum[p * 2 + 1];
    }

    // 参数 a[1..n] 是初值；返回 void，只初始化节点 sum，不清 lazy；须对刚构造的新对象调用一次，已有更新后重建需重新构造对象。
    void build(const vector<ll>& a) { build(a, 1, 1, n); }

    // 参数指定节点区间和增量 delta；返回 void，直接修改该节点 sum/lazy。
    void apply(int p, int left, int right, ll delta) {
        // 整段每项增加 delta，所以区间和增加 delta * 区间长度。
        sum[p] += delta * (right - left + 1);
        lazy[p] += delta;
    }

    // 参数 p 管理闭区间 [left,right]；返回 void，将未下传增量写到子节点并清父标记。
    void pushDown(int p, int left, int right) {
        if (lazy[p] == 0 || left == right) return;
        int mid = (left + right) / 2;
        // 下传必须使用子区间真实长度；完成后清空父标记，避免重复应用。
        apply(p * 2, left, mid, lazy[p]);
        apply(p * 2 + 1, mid + 1, right, lazy[p]);
        lazy[p] = 0;
    }

    // ql/qr 为待加闭区间，p,left,right 为当前节点；要求区间合法且相交，返回 void 并修改覆盖节点。
    void rangeAdd(int ql, int qr, ll delta, int p, int left, int right) {
        // ql,qr 是待修改闭区间；调用前保证它合法且与当前区间有交集。
        if (ql <= left && right <= qr) {
            apply(p, left, right, delta);
            return;
        }
        pushDown(p, left, right);
        int mid = (left + right) / 2;
        if (ql <= mid) rangeAdd(ql, qr, delta, p * 2, left, mid);
        if (qr > mid) rangeAdd(ql, qr, delta, p * 2 + 1, mid + 1, right);
        // 子树修改后回收信息，保持 sum[p] 等于整个 [left,right] 的和。
        sum[p] = sum[p * 2] + sum[p * 2 + 1];
    }

    // 参数 left/right 为合法 1-based 闭区间、delta 为每项增量；返回 void，更新覆盖节点的和及懒标记。
    void rangeAdd(int left, int right, ll delta) {
        rangeAdd(left, right, delta, 1, 1, n);
    }

    // ql/qr 为查询闭区间，p,left,right 为当前节点；返回两区间交集之和，并可能下传懒标记。
    ll rangeSum(int ql, int qr, int p, int left, int right) {
        // 完全覆盖直接返回；部分覆盖前先下传，保证子节点信息最新。
        if (ql <= left && right <= qr) return sum[p];
        pushDown(p, left, right);
        int mid = (left + right) / 2;
        ll result = 0;
        if (ql <= mid) result += rangeSum(ql, qr, p * 2, left, mid);
        if (qr > mid) result += rangeSum(ql, qr, p * 2 + 1, mid + 1, right);
        return result;
    }

    // 参数为合法 1-based 闭区间；返回区间和，查询可能下传内部懒标记。
    ll rangeSum(int left, int right) {
        return rangeSum(left, right, 1, 1, n);
    }
};
```

片段可放在业务函数内。初值 `[1,2,3,4,5]`，将 `[2,4]` 每项加 `3` 后，数组逻辑值为 `[1,5,6,7,5]`，`rangeSum(3,5)` 返回 `18`：

```text
vector<ll> a = {0, 1, 2, 3, 4, 5}; // a[0] 不使用
SegmentTree st(5);
st.build(a);
st.rangeAdd(2, 4, 3);
ll answer = st.rangeSum(3, 5); // 18
```

**5. 要改哪里**

- 单点增量直接调用 `rangeAdd(i,i,delta)`；查询单点也可调用 `rangeSum(i,i)`。
- 若要区间赋值，需要新增赋值标记及其与加法标记的组合规则，不能把赋值当作一次区间加处理。
- 若要维护区间最小值/最大值等统计量，需修改 `sum` 的含义、节点合并方式、整段更新规则和查询返回值；仅改变量名不够。
- 若初值为全零，可不调用 `build`，因为构造函数已将节点初始化为零；有非零初值时必须构建。
- 多组数据或需要彻底重置时，为每组新建 `SegmentTree` 对象。当前 `build` 不清理旧懒标记，不能复用于已经做过更新的对象。
- 空数组不受支持；区间接口没有边界检查，调用者需保证 `1 <= l <= r <= n`。

**6. 自检**

初值 `[1,2,3,4,5]` 的总和是 `15`。执行 `rangeAdd(2,4,3)` 后，区间 `[2,4]` 的和应为 `18`，全数组和应为 `24`，`rangeSum(3,5)` 为 `18`。再执行 `rangeAdd(3,3,-6)`，位置 3 变为 0，`rangeSum(1,5)` 应为 `18`。单元素数组 `[7]` 上查询 `[1,1]` 得 `7`，加 `-7` 后得 `0`。这些检查也覆盖负增量和端点区间。

**7. 坑**

1. 把区间增量只加到区间和一次；正确增量是 `delta * 区间长度`。
2. 部分访问前未下传懒标记，子节点记录因此过期；检查递归进入孩子前是否调用 `pushDown`。
3. 下传后没清父标记会重复加；本模板在更新完孩子后将 `lazy[p]` 置零。
4. 把 0-based 区间传给接口；本模板所有公开区间和初值位置都是 1-based 闭区间。
5. 对已更新对象再次 `build` 试图重置；它只写 `sum`，不会清 `lazy`，重置时重新构造对象。

**8. 一句话原理**

整段更新先记在节点的和与懒标记中，只有递归访问子区间时才下传，从而避免逐个修改区间元素。

**参考：**

- [OI Wiki：线段树](https://oi-wiki.org/ds/seg/)

## 5.8 ST 表（静态 RMQ）

**1. 它是做什么的**

ST 表用于静态、不可修改的数组，预处理后查询闭区间最大值。本模板的数组按 `1..n` 存储，要求至少一个有效元素；构造时间和空间均为 $O(n\log n)$，每次查询为 $O(1)$。查询将两个长度为 $2^j$ 的区间合并，二者可能重叠，因此运算须同时满足结合律和幂等性；`max`、`min`、`gcd` 都满足这两个条件，区间和不满足幂等性，不能这样查询。数组修改后需重建或改用支持更新的结构。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `n` | 有效元素数，输入 `a` 的下标 `1..n` 有效，`a[0]` 不用。 |
| `levels` | 预处理层数，覆盖长度 `2^0` 至 `2^(levels-1)`。 |
| `log2Floor[len]` | `floor(log2(len))`，用于选取不超过查询长度的最大幂次。 |
| `st[j][i]` | 闭区间 `[i, i+2^j-1]` 的最大值；只有该区间完全落在数组内的位置才用于查询。 |
| `left`, `right` | `query` 的 1-based 闭区间端点。 |

对长度 `len=right-left+1`，令 `j=floor(log2(len))`、`blockLen=2^j`。查询合并 `[left,left+blockLen-1]` 与 `[right-blockLen+1,right]`：两段长度相同，第一段从 `left` 开始，第二段从 `right-blockLen+1` 开始；因 `2*blockLen >= len`，它们覆盖查询区间，重叠部分由幂等运算安全重复计算。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `SparseTableMax(a)` | 参数为 1-based 非空静态数组；构造各幂长区间的最大值表，不修改 `a`。 |
| `query(left,right)` | 参数为满足 `1<=left<=right<=n` 的闭区间；返回该段最大值，不修改表。 |

**4. 怎么调用**

先把数据放入长度 `n+1` 的数组并保留 `a[0]` 作为占位，再构造一次，之后可重复查询：

```text
vector<int> a = {0, 4, 2, 7, 1, 5};
SparseTableMax rmq(a);
// rmq.query(2, 5) 为 7；rmq.query(3, 4) 为 7
```

原模板：

```cpp

#include <bits/stdc++.h>
using namespace std;

struct SparseTableMax {
    int n, levels;
    vector<int> log2Floor;
    // st[j][i] 保存闭区间 [i, i+2^j-1] 的最大值；输入 a 为 1-based。
    vector<vector<int>> st;

    // 参数 a 为 1-based 非空静态数组；构造各级区间最大值表，不修改 a。
    explicit SparseTableMax(const vector<int>& a) {
        n = (int)a.size() - 1;
        log2Floor.assign(n + 1, 0);
        // log2Floor[i] = floor(log2(i))，查询时可 O(1) 找到覆盖长度。
        for (int i = 2; i <= n; ++i) log2Floor[i] = log2Floor[i / 2] + 1;

        levels = log2Floor[n] + 1;
        st.assign(levels, vector<int>(n + 1));
        for (int i = 1; i <= n; ++i) st[0][i] = a[i];

        for (int j = 1; j < levels; ++j) {
            int length = 1 << j;
            for (int i = 1; i + length - 1 <= n; ++i) {
                // 长为 2^j 的区间由两个相邻、长为 2^(j-1) 的区间组成。
                st[j][i] = max(st[j - 1][i], st[j - 1][i + length / 2]);
            }
        }
    }

    // 参数为合法闭区间 1<=left<=right<=n；返回该区间最大值，不修改表。
    int query(int left, int right) const {
        // max 可重复贡献：用两个可能重叠的 2^j 区间覆盖 [left,right]。
        int j = log2Floor[right - left + 1];
        return max(st[j][left], st[j][right - (1 << j) + 1]);
    }
};
```

**5. 要改哪里**

- 求区间最小值时，将构造和查询中的 `max` 都改为 `min`。
- 求 GCD 时将两处合并都改为 `gcd`，并确保运算实现可用。
- 区间和不满足重叠计算的幂等条件，应使用前缀和、树状数组或线段树。
- 数组发生修改后，当前表不会自动更新；可重建整张表，或换用支持修改的数据结构。

**6. 自检**

数组 `[4,2,7,1,5]` 映射到下标 `1..5` 后，`query(2,5)` 和 `query(3,4)` 都应为 7，单点 `query(4,4)` 应为 1。包含负数的数组 `[-8,-3,-11]` 上，`query(1,3)` 应为 -3，`query(2,3)` 应为 -3；这能检查最大值初始化和重叠区间起点是否正确。长度为 1 时唯一合法查询返回该元素。

**7. 坑**

- 把 `a[0]` 当有效数据：输入约定从 1 开始。
- 第二段起点写错：应为 `right-2^j+1`；漏掉 `+1` 会错位。
- 把 ST 表用于求和：两段会重叠，重叠元素被重复计入。
- 在数组修改后沿用旧表：查询仍反映构造时的数据。

**8. 一句话原理**

预存各个 2 的幂长度区间的最大值，再用两个可能重叠的等长区间覆盖查询段。

**参考：**

- [OI Wiki：ST 表](https://oi-wiki.org/ds/sparse-table/)

## 5.9 分块（区间加、区间和）

**1. 它是做什么的**

本模板把非空 1-based 数组分成约 $\sqrt n$ 个块，支持闭区间加一个增量和查询闭区间和。数组长度为 `n` 时，构造耗时、空间均为 $O(n)$；一次 `rangeAdd` 或 `rangeSum` 最多扫描两端散块并处理完整中间块，时间为 $O(\sqrt n)$。它适合整块更新和查询都容易维护的场景；区间最值、赋值等操作需要重新设计块内状态，不能直接使用本模板。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `value[i]` | 下标 `i` 的基础值，不含所在块的懒标记。实际值是 `value[i] + lazy[belong[i]]`。 |
| `sum[b]` | 块 `b` 所有 `value` 的和，同样不含懒标记。 |
| `lazy[b]` | 整块统一增加的量。整块实际和为 `sum[b] + lazy[b] * 块长`。 |
| `belong[i]` | 1-based 位置 `i` 所属的 0-based 块编号。 |
| `leftEnd[b]`, `rightEnd[b]` | 块 `b` 的实际闭区间端点；末块可能比其他块短。 |
| `blockSize`, `blockCount` | 目标块长和实际块数，块长取 `max(1, floor(sqrt(n)))`。 |

输入数组需满足 `a.size() >= 2`，有效元素为 `a[1..n]`，`a[0]` 不使用。元素、懒标记、整块和及其乘积均须能放入 `long long`。所有操作端点必须满足 `1 <= left <= right <= n`。

**3. 函数在做什么**

| 函数 | 参数、返回与作用 |
|---|---|
| `SqrtDecomposition(a)` | 用 `a[1..n]` 初始化块，复制数据，不修改输入；要求数组非空且采用 1-based 存储。 |
| `rangeAdd(left,right,delta)` | 将闭区间内每项增加 `delta`，修改基础值或完整块懒标记，并同步散块的 `sum`；无返回值。 |
| `rangeSum(left,right)` | 返回当前闭区间和；读取散块时补上懒标记，读取完整块时整块计入标记贡献，不修改结构。 |

**4. 怎么调用**

先准备一个首项不用的数组，再构造一次；后续更新和查询都调用对象方法。下面片段可放在业务函数内：

```text
vector<long long> a = {0, 1, 2, 3, 4, 5};
SqrtDecomposition ds(a);
ds.rangeAdd(2, 4, 10);
// ds.rangeSum(1, 5) == 45；ds.rangeSum(2, 4) == 39
```

模板代码如下：

```cpp

#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct SqrtDecomposition {
    int n, blockSize, blockCount;
    // value[i] 与 sum[b] 均不含 lazy[b]；真实值为 value[i]+lazy[belong[i]]。
    vector<ll> value, sum, lazy;
    // belong 映射 1-based 下标到 0-based 块；块端点均为闭区间。
    vector<int> belong, leftEnd, rightEnd;

    // 参数 a[1..n] 为非空初始数组；构造块和懒标记副本，不修改 a。
    explicit SqrtDecomposition(const vector<ll>& a) {
        // 输入 a[1..n]，a[0] 不使用；要求 n>=1。
        n = (int)a.size() - 1;
        blockSize = max(1, (int)sqrt(n));
        blockCount = (n + blockSize - 1) / blockSize;
        value = a;
        sum.assign(blockCount, 0);
        lazy.assign(blockCount, 0);
        belong.resize(n + 1);
        leftEnd.resize(blockCount);
        rightEnd.resize(blockCount);

        for (int b = 0; b < blockCount; ++b) {
            leftEnd[b] = b * blockSize + 1;
            rightEnd[b] = min(n, (b + 1) * blockSize);
            for (int i = leftEnd[b]; i <= rightEnd[b]; ++i) {
                belong[i] = b;
                sum[b] += value[i];
            }
        }
    }

    // 参数为合法闭区间及每项增量；返回 void，更新散块元素/整块懒标记。
    void rangeAdd(int left, int right, ll delta) {
        // 修改闭区间 [left,right]：散块写 value/sum，完整块只累加 lazy。
        int bl = belong[left], br = belong[right];
        if (bl == br) {
            for (int i = left; i <= right; ++i) value[i] += delta;
            sum[bl] += delta * (right - left + 1);
            return;
        }
        for (int i = left; i <= rightEnd[bl]; ++i) value[i] += delta;
        sum[bl] += delta * (rightEnd[bl] - left + 1);
        for (int b = bl + 1; b < br; ++b) lazy[b] += delta;  // 不改原始块和
        for (int i = leftEnd[br]; i <= right; ++i) value[i] += delta;
        sum[br] += delta * (right - leftEnd[br] + 1);
    }

    // 参数 left/right 为合法 1-based 闭区间；返回当前区间和，不修改结构。
    ll rangeSum(int left, int right) const {
        // 查询闭区间 [left,right]；散块逐项补 lazy，整块一次补标记贡献。
        int bl = belong[left], br = belong[right];
        ll result = 0;
        if (bl == br) {
            for (int i = left; i <= right; ++i) result += value[i] + lazy[bl];
            return result;
        }
        for (int i = left; i <= rightEnd[bl]; ++i) result += value[i] + lazy[bl];
        for (int b = bl + 1; b < br; ++b) {
            result += sum[b] + lazy[b] * (rightEnd[b] - leftEnd[b] + 1);
        }
        for (int i = leftEnd[br]; i <= right; ++i) result += value[i] + lazy[br];
        return result;
    }
};
```

**5. 要改哪里**

- 改成区间加、单点查询时，可查询 `value[i] + lazy[belong[i]]`；若还维护其他聚合量，需同步更新散块和完整块状态。
- 增加区间赋值、区间最值等操作时，必须重新定义懒标记和块汇总值的组合及更新规则；不能只把某个循环里的加法替换掉。
- 若采用不同块长，应同时检查两端扫描长度与中间块数量，确保最坏时间仍符合预期。多组数据应为每组重新构造对象；构造函数会初始化全部块状态。

**6. 自检**

示例初始数组为 `[1,2,3,4,5]`，对 `[2,4]` 加 10 后为 `[1,12,13,14,5]`，总和 45，区间 `[2,4]` 和为 39。可用长度为 1 的区间检查点值，再查询整段核对总和；特意选跨块区间和落在最后一个短块的区间，检查边界端点及实际块长是否正确。

**7. 坑**

- 整块更新后散块查询少算：`value` 不含 `lazy`，扫描单个元素时必须加上所在块标记。
- 整块查询重复或漏算标记：`sum[b]` 也不含标记，应额外加 `lazy[b] * 块长`。
- 最后一块结果错误：末块长度可能不足 `blockSize`，计算整块贡献应使用 `rightEnd[b]-leftEnd[b]+1`。
- 用 0-based 输入直接调用：构造和操作都约定有效下标从 1 开始，需先调整存储方式或改写映射。

**8. 一句话原理**

两端不完整的块逐项处理，中间完整块用块和与懒标记一次处理。

**参考：**

- [OI Wiki：分块](https://oi-wiki.org/ds/decompose/)

## 5.10 树状数组：区间加与区间和

**1. 它是做什么的**

`RangeFenwick` 在长度为 `n` 的 1-based 数组上支持闭区间加法和区间求和。它把数组变化表示为差分，再用两棵 5.6 节的 `Fenwick` 维护差分系数。适用于区间加、区间和交错出现；不能直接支持区间赋值或区间最值。

构造两棵全零树状数组为 $O(n)$ 时间和空间。一次区间加和一次区间求和均为 $O(\log n)$；查询前缀同样为 $O(\log n)$。非零初值需逐点调用 `addRange(i,i,a[i])`，总初始化时间为 $O(n\log n)$。数组值及中间乘积使用 `long long`，需保证数值不溢出。本代码依赖 5.6 节的 `Fenwick` 类型及 `ll` 别名；单独摘出代码块不能编译。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `n` | 逻辑数组长度；合法位置为 `1..n`，构造要求正数。 |
| `b1`、`b2` | 两棵差分 Fenwick，分别存差分值和乘以位置偏移后的系数。 |
| `x` | 前缀右端点，`prefix(x)` 接受 `0..n`。 |
| `l`、`r` | 公开区间的左右端点，使用 1-based 闭区间。 |
| `v` | 每个被覆盖位置增加的值。 |
| `addPoint(x,v)` | 内部更新差分端点；`n+1` 是区间右界之后的哨兵，不写入树。 |

设 `D[i]=A[i]-A[i-1]`，则 `A[i]` 是 `D[1..i]` 的和。对 `A[l..r]` 加 `v`，令 `D[l]+=v`、`D[r+1]-=v` 即可。前缀数组和由 `x * sum(D[1..x]) - sum((i-1)D[i])` 得出，即 `x*b1.prefixSum(x)-b2.prefixSum(x)`。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及调用条件 |
|---|---|---|
| `RangeFenwick(size)` | 长度 `size`；构造对象。 | 初始化两棵全零 Fenwick，逻辑数组初值全为 0；要求 `size > 0`。 |
| `addPoint(x,v)` | 差分位置 `x` 与增量；返回 `void`。 | 同步修改两棵树；允许 `x=n+1` 哨兵并忽略该更新。内部辅助函数，通常通过 `addRange` 使用。 |
| `addRange(l,r,v)` | 1-based 闭区间及增量；返回 `void`。 | 通过两个差分端点更新逻辑数组；若 `l>r` 则不做事。非空区间要求 `1<=l<=r<=n`。 |
| `prefix(x)` | `x` 属于 `0..n`；返回 `long long`。 | 返回逻辑数组 `[1,x]` 的和；`x=0` 返回 0。 |
| `query(l,r)` | 1-based 闭区间；返回 `long long`。 | 返回 `[l,r]` 的和；若 `l>r` 返回 0。非空查询须在数组范围内。 |
| 依赖的 `Fenwick::add` | 位置 `1..n` 和增量；返回 `void`。 | 更新单点差分系数；不能对位置 0 调用。 |
| 依赖的 `Fenwick::prefixSum` | 位置 `0..n`；返回前缀和。 | 被 `prefix` 调用以取得系数前缀。 |

**4. 怎么调用**

先提供 5.6 节的 `Fenwick` 和 `ll` 定义，再构造 `RangeFenwick(n)`。它默认代表全零数组；非零初值按点初始化，然后使用 `addRange` 和 `query`。模板如下：

```cpp

struct RangeFenwick {
    // 两棵树保存差分系数，prefix(x)=x*B1.prefix-B2.prefix。
    int n;
    Fenwick b1,b2;
    // 参数 size 为正数组长度；初始化两棵差分 Fenwick，逻辑数组初始为零。
    explicit RangeFenwick(int size) : n(size), b1(size), b2(size) {}
    // 参数 x 属于 1..n+1，v 是差分增量；返回 void，更新系数树，n+1 哨兵不写树。
    void addPoint(int x, ll v) {
        // 差分在 l 加 v、在 r+1 减 v；n+1 的哨兵不需要写入树中。
        if (x <= n) {
            b1.add(x, v);
            b2.add(x, v * (x - 1));
        }
    }
    // 参数为 1-based 闭区间及增量；返回 void，修改两棵树表示的逻辑数组，空区间无操作。
    void addRange(int l, int r, ll v) {
        if (l > r) {
            return;
        }
        addPoint(l, v);
        addPoint(r + 1, -v);
    }
    // 参数 x 属于 0..n；返回逻辑数组 [1,x] 之和，不修改树。
    ll prefix(int x) const {
        return b1.prefixSum(x) * x - b2.prefixSum(x);
    }
    // 参数为合法闭区间；返回逻辑数组区间和，空区间返回 0。
    ll query(int l, int r) const {
        return l > r ? 0 : prefix(r) - prefix(l - 1);
    }
};
```

片段可放在业务函数内。初值 `[1,2,3,4,5]`，对 `[2,4]` 加 2 后数组为 `[1,4,5,6,5]`，查询 `[3,5]` 得 `16`：

```text
RangeFenwick fw(5);
for (int i = 1; i <= 5; ++i) fw.addRange(i, i, i);
fw.addRange(2, 4, 2);
long long answer = fw.query(3, 5); // 16
```

**5. 要改哪里**

- 单点增加用 `addRange(i,i,v)`；区间和使用 `query(l,r)`。
- 非零初值逐点调用 `addRange(i,i,a[i])`，总计 $O(n\log n)$；本模板没有线性建树接口。
- 区间赋值、区间最值等需求不能只改查询公式；差分及两棵和树的状态不足以维护它们，需换用或设计相应数据结构。
- 空更新区间 `l>r` 会忽略；空查询区间 `l>r` 返回 0。其他下标没有边界检查，调用者须保证合法。
- `r=n` 时 `r+1` 是 `n+1` 哨兵，`addPoint` 会跳过它；不要把哨兵传入底层 `Fenwick::add`。更新位置不能为 0。

**6. 自检**

构造长度 5 的全零数组，逐点加入 `[1,2,3,4,5]` 后 `query(1,5)` 应为 15。将 `[2,4]` 加 2 后，逻辑值为 `[1,4,5,6,5]`，`query(3,5)` 为 16，`query(1,1)` 仍为 1。`query(2,1)` 返回 0，`addRange(4,3,100)` 不改变数据。再执行 `addRange(5,5,1)`，`query(5,5)` 应为 6，可核对右端点哨兵。

**7. 坑**

1. 区间加没有转为两个差分端点；应在 `l` 加 `v`、在 `r+1` 减 `v`。
2. 忘记偏移树 `b2` 或写错 `x-1`，前缀公式会出错；核对 `x*b1.prefixSum(x)-b2.prefixSum(x)`。
3. `r=n` 时把 `n+1` 传给底层 Fenwick；底层合法下标只有 `1..n`，本实现会忽略哨兵。
4. 初始化非零数组后遗漏逐点加入；构造函数只创建全零逻辑数组。
5. 复制此结构时漏掉 5.6 节的 `Fenwick` / `ll`；需将依赖一并提供。

**8. 一句话原理**

把区间加转换为差分数组的两个端点变化，再用两棵 Fenwick 将差分前缀还原成原数组前缀和。

**参考：**

- [OI Wiki：树状数组](https://oi-wiki.org/ds/fenwick/)

## 5.11 DFS 序与子树展平

**1. 它是做什么的**

对一棵静态、连通无向树选定根后，DFS 序把每个节点的子树映射为连续闭区间 `[tin[u],tout[u]]`。因此可把子树查询或修改交给树状数组、线段树等区间结构。建序耗时 $O(n)$，辅助空间为 $O(n)$。本模板每个节点只记录一次，不是 LCA 常用的进入与回溯都记录的欧拉游程。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `g` | 1-based 无向邻接表。 |
| `timer` | 已进入 DFS 的节点数；每进入一个节点递增一次。 |
| `tin[u]` | 节点 `u` 的进入时间戳。 |
| `tout[u]` | `u` 子树遍历完成时的时间戳，与 `tin[u]` 构成闭区间。 |
| `order[t]` | DFS 时间戳 `t` 对应的节点编号，即 `order[tin[u]] == u`。 |
| `u`, `p` | 当前节点及父节点；根调用时父节点传 0。 |

两种映射用途不同：若要把每个节点的点值放进线段树或树状数组，应按 `tin[u]` 作为位置写入；若要逐个枚举子树节点，则遍历 `t=tin[u]..tout[u]`，并用 `order[t]` 取回节点编号。不能把时间戳 `t` 当成点编号。

例如边为 `1-2、1-3、2-4、2-5`，根为 1 且按邻接顺序访问时，`order` 为 `[1,2,4,5,3]`；节点 2 的区间 `[2,4]` 对应节点 2、4、5。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `DfsOrder(n)` | 分配图和序列数组；点编号范围为 `1..n`，应传正点数。 |
| `addEdge(u,v)` | 参数为合法树点编号；向 `g` 双向加入一条边，修改邻接表，无返回值；每条无向边只调用一次。 |
| `dfs(u,p)` | 从 `u` 开始遍历，写入 `tin`、`tout`、`order` 并增加 `timer`，无返回值；输入必须是树且不能形成递归环。根的 `p` 传 0，整张树由调用方指定根后调用一次。 |

**4. 怎么调用**

先构造对象并加入全部 `n-1` 条边，再从选定根调用 `dfs(root,0)`。之后点值按 `tin` 放入区间结构，或通过 `order` 枚举子树：

```text
DfsOrder d(5);
d.addEdge(1, 2); d.addEdge(1, 3);
d.addEdge(2, 4); d.addEdge(2, 5);
d.dfs(1, 0);
// tin[2]=2、tout[2]=4；order[2..4] 为 2,4,5
// 将点值 value[u] 写入序列位置 tin[u]；枚举子树 2 则读取 order[2..4]
```

原模板：

```cpp

struct DfsOrder {
    vector<vector<int>> g;
    vector<int> tin,tout,order;
    int timer=0;
    // 参数 n 为树点数；分配 1-based 图与 DFS 序数组，timer 初始为 0。
    explicit DfsOrder(int n)
        : g(n + 1), tin(n + 1), tout(n + 1), order(n + 1) {}
    // 参数 u、v 是 1..n 树点；返回 void，向 g 双向加入边；建 DFS 序前每条树边调用一次。
    void addEdge(int u, int v) {
        g[u].push_back(v);
        g[v].push_back(u);
    }
    // 参数 u 是当前子树根、p 是父点（根传 0）；返回 void，写 tin/tout/order/timer；输入须为树。
    void dfs(int u, int p) {
        // 进入时分配唯一时间戳，递归结束时的 timer 即子树最后一个时间戳。
        tin[u] = ++timer;
        order[timer] = u;
        for (int v : g[u]) {
            if (v != p) {
                dfs(v, u);
            }
        }
        tout[u] = timer;
    }
};
```

**5. 要改哪里**

- 更换根或重新计算 DFS 序：创建新对象，重新加入全部边，再调用 `dfs(newRoot,0)`。旧对象的 `timer` 和时间戳已被使用；不必在它上面清空图。
- 子树点值求和或更新：把 `value[u]` 放在位置 `tin[u]`，对闭区间 `[tin[u],tout[u]]` 操作。
- 需要枚举子树中的原节点编号：对 `t` 遍历该闭区间，再读取 `order[t]`。这是枚举映射，不等同于直接把 DFS 位置当作节点编号。
- 需要 LCA 的欧拉游程：另建会在进入及回溯时记录节点的序列，当前 `order` 每点只出现一次。

**6. 自检**

按示例树从根 1 遍历，应得到 `tin[1]=1`、`tin[2]=2`、`tin[4]=3`、`tin[5]=4`、`tin[3]=5`，并有 `tout[2]=4`。每个节点的 `tout[u]-tin[u]+1` 应等于其子树节点数；节点 2 的区间位置 `2..4` 映回节点应为 `2,4,5`。

**7. 坑**

- 把区间端点当半开区间：本模板的 `[tin,tout]` 两端都包含。
- 把 `order` 位置当作节点编号：应使用 `order[t]` 映回节点。
- 对一般图直接运行：代码只跳过父节点，没有 visited 标记；输入需为树。
- 重用已遍历对象：`timer` 和数组不会自动重置；重根或重新建序时新建对象并重新加边。

**8. 一句话原理**

DFS 完整遍历完一个节点的子树后才离开它，因此子树节点的进入时间连续排列。

## 5.12 树链剖分

**1. 它是做什么的**

树链剖分把一棵 1-based 连通无向树上两点间的路径拆成 $O(\log n)$ 个连续位置区间，供线段树等结构逐段处理。建树剖分耗时 $O(n)$、空间 $O(n)$；本模板的 `forPath` 产生 $O(\log n)$ 段。若每段在线段树上查询或更新一次，单次路径操作为 $O(\log^2 n)$。回调收到的区间端点闭合，但区间顺序不保证等于从 `u` 到 `v` 的路径顺序；可用于可交换聚合或各段独立更新。需要方向敏感的非交换运算时，必须额外记录方向并按路径顺序合并。

先看复杂度从哪里来：若沿树路径逐点向父亲走，最坏要访问 $O(n)$ 个点；DFS 序只能把子树展平，不能让任意路径成为单段。HLD 选最大子树孩子为重儿子，第二次 DFS 优先走它，使重链连续。沿路径向上跨一条轻边时，父点的子树规模至少是轻儿子子树规模的两倍；反向从父点走向轻儿子时，子树规模至少减半。因此每条根到点路径经过 $O(\log n)$ 条轻边，任意两点路径也只跨 $O(\log n)$ 条重链。

小例子：边为 `1-2,1-3,3-4,3-5`，以 1 为根，3 是 1 的重儿子，2 是轻儿子；若 4 被选为 3 的重儿子，重链为 `1-3-4`。查询 2 到 5 会得到覆盖点 2、1、3、5 的若干闭区间。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `g[u]` | 无向邻接表；通过 `addEdge` 加边，所有边必须在 `build` 前加入。 |
| `parent[u]`, `depth[u]` | 以指定根定根后的父节点和深度，根深度为默认初值 0。 |
| `sz[u]` | 以 `u` 为根的子树大小。 |
| `heavy[u]` | `u` 的最大子树孩子；无孩子时为 `-1`。 |
| `top[u]` | `u` 所在重链的链头。 |
| `pos[u]` | 剖分后的 1-based 连续位置；同一重链连续，子树也对应连续区间。 |
| `timer` | 分配 `pos` 时递增的全局位置计数器；对象构造时为 0，`build` 会重置。 |

点编号和剖分位置是两个不同维度：路径区间传给维护结构时使用 `pos`，建树时遍历点编号，令 `base[pos[u]]=weight[u]` 即可，不需要逆映射；若要从位置取回点编号，再另建 `vertexAt[pos[u]]=u`。

**3. 函数在做什么**

| 函数 | 参数、返回与作用 |
|---|---|
| `HLD(nodeCount)` | 分配 `1..nodeCount` 的邻接表和数组；点数应为正。 |
| `addEdge(u,v)` | 要求两个合法不同点；向邻接表双向加入一条边，须在 `build` 前且每条边只加一次。 |
| `dfs1(u,p)` | 内部递归，设置父亲、深度、子树大小及重儿子，返回子树大小；在合法树上由 `build` 调用。 |
| `dfs2(u,head)` | 内部递归，设置链头和位置，并优先遍历重儿子；无返回值。 |
| `build(root)` | 完成剖分；要求所有边已加入，`root` 在 `1..n`。会清空旧剖分数组并重建，要求输入仍为连通树；可重复调用或更换根。省略参数时根为 1。 |
| `forPath(u,v,use)` | 将路径拆成闭区间并逐段调用 `use(l,r)`；回调返回值被忽略，需通过捕获外部对象实现查询或更新。区间参数是剖分位置，次序不承诺对应原路径方向。 |

**4. 怎么调用**

用 `addEdge` 加完边，再调用 `build`；随后让 `forPath` 的回调把区间交给线段树。下例为链 `1-2-3`，路径查询得到的位置区间 `[1,3]`：

```text
HLD hld(3);
hld.addEdge(1, 2);
hld.addEdge(2, 3);
hld.build();
// l/r 为剖分位置闭区间；回调输出端点，不修改 hld。
hld.forPath(1, 3, [&](int l, int r) { cout << l << " " << r << "\n"; });
// 输出：1 3
```

模板代码如下：

```cpp

struct HLD {
    // heavy 子树最大者优先同链；任意树路径被拆成 O(log n) 个连续区间。
    int n, timer = 0;
    vector<vector<int>> g;
    vector<int> parent,depth,sz,heavy,top,pos;
    // nodeCount 为点数（须 >=1）；分配 1-based 邻接表和剖分数组，不修改调用方点权。
    explicit HLD(int nodeCount)
        : n(nodeCount), g(nodeCount + 1), parent(nodeCount + 1),
          depth(nodeCount + 1), sz(nodeCount + 1),
          heavy(nodeCount + 1, -1), top(nodeCount + 1), pos(nodeCount + 1) {
        assert(n >= 1);
    }
    // u、v 为 1..n 的树点；返回 void，向 g 双向加入一条边；必须在 build 前且每条边只加一次。
    void addEdge(int u, int v) {
        assert(1 <= u && u <= n && 1 <= v && v <= n && u != v);
        g[u].push_back(v);
        g[v].push_back(u);
    }
    // u 为当前子树根、p 为父点；返回子树大小，并写 parent/depth/sz/heavy；输入必须是树。
    int dfs1(int u, int p) {
        parent[u] = p;
        sz[u] = 1;
        heavy[u] = -1;
        int best = 0;
        for (int v : g[u]) {
            if (v == p) continue;
            depth[v] = depth[u] + 1;
            int sub = dfs1(v, u);
            sz[u] += sub;
            if (sub > best) {
                best = sub;
                heavy[u] = v;
            }
        }
        return sz[u];
    }
    // u 为子树根、head 为其链头；返回 void，按重儿子优先写 top/pos 并递增 timer。
    void dfs2(int u, int head) {
        top[u] = head;
        pos[u] = ++timer;
        if (heavy[u] != -1) dfs2(heavy[u], head);
        for (int v : g[u]) {
            if (v != parent[u] && v != heavy[u]) dfs2(v, v);
        }
    }
    // root 为 1..n 的定根；返回 void，清空旧剖分并重建所有数组；要求 g 是连通树。
    void build(int root = 1) {
        assert(1 <= root && root <= n);
        timer = 0;
        fill(parent.begin(), parent.end(), 0);
        fill(depth.begin(), depth.end(), 0);
        fill(sz.begin(), sz.end(), 0);
        fill(heavy.begin(), heavy.end(), -1);
        fill(top.begin(), top.end(), 0);
        fill(pos.begin(), pos.end(), 0);
        dfs1(root, 0);
        dfs2(root, root);
        assert(timer == n);
    }
    // u/v 为已 build 的树端点；use(l,r) 接收 1-based 闭区间且返回值被忽略；区间方向不保证，返回 void。
    template<class F>
    void forPath(int u, int v, F use) const {
        assert(1 <= u && u <= n && 1 <= v && v <= n);
        while (top[u] != top[v]) {
            if (depth[top[u]] < depth[top[v]]) swap(u, v);
            use(pos[top[u]], pos[u]);
            u = parent[top[u]];
        }
        if (depth[u] > depth[v]) swap(u, v);
        use(pos[u], pos[v]);
    }
};
```


若要实际查询点权路径和，先提供 5.7 节的 `SegmentTree`，再将点权放到剖分位置上。接着上面的三点链，在业务函数中继续写：

```text
vector<ll> weight = {0, 10, 20, 30}, base(4);
for (int u = 1; u <= 3; ++u) base[hld.pos[u]] = weight[u];
SegmentTree st(3);
st.build(base);
ll pathSum = 0;
// l/r 为剖分位置闭区间；将该段和累加到 pathSum，返回 void。
hld.forPath(1, 3, [&](int l, int r) { pathSum += st.rangeSum(l, r); });
// pathSum == 60
```

子树查询可直接使用 `[pos[u], pos[u]+sz[u]-1]`，同样交给数组维护结构处理。

**5. 要改哪里**

- 点权路径查询或更新：把回调区间 `[l,r]` 交给线段树处理，线段树下标使用 `pos`。
- 边权路径查询：约定每条边的权值放在较深端点对应的位置；当两个端点落在同一条链时，最终区间要从 `pos[LCA]+1` 开始，排除代表 LCA 的位置。跨链段的链头位置代表的是与父亲相连的边，应保留。
- 非交换聚合（如字符串拼接、矩阵乘法）：当前回调区间无方向信息且分段顺序不保证，需改写分解接口，同时维护从两端收集的区间和方向；不能直接按回调顺序合并。
- 多测或更换根：边加入后可再次调用 `build(root)`；它会清空并重建剖分数组。外部线段树也须按新 `pos` 重排。

区分模型：路径加、路径和或路径最值通常使用 HLD 加线段树；只有子树操作时 DFS 序更简单。路径上的字符串拼接、矩阵乘法等不可交换操作，需要记录每段方向并按原路径顺序合并，当前 `forPath` 不提供方向。

**6. 自检**

在链 `1-2-3` 上构建后，`forPath(1,3,...)` 应只回调一次，区间为 `[1,3]`；`forPath(2,2,...)` 应得到单点区间。再用树 `1-2, 1-3` 测 `forPath(2,3,...)`，回调区间覆盖点 2、1、3 对应的位置，不能遗漏 LCA。边权版本还要确认同链查询排除了 LCA 的位置。

**7. 坑**

- 结果像用了旧树：在加完边之前调用了 `build`；先完整建图再剖分。
- 深链上递归深度可达 $n$，栈不足时需将两次 DFS 改为显式栈。
- 重建后外部权值看似错乱：`build` 会改变 `pos`，需按新位置重建外部维护结构。
- 路径和/最值适用、路径拼接错误：回调区间顺序不保证路径方向；方向敏感操作需同时维护区间方向和两端的合并顺序。
- 边权答案多一条或少一条：最终同链段包含 LCA；将该段左端改为 `pos[LCA]+1`。

**8. 一句话原理**

最大子树孩子优先进入同一条链；每次跨轻边时子树规模至少减半，所以任一路径只跨 $O(\log n)$ 条链，每条链映射成连续区间。

## 5.13 线段树：区间加、赋值与求和

**1. 它是做什么的**

`AssignAddSegmentTree` 在长度为 `n` 的 1-based 数组上支持三种操作：把闭区间每项加上一个值、把闭区间每项设成同一个值、查询闭区间和。适合两种更新交错出现的场景；数组值、区间和及乘积必须能放进 `long long`。

构造节点空间为 $O(n)$，调用 `build` 初始化为 $O(n)$；一次区间加、区间赋值或区间求和均为 $O(\log n)$；空间为 $O(n)$，节点数组约为 `4n`。要求 `n>=1`，公开操作的区间须满足 `1<=l<=r<=n`，接口不检查这些条件。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `n` | 数组长度；位置从 1 到 `n`。 |
| `tr[p].sum` | 节点 `p` 管辖区间的当前总和，包含本节点尚未下传的更新效果。 |
| `tr[p].hasSet` | 是否存在等待下传的赋值操作；赋值为 0 时也必须为真。 |
| `tr[p].setValue` | `hasSet` 为真时，表示该节点区间每项待赋成的值。 |
| `tr[p].add` | 独立的待下传增量；若赋值标记存在，之后的增量会合并进 `setValue`，不另存此标记。 |
| `p,l,r` | 递归内部的节点编号和它管理的闭区间。 |
| `ql,qr` | 更新或查询目标闭区间；所有接口采用 1-based 下标。 |
| `assign` | 内部更新参数；真表示赋值，假表示加法。公开接口会替调用者设置它。 |

标记表示对整段尚未传给孩子的操作。组合顺序遵循时间先后：新赋值会覆盖旧赋值和旧加法；有赋值标记时再加 `delta`，应把 `delta` 加到待赋值数上；没有赋值标记时，加法累积在 `add` 中。向下传递时先赋值，再加法。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及调用条件 |
|---|---|---|
| `AssignAddSegmentTree(size)` | 正数组长度；构造对象。 | 创建初值为零、无标记的节点空间。 |
| `build(a)` | 1-based 初值 `a[1..n]`；返回 `void`。 | 仅初始化 `sum`，不清懒标记；在新对象上调用，重置需重新构造。 |
| 内部 `build(p,l,r,a)` | 初值和当前区间；返回 `void`。 | 递归写叶值并合并区间和，不重置标记；无需直接调用。 |
| `applySet(p,l,r,value)` | 当前节点和赋值值；返回 `void`。 | 更新区间和，设置赋值标记并清除加法标记。 |
| `applyAdd(p,l,r,delta)` | 当前节点和增量；返回 `void`。 | 更新区间和；依据是否已有赋值标记，把增量合并到赋值值或独立加法标记。 |
| `push(p,l,r)` | 当前节点及闭区间；返回 `void`。 | 先把赋值、再把加法下传到左右孩子，并清除父标记；内部调用。 |
| `rangeAdd(l,r,value)` | 合法闭区间和增量；返回 `void`。 | 将每个区间元素增加 `value`。 |
| `rangeSet(l,r,value)` | 合法闭区间和赋值值；返回 `void`。 | 将每个区间元素覆盖为 `value`，包括 0。 |
| `rangeSum(l,r)` | 合法闭区间；返回 `long long`。 | 返回区间和；部分查询可能下传标记。 |
| 内部 `update` / `query` | 当前节点、目标区间和操作参数；更新返回 `void`，查询返回区间和。 | 递归处理；通常使用上述公开接口，不直接调用。 |

**4. 怎么调用**

构造正长度的新对象；若有非零初值，准备 `a[1..n]` 并调用一次 `build(a)`。之后按需要调用 `rangeSet`、`rangeAdd` 和 `rangeSum`。模板如下：

```cpp

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct AssignAddSegmentTree {
    struct Node {
        ll sum = 0;
        ll add = 0;
        ll setValue = 0;
        bool hasSet = false; // 赋值为 0 也有效，不能用 setValue==0 表示“无标记”
    };
    int n;
    vector<Node> tr;

    // 参数 size 为正数组长度；分配初始零值节点，标记均无效。
    explicit AssignAddSegmentTree(int size) : n(size), tr(4 * size + 4) {}

    // 参数 p 管理闭区间 [l,r]、value 为赋值；返回 void，覆盖该节点和并设置赋值标记。
    void applySet(int p, int l, int r, ll value) {
        // 覆盖整个节点：清除旧加法，并留下待下传的赋值。
        tr[p].sum = value * (r - l + 1);
        tr[p].setValue = value;
        tr[p].add = 0;
        tr[p].hasSet = true;
    }
    // 参数 p 管理闭区间 [l,r]、delta 为增量；返回 void，修改该节点和并合并加法/赋值标记。
    void applyAdd(int p, int l, int r, ll delta) {
        tr[p].sum += delta * (r - l + 1);
        // 赋值标记仍在时把增量合并到赋值值，否则累积为独立加法标记。
        if (tr[p].hasSet) tr[p].setValue += delta;
        else tr[p].add += delta;
    }
    // 参数 p 管理闭区间 [l,r]；返回 void，按赋值后加法顺序下传标记并清理父标记。
    void push(int p, int l, int r) {
        if (l == r) return;
        int m = (l + r) / 2;
        // 操作顺序必须是先赋值后加法，才能保持时间顺序。
        if (tr[p].hasSet) {
            applySet(p * 2, l, m, tr[p].setValue);
            applySet(p * 2 + 1, m + 1, r, tr[p].setValue);
            tr[p].hasSet = false;
        }
        if (tr[p].add != 0) {
            applyAdd(p * 2, l, m, tr[p].add);
            applyAdd(p * 2 + 1, m + 1, r, tr[p].add);
            tr[p].add = 0;
        }
    }
    // 参数 a 为 1-based 初值，p 管理闭区间 [l,r]；返回 void，递归建立节点和。
    void build(int p, int l, int r, const vector<ll>& a) {
        if (l == r) {
            tr[p].sum = a[l];
            return;
        }
        int m = (l + r) / 2;
        build(p * 2, l, m, a);
        build(p * 2 + 1, m + 1, r, a);
        tr[p].sum = tr[p * 2].sum + tr[p * 2 + 1].sum;
    }
    // 参数 a[1..n] 为初值；返回 void，只建立节点和、不清懒标记；须在新对象上初始化，重置需重新构造对象。
    void build(const vector<ll>& a) { build(1, 1, n, a); }

    // 参数 p/l/r 为当前节点，ql/qr 为合法修改区间，value 为操作值、assign 选择赋值或加法；返回 void 并更新节点。
    void update(int p, int l, int r, int ql, int qr, ll value, bool assign) {
        if (ql <= l && r <= qr) {
            if (assign) applySet(p, l, r, value);
            else applyAdd(p, l, r, value);
            return;
        }
        push(p, l, r);
        int m = (l + r) / 2;
        if (ql <= m) update(p * 2, l, m, ql, qr, value, assign);
        if (qr > m) update(p * 2 + 1, m + 1, r, ql, qr, value, assign);
        tr[p].sum = tr[p * 2].sum + tr[p * 2 + 1].sum;
    }
    // 参数为合法闭区间及增量；返回 void，将区间每项增加 value 并修改树状态。
    void rangeAdd(int l, int r, ll value) { update(1, 1, n, l, r, value, false); }
    // 参数为合法闭区间及赋值；返回 void，将区间每项设为 value 并修改树状态。
    void rangeSet(int l, int r, ll value) { update(1, 1, n, l, r, value, true); }

    // 参数 p/l/r 为当前节点，ql/qr 为合法查询区间；返回交集和，并可能下传懒标记。
    ll query(int p, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return tr[p].sum;
        push(p, l, r);
        int m = (l + r) / 2;
        ll result = 0;
        if (ql <= m) result += query(p * 2, l, m, ql, qr);
        if (qr > m) result += query(p * 2 + 1, m + 1, r, ql, qr);
        return result;
    }
    // 参数为合法闭区间；返回区间和，查询可能下传内部标记。
    ll rangeSum(int l, int r) { return query(1, 1, n, l, r); }
};
```

片段可放在业务函数内。初值 `[1,2,3,4,5]`，先将 `[2,4]` 赋成 `7`，再给 `[3,5]` 加 `2`，数组变成 `[1,7,9,9,7]`，`rangeSum(2,5)` 返回 `32`：

```text
vector<ll> a = {0, 1, 2, 3, 4, 5};
AssignAddSegmentTree st(5);
st.build(a);
st.rangeSet(2, 4, 7);
st.rangeAdd(3, 5, 2);
ll answer = st.rangeSum(2, 5); // 32
```

**5. 要改哪里**

- 单点操作用 `[i,i]` 区间即可，例如 `rangeSet(i,i,v)` 或 `rangeAdd(i,i,d)`。
- 若只需要区间加与区间和，可使用更简单的 5.7 节模板；若还需要区间最值，须重新设计节点聚合和更新逻辑。
- 要增加新的更新类型，须定义其对 `sum` 的影响、懒标记的存法，以及它与现有赋值和加法标记的时间顺序组合；不能只增加一个接口函数。
- 初始数组全零时，构造后的逻辑值已为零，可跳过 `build`。非零初值需在新对象上构建。多测重置或重复初始化时重新构造对象，因为 `build` 不会清理旧标记。
- `n` 必须为正数，区间须合法；实现不做边界检查。还需保证所有中间乘法和区间和不溢出 `long long`。

**6. 自检**

对初值 `[1,2,3,4,5]`，先 `rangeSet(2,4,7)` 后为 `[1,7,7,7,5]`；再 `rangeAdd(3,5,2)` 后为 `[1,7,9,9,7]`，全数组和为 33，`rangeSum(2,5)` 为 32。再把 `[1,5]` 赋为 0，查询 `[1,5]` 必须得到 0，这能检查“赋值为零”由 `hasSet` 区分的行为。单元素数组 `[6]` 执行加 `-2` 后查询得 4；随后赋值 0 得 0。

**7. 坑**

1. 用 `setValue==0` 判断是否有赋值标记；0 是合法赋值，必须看 `hasSet`。
2. 有待下传赋值时仍把新加法记入独立 `add`；本实现将它合并到 `setValue`，保证时间顺序正确。
3. 下传时先加后赋值，会把较新的加法覆盖掉；应先下传赋值，再下传加法。
4. 用 `build` 重建一个已操作的对象；该函数只写节点和、不清标记，应重新构造对象后初始化。
5. 更新或查询越界、使用 0-based 区间；公开接口无边界保护，必须传入合法 1-based 闭区间。

**8. 一句话原理**

线段树用赋值标记表达覆盖、用加法标记表达增量，并按操作发生顺序合并和下传，从而在对数时间内维护区间和。

## 5.14 DSU on Tree（树上启发式合并）

**1. 它是做什么的**

给定一棵静态有根树和每个节点的颜色，本模板一次求出所有节点子树中的不同颜色数。颜色可以是负数或很大的整数，模板会先离散化。输入是 1-based 连通无向树 `tree`、颜色数组 `color[1..n]` 和根 `root`；`solve()` 返回长度 `n+1` 的数组，`answer[u]` 是节点 `u` 的子树答案，0 号位不用。

朴素地为每个点单独 DFS 其子树，一条链会扫描 $n+(n-1)+\cdots=O(n^2)$ 个节点；仅把子树展平为区间并不能消除重复扫描。DSU on Tree 的关键是保留最大子树的统计表，轻子树算完答案后清空，稍后再作为轻子树重新加入。每条轻边都会让子树规模至少翻倍，因此每个节点最多重新加入 $O(\log n)$ 次。 DSU on Tree 负责安排哪些节点加入或移出当前集合，桶、树状数组或线段树负责维护集合里的统计。本模板用颜色频次桶统计不同颜色数。它与普通并查集不同：这里没有合并集合代表元的操作，保留的是重儿子已经算好的频次状态。适合离线回答固定根下的子树统计，不直接支持在线改色、动态换根或路径查询。

预处理 DFS 序为 $O(n)$，颜色排序与压缩为 $O(n\log n)$。统计中节点的加入、删除共 $O(n\log n)$ 次；本模板每次频次变化为 $O(1)$，所以总时间为 $O(n\log n)$、额外空间为 $O(n)$，包括递归栈。若改用每次增删为 $O(\log n)$ 的统计结构，统计总时间就会变成 $O(n\log^2 n)$。这些界限还要求每个节点的答案能在对应代价内读出。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `tree`、`color` | 输入树和颜色的常量引用；被引用对象必须比求解器活得更久。 |
| `n`、`root` | 节点数与固定根；要求 `n>=1`、`1<=root<=n`。 |
| `parent[u]`、`subtreeSize[u]` | 定根后的父节点与子树大小。 |
| `heavy[u]` | 子树最大的那个儿子；叶子为 0。大小并列时选最先遇到的一个即可。 |
| `tin[u]`、`tout[u]` | 子树在 DFS 序上的闭区间 `[tin[u],tout[u]]`。 |
| `order[i]` | DFS 位置 `i` 对应的节点编号，满足 `order[tin[u]]==u`。 |
| `compressed[u]` | 节点 `u` 的颜色编号，范围为 `0..颜色种类数-1`。 |
| `frequency[c]`、`distinct` | 当前活跃集合中颜色编号 `c` 的次数，以及次数非零的颜色数。 |
| `answer[u]`、`timer` | 各子树答案，以及预处理时分配 DFS 位置的计数器。 |
| `keep` | 当前子树算完后是否保留频次；不是永久标记，也不表示跳过该子树。 |

例如边按 `1-2、1-3、2-4、2-5` 加入，根为 1，DFS 顺序是 `order[1..5]=[1,2,4,5,3]`。子树 2 对应位置 `[2,4]`，映回节点是 `{2,4,5}`。枚举它时先取 `order[i]`，再读该节点颜色；不能把位置 `i` 直接当节点号。

统计结构的下标由统计维度决定：这里是 `frequency[compressed[u]]`；若按深度计数，则用深度作桶或线段树的下标。只有维护“DFS 位置上的点值”时才把 `tin[u]` 用作线段树位置，不能把所有统计都套到 DFS 下标上。

**3. 函数在做什么**

| 函数 | 参数、返回与作用 |
|---|---|
| `DSUOnTree(tree,color,root)` | 保存输入引用并分配内部数组；树必须连通无环，颜色数组覆盖 `1..n`，构造时不修改输入。 |
| `prepare(u,p)` | 内部预处理；`u` 是当前点，`p` 是父点，根传 0；返回子树大小，并写父节点、DFS 区间和重儿子。 |
| `build()` | 无参数、无返回值；清空旧预处理状态，再以 `root` 建立 DFS 序等信息。只做结构预处理，不初始化频次。 |
| `changeColor(x,delta)` | 内部把节点 `x` 的颜色次数增减 1，`delta` 为 `+1/-1`；无返回值，修改频次和 `distinct`。压缩与频次数组须已就绪，删除的是当前集合中已有的节点贡献。 |
| `addSubtree(u,add)` | 内部枚举 `[tin[u],tout[u]]`，`add=true` 加入、`false` 移除；无返回值，修改频次状态，依赖预处理与频次初始化。 |
| `dfs(u,p,keep)` | 内部统计；记录 `u` 子树答案，`keep=true` 保留贡献，`false` 则移除；无返回值，修改答案与活跃集合。只应由 `solve()` 从空状态启动。 |
| `solve()` | 无参数；重新预处理、压缩颜色、清空频次后计算全部答案，返回 `vector<int>`；不修改输入，允许重复调用。 |

业务代码只需构造对象并调用 `solve()`。内部过程在计算 `u` 的答案时按以下顺序执行：

1. 递归处理所有轻儿子，传 `keep=false`；各自记下答案后清空，避免污染兄弟子树。
2. 递归处理重儿子，传 `keep=true`；保留它的整棵子树贡献。
3. 枚举每棵轻子树重新加入，再加入 `u` 自己；重子树已经在集合中，不能再加一次。
4. 此时活跃集合恰好是 `u` 的子树，令 `answer[u]=distinct`。
5. 若本层 `keep=false`，移除 `u` 整棵子树；否则保留给父层继续用。

在上述五点树中，颜色设为 `[3,3,5,5,3]`。根的轻儿子 3 先得到答案 1 后清空。处理重儿子 2 时，先算轻儿子 5 并清空，再保留重儿子 4 的颜色 5；重新加入节点 5 的颜色 3 和节点 2 的颜色 3 后，频次为 `{3:2,5:1}`，得到 `answer[2]=2`。回到根，再加入节点 3 和根，频次为 `{3:3,5:2}`，得到 `answer[1]=2`。

**4. 怎么调用**

先准备树和颜色，再构造求解器。以下模板统计不同颜色数，无需额外接线段树：

```cpp

#include <bits/stdc++.h>
using namespace std;

struct DSUOnTree {
    int n, root;
    const vector<vector<int>>& tree;
    const vector<int>& color;
    vector<int> compressed, parent, subtreeSize, heavy;
    vector<int> tin, tout, order, frequency, answer;
    int timer = 0, distinct = 0;

    // 输入 tree 为 1-based 连通无向树，color[1..n] 为任意整数颜色；引用对象须长于本对象。
    // 初始化数组；不修改 tree 或 color。要求 n>=1 且 root 在 1..n。
    DSUOnTree(const vector<vector<int>>& tree, const vector<int>& color, int root)
        : n((int)tree.size() - 1), root(root), tree(tree), color(color),
          compressed(n + 1), parent(n + 1), subtreeSize(n + 1), heavy(n + 1, 0),
          tin(n + 1), tout(n + 1), order(n + 1), answer(n + 1) {}

    // 对 u 子树做一次 DFS 序展平，计算 parent、子树大小和最大子树的重儿子；返回 subtreeSize[u]。
    // p 是 u 的父节点，根调用时 p=0；写入内部预处理数组，不改变输入树。
    int prepare(int u, int p) {
        parent[u] = p;
        subtreeSize[u] = 1;
        tin[u] = ++timer;
        order[timer] = u;
        int largest = 0;
        for (int v : tree[u]) {
            if (v == p) continue;
            int childSize = prepare(v, u);
            subtreeSize[u] += childSize;
            if (childSize > largest) {
                largest = childSize;
                heavy[u] = v;
            }
        }
        tout[u] = timer;
        return subtreeSize[u];
    }

    // 无参数；重新以 root 为根建立 DFS 序区间、父节点、子树大小和重儿子信息；清空旧预处理数组，不修改输入树。
    // 仅完成结构预处理；颜色频次要由 solve() 初始化后才能用于 dfs() 统计。
    void build() {
        timer = 0;
        fill(parent.begin(), parent.end(), 0);
        fill(subtreeSize.begin(), subtreeSize.end(), 0);
        fill(heavy.begin(), heavy.end(), 0);
        fill(tin.begin(), tin.end(), 0);
        fill(tout.begin(), tout.end(), 0);
        prepare(root, 0);
    }

    // 将节点 x 的颜色频次增加 delta（+1 或 -1）；更新 distinct，保持频次非负。
    // x 是 1..n 点号；只修改内部 frequency/distinct。
    void changeColor(int x, int delta) {
        int id = compressed[x];
        if (frequency[id] == 0 && delta == 1) ++distinct;
        frequency[id] += delta;
        if (frequency[id] == 0 && delta == -1) --distinct;
    }

    // 将以 u 为根的整棵子树加入当前频次表或移除；add=true 表示加入。
    // u 必须已由 prepare 建立 DFS 区间；只修改内部频次状态。
    void addSubtree(int u, bool add) {
        int delta = add ? 1 : -1;
        for (int i = tin[u]; i <= tout[u]; ++i) changeColor(order[i], delta);
    }

    // 处理 u 子树；keep=true 时保留该子树颜色频次供父层合并，false 时清空。
    // p 为父节点；结束时 answer[u] 是子树 distinct 数，频次表依 keep 决定是否保留。
    void dfs(int u, int p, bool keep) {
        for (int v : tree[u]) {
            if (v != p && v != heavy[u]) dfs(v, u, false);
        }
        if (heavy[u] != 0) dfs(heavy[u], u, true);
        for (int v : tree[u]) {
            if (v != p && v != heavy[u]) addSubtree(v, true);
        }
        changeColor(u, 1);
        answer[u] = distinct;
        if (!keep) addSubtree(u, false);
    }

    // 重新预处理并计算所有子树答案；每次调用都会清空并重建结果，允许安全重复调用。
    // 返回 n+1 长度数组，answer[0] 不使用；不修改输入 tree/color。
    vector<int> solve() {
        build();
        fill(answer.begin(), answer.end(), 0);

        vector<int> values(color.begin() + 1, color.begin() + n + 1);
        sort(values.begin(), values.end());
        values.erase(unique(values.begin(), values.end()), values.end());
        for (int u = 1; u <= n; ++u) {
            compressed[u] = lower_bound(values.begin(), values.end(), color[u]) - values.begin();
        }
        frequency.assign(values.size(), 0);
        distinct = 0;
        dfs(root, 0, true);
        return answer;
    }
};

// 示例：tree 为 1-based 无向邻接表，color[1..n] 可使用任意整数；答案按点号读取。
// DSUOnTree solver(tree, color, 1); vector<int> distinct = solver.solve();
```

下面片段可放入业务函数。注意输入数组的生命周期要覆盖 `solver.solve()`：

```text
vector<vector<int>> tree(6);
// u/v 为 1..5 的树点；向捕获的 tree 双向加边，返回 void。
auto addEdge = [&](int u, int v) {
    tree[u].push_back(v);
    tree[v].push_back(u);
};
addEdge(1, 2); addEdge(1, 3);
addEdge(2, 4); addEdge(2, 5);
vector<int> color = {0, 3, 3, 5, 5, 3};
DSUOnTree solver(tree, color, 1);
vector<int> answer = solver.solve();
// answer 为 {0, 2, 2, 1, 1, 1}，0 号位不使用
```

**5. 要改哪里**

| 需求 | 改动 |
|---|---|
| 换成颜色次数、众数等统计 | 改 `changeColor` 的状态维护与 `answer[u]` 的读取方式；不同颜色数的加减规则不能直接当作众数维护。 |
| 按深度或权值统计 | 将统计键改为深度或权值，调整离散化和桶/树的容量；DFS 序仍只负责枚举节点。 |
| 换成线段树维护频次 | 在节点增删时更新对应统计键的叶子，重算单次增删和读答案的代价；不把总时间一律写成 $O(n\log n)$。 |
| 换根或多组数据 | 为新根/新数据构造对象后运行 `solve()`；同一输入上重复 `solve()` 也会完整清空并重算。 |
| 维护子树内部边权 | 可将边放在较深端点上，但对 `u` 子树应排除连接 `u` 与父亲的那条边；不能把原点权统计原样套过去。 |
| 深链数据 | 递归深度可达 `n`；栈不足时需将预处理和统计遍历改为显式栈。 |

扩展到子树众数时，需同步改变加入、删除和答案读取。若只要求最高频率，可维护 `frequency[color]`、`countAtFrequency[f]` 和 `bestFrequency`：加入时更新频率桶并可能提高最大频率，删除时减少桶计数并在最高频率桶为空时向下移动。`keep=false` 仍须逐节点撤销。若还要并列时最小颜色，可对每个频率维护有序集合，操作增加 $O(\log n)$ 因子。只求最高频率时频率桶可均摊 $O(1)$。众数扩展不适用于在线改色或路径众数。

模型识别：静态树、每个点都要回答一个子树统计，且统计可以由频率表增删维护时考虑 DSU on Tree；少数子树区间查询可考虑 DFS 序加离线树状数组，在线修改则考虑动态结构。


**6. 自检**

用上述五点树检查 `order[tin[u]]==u`、`tout[u]-tin[u]+1==subtreeSize[u]`，以及 `heavy[u]` 是否为最大子树的孩子。答案应为 `[2,2,1,1,1]`；若所有颜色相同则每个答案都为 1，若各节点颜色不同则 `answer[u]==subtreeSize[u]`。单点树答案为 1；负颜色、大颜色经压缩后仍应满足这些规律。连续调用两次 `solve()`，结果必须相同。

调试时在 `dfs` 的 `keep=false` 分支结束后，检查本次子树贡献已清除；按此框架调用时应回到空频次状态，`distinct==0`。保留分支返回时，频次则恰好描述该子树。不要在重儿子返回后把全局频次清零。

**7. 坑**

- 子树统计像用了别的节点：把 DFS 位置当成节点号；必须通过 `order[i]` 映回节点，再查 `compressed`。
- 兄弟子树的答案偏大：轻子树处理后未完整删除；检查 `keep=false` 分支及所有统计变量的清理规则。
- 重子树频次翻倍：保留后又加入了一次；父层只重新枚举轻子树。
- 颜色越界：直接用原始负颜色或大颜色作桶下标；使用离散化编号。
- 改统计量后清空出错：新的状态未必能仅靠减频次还原；增删和清空必须成套设计，不能只替换取答案的一行。

**8. 一句话原理**

保留最大子树的状态，只重扫轻子树；沿轻边子树大小至少减半，因此每个节点只被反复加入、删除 $O(\log n)$ 次。

## 5.15 单点修改线段树与自定义合并 {#point-segment-tree-custom-merge}

**1. 它是做什么的**

这棵迭代线段树维护固定长度的非空 1-based 序列，支持单点替换和闭区间聚合。合并器 `merge` 必须满足结合律，并有左右两侧都成立的单位元 `identity`；合并器还必须能在 `rangeQuery` 的 `const` 函数中调用。构造时间为 $O(n)$，单点修改和区间查询各需 $O(\log n)$ 次合并，空间为 $O(n)$；这里按摘要的复制、存储和一次 `merge` 均为 $O(1)$ 计；若摘要或合并本身更昂贵，需乘上对应代价。它不支持非结合操作，也没有懒标记，不能直接执行区间更新。

示例用仿射函数 `f(x)=ax+b (mod MOD)` 作摘要。区间元素按下标从左到右依次作用，所以合并 `[left,right]` 时结果是 `right ∘ left`。模板保留查询区间的原始顺序，因而也能处理这种不满足交换律的合并。

**2. 变量在做什么**

| 变量 | 含义 |
|---|---|
| `n` | 序列元素个数；输入的有效元素位于 `initial[1..n]`。 |
| `tree` | 长度 `2*n` 的紧凑迭代树；叶子 `tree[n+i-1]` 对应原位置 `i`，内部节点合并左右孩子的摘要；非二次幂长度时，部分内部节点不对应原数组上的连续区间。 |
| `identity` | `merge` 的双侧单位元，用于查询左右累积器的初值；示例中为恒等仿射函数。 |
| `merge` | 用户提供的结合合并操作；参数顺序有意义，必须可在常量查询中调用。 |
| `leftResult`, `rightResult` | 查询期间分别从区间左侧和右侧累积摘要，最后按 `leftResult` 在前、`rightResult` 在后的次序合并。 |
| `Affine{a,b}` | 仿射摘要，表示模 `MOD` 下的函数 `a*x+b`，系数存为 `[0,MOD)`。 |

输入及查询端点都是 1-based 闭区间；`rangeQuery(l,r)` 要求 `1 <= l <= r <= n`。非二次幂长度时，紧凑树的 `tree[1]` 不一定代表原序列整体，需用 `rangeQuery(1,n)` 查询整段。

**3. 函数在做什么**

| 函数 | 参数、返回与作用 |
|---|---|
| `PointSegmentTree(initial, identity, merge)` | 复制 `initial[1..n]`，建立树；`initial` 必须非空且为 1-based，构造器用 `assert` 检查 `n>=1`。单位元和合并器需匹配且满足结合律。 |
| `pointSet(pos,value)` | 把位置 `pos` 替换为 `value`，重算叶子到根的摘要；要求 `1<=pos<=n`，无返回值。 |
| `rangeQuery(l,r)` | 返回闭区间 `[l,r]` 按原下标次序合并的摘要；要求合法非空区间，不修改树。 |
| `normalizeMod(x)` | 将任意 `long long` 规范到 `[0,MOD)`。 |
| `ComposeAffine::operator()(left,right)` | 返回先执行 `left` 再执行 `right` 的 `right∘left`；两输入系数应已规范化。 |
| `makeAffine(a,b)` | 建立 `a*x+b`，并将系数规范到 `[0,MOD)`。 |
| `affineExample()` | 演示初始化、点替换、区间查询和代入；返回最终模值。 |

**4. 怎么调用**

准备 1-based 的初始摘要、符合代数条件的合并器和单位元，构造后调用 `pointSet` / `rangeQuery`。示例中点 2 被替换为 `7x+2`，区间组合为 `70x+51`；代入 `x=11` 得到 `821`：

```text
ll result = affineExample();
// result == 821
```

模板代码如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

template<class T, class Merge>
struct PointSegmentTree {
    int n;
    T identity;
    Merge merge;
    vector<T> tree;

    // initial 为 1-based 非空序列，identity 是 merge 的双侧单位元，merge 满足结合律；复制到内部树并建树，不修改入参。
    explicit PointSegmentTree(const vector<T>& initial, T identity, Merge merge)
        : n((int)initial.size() - 1), identity(identity), merge(merge), tree(2 * n, identity) {
        assert(n >= 1);
        for (int i = 1; i <= n; ++i) tree[n + i - 1] = initial[i];
        for (int i = n - 1; i >= 1; --i) tree[i] = this->merge(tree[i << 1], tree[i << 1 | 1]);
    }

    // pos 为 1..n 的位置，value 是替换后的元素；返回 void，更新叶子及其祖先摘要，不改其他位置。
    void pointSet(int pos, const T& value) {
        int p = n + pos - 1;
        tree[p] = value;
        while (p > 1) {
            p >>= 1;
            tree[p] = merge(tree[p << 1], tree[p << 1 | 1]);
        }
    }

    // l、r 为 1-based 闭区间且 1<=l<=r<=n；返回按原序聚合的摘要，不修改树。
    T rangeQuery(int l, int r) const {
        int left = l + n - 1, right = r + n;
        T leftResult = identity, rightResult = identity;
        while (left < right) {
            if (left & 1) leftResult = merge(leftResult, tree[left++]);
            if (right & 1) rightResult = merge(tree[--right], rightResult);
            left >>= 1;
            right >>= 1;
        }
        return merge(leftResult, rightResult);
    }
};

constexpr ll MOD = 1000000007;

// x 为任意 long long；返回模 MOD 的 [0,MOD) 代表元。
ll normalizeMod(ll x) {
    x %= MOD;
    if (x < 0) x += MOD;
    return x;
}

struct Affine {
    ll a, b;
};

struct ComposeAffine {
    // left、right 的系数均已归一化；返回先执行 left 再执行 right 的复合 right∘left。
    Affine operator()(const Affine& left, const Affine& right) const {
        return {right.a * left.a % MOD,
                (right.a * left.b + right.b) % MOD};
    }
};

// 原始系数可为任意 long long；返回系数归一化后的 f(x)=ax+b。
Affine makeAffine(ll a, ll b) {
    return {normalizeMod(a), normalizeMod(b)};
}

// 示范仿射函数的顺序组合与点替换；仅修改本地线段树，返回区间函数作用于 x 的结果。
ll affineExample() {
    vector<Affine> functions(4);
    functions[1] = makeAffine(2, 1);
    functions[2] = makeAffine(3, 4);
    functions[3] = makeAffine(5, 6);
    PointSegmentTree<Affine, ComposeAffine> st(functions, makeAffine(1, 0), ComposeAffine{});
    st.pointSet(2, makeAffine(7, 2));
    Affine combined = st.rangeQuery(1, 3);
    ll x = normalizeMod(11);
    return (combined.a * x + combined.b) % MOD;
}
```

**5. 要改哪里**

- 维护区间和、最大值等摘要时，替换 `T`、`identity` 和 `merge`，并确保 `merge` 结合、`identity` 左右两侧均为单位元。最小值的单位元须不小于所有可能输入的值（如该类型的最大值），不能随意取 0。
- 维护非交换摘要时，严格保留“左段在前、右段在后”的合并顺序；不要交换 `merge(left,right)` 参数，也不要只用一个累积器改写查询。
- 仿射函数的作用顺序若改为从右向左，应同步重定义合并器和示例的区间语义，不能只交换说明。
- 增加区间修改需要引入懒标记及其与摘要的作用规则，当前模板没有这部分能力，应按操作重新设计。

**6. 自检**

示例的三项初值是 `2x+1`、`3x+4`、`5x+6`；将第二项替换为 `7x+2` 后，按顺序复合得到 `5(7(2x+1)+2)+6 = 70x+51`，代入 11 为 821。可分别检查单点区间、全区间和修改后查询；再用非二次幂长度（如 `n=3`）核对 `rangeQuery(1,n)`，不要把 `tree[1]` 当成全序列结果。

**7. 坑**

- 部分区间结果顺序反了：非交换合并时，右侧累积器必须用新块放在已有结果左侧；本模板通过 `merge(tree[--right], rightResult)` 保持顺序。
- 更新后结果异常：合并规则不满足结合律或单位元不匹配，线段树分组将改变结果。
- 整段查询拿错：`n` 非二次幂时 `tree[1]` 不是原序列整体摘要；使用 `rangeQuery(1,n)`。
- 下标越界或访问空叶子：接口按 1-based 编号且要求非空序列；构造输入的 `initial[0]` 不使用，查询端点须合法。

**8. 一句话原理**

每个节点保存其左段再接右段的摘要，单点替换后沿祖先重算，查询时按原序合并覆盖区间的节点。

## 5.16 启发式合并（Small-to-Large） {#small-to-large}

**1. 它是做什么的**

树上每个点有一个颜色，想知道每个点的子树里有几种颜色。比如父点有颜色 5，两个孩子分别是 5 和 8，那么父点子树的颜色集合是 `{5,8}`，答案为 2。

朴素做法是每个点都重新遍历整棵子树并收集颜色。链状树中，大量点会反复收集几乎相同的节点，工作量很大。

可以让孩子先收好自己的颜色，再把较小的一袋颜色加入较大的一袋。相同颜色只保留一份；合并完成后，大袋就代表父点整棵子树。

**2. 变量在做什么**

这里有两个容易混淆的量：集合里有多少种颜色，和这袋颜色来自多少个树节点。比如 `{5,5}` 去重后只有一种颜色，但它代表两个节点。模板用颜色集合回答题目，用节点数 `mass` 决定哪一边较小；不能拿不同颜色数代替 `mass`。

| 名称 | 含义 |
|---|---|
| `Bag::values` | 当前子树的颜色集合，使用 `set<int>` 去重；所有权由 `unique_ptr` 独占。 |
| `Bag::mass` | 当前子树包含的节点数，用于选定较小容器；不能用不同颜色数替代。 |
| `n`, `root` | 输入树点数与固定根；点号为 `1..n`。 |
| `tree`, `color` | 输入树及颜色的常量引用；必须比对象活得更久。 |
| `answer[u]` | 根为 `u` 的子树不同颜色数；0 号位不用。 |

**3. 函数在做什么**

沿用树 `1-2, 1-3`、颜色 `[5,5,8]`。

1. 叶子 2 形成 `{5}`、质量 1；叶子 3 形成 `{8}`、质量 1。
2. 点 1 自己先形成 `{5}`，收到点 2 的袋子后仍是 `{5}`，质量变成 2。
3. 点 3 的质量 1 袋子并入质量 2 袋子，得到 `{5,8}`、质量 3，答案为 2。

每袋的颜色集合正好是其子树颜色的并集，所以 `size()` 就是不同颜色数。扫描时只把较小质量袋子的元素插入较大袋子，结果集合仍是两边的并集；归纳到根时，每个点的答案都正确。

摊还理由也看节点质量而不是颜色数：每次扫描的小袋元素至多来自较小节点侧。对一个元素项，若重复颜色已在大袋中，该项本次就消失；若作为新颜色留下，它之后再次随袋子搬运时，所在子树质量至少翻倍。因此每个原始节点项最多被扫描 $O(\log n)$ 次；重复颜色不会破坏这个界。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `SmallToLargeDistinct` | tree 为 1-based 连通无向树，color 为颜色数组，root 为合法根。 返回：无（构造函数）。 | 保存输入引用并分配答案；输入必须比对象活得更久。 |
| `dfs(u,p)` | u 是当前子树根，p 是父点；根调用时 p=0。 返回：Bag，子树所有颜色的集合及其质量。 | 合并子树颜色集合并写入 answer[u]；集合所有权随返回值交给调用者。 |
| `solve()` | 无参数。 返回：vector&lt;int&gt;，下标 1..n 的答案。 | 重新计算所有子树不同颜色数；允许重复调用且不改输入。 |

复杂度：本实现按子树节点数（质量）选择容器。使用 `set` 时单次插入为 $O(\log n)$，总时间 $O(n\log^2 n)$、空间 $O(n)$。

若换成期望 $O(1)$ 插入的哈希集合，总时间期望 $O(n\log n)$。

**4. 怎么调用**

模板实现如下。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct SmallToLargeDistinct {
    struct Bag {
        unique_ptr<set<int>> values;
        int mass = 0; // 对应子树节点数，用于严谨的小并大选择
    };
    int n, root;
    const vector<vector<int>>& tree;
    const vector<int>& color;
    vector<int> answer;

    // 参数：tree 为 1-based 连通无向树，color 为颜色数组，root 为合法根。
    // 返回：无（构造函数）。
    // 效果：保存输入引用并分配答案；输入必须比对象活得更久。
    SmallToLargeDistinct(const vector<vector<int>>& tree,
                         const vector<int>& color, int root)
        : n((int)tree.size() - 1), root(root), tree(tree), color(color),
          answer(n + 1) {
        assert(n >= 1 && 1 <= root && root <= n);
    }
    // 参数：u 是当前子树根，p 是父点；根调用时 p=0。
    // 返回：Bag，子树所有颜色的集合及其质量。
    // 效果：合并子树颜色集合并写入 answer[u]；集合所有权随返回值交给调用者。
    Bag dfs(int u, int p) {
        Bag current{make_unique<set<int>>(), 1};
        current.values->insert(color[u]);
        for (int v : tree[u]) if (v != p) {
            Bag other = dfs(v, u);
            // 质量而非不同颜色数决定小侧；这样重复颜色也有明确的摊还收费。
            if (current.mass < other.mass) swap(current, other);
            current.values->insert(other.values->begin(), other.values->end());
            current.mass += other.mass;
        }
        answer[u] = (int)current.values->size();
        return current;
    }
    // 参数：无参数。
    // 返回：vector<int>，下标 1..n 的答案。
    // 效果：重新计算所有子树不同颜色数；允许重复调用且不改输入。
    vector<int> solve() {
        fill(answer.begin(), answer.end(), 0);
        Bag result = dfs(root, 0);
        (void)result; // 根集合所有权在本次调用结束时释放，只保留 answer。
        return answer;
    }
};
```

最小完整调用示例，树为 `1-2,1-3`，颜色为 `[5,5,8]`：

```text
vector<vector<int>> tree(4);
tree[1] = {2, 3}; tree[2] = {1}; tree[3] = {1};
vector<int> color = {0, 5, 5, 8};
SmallToLargeDistinct solver(tree, color, 1);
auto answer = solver.solve();
assert(answer[1] == 2 && answer[2] == 1 && answer[3] == 1);
```

**5. 要改哪里**

先确认摘要支持逐元素插入，并明确重复元素如何处理；只支持整体合并的 DP 摘要不能直接套用。可以先统计不同颜色，再用 `unordered_map<颜色,频次>` 求众数，最后替换成自定义摘要并重新证明搬运次数。

DSU on Tree 会清理临时表来回答子树询问；这里把集合所有权交给父节点，孩子集合被消费，只在 `answer` 中留下孩子答案。线段树合并则把单个元素换成值域树节点，适合值域统计或第 k 小。

**6. 自检**

再检查非叶合并：两个子树质量分别为 2 和 7，即使两边的颜色集合大小都是 2，也必须让质量 2 的集合并入质量 7 的集合，合并后 `mass=9`；答案仍取合并后集合大小。重复调用 `solve()` 会重新建临时袋子，因此上述例子再次得到 `[2,1,1]`。

**7. 坑**

不要按不同颜色数而非 `mass` 选小侧；重复颜色会破坏翻倍证明。交换 `Bag` 后继续使用新的 `current` 所有权，不能再访问已转移的容器。递归必须以父节点过滤邻接边；输入有环时会无限递归。`set` 插入为 $O(\log n)$，换哈希容器后复杂度是期望界且需考虑退化风险。

**8. 一句话原理**

始终把较小质量侧逐项加入较大侧，使仍存活的元素每次搬运后面对的子树质量至少翻倍。

## 5.17 线段树合并（Segment Tree Merge） {#segment-tree-merge}

**1. 它是做什么的**

有两个多重集合 `{3}` 和 `{1,3}`，合并后是 `{1,3,3}`：值 1 出现一次，值 3 出现两次。我们还想查某个值出现几次，或找第 k 小。值域线段树把每个值放在固定值域的一片叶子里，叶子记录频次。

若每次都逐个取出集合元素再插入，集合很大时会重复做许多工作。尤其树上每个子树都维护一份权值集合，父子集合常有大量相同值。

这里让两棵树的同值区间递归合并：对应节点的频次相加，空分支直接借用另一边已有的节点。

**2. 变量在做什么**

先分清树节点编号和权值：`root` 是节点池中的下标，不是原树的点号；叶子所在的区间才表示某个权值。编号 0 代表整片区间都没有节点。再分清“合并结果”和“两个原集合”：本模板会消费第二棵树，合并后只剩一棵有效树，不能把旧根继续当独立集合用。

| 名称 | 含义 |
|---|---|
| `lo`, `hi` | 所有集合共享的闭值域；中点计算要求 `hi-lo` 不溢出 `int`。 |
| `tr` | 动态节点池；下标是节点编号，`tr[0]` 是全零空节点。 |
| `Node::left/right` | 当前值域区间左右半边的根编号；0 表示该侧为空。 |
| `Node::sum` | 当前区间的总频次；必须非负且不超过 `INT_MAX`。 |

**3. 函数在做什么**

用 `{3}` 与 `{1,3}` 手算。

1. 值域 `[1,8]` 的两棵根总频次分别为 1 和 2。
2. 左半边 `[1,4]` 中，值 1 只在第二棵树出现，值 3 在两棵树都出现。

   递归把值 1 的非空节点接入结果，并把值 3 的叶子计数相加。
3. 结果频次为 `{1:1,3:2}`，所以第 1 小是 1、第 2 小是 3，`count(3)=2`。

每个叶子唯一对应一个值；对应区间的频次相加，等于把两个集合中每个值的出现次数相加。内部节点的左右区间互不重叠，因此递归完成后每个值都恰好被合并一次。遇到空根时直接返回另一根，等价于加上全零频次。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `SegmentTreeMerge` | lo&lt;=hi 是权值闭区间，reserveNodes 为预留节点数。 返回：无（构造函数）。 | 节点 0 为空；预留容量仅影响常数，不改变结果。 |
| `add(root,l,r,pos,delta)` | root 是旧频次树根；l、r 是当前值域区间；pos 是修改值；delta 是计数增量。 返回：int，更新后的根。 | 要求 pos 属于值域且更新后频次非负；修改节点池并更新根到叶路径。 |
| `add(root,pos,delta)` | root 是旧频次树根（可为 0）；pos 属于 lo..hi；delta 是计数增量。 返回：int，更新后的根。 | 只修改内部节点池。 |
| `merge(a,b,l,r)` | a、b 是待合并根（可有一个为 0）；l、r 是值域区间；非空根须互异且节点不共享。 返回：int，结果根。 | 破坏性合并频次；结果存回 a 对应的节点，b 不再可独立使用。 |
| `merge(a,b)` | a、b 来自本池同一值域且节点完全不共享。 返回：int，唯一有效的合并根，旧集合不可再独立使用。 | 破坏性合并两个不共享节点的频次树。 |
| `count(root,l,r,pos)` | root 是当前频次树根；l、r 是值域区间；pos 是待查询值。 返回：int，该值的出现次数，root 可为 0。 | 只读，不修改结构。 |
| `count(root,pos)` | root 是频次树根；pos 属于 lo..hi。 返回：int，该值的出现次数，root 可为 0。 | 只读，不修改结构。 |
| `kth(root,l,r,k)` | root 是频次树根，l、r 为值域闭区间，k 为 1-based 排名。 返回：int，全局第 k 小值，k 非法时断言失败。 | 只读，不修改结构。 |
| `kth(root,k)` | root 是频次树根；k 是从 1 开始且不超过总计数的排名。 返回：int，根的第 k 小值。 | 只读，不修改结构。 |

复杂度：`add` 为 $O(\log\sigma)$。一次破坏性合并访问第二棵树的非空节点及重叠分支。若总共创建 $P$ 个节点、外部调用合并 $M$ 次，这批合并总成本为 $O(P+M)$。

每次两个非空节点相遇都会让第二个节点退出独立可用的森林。空节点返回次数至多是递归分叉数的常数倍再加 $M$。

常见做法是每点先建一条值域路径，再沿原树合并 $n-1$ 次，创建与合并共 $O(n\log(\sigma+1))$；空间为已创建节点数。`sum`、计数、节点池下标都须在 `int` 范围内。

**4. 怎么调用**

模板实现如下。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct SegmentTreeMerge {
    struct Node { int left = 0, right = 0, sum = 0; };
    int lo, hi;
    vector<Node> tr;
    // 参数：lo<=hi 是权值闭区间，reserveNodes 为预留节点数。
    // 返回：无（构造函数）。
    // 效果：节点 0 为空；预留容量仅影响常数，不改变结果。
    SegmentTreeMerge(int lo, int hi, int reserveNodes = 0)
        : lo(lo), hi(hi) {
        assert(lo <= hi);
        tr.reserve(max(1, reserveNodes));
        tr.push_back(Node{});
    }
    // 参数：root 是旧频次树根；l、r 是当前值域区间；pos 是修改值；delta 是计数增量。
    // 返回：int，更新后的根。
    // 效果：要求 pos 属于值域且更新后频次非负；修改节点池并更新根到叶路径。
    int add(int root, int l, int r, int pos, int delta) {
        if (!root) { root = (int)tr.size(); tr.push_back(Node{}); }
        tr[root].sum += delta;
        assert(tr[root].sum >= 0);
        if (l == r) return root;
        int m = l + (r - l) / 2;
        if (pos <= m) tr[root].left = add(tr[root].left, l, m, pos, delta);
        else tr[root].right = add(tr[root].right, m + 1, r, pos, delta);
        return root;
    }
    // 参数：root 是旧频次树根（可为 0）；pos 属于 lo..hi；delta 是计数增量。
    // 返回：int，更新后的根。
    // 效果：只修改内部节点池。
    int add(int root, int pos, int delta = 1) {
        assert(lo <= pos && pos <= hi);
        return add(root, lo, hi, pos, delta);
    }
    // 参数：a、b 是待合并根（可有一个为 0）；l、r 是值域区间；非空根须互异且节点不共享。
    // 返回：int，结果根。
    // 效果：破坏性合并频次；结果存回 a 对应的节点，b 不再可独立使用。
    int merge(int a, int b, int l, int r) {
        if (!a) return b;
        if (!b) return a;
        tr[a].sum += tr[b].sum;
        if (l != r) {
            int m = l + (r - l) / 2;
            tr[a].left = merge(tr[a].left, tr[b].left, l, m);
            tr[a].right = merge(tr[a].right, tr[b].right, m + 1, r);
        }
        return a;
    }
    // 参数：a、b 来自本池同一值域且节点完全不共享。
    // 返回：int，唯一有效的合并根，旧集合不可再独立使用。
    // 效果：破坏性合并两个不共享节点的频次树。
    int merge(int a, int b) {
        assert(a == 0 || b == 0 || a != b); // merge(a,a) 会重复累计，调用契约禁止它
        return merge(a, b, lo, hi);
    }
    // 参数：root 是当前频次树根；l、r 是值域区间；pos 是待查询值。
    // 返回：int，该值的出现次数，root 可为 0。
    // 效果：只读，不修改结构。
    int count(int root, int l, int r, int pos) const {
        if (!root) return 0;
        if (l == r) return tr[root].sum;
        int m = l + (r - l) / 2;
        return pos <= m ? count(tr[root].left, l, m, pos)
                        : count(tr[root].right, m + 1, r, pos);
    }
    // 参数：root 是频次树根；pos 属于 lo..hi。
    // 返回：int，该值的出现次数，root 可为 0。
    // 效果：只读，不修改结构。
    int count(int root, int pos) const {
        assert(lo <= pos && pos <= hi);
        return count(root, lo, hi, pos);
    }
    // 参数：root 是频次树根，l、r 为值域闭区间，k 为 1-based 排名。
    // 返回：int，全局第 k 小值，k 非法时断言失败。
    // 效果：只读，不修改结构。
    int kth(int root, int l, int r, int k) const {
        assert(root && 1 <= k && k <= tr[root].sum);
        if (l == r) return l;
        int m = l + (r - l) / 2;
        int leftSum = tr[tr[root].left].sum;
        if (k <= leftSum) return kth(tr[root].left, l, m, k);
        return kth(tr[root].right, m + 1, r, k - leftSum);
    }
    // 参数：root 是频次树根；k 是从 1 开始且不超过总计数的排名。
    // 返回：int，根的第 k 小值。
    // 效果：只读，不修改结构。
    int kth(int root, int k) const { return kth(root, lo, hi, k); }
};
```

最小调用示例，可直接放在 `main` 函数体内：合并 `{3}` 与 `{1,3}`，结果第 2 小为 3。

```text
SegmentTreeMerge st(1, 8);
int a = st.add(0, 3);
int b = st.add(0, 1);
b = st.add(b, 3);
int merged = st.merge(a, b);
assert(st.count(merged, 3) == 2);
assert(st.kth(merged, 1) == 1 && st.kth(merged, 2) == 3);
```

**5. 要改哪里**

树上后序合并时，先记录孩子答案，再把孩子根交给父亲并将孩子根置 0；本模板不为每棵子树保留版本。先离散化到紧凑值域，再练习频次合并、子树第 k 小，之后再结合差分根或离线删除分析节点重叠。

若需要分裂操作，要另行设计节点所有权。本结构会破坏旧根并复用节点；主席树则复制路径并保留历史版本。

**6. 自检**

值域 `[1,8]`：A=`{3:1}`、B=`{1:1,3:1}`。先看根总数 `1+2=3`；再看左侧值 1 被保留、值 3 的两份计数相加；最后检查 `kth(1)=1`、`kth(2)=3`、`count(3)=2`。若合并空根与非空根，结果应等于非空根，因为空根没有任何非零计数。

**7. 坑**

两个根必须来自同一节点池和同一值域，且节点集合不得共享；非空 `merge(a,a)` 会重复累计。合并后第二棵树不可继续独立读取或修改。`sum`、总频次、节点池下标和 `hi-lo` 都受 `int` 范围限制；不要把总频次误当不同值个数。

**8. 一句话原理**

相同值域的对应节点频次相加，空分支直接复用另一侧节点；节点所有权随破坏性合并转移。

## 5.18 主席树（可持久化线段树） {#persistent-segment-tree}

**1. 它是做什么的**

给定一个静态数组，多次询问某个区间内的第 `k` 小值。例如：

```plain
数组：[40, 10, 30, 20, 10]
询问 [2,5] 的第 3 小：
取出 [10,30,20,10]，排序为 [10,10,20,30]，答案是 20。
```

每次取出区间再排序，可以得到答案，但大量询问会重复排序。主席树先为每个前缀保存一份“各种值出现了多少次”的记录。查询 `[l,r]` 时，用前 `r` 项的记录减去前 `l-1` 项的记录，得到该区间的频次，再寻找第 `k` 小。

这里的“可持久化”，就是**更新后保留旧版本，旧版本仍然可以查询**。如果每个前缀都复制一整份记录，空间会很大；主席树只复制本次更新影响的部分，其他部分由不同版本共享。

本节先讲静态数组区间第 `k` 小。树上路径第 `k` 小使用同样的频次思想，放在基本过程之后理解。

**2. 变量在做什么**

首先区分两种区间：**数组区间** `[l,r]` 指要查询原数组的哪些位置；**值域区间**指线段树节点负责统计哪些值。本模板的线段树按值划分，节点保存这些值的出现次数。

先把原值排序去重并编号：

```plain
原值：  10  20  30  40
编号：   1   2   3   4
```

值域节点 `[1,2]` 统计的是值 10 和 20 一共出现多少次，不是原数组前两个位置的信息。

| 名称 | 含义 |
|---|---|
| `lo`、`hi` | 离散值编号的闭区间，本例为 `[1,4]`。 |
| `root[i]` | 前 `i` 个数组元素对应的版本根；由调用方保存，不是类的成员。 |
| `tr` | 所有版本共用的节点池，根和孩子都用池内编号表示。 |
| `Node::sum` | 当前节点负责的值域内，元素一共出现了多少次。 |
| `Node::left/right` | 左右孩子在节点池中的编号。 |
| `previous`、`now` | 更新使用的旧节点编号，以及复制后新节点的编号。 |
| `pos`、`delta` | 本次修改的值编号，以及频次增量；前缀建树每次加 1。 |
| `k` | 要找第几小，从 1 开始，重复值分别计数。 |

`root[i]` 只保存一个节点编号。不同版本可以共享没有变化的节点，不需要各自复制一整棵树。节点编号 0 表示空树，频次为 0；因此 `root[0]=0` 表示还没有加入任何元素。

**3. 函数在做什么**

先看“前缀版本”记录了什么。本例的各版本频次如下：

| 版本 | 已加入的数组元素 | 10 的次数 | 20 的次数 | 30 的次数 | 40 的次数 |
|---|---|---|---|---|---|
| `root[0]` | 无 | 0 | 0 | 0 | 0 |
| `root[1]` | `40` | 0 | 0 | 0 | 1 |
| `root[2]` | 40, 10 | 1 | 0 | 0 | 1 |
| `root[3]` | 40, 10, 30 | 1 | 0 | 1 | 1 |
| `root[4]` | 40, 10, 30, 20 | 1 | 1 | 1 | 1 |
| `root[5]` | 40, 10, 30, 20, 10 | 2 | 1 | 1 | 1 |

**怎样建立新版本？**

从 `root[2]` 建立 `root[3]` 时，新加入的是 30，即编号 3。只有包含编号 3 的节点计数需要加一：

```plain
值域 [1,4] → 值域 [3,4] → 值域 [3,3]
```

模板复制这条路径上的节点，并修改新节点。其他分支继续指向旧节点。例如 `[1,2]` 内没有新增元素，它的整棵子树都可以共享。

因此 `root[3]` 能查到新加入的 30，`root[2]` 仍表示原来的两个元素，两版本共享的节点都没有被修改。这就是“路径复制”。

**怎样查询区间第 k 小？**

查询 `[2,5]` 时，使用 `root[5]` 和 `root[1]`。对同一个值，它在区间内的次数等于“前 5 项中的次数减去前 1 项中的次数”，于是得到 `10:2，20:1，30:1，40:0`。

寻找第 3 小，从值域根开始：

1. 左半值域 `[1,2]`，即 10、20，共有 3 个元素。第 3 小一定在这里，进入两版本的左孩子，`k` 保持为 3。
2. 再看左半值域 `[1,1]`，即 10，有 2 个元素。第 3 小不在这里，跳过这两个元素，进入两版本的右孩子，并令 `k=3-2=1`。
3. 到达编号 2 的叶子，对应原值 20，查询结束。

每层只需判断：**左边有多少个元素，足不足以包含我要找的第 k 个？** 两个根同步下降，计数用相应左孩子的 `sum` 作差，并不真的建立一棵区间差树。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `PersistentSegmentTree` | 输入值编号范围和可选预留节点数；构造函数无返回值。 | 建立节点池和空版本 0；预留容量只影响扩容次数。 |
| `add(previous,pos,delta)` | 输入旧根、值编号及频次增量；返回新版本根。 | 复制受影响路径，保留旧版本；前缀建树时使用默认增量 1。 |
| 内部 `add` | 额外输入当前值域边界 `l,r`；返回新节点编号。 | 复制当前节点并递归复制受影响孩子，未修改分支继续共享。 |
| `kthRange` | 输入 `root[r]`、`root[l-1]` 和排名；返回离散值编号。 | 通过两个前缀的计数差寻找第 k 小，要求 k 合法。 |
| `kthPath` | 输入分别对应 u、v、LCA、parent(LCA) 的四个版本根及排名；返回离散值编号。 | 用于后述树路径扩展；要求四根的组合构成合法频次。 |
| 内部 `kth4` | 输入四根、当前值域和排名；返回叶子的离散编号。 | 计算左侧组合频次，决定下降方向；查询不创建或修改节点。 |

设不同值有 `σ` 种，树高为 $O(\log(\sigma+1))$。每次加入只复制一条路径，建立全部前缀版本需要 $O(n\log(\sigma+1))$ 时间和空间；一次区间或路径第 k 小查询也只走一条路径，为 $O(\log(\sigma+1))$。离散化另需 $O(n\log n)$ 时间。

**4. 怎么调用**

依次完成离散化、建立前缀版本、查询和还原原值。先放入下面的完整模板。所有版本根必须来自同一个对象；值编号在 `[lo,hi]` 内，构造范围非空。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct PersistentSegmentTree {
    struct Node { int left = 0, right = 0, sum = 0; };
    int lo, hi;
    vector<Node> tr;

    // 参数：lo<=hi 为离散值域闭区间，reserveNodes 为预留节点数。
    // 返回：无（构造函数）。
    // 效果：建立空版本 0；预留容量只影响扩容次数。
    PersistentSegmentTree(int lo, int hi, int reserveNodes = 0) : lo(lo), hi(hi) {
        assert(lo <= hi);
        tr.reserve(max(1, reserveNodes));
        tr.push_back(Node{});
    }
    // 参数：previous 是旧版本根；l、r 是值域区间；pos 是修改值；delta 是计数增量。
    // 返回：int，新版本根。
    // 效果：要求 pos 属于值域且更新后频次非负；复制并修改根到叶路径，旧版本保持不变。
    int add(int previous, int l, int r, int pos, int delta) {
        int now = (int)tr.size();
        tr.push_back(tr[previous]);
        tr[now].sum += delta;
        assert(tr[now].sum >= 0); // 合法 delta 不得让任一值域区间频次为负
        if (l == r) return now;
        int m = l + (r - l) / 2;
        if (pos <= m) tr[now].left = add(tr[previous].left, l, m, pos, delta);
        else tr[now].right = add(tr[previous].right, m + 1, r, pos, delta);
        return now;
    }
    // 参数：previous 是已有版本根；pos 属于值域；delta 是计数增量。
    // 返回：int，只比旧版本多 delta 个 pos 的新根。
    // 效果：创建新版本节点，previous 对应的旧版本保持不变。
    int add(int previous, int pos, int delta = 1) {
        assert(0 <= previous && previous < (int)tr.size());
        assert(lo <= pos && pos <= hi);
        return add(previous, lo, hi, pos, delta);
    }
    // 参数：ru、rv、rlca、rparent 是路径差分版本根；l、r 是值域区间；k 是从 1 开始的排名。
    // 返回：int，路径第 k 小的离散值。
    // 效果：四个版本根按 +rootU +rootV -rootLca -rootParentLca 组合。
    int kth4(int ru, int rv, int rlca, int rparent, int l, int r, int k) const {
        int total = tr[ru].sum + tr[rv].sum - tr[rlca].sum - tr[rparent].sum;
        assert(1 <= k && k <= total);
        if (l == r) return l;
        int m = l + (r - l) / 2;
        int leftCount = tr[tr[ru].left].sum + tr[tr[rv].left].sum
                      - tr[tr[rlca].left].sum - tr[tr[rparent].left].sum;
        if (k <= leftCount)
            return kth4(tr[ru].left, tr[rv].left, tr[rlca].left,
                        tr[rparent].left, l, m, k);
        return kth4(tr[ru].right, tr[rv].right, tr[rlca].right,
                    tr[rparent].right, m + 1, r, k - leftCount);
    }
    // 参数：四根均为本对象版本根，k 从 1 开始。
    // 返回：int，路径第 k 小值，父根为空时传 0。
    // 效果：只读，不修改结构。
    int kthPath(int ru, int rv, int rlca, int rparent, int k) const {
        return kth4(ru, rv, rlca, rparent, lo, hi, k);
    }
    // 参数：rootR、rootBeforeL 分别是前缀 [1..r]、[1..l-1] 的版本根；k 是排名。
    // 返回：int，区间第 k 小值。
    // 效果：只读，不修改结构。
    int kthRange(int rootR, int rootBeforeL, int k) const {
        return kth4(rootR, 0, rootBeforeL, 0, lo, hi, k);
    }
};
```

下面用本节数组验证完整调用。外层大括号让这个例子拥有独立的局部变量：

```text
{
    vector<int> a = {0, 40, 10, 30, 20, 10};
    vector<int> values(a.begin() + 1, a.end());
    sort(values.begin(), values.end());
    values.erase(unique(values.begin(), values.end()), values.end());

    PersistentSegmentTree pst(1, (int)values.size());
    vector<int> root(a.size(), 0);
    for (int i = 1; i < (int)a.size(); ++i) {
        int pos = int(lower_bound(values.begin(), values.end(), a[i])
                      - values.begin()) + 1;
        root[i] = pst.add(root[i - 1], pos);
    }
    int rank = pst.kthRange(root[5], root[1], 3);
    int answer = values[rank - 1];
    assert(answer == 20);
}
```

查询返回的是编号 2，需要通过 `values[1]` 还原成 20。`add` 返回的新根也必须保存，它不会替调用方修改 `root[i]`。排名必须满足 `1<=k<=r-l+1`。

若输入已经是 `[1,3]` 内的值，可直接建立版本。下面保留这组更短的调用：

```text
PersistentSegmentTree pst(1, 3);
int root0 = 0;
int root1 = pst.add(root0, 2);
int root2 = pst.add(root1, 1);
int root3 = pst.add(root2, 3);
assert(pst.kthRange(root3, root0, 2) == 2);
assert(pst.kthRange(root3, root1, 1) == 1); // 区间 [2,3]
```

**5. 要改哪里**

先掌握数组前缀版本，再考虑改变“每个版本代表什么”。树上路径第 k 小中，可以令 `root[u]` 表示总根到节点 u 的路径频次，包含 u。设 `w=LCA(u,v)`，路径频次由四个版本组合：

$$
root[u]+root[v]-root[w]-root[parent[w]].
$$

这个式子表示**对应节点的计数相加减**，不是把四个根编号进行整数运算。根到 u、根到 v 的两条路径重复计算了公共部分；LCA 以上点的系数为 `2-1-1=0`，LCA 自身的系数为 `2-1=1`，更深的路径点保留一次。令总根父亲的版本为空根 0，就能统一边界。

例如点权依次为 `2:3，1:1，3:2` 的路径 `2-1-3`，组合后得到 `{1:1,2:1,3:1}`，第 2 小为 2。查询仍根据左侧元素数量选择方向，只是计数由“两根相减”改为“四根组合”。每个值编号的组合频次必须非负，不能随意拿四个历史根拼在一起。

空间要按全部版本估算。若每次复制约 `ceil(log2(σ))+1` 个节点，节点含三个 int，在常见 4 字节 int 环境中，`n=10^5`、约 18 层时节点数据约 22 MB，还需根数组和容器多分配的容量。

若要在线修改原数组，后面的多个前缀都会受影响，不能直接沿用这套静态前缀建树。大量元素同时改变的区间修改，也不属于本模板直接支持的操作。

**6. 自检**

本例 `[2,5]` 排序为 `[10,10,20,30]`，第 1、2、3、4 小分别是 10、10、20、30；`[1,1]` 的第 1 小为 40，`[5,5]` 的第 1 小为 10。

建完全部版本后，`root[1]` 仍只包含一个 40；每个前缀根的 `sum` 应等于前缀长度。再检查全相等数组、只有一个不同值、单元素区间和路径两端相同的情况。

对拍时随机选合法 `[l,r]` 和 k，复制区间排序，与第 k 项比较；树路径版则用暴力枚举路径上的点权排序。查询旧版本的结果不能因后续 `add` 改变。

**7. 坑**

- 混淆数组位置和值编号：`root[i]` 的 i 是前缀长度，`add` 的 pos 是值编号。
- 修改了共享旧节点：新版本必须先复制路径节点，否则旧版本也会变化。
- 左端少减一：查询 `[l,r]` 必须使用 `root[r]` 和 `root[l-1]`。
- 把根编号相减：实际相减的是对应节点的 `sum`。
- 把重复值当作一个元素：两个 10 要占两个名次。
- 忘记还原原值：查询返回离散编号，不是原值。
- 树路径公式漏掉 LCA 父根：不能正确抵消全部公共部分。
- 传入非法 k 或负频次：`delta` 更新后每个值频次都须非负，排名须在组合总频次内；断言不能代替调用方保证合法。
- 节点池和计数溢出：当前模板的 `sum`、中间组合频次、节点池下标和 `hi-lo` 均须能放进 int；范围过大时应先离散化。

**8. 一句话原理**

通过路径复制保存每个前缀的频次树，再用两个前缀的计数差，在值域上逐层定位区间第 k 小。

## 5.19 虚树 {#virtual-tree}

**1. 它是做什么的**

原树很大，但一次询问只给少量关键点。以树 `1-2, 1-3, 2-6, 6-7, 7-4, 7-5` 为例，关键点 `{4,5,3}` 的虚树保留点 `1,7,4,5,3`；原树的 `1→7` 被压成一条距离为 3 的边。

朴素地在原树上为每次询问跑完整 DFS，会反复访问与关键点无关的点。若只留下关键点，它们之间又可能隔着决定分叉位置的祖先。

虚树补上这些关键点间必要的公共祖先，再把中间未保留的路径压成一条边；这样小问题仍保留原树上真正相关的分叉和距离。

**2. 变量在做什么**

原树的点号始终不变，虚树只是从中挑出一部分点；`vertices` 是按 DFS 先后排列的原树点号，不是新编号。虚树边也不一定是原树直接相邻边，它连接两个保留点，并记录两点间原树路径的长度。

| 名称 | 含义 |
|---|---|
| `n`, `logn`, `timer` | 原树点数、倍增层数、DFS 进入计时器。 |
| `g[u]` | 原树无向邻接表；必须在 `build` 前完成。 |
| `tin[u]`, `tout[u]` | DFS 进入时间及子树区间末端；祖先判定使用同一轮 DFS 的两个时间。 |
| `depth[u]` | 相对预处理根的深度；虚树边权用深度差表示原树距离。 |
| `up[j][u]` | 节点 u 向上 `2^j` 步的祖先；0 表示越过根。 |
| `VirtualTreeResult::vertices` | 本次虚树保留的原树点号，按 DFS 序排列。 |
| `VirtualTreeResult::edges` | `(父点,子点,原树距离)` 三元组；不是原树直接边。 |
| `VirtualTreeResult::root` | 虚树根；空询问时为 0。 |

**3. 函数在做什么**

用下面这棵树，带星号的是关键点：

```plain
1
├─2
│ └─6
│   └─7
│     ├─4*
│     └─5*
└─3*
```

第一步，DFS 顺序为 `1,2,6,7,4,5,3`，关键点顺序是 `4,5,3`，相邻 LCA 分别为 7 和 1。

第二步，加入 LCA 并排序去重，保留点按 DFS 序为 `1,7,4,5,3`。

第三步，按上述顺序使用祖先栈。每次先弹出不是当前点祖先的栈顶，再连到剩余栈顶：

| 当前点 | 弹出哪些点 | 连出的虚边 | 入栈后的状态 |
|---|---|---|---|
| 1 | 无 | 根，无父边 | `[1]` |
| 7 | 无 | `1→7`，距离 3 | `[1,7]` |
| 4 | 无 | `7→4`，距离 1 | `[1,7,4]` |
| 5 | 4 | `7→5`，距离 1 | `[1,7,5]` |
| 3 | 5、7 | `1→3`，距离 1 | `[1,3]` |

点 4 在处理 5 时已经出栈，不会等到处理 3 才出栈。原树点 2、6 不需要保留，它们压缩在距离为 3 的 `1→7` 中。

```plain
1
├─7 (距离 3)
│ ├─4 (距离 1)
│ └─5 (距离 1)
└─3 (距离 1)
```

正确性来自两点：DFS 序相邻关键点的 LCA 保留了关键点之间发生分叉所需的祖先；栈则把每个点连到当前路径上最近的保留祖先。两端点间没保留的原树点只能是被压缩的路径中间点，故边权 `depth[child]-depth[parent]` 就是原树距离。

去重后有 $k$ 个关键点时，相邻对只有 $k-1$ 个，因此至多补入 $k-1$ 个 LCA；最多保留 $2k-1$ 个点、产生 $2k-2$ 条边。这里的 $k$ 是输入关键点去重后的数量。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `VirtualTree(nodeCount)` | nodeCount 为原树点数。 返回：无（构造函数）。 | 分配 1-based 图和 LCA 表，要求随后加入 n-1 条树边。 |
| `addEdge(u,v)` | u、v 为 1..n。 返回：void。 | 向原树加入无向边；必须在 build 前调用。 |
| `dfs(u,p)` | p 是父点。 返回：void。 | u 的 DFS 进入/离开时间；写 tin/tout/depth/up[0]。 |
| `build(root)` | root 为原树根。 返回：void。 | 清空并重建 tin/tout/depth/up；要求原图为连通树。 |
| `isAncestor(u,v)` | u、v 是已 build 的树中合法点号。 返回：bool，u 是否为 v 的祖先（包括 u==v）。 | 只读，不修改结构。 |
| `lca(u,v)` | u、v 是已 build 的树中合法点号。 返回：int，u、v 的最近公共祖先。 | 要求已 build 且两点在树中。 |
| `buildVirtual(special)` | special 是本次询问的原树关键点，可重复。 返回：VirtualTreeResult，含关键点及必要 LCA 的虚树，要求已 build。 | 只读，不修改结构。 |

复杂度：预处理倍增 LCA 为 $O(n\log n)$。若输入 $k$ 个关键点（可重复），单次询问为 $O(k\log k+k\log n)$：排序关键点、求相邻 LCA、加入至多 $k-1$ 个 LCA、再次排序并用栈建树。

即使调用者已按 DFS 序排序，本模板仍会求 LCA 并对补点后的 `all` 再排序；只有另写复用排序的接口才能省第一次排序。空间 $O(n\log n+k)$。空询问返回空点边、根为 0；单个关键点只产生一个保留点和零条边。

**4. 怎么调用**

模板实现如下。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct VirtualTreeResult {
    vector<int> vertices;                 // 按 DFS 序排列的原树点号
    vector<tuple<int, int, int>> edges;   // (父点, 子点, 原树距离)
    int root = 0;                         // vertices 非空时为虚树根
};

struct VirtualTree {
    int n, logn, timer = 0;
    vector<vector<int>> g;
    vector<int> tin, tout, depth;
    vector<vector<int>> up;
    // 参数：nodeCount 为原树点数。
    // 返回：无（构造函数）。
    // 效果：分配 1-based 图和 LCA 表，要求随后加入 n-1 条树边。
    explicit VirtualTree(int nodeCount)
        : n(nodeCount), logn(1), g(nodeCount + 1), tin(nodeCount + 1),
          tout(nodeCount + 1), depth(nodeCount + 1) {
        assert(n >= 1);
        while ((1 << logn) <= n) ++logn;
        up.assign(logn, vector<int>(n + 1, 0));
    }
    // 参数：u、v 为 1..n。
    // 返回：void。
    // 效果：向原树加入无向边；必须在 build 前调用。
    void addEdge(int u, int v) {
        assert(1 <= u && u <= n && 1 <= v && v <= n && u != v);
        g[u].push_back(v);
        g[v].push_back(u);
    }
    // 参数：p 是父点。
    // 返回：void。
    // 效果：u 的 DFS 进入/离开时间；写 tin/tout/depth/up[0]。
    void dfs(int u, int p) {
        tin[u] = ++timer;
        up[0][u] = p;
        for (int j = 1; j < logn; ++j) up[j][u] = up[j - 1][up[j - 1][u]];
        for (int v : g[u]) if (v != p) {
            depth[v] = depth[u] + 1;
            dfs(v, u);
        }
        tout[u] = timer;
    }
    // 参数：root 为原树根。
    // 返回：void。
    // 效果：清空并重建 tin/tout/depth/up；要求原图为连通树。
    void build(int root = 1) {
        assert(1 <= root && root <= n);
        timer = 0;
        fill(tin.begin(), tin.end(), 0);
        fill(tout.begin(), tout.end(), 0);
        fill(depth.begin(), depth.end(), 0);
        for (auto& row : up) fill(row.begin(), row.end(), 0);
        dfs(root, 0);
        assert(timer == n);
    }
    // 参数：u、v 是已 build 的树中合法点号。
    // 返回：bool，u 是否为 v 的祖先（包括 u==v）。
    // 效果：只读，不修改结构。
    bool isAncestor(int u, int v) const {
        return tin[u] <= tin[v] && tout[v] <= tout[u];
    }
    // 参数：u、v 是已 build 的树中合法点号。
    // 返回：int，u、v 的最近公共祖先。
    // 效果：要求已 build 且两点在树中。
    int lca(int u, int v) const {
        if (isAncestor(u, v)) return u;
        if (isAncestor(v, u)) return v;
        int x = u;
        for (int j = logn - 1; j >= 0; --j)
            if (up[j][x] != 0 && !isAncestor(up[j][x], v)) x = up[j][x];
        return up[0][x];
    }
    // 参数：special 是本次询问的原树关键点，可重复。
    // 返回：VirtualTreeResult，含关键点及必要 LCA 的虚树，要求已 build。
    // 效果：只读，不修改结构。
    VirtualTreeResult buildVirtual(vector<int> special) const {
        VirtualTreeResult result;
        if (special.empty()) return result;
        // 参数：a、b 是原树点号。
        // 返回：bool，a 的 DFS 进入时间是否早于 b。
        // 效果：比较器只读 tin；sort 据此原地排序 special。
        sort(special.begin(), special.end(), [&](int a, int b) { return tin[a] < tin[b]; });
        special.erase(unique(special.begin(), special.end()), special.end());
        vector<int> all = special;
        for (int i = 1; i < (int)special.size(); ++i) all.push_back(lca(special[i - 1], special[i]));
        // 参数：a、b 是关键点或 LCA 点号。
        // 返回：bool，a 的 DFS 进入时间是否早于 b。
        // 效果：比较器只读 tin；sort 据此原地排序 all。
        sort(all.begin(), all.end(), [&](int a, int b) { return tin[a] < tin[b]; });
        all.erase(unique(all.begin(), all.end()), all.end());
        result.vertices = all;
        vector<int> st;
        for (int x : all) {
            while (!st.empty() && !isAncestor(st.back(), x)) st.pop_back();
            if (!st.empty())
                result.edges.push_back({st.back(), x, depth[x] - depth[st.back()]});
            st.push_back(x);
        }
        result.root = all.front();
        return result;
    }
};
```

最小调用示例，可直接放在 `main` 函数体内：原树为 `1-2,1-3,2-4,2-5`，关键点 `{4,5,3}`，其虚树应有根 1、五个保留点和四条边。

```text
VirtualTree vt(5);
vt.addEdge(1, 2); vt.addEdge(1, 3);
vt.addEdge(2, 4); vt.addEdge(2, 5);
vt.build(1);
auto result = vt.buildVirtual({4, 5, 3});
assert(result.root == 1);
assert(result.vertices.size() == 5 && result.edges.size() == 4);
```

本节七点压缩例也可直接验证；以下局部作用域与上一例独立：

```text
{
    VirtualTree compressedTree(7);
    compressedTree.addEdge(1, 2); compressedTree.addEdge(1, 3);
    compressedTree.addEdge(2, 6); compressedTree.addEdge(6, 7);
    compressedTree.addEdge(7, 4); compressedTree.addEdge(7, 5);
    compressedTree.build(1);
    auto small = compressedTree.buildVirtual({4, 5, 3});
    assert((small.vertices == vector<int>{1, 7, 4, 5, 3}));
    assert((small.edges == vector<tuple<int, int, int>>{
        {1, 7, 3}, {7, 4, 1}, {7, 5, 1}, {1, 3, 1}}));
}
```

**5. 要改哪里**

每次询问的 DP 标记、度数和答案数组只初始化或清理 `vertices` 中至多 `2k-1` 个点；不要为了小询问清空整棵原树。虚树边权是原树距离，不是原树单边，距离 DP 要使用这段距离。

HLD 适合动态路径修改或查询；虚树适合原树大、每次询问关键点少的场景。可继续练习关键点两两路径总长、关键点覆盖或最近关键点 DP。

**6. 自检**

对本节七点树，关键点 `{4,5,3}` 应补出 7 和 1，按 DFS 序得到 `[1,7,4,5,3]`；虚边为 `1→7`（3）、`7→4`（1）、`7→5`（1）、`1→3`（1）。压缩前后关键点距离不变，例如 4 到 3 都为 5。

第 4 部分保留的五点调用是另一个小例：应补出 2、1，共五个保留点和四条边。空关键点返回空点边且根为 0；单关键点只有一个点、没有边。重复给出同一个关键点不应产生重复虚边。

对拍可随机取几个关键点，比较原树和虚树上的两两距离，并核对虚树每条边都是原树的祖先到后代路径。

**7. 坑**

关键点重复时先去重；只加入关键点会丢失分叉祖先，必须补入 DFS 序相邻关键点的 LCA。`buildVirtual` 会对输入排序、补 LCA 后再次排序，单次复杂度为 $O(k\log k+k\log n)$，不能只报栈扫描的线性复杂度。

`tout` 与 `tin` 必须来自同一次 build；虚树边代表原树压缩路径。递归 DFS 在深链上可能栈溢出。若使用同根 HLD，`pos[u] <= pos[v] < pos[u]+sz[u]` 也可用于祖先判断；此实现用 `tin/tout`。

**8. 一句话原理**

关键点按 DFS 序排列后补入相邻 LCA，再用祖先栈连接，删去对本次问题无贡献的原树分支。

## 5.20 带权并查集 {#weighted-dsu}

**1. 它是做什么的**

有若干元素，约束会逐条告诉我们两个元素的数值差，例如 `value[2]-value[1]=5`、`value[3]-value[2]=2`。因此 `value[3]-value[1]=7`；若再要求它等于 6，就与已有关系矛盾。我们也可以查询两个已连通元素的差值。

普通并查集能快速判断两个元素是否属于同一组，却不知道组内相差多少。若每次沿所有已知关系重新计算差值，关系多时会重复走许多边。

带权并查集在并查集的父子边上额外记一个差值。路径缩短时把沿途差值累加，于是既能知道是否同组，也能得到组内相对值。

**2. 变量在做什么**

要分清元素的绝对值和它相对父亲的差。模板并不保存每个 `value[x]` 的绝对值；它只保存 `value[x]-value[parent[x]]`。根的差为 0 只是把根当作参考原点，绝不表示题目规定根的真实数值是 0。

| 名称 | 含义 |
|---|---|
| `parent[i]` | 父结点；根的父亲是自身。下标 `1..n` 有效，`0` 是未使用哨兵。 |
| `size[i]` | 仅根结点的集合大小，用于按大小合并。 |
| `potential[i]` | `value[i]-value[parent[i]]`；经过 `find(i)` 后变为 `value[i]-value[root]`。 |

**3. 函数在做什么**

沿用 `value[2]-value[1]=5`、`value[3]-value[2]=2`，按本模板的实际挂接规则手算：

| 操作 | 父指针变化 | 保存的差值 |
|---|---|---|
| `unite(1,2,5)` | 两组大小相等，将根 1 挂到根 2 | `potential[1]=-5`，表示 1 比 2 小 5 |
| `unite(2,3,2)` | 2 所在组更大，将根 3 挂到根 2 | `potential[3]=2`，表示 3 比 2 大 2 |
| `relation(1,3)` | 两点根均为 2 | 差为 `2-(-5)=7` |
| `unite(1,3,6)` | 已同根，不再合并 | 已有差是 7，与 6 矛盾，返回 `false` |

这份小例的父链较短。若父链是 `x→p→root`，压缩时要把两段差相加：`value[x]-value[root]=(value[x]-value[p])+(value[p]-value[root])`。因此必须先递归处理 p，再用它已经算好的根差更新 x。

记 `dx=value[x]-value[rootX]`、`dy=value[y]-value[rootY]`。同根时约束 `value[y]-value[x]=w` 当且仅当 `dy-dx=w`。

若把 `rootX` 接到 `rootY`，需存 `value[rootX]-value[rootY]=dy-dx-w`；若把 `rootY` 接到 `rootX`，需存 `value[rootY]-value[rootX]=w+dx-dy`。

路径压缩把父链上的差相加，不改变实际关系，因此公式能保持已有约束。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `find(x)` | x 必须在 1..n。 返回：int，代表元。 | potential[x] 改成 value[x]-value[root]。 |
| `WeightedDSU(n)` | n 为元素个数。 返回：无（构造函数）。 | 建立 n 个互不连通的单点集合，初始差值均为 0。 |
| `unite(x,y,w)` | x、y 在 1..n，w 表示 value[y]-value[x]=w。 返回：bool，是否与现有约束相容。 | 先 find 并压缩路径；异组时加入约束并合并，同组时仅检查是否相容。 |
| `relation(x,y)` | x、y 在 1..n。 返回：optional&lt;long long&gt;，连通时为 value[y]-value[x]，否则为空。 | find 可能压缩路径但不改变集合划分。 |

复杂度：每次合并、查找或查询的均摊时间为 $O(\alpha(n))$，空间 $O(n)$。

**4. 怎么调用**

完整模板如下。代码中每个函数的参数、返回和副作用契约见其定义前注释。

```cpp
#include <bits/stdc++.h>
using namespace std;

class WeightedDSU {
    vector<int> parent, size;
    // potential[x] = value[x] - value[parent[x]]；根的值为 0 只是参考原点。
    vector<long long> potential;
    // 参数：x 必须在 1..n。
    // 返回：int，代表元。
    // 效果：potential[x] 改成 value[x]-value[root]。
    int find(int x) {
        if (parent[x] == x) return x;
        int p = parent[x];
        parent[x] = find(p);
        potential[x] += potential[p];
        return parent[x];
    }

public:
    // 参数：n 为元素个数。
    // 返回：无（构造函数）。
    // 效果：建立 n 个互不连通的单点集合，初始差值均为 0。
    explicit WeightedDSU(int n)
        : parent(n + 1), size(n + 1, 1), potential(n + 1, 0) {
        assert(n >= 0);
        iota(parent.begin(), parent.end(), 0);
    }
    // 参数：x、y 在 1..n，w 表示 value[y]-value[x]=w。
    // 返回：bool，是否与现有约束相容。
    // 效果：先 find 并压缩路径；异组时加入约束并合并，同组时仅检查是否相容。
    bool unite(int x, int y, long long w) {
        int rx = find(x), ry = find(y);
        long long dx = potential[x], dy = potential[y];
        if (rx == ry) return dy - dx == w;
        if (size[rx] > size[ry]) {
            // value[ry]-value[rx] = w + dx - dy。
            parent[ry] = rx;
            potential[ry] = w + dx - dy;
            size[rx] += size[ry];
        } else {
            // value[rx]-value[ry] = dy - dx - w。
            parent[rx] = ry;
            potential[rx] = dy - dx - w;
            size[ry] += size[rx];
        }
        return true;
    }
    // 参数：x、y 在 1..n。
    // 返回：optional<long long>，连通时为 value[y]-value[x]，否则为空。
    // 效果：find 可能压缩路径但不改变集合划分。
    optional<long long> relation(int x, int y) {
        if (find(x) != find(y)) return nullopt;
        return potential[y] - potential[x];
    }
};
```

调用示例：

```text
WeightedDSU dsu(3);
assert(dsu.unite(1, 2, 5));
assert(dsu.unite(2, 3, 2));
auto d = dsu.relation(1, 3);
assert(d.has_value() && *d == 7);
assert(!dsu.unite(1, 3, 6));
```

**5. 要改哪里**

模 3 关系要把每个差值归一到 `{0,1,2}`，例如 `norm(t)=((t%3)+3)%3`。先把题意统一写成 `value[y]-value[x]=w (mod 3)`。

然后 `potential`、`w` 和合并公式中的每次加减都取模。食物链等方向关系若只改比较、不统一差值方向，公式仍会错。

普通并查集只问连通性即可；若需要删除约束或回滚，不能在这个带路径压缩的结构上直接删边，应考虑可撤销并查集和时间分治。

**6. 自检**

加入 `value[2]-value[1]=5`、`value[3]-value[2]=2` 后，查询 1 到 3 应为 7，反向应为 -7；再加入差值 6 应返回矛盾。未连通两点返回空值，同点差值为 0。

**分层练习：** 入门：食物链或相对距离的三类关系；进阶：带时间戳的坐标约束与矛盾输出；提高：离线删除边、线段树分治和可撤销带权并查集。若关系是在模 $3$ 意义下的类别差，不能直接把本模板的整数加减照搬：`potential`、`w` 和每次加减都要改成模 $3$ 代表元，并按题目定义统一方向。

**7. 坑**

差值方向固定为 `value[y]-value[x]`；方向写反会使合并式和查询错。每次差值累加、两点相减以及合并公式的中间值，都必须能由 `long long` 表示。

组合应用：差值约束可先离散化元素，再由带权并查集维护；在线判矛盾可用于检查方程组的一致性；与二分答案结合时，每次二分检查一批差值约束。注意该模板不能处理“边删除”或要求路径上每条边的明细。

**8. 一句话原理**

沿父亲路径累加差值，使并查集同时维护连通性和组内相对值。

## 5.21 离线树状数组 {#offline-fenwick}

**1. 它是做什么的**

有时所有查询都已给出，可以先排序再回答。例如给定点 `(1,2),(2,1),(2,2)`，询问横坐标不超过 2、纵坐标也不超过 2 的点有几个，答案是 3。这里两个坐标条件都要满足。

逐个查询都从头检查所有点或所有区间元素，会反复访问相同数据。若查询之间互不影响，可以把它们按某个坐标排序，让已经处理的数据只扫一次。

先把点和询问按横坐标排序，逐步加入横坐标合格的点；树状数组再统计其中纵坐标合格的点数。这类两个坐标同时满足大小条件的计数，常称为二维偏序。区间不同数和逆序对是后面介绍的另外两个应用。

**2. 变量在做什么**

离散化把很大或负数坐标换成从 1 开始的紧凑编号；相同坐标必须得到相同编号。二维计数的查询 `id` 用来把排序后的答案放回输入顺序。

本节先按 x 扫描，再用树状数组的 y 前缀统计，所以 BIT 下标代表纵坐标编号，不是点在输入中的顺序。后面的区间不同数改用数组位置作下标；逆序对则改用值的排名。

树状数组可看成维护一串数字：`add(pos,delta)` 改一个位置，`sumPrefix(pos)` 统计从 1 到该位置的总和。区间和用 `sumPrefix(r)-sumPrefix(l-1)` 得到。

| 名称 | 含义 |
|---|---|
| `Fenwick::n/bit` | 有效位置上界 `n` 与树状数组；`bit` 下标从 1 开始。 |
| `PointXY{x,y}` | 一个可重复计数的点坐标。 |
| `QueryXY{x,y,id}` | 询问右上界及原输入编号；`id` 须为 `0..q-1`。 |
| `RangeQuery{l,r,id}` | 1-based 闭区间及答案编号。 |
| `ys`、`rankOf` | 合并点和询问的 y 坐标后离散化；Fenwick rank 为 1-based。 |
| `last[value]` | 区间不同数扫描中，当前前缀内该值最后出现的位置。 |
| `values`、`rank` | 逆序对压缩值域；相同值映射到同一 rank。 |

**3. 函数在做什么**

二维偏序例子取点 `(1,2),(2,1),(2,2)`，查询 `(2,2)`。

1. 按 x 扫描，把所有 `x<=2` 的点加入 BIT。
2. y 排名为 1、2；前缀 2 中累计了三次加一。
3. 读出 3。加入条件保证 `px<=X`，前缀条件保证 `py<=Y`，故每个满足两条件的点恰计一次，重复点按重数计。

区间不同数例子 `a=[7,3,7]`、查询 `[2,3]`。扫到位置 3 时先把 7 在位置 1 的旧标记减掉，再在位置 3 加标记；`sum(3)-sum(1)` 得到位置 2、3 上的两个标记，即两种数。

每种值在当前前缀只有最后一次出现位置有标记，所以区间和正好数出最后位置落在 `[l,r]` 的值。

逆序对例子 `[3,1,2]` 从右向左扫：遇到 2、1 时右侧都没有比它更小的值；遇到 3 时右侧有 1、2 两个更小值，因此总数为 2。查询 `rank-1` 排除相等值，正好对应严格条件 `i<j` 且 `a[i]>a[j]`。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `Fenwick(n)` | n 是最大可用下标；n 可以为 0。 返回：无（构造函数）。 | 建立全零树状数组。 |
| `add(pos,delta)` | pos 必须在 1..n。 返回：void。 | 把 bit[pos..] 对应的前缀结构都增加 delta。 |
| `sumPrefix(pos)` | pos 在 0..n。 返回：ll，原数组下标 1..pos 的元素和。 | 只读，不修改结构。 |
| `rangeSum(l,r)` | l、r 为 1-based 合法闭区间。 返回：ll，该区间和。 | 只读，不修改结构。 |
| `countDominated` | points 为二维点，queries 的 id 必须为 0..queries.size()-1。 返回：vector&lt;ll&gt;，各询问的支配点数。 | 只读，不修改结构。 |
| `distinctInRanges` | a 是 1-based 数组，a[0] 不参与；queries 中 id 连续且区间合法。 返回：vector&lt;int&gt;，每个闭区间的不同元素数。 | 排序 queries 副本并维护局部 BIT；不修改输入数组。 |
| `countInversions(a)` | a 是 0-based 输入数组。 返回：ll，满足 i&lt;j 且 a[i]&gt;a[j] 的逆序对数量。 | 只读，不修改输入 a。 |

复杂度：树状数组操作 $O(\log n)$。二维偏序含 y 坐标压缩、点和询问排序，时间 $O((p+q)\log(p+q+1))$，空间 $O(p+q)$。

区间不同数为 $O(n\log(n+1)+q\log(q+1)+q\log(n+1))$，分别对应最后出现位置维护、询问排序和查询，空间 $O(n+q)$。逆序对为 $O(n\log(n+1))$，空间 $O(n)$。

**4. 怎么调用**

完整模板如下。代码中每个函数的参数、返回和副作用契约见其定义前注释。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Fenwick {
    int n;
    vector<ll> bit;
    // 参数：n 是最大可用下标；n 可以为 0。
    // 返回：无（构造函数）。
    // 效果：建立全零树状数组。
    explicit Fenwick(int n) : n(n), bit(n + 1, 0) { assert(n >= 0); }
    // 参数：pos 必须在 1..n。
    // 返回：void。
    // 效果：把 bit[pos..] 对应的前缀结构都增加 delta。
    void add(int pos, ll delta) {
        assert(1 <= pos && pos <= n);
        for (int i = pos; i <= n; i += i & -i) bit[i] += delta;
    }
    // 参数：pos 在 0..n。
    // 返回：ll，原数组下标 1..pos 的元素和。
    // 效果：只读，不修改结构。
    ll sumPrefix(int pos) const {
        assert(0 <= pos && pos <= n);
        ll answer = 0;
        for (int i = pos; i > 0; i -= i & -i) answer += bit[i];
        return answer;
    }
    // 参数：l、r 为 1-based 合法闭区间。
    // 返回：ll，该区间和。
    // 效果：只读，不修改结构。
    ll rangeSum(int l, int r) const { return sumPrefix(r) - sumPrefix(l - 1); }
};

struct PointXY { ll x, y; };
struct QueryXY { ll x, y; int id; };
// 参数：points 为二维点，queries 的 id 必须为 0..queries.size()-1。
// 返回：vector<ll>，各询问的支配点数。
// 效果：只读，不修改结构。
vector<ll> countDominated(const vector<PointXY>& points, vector<QueryXY> queries) {
    vector<ll> ys;
    ys.reserve(points.size() + queries.size());
    for (const auto& p : points) ys.push_back(p.y);
    for (const auto& q : queries) ys.push_back(q.y);
    sort(ys.begin(), ys.end());
    ys.erase(unique(ys.begin(), ys.end()), ys.end());
    // 参数：y 是输入点或查询的纵坐标。
    // 返回：int，离散化后 1-based 的位置。
    // 效果：只读，不修改结构；不修改 ys。
    auto rankOf = [&](ll y) -> int {
        return int(lower_bound(ys.begin(), ys.end(), y) - ys.begin()) + 1;
    };
    vector<PointXY> sortedPoints = points;
    // 参数：a、b 为两个平面点。
    // 返回：a.x < b.x。
    // 效果：只读比较；同 x 点任意顺序均可。
    sort(sortedPoints.begin(), sortedPoints.end(),
         [](const PointXY& a, const PointXY& b) { return a.x < b.x; });
    // 参数：a、b 为两个二维询问。
    // 返回：a.x < b.x。
    // 效果：只读比较；同 x 的点会在回答前全部加入。
    sort(queries.begin(), queries.end(),
         [](const QueryXY& a, const QueryXY& b) { return a.x < b.x; });
    Fenwick fw((int)ys.size());
    vector<ll> answer(queries.size());
    size_t ptr = 0;
    for (const auto& q : queries) {
        // <= 保证 px==q.x 的点先进入；重复点会被重复计数。
        while (ptr < sortedPoints.size() && sortedPoints[ptr].x <= q.x) {
            fw.add(rankOf(sortedPoints[ptr].y), 1);
            ++ptr;
        }
        int upto = int(upper_bound(ys.begin(), ys.end(), q.y) - ys.begin());
        answer[q.id] = fw.sumPrefix(upto);
    }
    return answer;
}

struct RangeQuery { int l, r, id; };
// 参数：a 是 1-based 数组，a[0] 不参与；queries 中 id 连续且区间合法。
// 返回：vector<int>，每个闭区间的不同元素数。
// 效果：排序 queries 副本并维护局部 BIT；不修改输入数组。
vector<int> distinctInRanges(const vector<int>& a, vector<RangeQuery> queries) {
    int n = (int)a.size() - 1;
    // 按右端点升序处理；右端点相等时按左端点升序只是稳定的次序选择。
    // 参数：u、v 是两个区间查询。
    // 返回：bool，按 r 升序、再按 l 升序比较。
    // 效果：比较器只读查询；sort 据此原地排序 queries。
    sort(queries.begin(), queries.end(),
         [](const RangeQuery& u, const RangeQuery& v) {
             return u.r != v.r ? u.r < v.r : u.l < v.l;
         });
    Fenwick fw(n);
    map<int, int> last; // 用 map 避免哈希碰撞；值的范围无需预先知道。
    vector<int> answer(queries.size());
    int right = 0;
    for (const auto& q : queries) {
        while (right < q.r) {
            ++right;
            auto it = last.find(a[right]);
            if (it != last.end()) fw.add(it->second, -1);
            fw.add(right, 1);
            last[a[right]] = right;
        }
        answer[q.id] = (int)fw.rangeSum(q.l, q.r);
    }
    return answer;
}
// 参数：a 是 0-based 输入数组。
// 返回：ll，满足 i<j 且 a[i]>a[j] 的逆序对数量。
// 效果：只读，不修改输入 a。
ll countInversions(const vector<ll>& a) {
    vector<ll> values = a;
    sort(values.begin(), values.end());
    values.erase(unique(values.begin(), values.end()), values.end());
    Fenwick fw((int)values.size());
    ll answer = 0;
    for (auto it = a.rbegin(); it != a.rend(); ++it) {
        int rank = int(lower_bound(values.begin(), values.end(), *it) - values.begin()) + 1;
        answer += fw.sumPrefix(rank - 1); // 已见元素中严格小于当前值，正好构成当前左端点的逆序对。
        fw.add(rank, 1);
    }
    return answer;
}
```

调用示例：

```text
vector<PointXY> points = {{2, 2}, {2, 2}, {3, 1}};
auto dominated = countDominated(points, {{2, 2, 0}});
assert(dominated[0] == 2);
vector<int> a = {0, 7, 3, 7};
auto distinct = distinctInRanges(a, {{2, 3, 0}});
assert(distinct[0] == 2);
auto inversions = countInversions({3, 1, 2});
assert(inversions == 2);
```

**5. 要改哪里**

二维偏序若 x 条件严格小于，把加入条件 `point.x <= q.x` 改为 `<`；若 y 条件严格小于，把 `upper_bound` 改为 `lower_bound`。

区间不同数必须先删旧最后位置，再加新位置；不能给每个位置永久加一。逆序对统计严格 `>` 时查 `rank-1`；若要统计相等关系，先明确题意再调整边界。

看到“所有点左下方有多少点”可考虑二维偏序；看到区间有多少种数可考虑右端点排序；看到 `i<j` 且大小关系可考虑离散化加 BIT。进阶可学三维偏序、CDQ 分治，并比较区间不同数用莫队的取舍。

**6. 自检**

第 4 部分调用中的重复点 `(2,2)` 应计两次；数组 `[7,3,7]` 的 `[2,3]` 区间有 2 个不同值；`[3,1,2]` 有 2 个严格逆序对。把所有值改成相等时，逆序对应为 0，任意非空区间的不同数为 1。

**分层练习：** 入门：静态单点修改、区间和与逆序对；进阶：二维矩形左下计数、区间不同数；提高：三维偏序、带时间维度的修改查询和 CDQ 分治。要特别测试空询问列表、相同 `x/y` 的重复点、全相同数组和全逆序数组。

**7. 坑**

等号由扫描条件及 `lower_bound/upper_bound` 决定；重复点按重数计，查询 id 和闭区间范围须合法。

组合应用：二维偏序还能扩展到 CDQ 分治、三维偏序和扫描线；区间不同数可与莫队比较取舍；逆序对可作为归并排序、Fenwick 或线段树的练习。值域很大时先坐标压缩，重复值必须保留相同 rank。

**8. 一句话原理**

排序把一个维度变成扫描进度，树状数组维护剩余维度的前缀统计。

## 5.22 莫队算法 {#mo-algorithm}

**1. 它是做什么的**

给定一个数组，有很多次询问，每次给出一个区间，要求统计其中有多少种不同的数。例如：

```plain
数组：[1, 2, 1, 3, 2]
询问 [1,3]：里面是 [1,2,1]，不同的数有 1、2，答案是 2。
询问 [2,5]：里面是 [2,1,3,2]，不同的数有 1、2、3，答案是 3。
```

最直接的办法是每次重新扫描询问区间，统计出现过哪些数。如果数组和询问都很多，这些扫描会反复处理同一批元素。

莫队的做法是：**保留上一个区间的统计结果，移动左右端点，把它调整成下一个区间。** 从 `[1,3]` 调整到 `[2,5]`，只需要加入位置 4、5，再移除位置 1，不必重新扫描整个 `[2,5]`。

如果询问顺序很乱，左右端点仍可能来回横跨整个数组。莫队因此会先重新排列询问，让相邻询问尽量共享已有的统计结果。全部处理完后，再按原来的询问顺序输出答案。先读入全部询问、再统一计算，称为“离线处理”。本节处理过程中数组保持不变。

**2. 变量在做什么**

理解莫队时，先分清两个东西：**当前维护的是哪个区间，以及这个区间里有什么。**

| 名称 | 含义 |
|---|---|
| `left`、`right` | 当前已经统计好的闭区间 `[left,right]`。 |
| `frequency[v]` | 值编号 `v` 在当前区间内出现了多少次。 |
| `distinct` | 当前区间里有多少种不同的值，也就是多少个频次大于 0。 |
| `compressed[i]` | 原数组位置 `i` 上的值经过离散化后的编号。 |
| `MoQuery::l,r` | 某次询问要求的区间，不是当前窗口的端点。 |
| `MoQuery::id` | 询问在输入中的编号，用来恢复答案顺序。 |
| `blockLength` | 左端点分块时，每块包含的位置数，至少为 1。 |
| `answer[id]` | 原编号为 `id` 的询问答案。 |

其中，`frequency` 按**值编号**访问，`compressed` 按**数组位置**访问：

```plain
位置 i → compressed[i] 得到值编号 → frequency[值编号] 得到出现次数
```

离散化只是把可能很大的原值换成紧凑编号。例如原值为 `[100,500,100]`，可以编号为 `[0,1,0]`。相同的数仍使用相同编号，所以不同数的数量不会改变。为了便于手算，下面的频次表直接写原值；代码实际使用从 0 开始的离散编号。

**3. 函数在做什么**

对“区间不同数”这个问题，最重要的是加入、删除时如何更新答案。

加入一个值时，若频次从 0 变成 1，就多了一种数，`distinct` 加一；原来已经出现过，就只增加频次。

删除一个值时，若频次从 1 变成 0，就少了一种数，`distinct` 减一；删除后仍出现至少一次，答案不变。

例如，从 `[1,3]` 移动到 `[2,5]`：

| 操作 | 当前区间 | 非零频次 | `distinct` |
|---|---|---|---|
| 已经维护好 `[1,3]` | `[1,3]` | `1:2，2:1` | 2 |
| 加入位置 4 的值 3 | `[1,4]` | `1:2，2:1，3:1` | 3 |
| 加入位置 5 的值 2 | `[1,5]` | `1:2，2:2，3:1` | 3 |
| 删除位置 1 的值 1 | `[2,5]` | `1:1，2:2，3:1` | 3 |

删除位置 1 时，值 1 仍在位置 3 出现，所以答案不能减一。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `MoDistinct(a)` | 输入 1-based 数组；构造函数无返回值。 | 将原值离散化，准备频次数组和块长。 |
| `addValue` | 输入值编号和答案的引用；返回 `void`。 | 增加频次，必要时增加不同数数量；内部调用。 |
| `removeValue` | 输入值编号和答案的引用；返回 `void`。 | 减少频次，必要时减少不同数数量；被删除的贡献必须已经在窗口中。 |
| `solve(queries)` | 输入全部询问；返回按原编号排列的答案数组。 | 清空统计、排序询问，然后移动窗口并记录答案；可以重复调用。 |

`solve` 开始时令 `left=1,right=0`，表示尚未加入任何元素的空区间。之后始终保持：频次表和 `distinct` 恰好对应当前 `[left,right]` 内的元素。向左扩展、向右扩展都是加入；向左收缩、向右收缩都是删除。本节统计不依赖元素排列，因此两端可以共用增删函数。

询问先按左端点所在块排序，同一块内再按右端点排序；相邻块交替使用升序、降序，减少右端点折返。当前代码使用 `l/blockLength` 划分块，首块稍短不影响复杂度。

设数组长度为 `n`、询问数为 `q`、块长为 `B`，端点移动次数上界为 $O(n^2/B+qB)$：右端点在每个左端点块内沿一个方向扫描，合计约为 `n²/B`；同块内左端点每次最多移动约 `B`，合计约为 `qB`。蛇形排序改善常数，不改变这个上界。

本模板取 `B≈√n`，每次增删为常数时间，再计入离散化和询问排序，总时间为 $O((n+q)\sqrt n+n\log(n+1)+q\log(q+1))$，空间为 $O(n+q)$。若维护别的统计需要更昂贵的增删操作，移动部分还须乘上单次增删的代价。

**4. 怎么调用**

将 `MoQuery` 和 `MoDistinct` 模板放在业务代码之前。数组下标 0 占位；每个查询满足 `1<=l<=r<=n`，`id` 恰好覆盖 `0..q-1`。空查询列表可以直接返回空答案；没有有效数组元素时也不能给出非空区间查询。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct MoQuery { int l, r, id; };

class MoDistinct {
    int n;
    vector<int> compressed;
    int blockLength;
    vector<int> frequency;
    // 参数：value 是已离散化的值编号。
    // 返回：void。
    // 效果：把它加入当前窗口并更新 distinct 的引用值。
    void addValue(int value, int& distinct) {
        if (frequency[value]++ == 0) ++distinct;
    }
    // 参数：value 是已离散化的值编号。
    // 返回：void。
    // 效果：它必须当前至少出现一次，再删除并更新 distinct。
    void removeValue(int value, int& distinct) {
        assert(frequency[value] > 0);
        if (--frequency[value] == 0) --distinct;
    }

public:
    // 参数：a 为 1-based 静态数组。
    // 返回：无（构造函数）。
    // 效果：压缩其值并建立计数表，后续 solve 不修改 a 的逻辑内容。
    explicit MoDistinct(const vector<int>& a) : n((int)a.size() - 1) {
        assert(n >= 0);
        vector<int> values(a.begin() + (n ? 1 : 0), a.end());
        sort(values.begin(), values.end());
        values.erase(unique(values.begin(), values.end()), values.end());
        compressed.assign(n + 1, 0);
        for (int i = 1; i <= n; ++i)
            compressed[i] = int(lower_bound(values.begin(), values.end(), a[i]) - values.begin());
        frequency.assign(values.size(), 0);
        blockLength = max(1, (int)sqrt(max(1, n)));
    }
    // 参数：queries 的 l、r 合法且 id 连续。
    // 返回：vector<int>，各区间不同数，输入查询顺序不影响结果。
    // 效果：每次调用都会清空计数，因此可重复调用；数组本身必须保持静态。
    vector<int> solve(vector<MoQuery> queries) {
        for (int& x : frequency) x = 0;
        // 先按左端点所在块，再按右端点蛇形排序；返回严格弱序比较结果。
        // 参数：a、b 是两个闭区间查询。
        // 返回：bool，按分块和奇偶蛇形顺序比较。
        // 效果：只读 blockLength；sort 据此原地排序 queries。
        sort(queries.begin(), queries.end(), [this](const MoQuery& a, const MoQuery& b) {
            int ba = a.l / blockLength, bb = b.l / blockLength;
            if (ba != bb) return ba < bb;
            return (ba & 1) ? a.r > b.r : a.r < b.r;
        });
        vector<int> answer(queries.size());
        int left = 1, right = 0, distinct = 0;
        for (const MoQuery& q : queries) {
            while (left > q.l) addValue(compressed[--left], distinct);
            while (right < q.r) addValue(compressed[++right], distinct);
            while (left < q.l) removeValue(compressed[left++], distinct);
            while (right > q.r) removeValue(compressed[right--], distinct);
            answer[q.id] = distinct;
        }
        return answer;
    }
};
```

先用本节贯穿的例子验证调用。下面的大括号仅用于让这一示例拥有独立的局部变量：

```text
{
    vector<int> a = {0, 1, 2, 1, 3, 2};
    vector<MoQuery> queries = {{1, 3, 0}, {2, 5, 1}};
    MoDistinct mo(a);
    vector<int> answer = mo.solve(queries);
    assert(answer[0] == 2 && answer[1] == 3);
}
```

业务代码只需要构造对象并调用 `solve`。即使处理顺序发生改变，结果仍写入 `answer[q.id]`。下面保留另一组较短的调用，检查区间 `[1,2]` 和 `[2,4]`：

```text
vector<int> a = {0, 1, 2, 1, 3};
MoDistinct mo(a);
auto answer = mo.solve({{1, 2, 0}, {2, 4, 1}});
assert(answer[0] == 2 && answer[1] == 3);
```

**5. 要改哪里**

换成其他区间统计时，先问：已经知道当前区间的状态，加入或删除一个值时，需要怎样调整？

例如，要求所有值的“出现次数平方和” $S=\sum_v frequency[v]^2$。某个值原来出现 `f` 次，加入后贡献增加 $(f+1)^2-f^2=2f+1$。所以先执行 `S += 2*f+1`，再增加频次。删除时先减去 `2*f-1`，再减少频次。

窗口移动和排序逻辑可以保留，需要改的是统计状态、增删函数，以及记录答案的位置。平方和可能很大，应使用 `long long`。若要求最高频次，则还需要记录“有多少种值恰好出现 f 次”等状态，不能只替换一个答案变量。

适合莫队的模型通常是“静态数组、大量区间询问、单点增删可以维护”。区间不同数也能用离线树状数组解决；遇到难以按右端点单向扫描、但可以双向增删的统计，再考虑莫队。若统计依赖顺序，例如逆序对，还要区分从左端或右端增删的贡献。

数组有修改时，需要学习带修改莫队；树路径查询可以学习树上莫队；删除难做时可继续了解回滚莫队。无法快速维护单点增删的目标，不能直接套这份模板。

**6. 自检**

先检查几组容易手算的输入：全相等数组 `[1,1,1]` 的任意非空区间答案都是 1；互不相同数组 `[1,2,3]` 的答案等于区间长度；单点区间答案为 1。

本节例子的 `[1,3]`、`[2,5]` 应分别得到 2、3。同一区间重复询问结果一致，打乱询问顺序后按 `id` 还原的答案也应一致。重复调用 `solve` 会清空频次，不应继承上一次状态。

对拍时生成小数组，暴力扫描每个区间，用 `set` 统计不同数，与莫队逐项比较；特别加入相隔很远的两个窗口，检查扩展、收缩顺序。

**7. 坑**

- 删除一次就减少不同数数量：只有频次从 1 变成 0 时，答案才减少。
- 把位置当作值编号：移动到位置 `i` 时，应更新 `frequency[compressed[i]]`。
- 排序后直接顺序输出：必须通过 `id` 保存答案，且编号不能重复或越界。
- 随意交换四个移动循环：本模板先扩展窗口，再收缩窗口，保证删除的是已经加入的贡献。
- 使用过程中修改原数组的逻辑值：对象保存的是构造时离散化后的数组，后续查询不会自动反映修改。
- 用于必须立即回答、不能重排的询问：这不满足普通莫队的使用条件。

**8. 一句话原理**

重排询问后复用上一个区间的统计结果，只在左右端点移动时加入或删除元素。

## 5.23 笛卡尔树 {#cartesian-tree}

**1. 它是做什么的**

数组 `[3,1,4,2]` 中，下标 2 的值 1 是整个区间最小值。若对许多区间各自扫描，区间常会重复比较同一批元素。笛卡尔树把“下标从左到右的顺序”和“最小值在上层”的关系放进同一棵树，方便之后沿树处理区间；例如下标 `[2,4]` 中最小值为 1，它恰好位于本例整棵树的根；其他区间的最小值未必是整树根。

这组数据的树形结果如下，节点标的是“下标:值”：

```plain
       2:1
      /   \
   1:3     4:2
           /
         3:4
```

从左到右中序读下标仍是 `1,2,3,4`；每个父节点的值都不大于孩子。

**2. 变量在做什么**

节点编号是原数组下标，节点的大小比较才看 `a[u]`。这两件事不能混：中序顺序由下标保证，堆序由值保证；值相同的节点也仍是不同位置。区间最小值并列时，模板规定靠左位置优先作为该区间的最小值归属点。

| 名称 | 含义 |
|---|---|
| `root` | 树根的原数组下标，范围 `1..n`。 |
| `left[u]`,`right[u]` | 下标 `u` 的左右孩子；0 表示没有孩子。 |
| `parent[u]` | 下标 `u` 的父亲；根和不存在的结点均为 0。 |
| `stack` | 从底到顶对应值非递减的候选祖先下标。 |
| `last` | 本轮最后弹出的子树根；它成为新节点的左儿子。 |

**3. 函数在做什么**

按 `[3,1,4,2]` 手算建树，栈里记录下标：

| 读入 | 栈顶处理 | 新连边与栈 |
|---|---|---|
| 下标 1，值 3 | 无可弹出 | 栈 `[1]`。 |
| 下标 2，值 1 | 弹出下标 1，令 `last=1` | `left[2]=1`；栈 `[2]`，2 是根候选。 |
| 下标 3，值 4 | 1 不大于 4，不弹 | `right[2]=3`；栈 `[2,3]`。 |
| 下标 4，值 2 | 弹出 3，因为 `4>2` | `last=3`，令 `right[2]=4`、`left[4]=3`；栈 `[2,4]`。 |

新值比栈顶小时，栈顶对应的整棵候选子树都要转到新节点左侧；栈里剩下的最近节点则把新节点接到右边。每次只改这一条右侧边，因此中序顺序保持原下标顺序。末尾栈底是根。对例子中序得到下标 `1,2,3,4`，堆序也成立。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `buildMinCartesian(a)` | `a` 是下标 1..n 的非空数组；返回 `CartesianTree`。 | 建立中序下标为 1..n、满足最小堆序的树；严格用 `>` 弹栈，所以相等时左侧节点优先。 |

每个下标入栈一次、最多出栈一次，建树时间 $O(n)$，空间 $O(n)$。

**4. 怎么调用**

完整模板如下。代码中每个函数的参数、返回和副作用契约见其定义前注释。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct CartesianTree {
    int root = 0;
    vector<int> left, right, parent;
};
// 参数：a 是下标 1..n 的非空数组。
// 返回：CartesianTree，中序下标为 1..n 且满足最小堆性质的树。
// 效果：相等值不弹栈，因此相等最小值中下标较小者为祖先。
CartesianTree buildMinCartesian(const vector<ll>& a) {
    int n = (int)a.size() - 1;
    assert(n >= 1);
    CartesianTree result;
    result.left.assign(n + 1, 0);
    result.right.assign(n + 1, 0);
    result.parent.assign(n + 1, 0);
    vector<int> stack;
    for (int i = 1; i <= n; ++i) {
        int last = 0;
        while (!stack.empty() && a[stack.back()] > a[i]) {
            last = stack.back();
            stack.pop_back();
        }
        if (!stack.empty()) result.right[stack.back()] = i;
        result.left[i] = last;
        stack.push_back(i);
    }
    result.root = stack.front();
    for (int u = 1; u <= n; ++u) {
        if (result.left[u]) result.parent[result.left[u]] = u;
        if (result.right[u]) result.parent[result.right[u]] = u;
    }
    return result;
}
```

调用示例：

```text
vector<ll> a = {0, 3, 1, 4, 2};
CartesianTree tree = buildMinCartesian(a);
assert(tree.root == 2);
assert(tree.left[2] == 1 && tree.right[2] == 4);
// 对完整验证，另做中序遍历并核对结果为 1,2,3,4。
```

**5. 要改哪里**

若要让相等最小值中更靠右者优先，把弹栈比较从 `>` 改成 `>=`；等值旧节点就会被弹出，较右节点成为祖先。最大值版本建立最大笛卡尔树并同步调整比较符。查询一般区间 `[l,r]` 时，区间最小值位于两端点 l、r 在笛卡尔树上的最近公共祖先（LCA）：树按下标划分连续区间，父节点又不会比后代更大。应先预处理 LCA，而不能对任意区间直接读取整树根。静态 RMQ 也可用稀疏表；值会在线修改时通常改用线段树，因为本树不支持值修改。

对每个节点 `i`，设左右子树大小为 `L`、`R`。最小值归给 `i` 的连续子数组，可以从 `i` 向左跨过左子树中任意 `0..L` 个位置，并向右跨过右子树中任意 `0..R` 个位置，因此有 `(L+1)(R+1)` 种。相等值按左侧优先归属，避免一个区间重复记给两个相等最小值。所有子数组最小值之和为 `sum(a[i]*(L+1)*(R+1))`；乘积和总和需选够宽的整数类型。

识别线索是：问题既要求保留原下标顺序，又反复用区间最值作分治枢纽或统计子数组贡献。

**6. 自检**

数组 `[3,1,4,2]` 的根为下标 2，左儿子为 1、右儿子为 4；中序遍历须恢复下标 `[1,2,3,4]`。全相等数组在严格 `>` 弹栈规则下形成向右的链，根为最左位置。

**分层练习：** 入门：验证中序和堆性质；进阶：用笛卡尔树加 LCA 做静态 RMQ；提高：所有子数组最小值之和及重复最值的贡献分配。

**7. 坑**

比较条件决定相等值归属；本模板严格用 `>`，较左相等最小值优先；数组不可为空。

组合应用：笛卡尔树的父子关系可让某些子数组贡献转为子树贡献；建树后给每个节点做 DFS 序，再用 LCA 回答 RMQ。大数组递归 DFS 可能爆栈，应改写为显式栈或使用安全的递归深度策略。

**8. 一句话原理**

单调栈把原序列中序次序和最值堆序编码为一棵树。

## 5.24 李超线段树 {#li-chao-tree}

**1. 它是做什么的**

已加入直线 `y=x`、`y=-x+4`，要回答 `x=0,2,5` 的最大值，依次是 `4,2,5`。每次都逐条代入会在直线很多、查询很多时反复计算。

李超树把横坐标范围切成小段，每段留下当前的代表直线；可能在某一侧胜出的竞争线只往那一侧传。这样以后只沿查询坐标所在的路径比较少量直线。

**2. 变量在做什么**

`left/right/mid` 是排序去重后坐标的下标，不是原始横坐标值；真正代入直线计算的是 `xs[index]`。在分配到该节点的候选线中，节点保留中点胜出的直线；其他候选线可能只在一侧更优。

| 名称 | 含义 |
|---|---|
| `Line{k,b}` | 斜率与截距，均为 `long long`；代表 `y=kx+b`。 |
| `xs` | 排序去重后的可查询横坐标；查询只能使用其中的值。 |
| `tree[node]` | 节点当前保留的直线。 |
| `used[node]` | 节点是否已经有直线。 |
| `left/right/mid` | 离散坐标下标的区间和中点。 |
| `position` | 查询横坐标在 `xs` 中的下标。 |

**3. 函数在做什么**

继续看 `x=0,2,5`，一步步插入和查询：

1. 插入 `y=x`：根节点原来为空，直接保存它。
2. 插入 `y=-x+4`：中点对应 `x=2`，两条线都等于 2，根保留原线。
3. 判断另一条线的去向：左端 `x=0` 时新线值 4 大于原线值 0；右端 `x=5` 时新线值 -1 小于原线值 5。因此只把它送入左孩子。
4. 查询 `x=0`：沿根到左叶的路径比较，答案是 4。查询 `x=2` 或 `x=5` 时，同样只比较各自路径上的线，得到 2、5。

插入时交换以后，节点线在中点不劣，待下传线在中点不可能胜出。两条直线至多相交一次，若待下传线还可能获胜，只会在某个端点仍胜出的那一侧；代码按左右端点判断并至多递归一个孩子。这就是 `swap` 后必须用新的 `tree[node]` 和剩余 `line` 判断方向的原因。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `value` | 横坐标；返回 `i128` 函数值。 | 精确计算当前直线，不修改它。 |
| `LiChaoMax` | 可查询坐标集合；构造空树。 | 排序去重坐标，分配节点空间；空集合也可构造。 |
| `insert` | 节点区间和待插线；返回 void。 | 中点保留较优线，竞争线递归到可能胜出的一侧。 |
| `indexOf` | 合法查询坐标；返回离散下标。 | 二分查找；坐标不在集合时断言失败。 |
| `queryNode` | 节点区间和查询位置；返回可选最大值。 | 汇总根到叶路径上的直线值；空路径结果为空。 |
| `addLine` | 斜率、截距；返回 void。 | 加入整条线；空坐标集合时忽略。 |
| `query` | 已声明坐标；返回 `optional<i128>`。 | 查询所有已加入直线的最大值；没有直线时为空。 |

令 `m` 为不同查询坐标数，插线和单点查询均为 $O(\log m)$，空间 $O(m)$。当前横坐标需预先给出；任意整数域在线查询需改成动态节点树。

**4. 怎么调用**

完整模板如下。代码中每个函数的参数、返回和副作用契约见其定义前注释。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using i128 = __int128_t;

struct LiChaoMax {
    struct Line {
        ll k = 0, b = 0;
        // 参数：x 是查询横坐标；k、b 是当前直线字段。
        // 返回：i128，直线在 x 处的精确值 k*x+b。
        // 效果：只读，不修改直线。
        i128 value(ll x) const { return (i128)k * x + b; }
    };

    vector<ll> xs;
    vector<Line> tree;
    vector<char> used;
    // 参数：xs 是允许查询的横坐标集合，可以为空。
    // 返回：无（构造函数）。
    // 效果：保存排序去重后的所有合法查询横坐标，并建立空节点树。
    explicit LiChaoMax(vector<ll> xs) : xs(std::move(xs)) {
        sort(this->xs.begin(), this->xs.end());
        this->xs.erase(unique(this->xs.begin(), this->xs.end()), this->xs.end());
        tree.assign(max(1, 4 * (int)this->xs.size()), Line{});
        used.assign(tree.size(), false);
    }

private:
    // 参数：node 对应树节点；left、right 是其离散下标区间；line 是待插入直线。
    // 返回：void。
    // 效果：修改节点树，将 line 存入当前节点或唯一可能继续获胜的子树。
    void insert(int node, int left, int right, Line line) {
        if (!used[node]) {
            tree[node] = line;
            used[node] = true;
            return;
        }
        int mid = (left + right) / 2;
        if (line.value(xs[mid]) > tree[node].value(xs[mid]))
            swap(line, tree[node]);
        if (left == right) return;
        // swap 后 tree[node] 在中点不劣，line 才是需要继续寻找胜点的候选。
        bool lineBetterAtLeft = line.value(xs[left]) > tree[node].value(xs[left]);
        bool lineBetterAtRight = line.value(xs[right]) > tree[node].value(xs[right]);
        if (lineBetterAtLeft)
            insert(node * 2, left, mid, line);
        else if (lineBetterAtRight)
            insert(node * 2 + 1, mid + 1, right, line);
    }
    // 参数：x 必须属于构造时给出的查询坐标集合。
    // 返回：int，x 在去重坐标数组 xs 中的下标。
    // 效果：二分查找 xs；参数不在集合中时断言失败。
    int indexOf(ll x) const {
        auto it = lower_bound(xs.begin(), xs.end(), x);
        assert(it != xs.end() && *it == x);
        return int(it - xs.begin());
    }
    // 参数：node、left、right 是当前节点及其区间；position 是查询离散下标。
    // 返回：optional<i128>，该路径上直线的最大值；没有直线时为空。
    // 效果：只读，不修改结构。
    optional<i128> queryNode(int node, int left, int right, int position) const {
        optional<i128> answer;
        if (used[node]) answer = tree[node].value(xs[position]);
        if (left == right) return answer;
        int mid = (left + right) / 2;
        optional<i128> child = position <= mid
            ? queryNode(node * 2, left, mid, position)
            : queryNode(node * 2 + 1, mid + 1, right, position);
        if (!child) return answer;
        if (!answer || *child > *answer) return child;
        return answer;
    }

public:
    // 参数：k、b 分别是新直线 y=kx+b 的斜率和截距。
    // 返回：void。
    // 效果：空横坐标集合时忽略插入，其他情况修改树。
    void addLine(ll k, ll b) {
        if (!xs.empty()) insert(1, 0, (int)xs.size() - 1, Line{k, b});
    }
    // 参数：x 必须属于构造时坐标集合。
    // 返回：optional<i128>，所有已加入直线在 x 处的最大值，空集合返回 nullopt。
    // 效果：只读，不修改结构。
    optional<i128> query(ll x) const {
        if (xs.empty()) return nullopt;
        return queryNode(1, 0, (int)xs.size() - 1, indexOf(x));
    }
};
```

调用示例：

```text
LiChaoMax lc({0, 2, 5});
lc.addLine(1, 0);
lc.addLine(-1, 4);
auto best = lc.query(2);
assert(best.has_value() && *best == 2);
auto missing = lc.query(0);
assert(missing.has_value() && *missing == 4);
```

**5. 要改哪里**

斜率优化 DP 常能整理为 `dp[i]=max_j(m_j*x_i+b_j)`。例如 `dp[i]=max_j{dp[j]+a[j]*x_i+c[j]}`，把已求出的状态 j 变成斜率 `a[j]`、截距 `dp[j]+c[j]` 的直线，在 `x_i` 查询。先算出 `dp[i]`，再插入它供后续使用，避免错误使用尚未得到的状态。

求最小值时，可以对每条线的斜率、截距取反，用最大值树查询，再将结果取反。求负数前先转成 `i128`，避免 `LLONG_MIN` 取反溢出；当前字段仍是 `long long`，取反后的系数还必须能放回该类型，否则应同时扩展 `Line` 字段和 `addLine` 参数。

若斜率和查询横坐标都单调，可进一步比较凸包优化的实现。若查询坐标无法预先给出，需改成动态坐标域；若一条线只在某段横坐标有效，需增加区间插线逻辑，不能直接使用本节整线插入。

**6. 自检**

**手算小例子：** 先加入 `y=x`，再加入 `y=-x+4`，查询 `x=0,2,5` 得到 `4,2,5`。两线在 `x=2` 相等，李超树在中点保留哪一条都不影响答案；若再加入平行线 `y=x+3`，它会在所有查询点压过 `y=x`，而无需特殊分支。

**分层练习：** 入门：固定横坐标集合上的直线最大值；进阶：斜率优化 DP、平行线和负坐标；提高：区间加线、持久化李超树和动态坐标域。

**7. 坑**

- 查询 x 必须在构造时给出的坐标集中；离散化保持坐标大小关系，但求值仍要用原坐标。
- 中点交换后要用交换后的节点线和剩余线判断左右方向，不能继续用旧比较结果。
- 本模板只插入直线，不支持删除；空坐标集会忽略插入，查询返回空值。
- 斜率、截距和坐标是 `long long`，仅求值提升为 `__int128`；这并不表示构造出的 DP 系数可以任意大。
- 平行线由比较自然保留截距较大者；负数和重复坐标可以输入。
- `optional` 为空表示尚无有效直线，不能直接解引用；输出 `i128` 要另写十进制转换，不能直接交给 `cout`。

**8. 一句话原理**

两条直线至多交一次，节点保留中点胜者并沿可能获胜的方向下传另一条线。

## 5.25 差分 + GCD 线段树 {#difference-gcd-tree}

**1. 它是做什么的**

给数组 `[6,10,14,15]` 的第 2、3 项各加 5，再查询第 2 到第 4 项的 GCD。更新后是 `[6,15,19,15]`，答案是 `gcd(15,19,15)=1`。

直接做法要逐项改区间，再逐项求 GCD；长区间每次都要走很多项。差分把区间加变成最多两个位置的变化；查询时只需还原左端原值，并合并后续差分的 GCD。

**2. 变量在做什么**

`a[i]` 是原数组的实际值，`diff[i]` 不是另一个待查询数组的原值，而是相邻两个原值的差。原值靠差分前缀和还原；区间内变化则由这些差值的 GCD 概括。

| 名称 | 含义 |
|---|---|
| `n` | 原数组长度；所有公开区间是 1-based 闭区间。 |
| `diff[i]` | `b[1]=a[1]`，`b[i]=a[i]-a[i-1]`。 |
| `bit` | Fenwick 树，维护 `diff` 前缀和；`sumBit(i)` 还原 `a[i]`。 |
| `seg` | GCD 线段树，叶子为 `|diff[i]|`，内部为儿子 GCD。 |
| `p,l,r` | 线段树节点及其管理的闭区间；`pos` 是差分修改位置。 |

**3. 函数在做什么**

先解释为什么 GCD 能换成差值。对任意整数 `x,y`，`gcd(x,y)=gcd(x,y-x)`：两边的公因数集合相同，因为能整除 `x,y` 就能整除 `x,y-x`，反过来也成立。

反复使用这一性质，可以把后一项减去前一项而不改变 GCD，得到 `gcd(a[l],a[l+1]-a[l],...,a[r]-a[r-1])`，也就是 `gcd(a[l],diff[l+1],...,diff[r])`。差分求前缀和时，相邻项正负抵消，得到 `diff[1]+...+diff[i]=a[i]`，所以 BIT 可还原 `a[i]`。

以本节数组和操作手算：

1. 初始 `diff=[6,4,4,1]`。
2. `[2,3]` 加 5，只改变 `diff[2]+=5`、`diff[4]-=5`，得到 `[6,9,4,-4]`；BIT 同步修改这两个点。
3. 查询 `[2,4]`，用 `sumBit(2)=6+9=15` 得到左端原值。
4. GCD 树查询 `diff[3..4]` 得 4，再合并 `gcd(15,4)=1`。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `DifferenceGcdTree(a)` | a 为非空 1-based 初值数组；返回无（构造函数）。 | 复制差分，建立 BIT 和 GCD 树；不修改 a。 |
| `addBit(i,delta)` | i 为 1..n 差分下标，delta 为增量；返回void。 | 只更新 BIT；须与差分树的对应修改配合使用。 |
| `sumBit(i)` | i 为 0..n 前缀右端；返回diff[1..i] 的和；i=0 返回 0，其余还原 a[i]。 | 只读 BIT。 |
| `build(p,l,r)` | p 为管理闭区间 [l,r] 的节点；返回void。 | 从 diff 构建 seg；由构造函数调用。 |
| `pointAdd` | p 管理 [l,r]，pos 为区间内差分下标，delta 为增量；返回void。 | 修改 diff[pos] 和祖先 GCD；不更新 BIT。 |
| `query(p,l,r,ql,qr)` | p 管理 [l,r]，目标闭区间 [ql,qr] 与其相交；返回相交部分差分绝对值的 GCD。 | 只读 seg；公开入口保证目标位于 1..n。 |
| `rangeAdd(l,r,x)` | 1&lt;=l&lt;=r&lt;=n，x 为增量；返回void。 | 同步修改边界差分与 BIT；差分、前缀和、-x 和绝对值均须可用 ll 表示。 |
| `rangeGcd(l,r)` | 1&lt;=l&lt;=r&lt;=n；返回当前 a[l..r] 的非负 GCD。 | 只读结构；单点区间返回该值的绝对值。 |

BIT 单点修改或前缀查询需要 $O(\log n)$，线段树点修改或区间查询会处理 $O(\log n)$ 个节点。每个节点还要计算 GCD。构造时间 $O(n\log V)$，单次区间加或 GCD 查询 $O(\log n\log V)$，空间 $O(n)$；`V` 是参与计算的数值绝对值的上界，64 位数的欧几里得算法迭代次数有固定小上限。

**4. 怎么调用**

将本节模板放在业务代码之前，再按下面的输入调用。

```text
vector<long long> a = {0, 6, 10, 14, 15};
DifferenceGcdTree st(a);
st.rangeAdd(2, 3, 5);
long long answer = st.rangeGcd(2, 4);
assert(answer == 1);
```

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct DifferenceGcdTree {
    int n;
    vector<ll> diff, bit, seg;

    // 参数：a 为非空 1-based 初值数组。
    // 返回：无（构造函数）。
    // 效果：复制差分，建立 BIT 和 GCD 树；不修改 a。
    explicit DifferenceGcdTree(const vector<ll>& a) : n((int)a.size() - 1), diff(n + 1, 0), bit(n + 1, 0), seg(4 * n + 4, 0) {
        assert(n >= 1);
        for (int i = 1; i <= n; ++i) diff[i] = a[i] - (i == 1 ? 0 : a[i - 1]);
        for (int i = 1; i <= n; ++i) bit[i] += diff[i];
        for (int i = 1; i <= n; ++i) if (i + (i & -i) <= n) bit[i + (i & -i)] += bit[i];
        build(1, 1, n);
    }

    // 参数：i 为 1..n 差分下标，delta 为增量。
    // 返回：void。
    // 效果：只更新 BIT；须与差分树的对应修改配合使用。
    void addBit(int i, ll delta) {
        for (; i <= n; i += i & -i) bit[i] += delta;
    }

    // 参数：i 为 0..n 前缀右端。
    // 返回：diff[1..i] 的和；i=0 返回 0，其余还原 a[i]。
    // 效果：只读 BIT。
    ll sumBit(int i) const {
        ll result = 0;
        for (; i > 0; i -= i & -i) result += bit[i];
        return result;
    }

    // 参数：p 为管理闭区间 [l,r] 的节点。
    // 返回：void。
    // 效果：从 diff 构建 seg；由构造函数调用。
    void build(int p, int l, int r) {
        if (l == r) { seg[p] = llabs(diff[l]); return; }
        int m = (l + r) / 2;
        build(p * 2, l, m); build(p * 2 + 1, m + 1, r);
        seg[p] = gcd(seg[p * 2], seg[p * 2 + 1]);
    }

    // 参数：p 管理 [l,r]，pos 为区间内差分下标，delta 为增量。
    // 返回：void。
    // 效果：修改 diff[pos] 和祖先 GCD；不更新 BIT。
    void pointAdd(int p, int l, int r, int pos, ll delta) {
        if (l == r) { diff[pos] += delta; seg[p] = llabs(diff[pos]); return; }
        int m = (l + r) / 2;
        if (pos <= m) pointAdd(p * 2, l, m, pos, delta);
        else pointAdd(p * 2 + 1, m + 1, r, pos, delta);
        seg[p] = gcd(seg[p * 2], seg[p * 2 + 1]);
    }

    // 参数：p 管理 [l,r]，目标闭区间 [ql,qr] 与其相交。
    // 返回：相交部分差分绝对值的 GCD。
    // 效果：只读 seg；公开入口保证目标位于 1..n。
    ll query(int p, int l, int r, int ql, int qr) const {
        if (ql <= l && r <= qr) return seg[p];
        int m = (l + r) / 2; ll result = 0;
        if (ql <= m) result = gcd(result, query(p * 2, l, m, ql, qr));
        if (qr > m) result = gcd(result, query(p * 2 + 1, m + 1, r, ql, qr));
        return result;
    }

    // 参数：1<=l<=r<=n，x 为增量。
    // 返回：void。
    // 效果：同步修改边界差分与 BIT；差分、前缀和、-x 和绝对值均须可用 ll 表示。
    void rangeAdd(int l, int r, ll x) {
        assert(1 <= l && l <= r && r <= n);
        assert(x != LLONG_MIN);
        addBit(l, x); pointAdd(1, 1, n, l, x);
        if (r < n) { addBit(r + 1, -x); pointAdd(1, 1, n, r + 1, -x); }
    }

    // 参数：1<=l<=r<=n。
    // 返回：当前 a[l..r] 的非负 GCD。
    // 效果：只读结构；单点区间返回该值的绝对值。
    ll rangeGcd(int l, int r) const {
        assert(1 <= l && l <= r && r <= n);
        ll inside = (l == r ? 0 : query(1, 1, n, l + 1, r));
        return gcd(sumBit(l), inside);
    }
};
```

**5. 要改哪里**

- 若更新只发生在单点 `[l,l]`，仍须在存在时修改 `diff[l+1]`，才能抵消对后续元素的影响；只有右端点等于 `n` 时跳过 `diff[n+1]`。
- 如果需要查询区间和，应另维护前缀和结构或换用懒标记线段树；GCD 摘要无法直接支持区间加。 例如 `[6,10]` 的 GCD 是 2，整体加 1 后 `[7,11]` 的 GCD 是 1，并非 `2+1`。
- 若改为区间赋值，差分会影响边界内的大量差分项，不能只调用两次 `pointAdd`。

**6. 自检**

原数组 `[6,10,14,15]` 经 `[2,3] += 5` 后为 `[6,15,19,15]`，故 `rangeGcd(2,4)==1`；`rangeGcd(3,3)==19`。`r=n` 的更新后查询不可触及 `n+1`。

**7. 坑**

构造器接收非空的 1-based 数组，区间必须满足 `1<=l<=r<=n`。元素、差分、前缀和、`-x` 以及绝对值中间结果都必须能用 `long long` 表示；特别不能出现 `LLONG_MIN`，其绝对值无法表示。负数数组可以输入，GCD 结果为非负值。

- GCD 必须按非负绝对值计算；不能直接把有符号差分送给 `llabs` 并忽略 `LLONG_MIN`。
- 更新 `[l,r]` 时忘记在 `r+1` 减去 x，会让区间右侧整体偏移。
- 区间 GCD 由 `gcd(a[l], gcd(diff[l+1..r]))` 得出，不能错误查询 `diff[l..r]` 后再与 `a[l]` 合并。
- `rangeAdd` 断言范围，不代表算术溢出会被检测；调用者仍须保证所有中间值安全。

**8. 一句话原理**

区间加只改变差分数组的两个端点，而区间 GCD 可由左端原值与内部差分的 GCD 合成。

## 5.26 扫描线 + 线段树 {#sweep-line-segment-tree}

**1. 它是做什么的**

两个正方形 `A=[0,2)×[0,2)`、`B=[1,3)×[1,3)` 的面积各是 4，但并集面积是 7，因为重叠部分不能算两次。按 x 方向切成窄片，每片只需知道当前 y 方向覆盖了多长，再乘片宽并相加。

矩形的左右边界会改变当前覆盖状态；线段树负责汇总这时 y 轴上被覆盖的总长度。

**2. 变量在做什么**

压缩后的 `ys[i]` 是边界坐标，线段树叶子表示相邻边界之间的间隔 `[ys[i],ys[i+1])`，不是坐标点。点本身宽度为零，真正有面积的是间隔；所以矩形 `[y1,y2)` 要更新从 `index(y1)` 到 `index(y2)-1` 的叶子。

| 名称 | 含义 |
|---|---|
| `Rectangle` | 四边界定义的半开矩形。 |
| `Event` | 横坐标处的加入 `+1` 或移除 `-1`。 |
| `ys` | 有效矩形的 y 边界，排序去重。 |
| `cover[p]` | 节点区间被整段覆盖的层数。 |
| `length[p]` | 节点实际被覆盖的 y 长度；根值供面积累加。 |
| `area,previousX` | 已算面积与上批事件横坐标。 |

**3. 函数在做什么**

手算矩形 A、B。`x=0` 加入 A 后覆盖长度是 2；到 `x=1` 先累加 `2*(1-0)=2`，再加入 B，覆盖 y 变成 `[0,3)`、长度 3；到 `x=2` 累加 `3*(2-1)=3`，再移除 A，剩下长度 2；到 `x=3` 累加 `2*(3-2)=2`。合计 `2+3+2=7`。

扫描到一个 x 时先用旧覆盖状态结算 `[previousX,x)`，再处理同 x 的全部事件。更新线段树时，完整覆盖节点增加或减少 `cover`；若 `cover>0`，节点长度就是 `y[r+1]-y[l]`，否则叶子长度为零、内部长度取两个孩子之和。该规则让重叠矩形只计一次。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `CoveredLengthTree` | 至少两个严格递增 y 坐标；构造对象。 | 建立空覆盖树。 |
| `pull` | 线段树节点区间；返回 void。 | 按覆盖计数和子节点摘要重算覆盖长度。 |
| `update`（递归） | 节点区间、目标间隔范围、`delta`；返回 void。 | 加减覆盖数；删除必须对应先前添加。 |
| `update(y1,y2,delta)` | 已压缩边界与 `+1/-1`；返回 void。 | 将半开 y 区间换成叶子范围后更新。 |
| `covered` | 无；返回当前覆盖 y 长度。 | 读取根节点摘要。 |
| `rectangleUnionArea` | 矩形列表；返回并面积。 | 忽略反向或退化矩形，不修改输入。 |

过滤后有 `m` 个矩形、至多 `2m` 个不同 y 坐标时，时间 $O(m\log m)$、空间 $O(m)$。

**4. 怎么调用**

将本节模板放在业务代码之前，再按下面的输入调用。

```text
vector<Rectangle> rectangles = {{0, 0, 2, 2}, {1, 1, 3, 3}};
long long area = rectangleUnionArea(rectangles);
assert(area == 7);
```

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Rectangle { ll x1, y1, x2, y2; };

struct CoveredLengthTree {
    vector<ll> y;
    vector<int> cover;
    vector<ll> length;

    // 参数：ys 含至少两个严格递增坐标。
    // 返回：无（构造函数）。
    // 效果：移动参数副本到 y，初始化空覆盖树。
    explicit CoveredLengthTree(vector<ll> ys) : y(move(ys)), cover(4 * max(1, (int)y.size()) + 4, 0), length(cover.size(), 0) {
        assert(y.size() >= 2);
    }

    // 参数：p 管理间隔下标闭区间 [l,r]。
    // 返回：void。
    // 效果：根据 cover 和孩子摘要重算 length[p]。
    void pull(int p, int l, int r) {
        if (cover[p] > 0) length[p] = y[r + 1] - y[l];
        else if (l == r) length[p] = 0;
        else length[p] = length[p * 2] + length[p * 2 + 1];
    }

    // 参数：p 管理 [l,r]，目标为间隔下标 [ql,qr]，delta 为 +1 或 -1。
    // 返回：void。
    // 效果：更新覆盖计数与长度；减覆盖必须对应先前加入的同一区间。
    void update(int p, int l, int r, int ql, int qr, int delta) {
        if (ql <= l && r <= qr) { cover[p] += delta; pull(p, l, r); return; }
        int m = (l + r) / 2;
        if (ql <= m) update(p * 2, l, m, ql, qr, delta);
        if (qr > m) update(p * 2 + 1, m + 1, r, ql, qr, delta);
        pull(p, l, r);
    }

    // 参数：y1<y2 为已有压缩坐标，delta 为 +1 或 -1。
    // 返回：void。
    // 效果：将 [y1,y2) 映射为间隔下标后更新树；删除须与添加配对。
    void update(ll y1, ll y2, int delta) {
        auto leftIt = lower_bound(y.begin(), y.end(), y1);
        auto rightIt = lower_bound(y.begin(), y.end(), y2);
        assert(y1 < y2 && leftIt != y.end() && rightIt != y.end() && *leftIt == y1 && *rightIt == y2);
        int l = leftIt - y.begin();
        int r = rightIt - y.begin() - 1;
        if (l <= r) update(1, 0, (int)y.size() - 2, l, r, delta);
    }

    // 参数：无。
    // 返回：当前 y 轴覆盖长度。
    // 效果：只读根摘要。
    ll covered() const { return length[1]; }
};

// 参数：rectangles 为轴对齐矩形列表。
// 返回：矩形并面积；空输入或全无效时为 0。
// 效果：不修改输入；忽略反向或退化矩形，坐标差、面积乘积及累加均须可用 ll 表示。
ll rectangleUnionArea(const vector<Rectangle>& rectangles) {
    struct Event { ll x, y1, y2; int delta; };
    vector<Event> events; vector<ll> ys;
    for (const Rectangle& rec : rectangles) {
        if (rec.x1 >= rec.x2 || rec.y1 >= rec.y2) continue;
        events.push_back({rec.x1, rec.y1, rec.y2, +1});
        events.push_back({rec.x2, rec.y1, rec.y2, -1});
        ys.push_back(rec.y1); ys.push_back(rec.y2);
    }
    if (events.empty()) return 0;
    sort(ys.begin(), ys.end()); ys.erase(unique(ys.begin(), ys.end()), ys.end());
    // 参数：a、b 为扫描事件。
    // 返回：a.x < b.x。
    // 效果：只读事件；同 x 事件统一处理。
    sort(events.begin(), events.end(), [](const Event& a, const Event& b) {
        return a.x < b.x;
    });
    CoveredLengthTree tree(ys); ll area = 0, previousX = events.front().x;
    size_t i = 0;
    while (i < events.size()) {
        ll x = events[i].x;
        // 先用旧覆盖长度累积 [previousX,x)，再处理同 x 的所有事件。
        area += tree.covered() * (x - previousX);
        while (i < events.size() && events[i].x == x) {
            tree.update(events[i].y1, events[i].y2, events[i].delta); ++i;
        }
        previousX = x;
    }
    return area;
}
```

**5. 要改哪里**

- 若要计算矩形并周长，单靠根覆盖长度不够，还需维护覆盖段数及左右端覆盖状态，且同一 x 的加入/删除要按周长规则处理。
- 要求输出覆盖次数至少 k 的长度时，把节点摘要从 `cover>0` 的长度扩展为覆盖层数分布。
- 坐标或面积可能超出 `long long` 时，统一将差、乘积、面积改为更宽类型；只改最终返回类型不够。

**6. 自检**

矩形 `[0,2)×[0,2)` 与 `[1,3)×[1,3)` 的并面积为 7；单个矩形面积为宽乘高；空输入和全部反向或退化矩形返回 0。

**7. 坑**

坐标可为负数，输入矩形用半开边界；反向或宽、高为零的矩形不贡献面积。每个 x 差、y 覆盖跨度、`coveredY*(x-previousX)` 中间乘积及面积累加都必须能放入 `long long`，否则相关变量和计算均需改用更宽整数。

- 叶子代表坐标间隔 `[ys[i],ys[i+1])`，不是坐标点；更新右端点映射到 `index(y2)-1`。
- 面积必须用到达 x 前的覆盖长度乘 `x-previousX`，再处理该 x 的事件。
- 同 x 的事件顺序不影响面积，但不得把边界本身计为正面积。
- 面积乘积可能先溢出再累加；返回类型足够不等于中间乘法安全。

**8. 一句话原理**

按 x 切片累加面积，并在线段树上维护当前被矩形覆盖的 y 间隔总长度。

## 5.27 线段树 + 矩阵乘法 {#matrix-segment-tree}

**1. 它是做什么的**

假设一个计数过程有两种状态，当前方案数为 x、y。每个位置规定一次状态转移，我们会修改某个位置的规则，并询问连续一段规则执行后的结果。

例如规则 A 将 `(x,y)` 变成 `(x+y,y)`，规则 B 将它变成 `(x,x+y)`。从 `(1,1)` 开始，先 A 后 B，依次得到 `(2,1)`、`(2,3)`。如果每次查询都逐个执行区间内的规则，就会反复做许多相同转移。

每条规则都能写成矩阵，相邻规则也能合成一个矩阵。线段树保存每一段规则的合成结果，于是查询可以复用已经合成的部分；修改一条规则时，只重算它到根的路径。

**2. 变量在做什么**

状态按列向量写。规则 A 的新 x 是 `1*x+1*y`，新 y 是 `0*x+1*y`，所以两行系数构成矩阵 `[[1,1],[0,1]]`；同理 B 为 `[[1,0],[1,1]]`。

位置顺序和乘法书写顺序要分清：先 A 后 B，结果是 `B*(A*v)=(B*A)*v`。因此区间 `[l,r]` 的总转移为 `M_r⋯M_l`，右位置的矩阵乘在左边。乘法满足结合律，但不能随意交换位置。

| 名称 | 含义 |
|---|---|
| `Matrix::n` | 状态维数，也是方阵的行数和列数；示例为 2。 |
| `Matrix::a` | 每一条转移的系数，运算时规范到 `[0,MATRIX_MOD)`。 |
| `MATRIX_MOD` | 计数使用的模数，当前为 1000000007。 |
| `initial[i]` | 第 i 个位置的转移矩阵；数组下标 0 占位。 |
| `MatrixCompose` | 定义左右两个区间怎样合并，返回 `right*left`。 |
| `MatrixSegmentTree` | 复用 5.15 通用线段树的矩阵树类型，支持点修改和区间查询。 |

单位矩阵表示“不做任何变化”，用作空区间的合并单位元。

**3. 函数在做什么**

沿用规则 A、B 和初始状态 `(1,1)`：

1. 两个叶子分别保存 A 和 B，表示两个位置各自的转移。
2. 父节点保存 `B*A=[[1,1],[1,2]]`。乘初始列向量，得到 `(2,3)`，与逐条执行相同。
3. 若误写为 `A*B=[[2,1],[1,1]]`，得到 `(3,2)`，答案不同，说明乘法次序不能交换。
4. 把第二条规则改成单位矩阵，只需更新第二个叶子和祖先。区间总转移变成 A，状态变成 `(2,1)`。

线段树不改变规则的先后顺序，只改变相乘的分组。结合律保证先合成左段或右段都得到相同总转移。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `Matrix` | 非负维数；构造零矩阵。 | 0 阶仅作占位，参与运算的矩阵须正阶。 |
| `identityMatrix` | 正阶数；返回单位矩阵。 | 供线段树空区间使用。 |
| `normalizedMatrix` | 方阵副本；返回规范化副本。 | 把元素调整到模数范围，不改调用方对象。 |
| `multiplyMatrix` | 同阶正方阵；返回 `left*right`。 | 模 `MATRIX_MOD` 计算，不修改输入。 |
| `MatrixCompose::operator` | 左右相邻区间摘要；返回合并摘要。 | 以 `right*left` 表示先左后右。 |
| `matrixRange` | 1-based 矩阵数组与闭区间；返回总转移。 | 归一化副本后建临时树，不改原数组。 |
| `replaceAndQuery` | 矩阵树、合法位置、新矩阵和查询区间；返回区间摘要。 | 先替换归一化后的叶子，再查询。 |

设状态维数为 k，一次矩阵乘法需 $O(k^3)$；建树 $O(nk^3)$，点改和区间查询 $O(k^3\log n)$，空间 $O(nk^2)$。若每次使用 `matrixRange`，会重新建一棵临时树，单次总成本为 $O(nk^3+k^3\log n)$；多次修改查询时应像第 4 部分一样持有 `MatrixSegmentTree` 对象。逐个应用一个向量需 $O((r-l+1)k^2)$，逐项构造完整区间矩阵需 $O((r-l+1)k^3)$。

**4. 怎么调用**

将本节模板放在业务代码之前，再按下面的输入调用。

```text
Matrix a(2), b(2);
a.a = {{1, 1}, {0, 1}};
b.a = {{1, 0}, {1, 1}};
vector<Matrix> initial = {Matrix(2), a, b};
MatrixSegmentTree tree(initial, identityMatrix(2), MatrixCompose{});
Matrix product = tree.rangeQuery(1, 2); // b*a
assert((product.a == vector<vector<ll>>{{1, 1}, {1, 2}}));
tree.pointSet(2, identityMatrix(2));
assert(tree.rangeQuery(1, 2).a == a.a);
```

```cpp
// 依赖：先放入 5.15 节的 PointSegmentTree<T, Merge> 定义。
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
constexpr ll MATRIX_MOD = 1000000007;

struct Matrix {
    int n;
    vector<vector<ll>> a;
    // 参数：n 为非负阶数；0 只用于占位。
    // 返回：无（构造函数）。
    // 效果：分配 n×n 零矩阵。
    explicit Matrix(int n = 0) : n(n), a(n, vector<ll>(n, 0)) {}
};

// 参数：n 为正矩阵阶数。
// 返回：n 阶单位矩阵。
// 效果：只创建局部结果。
Matrix identityMatrix(int n) {
    assert(n > 0);
    Matrix result(n);
    for (int i = 0; i < n; ++i) result.a[i][i] = 1;
    return result;
}

// 参数：matrix 为正阶方阵副本。
// 返回：元素规范到 [0,MATRIX_MOD) 的矩阵。
// 效果：只修改参数副本。
Matrix normalizedMatrix(Matrix matrix) {
    assert(matrix.n > 0);
    for (auto& row : matrix.a) for (ll& value : row) {
        value %= MATRIX_MOD;
        if (value < 0) value += MATRIX_MOD;
    }
    return matrix;
}

// 参数：left、right 同阶且正阶，元素已按模数规范。
// 返回：模 MATRIX_MOD 的 left*right。
// 效果：不修改输入；返回新矩阵。
Matrix multiplyMatrix(const Matrix& left, const Matrix& right) {
    assert(left.n == right.n && left.n > 0);
    Matrix result(left.n);
    for (int i = 0; i < left.n; ++i)
        for (int k = 0; k < left.n; ++k) if (left.a[i][k])
            for (int j = 0; j < left.n; ++j)
                result.a[i][j] = (result.a[i][j] + left.a[i][k] * right.a[k][j]) % MATRIX_MOD;
    return result;
}

struct MatrixCompose {
    // 参数：left、right 为相邻区间同阶矩阵摘要。
    // 返回：right*left。
    // 效果：只读输入；对应从左到右作用于列向量。
    Matrix operator()(const Matrix& left, const Matrix& right) const {
        return multiplyMatrix(right, left);
    }
};

// 矩阵线段树类型：复用 5.15 的 PointSegmentTree，合并顺序由 MatrixCompose 指定。
using MatrixSegmentTree = PointSegmentTree<Matrix, MatrixCompose>;

// 参数：initial[1..n] 为同阶正阶矩阵，1<=l<=r<=n。
// 返回：区间总转移 M_r…M_l。
// 效果：归一化全部矩阵副本，再建立临时树查询；不修改 initial。
Matrix matrixRange(const vector<Matrix>& initial, int l, int r) {
    assert(l >= 1 && l <= r && r < (int)initial.size());
    vector<Matrix> normalized(initial.size());
    for (int i = 1; i < (int)initial.size(); ++i) normalized[i] = normalizedMatrix(initial[i]);
    MatrixSegmentTree tree(normalized, identityMatrix(normalized[1].n), MatrixCompose{});
    return tree.rangeQuery(l, r);
}

// 参数：tree 为矩阵树，pos 为合法下标，updated 同阶，[l,r] 为合法闭区间。
// 返回：替换后的区间总转移。
// 效果：归一化 updated 后修改 tree 的对应叶子并查询。
Matrix replaceAndQuery(MatrixSegmentTree& tree, int pos, Matrix updated, int l, int r) {
    tree.pointSet(pos, normalizedMatrix(move(updated)));
    return tree.rangeQuery(l, r);
}
```

**5. 要改哪里**

- 若区间转移次序相反，应同步改 `MatrixCompose` 的乘法顺序，并用两个不交换矩阵验证。
- 若更新字符或状态，替换对应叶矩阵后查询受影响区间；不必重建整个树。
- 若改模数，更新 `MATRIX_MOD` 并确认乘法中间值仍不溢出；当前 `long long` 乘积要求模数范围受控。

**6. 自检**

用两个不交换矩阵 `A,B` 检查区间 `[1,2]` 结果是 `B*A`，不是 `A*B`；单元素区间应返回该叶矩阵，替换一个叶后其余区间查询不变。

**7. 坑**

- 矩阵乘法通常不交换；本代码有意组合为 `right*left`，不可随手交换。
- `PointSegmentTree` 是 5.15 的依赖，单独编译此片段前需合并依赖定义。
- 传入矩阵维数必须一致且元素先归一化；构造时 `initial[1]` 必须存在。
- 模乘中间乘积需能容纳 `MATRIX_MOD` 下两个元素的乘积。

**8. 一句话原理**

矩阵乘法满足结合律，因此可将一段连续状态转移按顺序合并成线段树摘要。

## 5.28 线段树上二分 {#segment-tree-search}

**1. 它是做什么的**

数组 `[2,-4,7,1,7]` 中，问位置 2 到 5 第一个不小于 7 的数在哪。答案是位置 3。

逐个检查时先看位置 2，再看位置 3；重复查询会重复扫描。线段树把一段数组汇总成“这一段的最大值”。如果整段最大值都不到 7，就能一次跳过整段；否则继续找左边可能有答案的部分。

数组不要求有序，找答案靠的是每个节点能否证明整段不合格。找到位置后即可停止。

**2. 变量在做什么**

`tree[p]` 是一段区间的最大值，回答“这段有没有机会达到阈值”；它不是原数组中的某个固定位置。`ql,qr` 是要查的下标范围，`need` 是数值门槛，两者不能混为一谈。

| 名称 | 含义 |
|---|---|
| `n` | 初始 1-based 数组长度。 |
| `tree[p]` | 节点管理区间的最大值；若小于 `need`，该段不可能有答案。 |
| `initial` | 构造时传入的 1-based 初值，复制到树中。 |
| `ql,qr,need` | 搜索区间闭端点和目标下界。 |
| `pos,value` | `pointSet` 的 1-based 修改位置和值。 |

**3. 函数在做什么**

沿用数组 `[2,-4,7,1,7]`，查询 `[2,5]`、门槛 7：

1. 根节点管 `[1,5]`，与查询相交，最大值 7，不能剪掉。
2. 看左半 `[1,3]`，它和查询只交于 `[2,3]`；继续看 `[1,2]`，该节点保存的整段最大值为 2，不足 7，可以直接跳过；不需要临时计算交集摘要。
3. 检查 `[3,3]`，值为 7，返回下标 3；右侧无需再看。

若查询改成 `[4,5]`， `[4,4]` 最大值为 1，可剪掉，再到 `[5,5]` 返回 5。这些节点访问说明最左优先和整段剪枝如何配合。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `FirstAtLeastTree` | initial 为非空 1-based 初值数组；返回无（构造函数）。 | 建立区间最大值树；不修改 initial。 |
| `build(p,l,r,initial)` | p 管理闭区间 [l,r]，initial 为初值；返回void。 | 递归写入 tree 的最大值摘要。 |
| `pointSet` | p 管理 [l,r]，pos 位于该区间，value 为新值；返回void。 | 修改叶子并重算祖先最大值。 |
| `search(p,l,r,ql,qr,need)` | p 管理 [l,r]，目标为闭区间 [ql,qr]，need 为阈值；返回区间内首个值至少为 need 的下标；没有则 -1。 | 只读树；先剪枝再搜索左孩子。 |
| `pointSet(pos,value)` | pos 为 1..n 下标，value 为新值；返回void。 | 从根调用点赋值辅助函数。 |
| `firstAtLeast(l,r,need)` | 1&lt;=l&lt;=r&lt;=n，need 为阈值；返回[l,r] 内首个值至少为 need 的位置；没有则 -1。 | 只读结构；从根执行搜索。 |

建树 $O(n)$，单点修改和一次搜索均为 $O(\log n)$，空间 $O(n)$。搜索先跳过不相交节点，再剪去最大值不足的整段；在找到的第一个合格节点中，只沿最左答案的路径下降。查询边界分解成的节点数和下降的树高都为对数级，因此不会遍历所有合格叶子。

**4. 怎么调用**

将本节模板放在业务代码之前，再按下面的输入调用。

```text
vector<long long> initial = {0, 1, 2, 3, 4, 5};
FirstAtLeastTree tree(initial);
tree.pointSet(3, 8);
int pos = tree.firstAtLeast(2, 5, 7);
assert(pos == 3);
```

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct FirstAtLeastTree {
    int n;
    vector<ll> tree;

    // 参数：initial 为非空 1-based 初值数组。
    // 返回：无（构造函数）。
    // 效果：建立区间最大值树；不修改 initial。
    explicit FirstAtLeastTree(const vector<ll>& initial) : n((int)initial.size() - 1), tree(4 * n + 4, LLONG_MIN) {
        assert(n >= 1); build(1, 1, n, initial);
    }

    // 参数：p 管理闭区间 [l,r]，initial 为初值。
    // 返回：void。
    // 效果：递归写入 tree 的最大值摘要。
    void build(int p, int l, int r, const vector<ll>& initial) {
        if (l == r) { tree[p] = initial[l]; return; }
        int m = (l + r) / 2;
        build(p * 2, l, m, initial); build(p * 2 + 1, m + 1, r, initial);
        tree[p] = max(tree[p * 2], tree[p * 2 + 1]);
    }

    // 参数：p 管理 [l,r]，pos 位于该区间，value 为新值。
    // 返回：void。
    // 效果：修改叶子并重算祖先最大值。
    void pointSet(int p, int l, int r, int pos, ll value) {
        if (l == r) { tree[p] = value; return; }
        int m = (l + r) / 2;
        if (pos <= m) pointSet(p * 2, l, m, pos, value);
        else pointSet(p * 2 + 1, m + 1, r, pos, value);
        tree[p] = max(tree[p * 2], tree[p * 2 + 1]);
    }

    // 参数：p 管理 [l,r]，目标为闭区间 [ql,qr]，need 为阈值。
    // 返回：区间内首个值至少为 need 的下标；没有则 -1。
    // 效果：只读树；先剪枝再搜索左孩子。
    int search(int p, int l, int r, int ql, int qr, ll need) const {
        if (r < ql || qr < l || tree[p] < need) return -1;
        if (l == r) return l;
        int m = (l + r) / 2;
        int left = search(p * 2, l, m, ql, qr, need);
        return left != -1 ? left : search(p * 2 + 1, m + 1, r, ql, qr, need);
    }

    // 参数：pos 为 1..n 下标，value 为新值。
    // 返回：void。
    // 效果：从根调用点赋值辅助函数。
    void pointSet(int pos, ll value) { assert(1 <= pos && pos <= n); pointSet(1, 1, n, pos, value); }

    // 参数：1<=l<=r<=n，need 为阈值。
    // 返回：[l,r] 内首个值至少为 need 的位置；没有则 -1。
    // 效果：只读结构；从根执行搜索。
    int firstAtLeast(int l, int r, ll need) const {
        assert(1 <= l && l <= r && r <= n);
        return search(1, 1, n, l, r, need);
    }
};
```

**5. 要改哪里**

- 若查“最后一个满足条件的位置”，改为先搜右儿子再搜左儿子。
- 若摘要为最小值，寻找首个 `a[i]<=x` 时将剪枝条件改为区间最小值仍大于 x。
- 若用区间和找首个前缀达到阈值，必须保证元素非负；有负数时前缀不单调，不能安全剪枝。

**6. 自检**

初值 `{0,2,-4,7,1,7}` 查询 `[2,5]`、need=7 应返回 3；改位置 3 为 0 后应返回 5；need=10 无解返回 -1。

**7. 坑**

- 搜索必须先检查当前节点最大值是否小于 need；不满足时下探会失去剪枝收益。
- 先搜左子树才能保证返回最小下标。
- `tree` 以 `LLONG_MIN` 初始化，构造器要求非空数组。
- 区间求和只有在非负元素保证前缀单调时才能做同类搜索。

**8. 一句话原理**

若一个节点的区间最大值仍小于阈值，节点内所有位置都不可能满足条件，可以整段跳过。

## 5.29 倍增 + 单调栈 {#doubling-monotone-stack}

**1. 它是做什么的**

数组 `[2,1,4,3,5]` 从位置 1 出发，每次跳到右边第一个更大的数：位置 1 跳到 3，再跳到 5。跳两次的答案是位置 5。

每次从当前点向右重新找，会在许多查询中反复扫描相同位置。先一次性算出每个位置的一步去处，再把两步、四步等结果预先接起来，就能快速走长链。

数组固定不变；这里的“更大”指严格大于。

**2. 变量在做什么**

`up[0][i]` 是位置 `i` 的下一个更大元素位置；沿着它反复跳构成一条后继链。它只保留“每一步的第一个更大”，不是把所有更大元素按大小排名，也不是区间第 k 大。

`up[j][i]` 表示从 `i` 沿这条链跳 `2^j` 次的位置。`mono` 是建第一层后继时保留的候选下标栈，`k` 是链上跳数而非数值门槛。

| 名称 | 含义 |
|---|---|
| `n` | 1-based 数组长度。 |
| `log` | 倍增层数，表下标为 `0..log-1`；链上最多有 `n-1` 次有效跳转。 |
| `up[j][i]` | 从 i 沿 next-greater 链跳 `2^j` 次的位置；0 表示链已断。 |
| `mono` | 从右往左扫描时的单调栈，保存可能成为 next greater 的下标。 |
| `start,k,right` | 起点、正跳数和查询右边界；`k` 为 `long long`。 |

**3. 函数在做什么**

对 `[2,1,4,3,5]` 从右向左扫描，栈内写下标：

| 当前位置 | 弹出不大于当前值的候选 | 一步后继 | 入栈后的下标栈 |
|---|---|---|---|
| 5，值 5 | 无 | 0，无后继 | `[5]` |
| 4，值 3 | 无 | 5 | `[5,4]` |
| 3，值 4 | 弹出 4，因其值 3 不大于 4 | 5 | `[5,3]` |
| 2，值 1 | 无 | 3 | `[5,3,2]` |
| 1，值 2 | 弹出 2，因其值 1 不大于 2 | 3 | `[5,3,1]` |

被弹出的候选更远且不更大；对将来位于更左侧的位置而言，当前元素至少与它一样有用，所以可以永久淘汰。栈顶因此给出最近的严格更大位置。

从位置 1 出发，一步到 3，再一步到 5。倍增表直接保存 `up[1][1]=5`，跳两次只查这一项。若跳数为 5，二进制为 `4+1`，就组合四步和一步的结果；途中遇到哨兵 0 表示链已经结束。

重复值要从候选栈弹掉，因条件是严格更大。倍增关系为 `up[j][i]=up[j-1][up[j-1][i]]`，把跳数拆成二进制位依次走。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `NextGreaterDoubling(a)` | a 为非空 1-based 数组；返回无（构造函数）。 | 预处理严格更大后继和倍增表；不修改 a。 |
| `kthGreater(start,k)` | start 为起点，k 为后继链上的跳数；返回跳 k 次后的下标；非法起点、k&lt;=0 或不存在时为 0。 | 只读倍增表；并非区间第 k 大。 |
| `firstGreaterWithin` | start 为起点，right 为合法数组右界；返回[start+1,right] 首个严格更大位置；不存在或起点非法则 0。 | O(1) 读取一步后继，不修改状态。 |

单调栈中每个位置至多入栈、出栈一次，第一层为 $O(n)$；倍增表建表时间和空间都是 $O(n\log n)$。查询只沿二进制跳数所需的层走，时间 $O(\log(k+1))$；有效链长最多 `n-1`。

**4. 怎么调用**

将本节模板放在业务代码之前，再按下面的输入调用。

```text
vector<long long> a = {0, 2, 1, 4, 3, 5};
NextGreaterDoubling jumps(a);
int first = jumps.firstGreaterWithin(1, 4);
int second = jumps.kthGreater(1, 2);
assert(first == 3 && second == 5);
```

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct NextGreaterDoubling {
    int n, log;
    vector<vector<int>> up;

    // 参数：a 为非空 1-based 数组。
    // 返回：无（构造函数）。
    // 效果：预处理严格更大后继和倍增表；不修改 a。
    explicit NextGreaterDoubling(const vector<ll>& a) : n((int)a.size() - 1), log(1) {
        assert(n >= 1);
        while ((1LL << log) <= n) ++log;
        up.assign(log, vector<int>(n + 1, 0));
        vector<int> mono;
        for (int i = n; i >= 1; --i) {
            while (!mono.empty() && a[mono.back()] <= a[i]) mono.pop_back();
            up[0][i] = mono.empty() ? 0 : mono.back();
            mono.push_back(i);
        }
        for (int j = 1; j < log; ++j)
            for (int i = 1; i <= n; ++i)
                up[j][i] = up[j - 1][up[j - 1][i]];
    }

    // 参数：start 为起点，k 为后继链上的跳数。
    // 返回：跳 k 次后的下标；非法起点、k<=0 或不存在时为 0。
    // 效果：只读倍增表；并非区间第 k 大。
    int kthGreater(int start, ll k) const {
        if (start < 1 || start > n || k <= 0) return 0;
        int node = start;
        for (int bit = 0; k > 0 && node != 0; ++bit, k >>= 1)
            if (k & 1) node = bit < log ? up[bit][node] : 0;
        return node;
    }

    // 参数：start 为起点，right 为合法数组右界。
    // 返回：[start+1,right] 首个严格更大位置；不存在或起点非法则 0。
    // 效果：O(1) 读取一步后继，不修改状态。
    int firstGreaterWithin(int start, int right) const {
        if (start < 1 || start > n || right <= start) return 0;
        int next = up[0][start];
        return next != 0 && next <= right ? next : 0;
    }
};
```

**5. 要改哪里**

- 要求“下一个大于等于”时，构栈弹出条件需从 `<=` 改为 `<`，并验证重复值链。
- 若只需单次 next greater 查询，不必建倍增表，单调栈的 `up[0]` 已足够。
- 若问独立阈值 x 在 `[l,r]` 的首个满足位置，本节按跳数查询的接口不能直接回答；可使用 5.28 的区间最大值剪枝，或另设计按值判断的后继链倍增查询。

**6. 自检**

数组 `{0,2,1,4,3,5}` 中 `firstGreaterWithin(1,4)==3`，`kthGreater(1,2)==5`；严格关系下从值 4 不会跳到相等值 4。

**7. 坑**

- 严格更大使用弹栈条件 `<=`；改成 `<` 后语义会包含相等值。
- `up[0][i]` 是下一个更大位置，不是更大值；哨兵 0 不能当数组下标访问。
- `kthGreater` 沿后继链跳 k 次，不等同于区间第 k 大。
- `firstGreaterWithin` 的 `right` 必须是有效数组边界。

**8. 一句话原理**

单调栈找出每个位置的一步更大后继，倍增表将后继链上的多步跳跃拆成二进制块。

## 5.30 可撤销并查集 {#rollback-dsu}

**1. 它是做什么的**

四个点开始时互不连通。先记下此时的状态，再合并 `1-2`、`2-3`，询问 1 和 3 是否连通，答案是“是”。回到刚才记录的状态，再问则是“否”。

普通并查集擅长合并，却不直接支持恢复先前状态。可撤销版本记录每次合并改了哪些字段，回退时倒着恢复。

这里的快照像书签，只能沿当前历史向过去回滚；它不会自动保存所有历史版本。

**2. 变量在做什么**

`parent[x]` 指向父节点，根的父节点是自己；`size[root]` 只记录根所代表集合的大小。一次合并成功会让一个根成为另一个根的孩子。`history` 记录这次变化，`components` 是当前集合数。

快照 `snap` 是历史栈长度，不是连通分量数；它只在同一对象当前仍保留的历史分支上有效；回滚后产生新分支，不能凭长度相同就把旧分支的书签重新当作有效状态。即使两个点已连通，重复 `unite` 也压入一条标记为空操作的历史，保证每次尝试都能对应一次回退。

| 名称 | 含义 |
|---|---|
| `parent[x]` | 并查集父指针；根满足 `parent[x]==x`。 |
| `size[root]` | 根所代表集合的大小，只对根有意义。 |
| `history` | 每次 `unite` 一条记录；成功记录旧根大小，失败记录 `merged=false`。 |
| `components` | 当前连通分量数。 |
| `Change` | `child`、被挂接的 `parentRoot`、合并前 `oldSize` 及是否成功。 |

**3. 函数在做什么**

取 4 个点，初始分量数为 4：

| 操作 | history 长度 | `components` | 连通关系 |
|---|---:|---:|---|
| `snapshot()` | 0 | 4 | 四个单点集合 |
| `unite(1,2)` | 1 | 3 | 1 与 2 连通 |
| `unite(2,3)` | 2 | 2 | 1、2、3 连通 |
| `rollback(0)` | 0 | 4 | 恢复四个单点集合 |

为了让每次合并只改少量字段，本模板不做路径压缩，只按集合大小挂接根。回滚逐条弹出历史，恢复被挂接根的父指针和接收根的旧大小，同时恢复分量数；重复合并的空记录只弹出，不改集合状态。`find` 只沿父链向上走，不做路径压缩。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `RollbackDSU(n)` | n&gt;=1 为点数，编号 1..n；返回无（构造函数）。 | 建立 n 个单点集合，清空历史。 |
| `find(x)` | x 为 1..n 元素编号；返回所属集合根。 | 只读父链，不进行路径压缩。 |
| `snapshot()` | 无；返回当前 history 长度，作为回滚快照。 | 只读历史；长度必须可由 int 表示。 |
| `unite(u,v)` | u、v 为合法元素编号；返回两个不同集合合并成功时 true，已同组时 false。 | 按大小合并；每次尝试均压入一条历史，成功时修改父指针、大小和分量数。 |
| `rollback(snap)` | snap 为当前历史分支上仍有效的较早或当前快照；返回void。 | 弹出历史至 snap，恢复父指针、大小与分量数；不能恢复已丢弃的未来分支。 |
| `same(u,v)` | u、v 为合法元素编号；返回两点当前是否连通。 | 只读父链和历史。 |

按大小合并使树高为 $O(\log n)$，因此 `find` 和成功合并为 $O(\log n)$，取快照为 $O(1)$。回滚是每条弹出记录 $O(1)$，总耗时按本次弹出记录数计算；若累计尝试 q 次合并，每次最多保留一条记录，空间为 $O(n+q)$。

**4. 怎么调用**

将本节模板放在业务代码之前，再按下面的输入调用。

```text
RollbackDSU dsu(4);
int snap = dsu.snapshot();
dsu.unite(1, 2);
bool connected = dsu.same(1, 2);
assert(connected);
dsu.rollback(snap);
assert(!dsu.same(1, 2));
```

```cpp
#include <bits/stdc++.h>
using namespace std;

struct RollbackDSU {
    struct Change { int child, parentRoot, oldSize; bool merged; };
    vector<int> parent, size;
    vector<Change> history;
    int components;

    // 参数：n>=1 为点数，编号 1..n。
    // 返回：无（构造函数）。
    // 效果：建立 n 个单点集合，清空历史。
    explicit RollbackDSU(int n) : parent(n + 1), size(n + 1, 1), components(n) {
        assert(n >= 1);
        iota(parent.begin(), parent.end(), 0);
    }

    // 参数：x 为 1..n 元素编号。
    // 返回：所属集合根。
    // 效果：只读父链，不进行路径压缩。
    int find(int x) const {
        while (parent[x] != x) x = parent[x];
        return x;
    }

    // 参数：无。
    // 返回：当前 history 长度，作为回滚快照。
    // 效果：只读历史；长度必须可由 int 表示。
    int snapshot() const { return (int)history.size(); }

    // 参数：u、v 为合法元素编号。
    // 返回：两个不同集合合并成功时 true，已同组时 false。
    // 效果：按大小合并；每次尝试均压入一条历史，成功时修改父指针、大小和分量数。
    bool unite(int u, int v) {
        int ru = find(u), rv = find(v);
        if (ru == rv) { history.push_back({0, 0, 0, false}); return false; }
        if (size[ru] < size[rv]) swap(ru, rv);
        history.push_back({rv, ru, size[ru], true});
        parent[rv] = ru; size[ru] += size[rv]; --components;
        return true;
    }

    // 参数：snap 为当前历史分支上仍有效的较早或当前快照。
    // 返回：void。
    // 效果：弹出历史至 snap，恢复父指针、大小与分量数；不能恢复已丢弃的未来分支。
    void rollback(int snap) {
        assert(0 <= snap && snap <= (int)history.size());
        while ((int)history.size() > snap) {
            Change change = history.back(); history.pop_back();
            if (!change.merged) continue;
            parent[change.child] = change.child;
            size[change.parentRoot] = change.oldSize;
            ++components;
        }
    }

    // 参数：u、v 为合法元素编号。
    // 返回：两点当前是否连通。
    // 效果：只读父链和历史。
    bool same(int u, int v) const { return find(u) == find(v); }
};
```

**5. 要改哪里**

- 若上层需要每次尝试都能按次数回滚，保留失败合并的空记录；删除该记录时，上层快照仍可用，但快照语义变为历史修改数而非尝试数。
- 若要维护额外集合摘要（如点权和），需在成功合并记录旧摘要并在 rollback 中恢复。
- 需要在线路径压缩并查集时，不适合本结构；路径压缩会产生多处需记录的父指针变化。

**6. 自检**

4 个点先取快照，合并 1-2、2-3 后 `same(1,3)` 为真且分量数为 2；回滚快照后该查询为假、分量数为 4。重复合并也应能完整回滚。

**7. 坑**

- 不能做路径压缩，否则 `rollback` 没有记录那些被压缩的父指针。
- 快照是 history 长度，必须来自同一对象且不得大于当前长度。
- 快照后的修改必须按后进先出回滚；不能保留后续状态再回滚到更早快照。
- `find/same` 仅在点编号合法时安全；代码不会逐点检查范围。

**8. 一句话原理**

只按大小合并且不压缩路径，使每次合并只需记录少量字段便能按历史逆序恢复。

## 5.31 线段树分治（动态连通性） {#segment-tree-offline}

**1. 它是做什么的**

有四个时刻：加边 `1-2`、询问连通、删边 `1-2`、再询问。答案分别是“是”和“否”。

如果每个时刻都从头重建图，会重复处理仍然有效的边。离线时可以先找出每条边在哪些时间段存在，再将它们放到时间线的线段树上；沿树走到一个时刻时，只需合并覆盖它的边。

离开一个时间段就撤销该段引入的边，这样兄弟时间段不会互相影响。

**2. 变量在做什么**

`operations[t]` 是时刻 `t` 的输入；`tree[p]` 则存放整段时间都活跃、可由节点 `p` 一并加入的边。时间树的区间按半开形式 `[l,r)` 表示，`starts` 为每条规范化无向边保存尚未删除的添加时刻。

`answers` 只收集问号操作的结果，`dsu` 是 5.30 的可撤销并查集。边实例按 LIFO 匹配：重复添加会各自活跃，删除关闭最近一次仍未关闭的实例。

| 名称 | 含义 |
|---|---|
| `Operation` | 单个时间点操作：`type` 为 `A`、`D` 或 `?`，`u,v` 是 1..n 端点。 |
| `operations` | 按时间下标 0..q-1 保存的输入操作。 |
| `tree[p]` | 时间线线段树节点所负责时段内始终活跃的边。 |
| `answers` | 依查询出现顺序写入的 0/1 连通结果；每次 `run()` 前清空。 |
| `dsu` | 依赖 5.30 的无路径压缩可撤销并查集。 |
| `starts` | 构造阶段按规范化无向边保存未删除添加时刻的栈。 |

**3. 函数在做什么**

操作序列的时刻表如下：

| 时刻 | 操作 | 查询结果 | 操作后边是否活跃 |
|---:|---|---|---|
| 0 | `A(1,2)` | — | 是 |
| 1 | `?(1,2)` | 连通 | 是 |
| 2 | `D(1,2)` | — | 否 |
| 3 | `?(1,2)` | 不连通 | 否 |

边在添加时刻开始生效、删除时刻不再生效，因此活跃区间恰为 `[0,2)`。时间树根管 `[0,4)`，其左孩子正好覆盖 `[0,2)`，整条边只需放在该节点；它不会进入右孩子 `[2,4)`。

DFS 进入 `[0,2)` 时先取快照，再合并节点上的边，访问时刻 0 和 1 两个叶子；离开该节点时回滚到快照，恢复无边状态。于是两次查询答案为 `{1,0}`。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `构造函数` | n&gt;=1；operations 按时间给出 A/D/?，端点为 1..n；返回无（构造函数）。 | 保存操作副本，按 LIFO 配对重复边并构造半开活跃时间段。 |
| `normalized(u,v)` | u、v 为无向边端点；返回(min(u,v),max(u,v))。 | 不修改参数或对象。 |
| `addInterval` | p 管理 [l,r)，边 e 活跃于 [ql,qr)；返回void。 | 将 e 存入被活跃时间段完全覆盖的节点；不相交时返回。 |
| `buildIntervals()` | 无；返回void。 | 仅构造时调用；按 LIFO 配对 A/D 写入时间树，未匹配删除忽略。 |
| `solve(p,l,r)` | p 管理非空时间段 [l,r)；返回void。 | 临时合并节点边，叶子回答查询，退出前回滚至进入时快照。 |
| `run()` | 无；返回按时间顺序排列的 0/1 连通结果。 | 清空答案并从空边 DSU 状态重跑；支持重复调用，q=0 返回空向量。 |

若有 `q` 个操作和 `s` 个活跃区间，每个区间分解进 $O(\log(q+1))$ 个节点；配对 map 扫描 $O(q\log(q+1))$。总时间安全上界 $O(q\log(q+1)+s\log(q+1)\log(n+1)+q\log(n+1))$，空间 $O(q+s\log(q+1)+n)$。合并因按大小而为对数代价，回滚按实际弹出的历史记录计费。

**4. 怎么调用**

将本节模板放在业务代码之前，再按下面的输入调用。

```text
vector<Operation> ops = {{'A', 1, 2}, {'?', 1, 2}, {'D', 1, 2}};
OfflineDynamicConnectivity solver(3, ops);
vector<int> answers = solver.run();
assert(answers.size() == 1 && answers[0] == 1);
```

```cpp
// 依赖：先放入 5.30 节的 RollbackDSU；本节不重复定义它。
#include <bits/stdc++.h>
using namespace std;

struct Operation { char type; int u, v; };

struct OfflineDynamicConnectivity {
    struct Edge { int u, v; };
    int n, q;
    vector<Operation> operations;
    vector<vector<Edge>> tree;
    vector<int> answers;
    RollbackDSU dsu;

    // 参数：n>=1；operations 按时间给出 A/D/?，端点为 1..n。
    // 返回：无（构造函数）。
    // 效果：保存操作副本，按 LIFO 配对重复边并构造半开活跃时间段。
    OfflineDynamicConnectivity(int n, vector<Operation> operations)
        : n(n), q((int)operations.size()), operations(move(operations)), tree(4 * max(1, q) + 4), dsu(n) {
        assert(n >= 1);
        buildIntervals();
    }

    // 参数：u、v 为无向边端点。
    // 返回：(min(u,v),max(u,v))。
    // 效果：不修改参数或对象。
    pair<int, int> normalized(int u, int v) const { return {min(u, v), max(u, v)}; }

    // 参数：p 管理 [l,r)，边 e 活跃于 [ql,qr)。
    // 返回：void。
    // 效果：将 e 存入被活跃时间段完全覆盖的节点；不相交时返回。
    void addInterval(int p, int l, int r, int ql, int qr, Edge e) {
        if (qr <= l || r <= ql) return;
        if (ql <= l && r <= qr) { tree[p].push_back(e); return; }
        int m = (l + r) / 2;
        addInterval(p * 2, l, m, ql, qr, e);
        addInterval(p * 2 + 1, m, r, ql, qr, e);
    }

    // 参数：无。
    // 返回：void。
    // 效果：仅构造时调用；按 LIFO 配对 A/D 写入时间树，未匹配删除忽略。
    void buildIntervals() {
        if (q == 0) return;
        map<pair<int, int>, vector<int>> starts;
        for (int t = 0; t < q; ++t) {
            if (operations[t].type == 'A') {
                starts[normalized(operations[t].u, operations[t].v)].push_back(t);
            } else if (operations[t].type == 'D') {
                auto key = normalized(operations[t].u, operations[t].v);
                auto it = starts.find(key);
                if (it != starts.end() && !it->second.empty()) {
                    int begin = it->second.back(); it->second.pop_back();
                    addInterval(1, 0, q, begin, t, {key.first, key.second});
                }
            }
        }
        for (const auto& item : starts) for (int begin : item.second)
            addInterval(1, 0, q, begin, q, {item.first.first, item.first.second});
    }

    // 参数：p 管理非空时间段 [l,r)。
    // 返回：void。
    // 效果：临时合并节点边，叶子回答查询，退出前回滚至进入时快照。
    void solve(int p, int l, int r) {
        int snap = dsu.snapshot();
        for (const Edge& edge : tree[p]) dsu.unite(edge.u, edge.v);
        if (r - l == 1) {
            const Operation& op = operations[l];
            if (op.type == '?') answers.push_back(dsu.same(op.u, op.v));
        } else {
            int m = (l + r) / 2;
            solve(p * 2, l, m); solve(p * 2 + 1, m, r);
        }
        dsu.rollback(snap);
    }

    // 参数：无。
    // 返回：按时间顺序排列的 0/1 连通结果。
    // 效果：清空答案并从空边 DSU 状态重跑；支持重复调用，q=0 返回空向量。
    vector<int> run() {
        answers.clear(); dsu.rollback(0);
        if (q > 0) solve(1, 0, q);
        return answers;
    }
};
```

**5. 要改哪里**

- 若删除匹配最早尚未删除的添加实例，把每条边的起点容器从栈改为队列，并按 FIFO 取出。
- 若要回答组件大小等问题，可扩展 5.30 的 DSU 查询与回滚记录；时间区间分解框架保持不变。
- 若查询要求在线回答，未来操作尚未知，无法预先构造活跃时间段，应选择在线动态连通结构。

**6. 自检**

操作序列 A(1,2), ?(1,2), D(1,2), ?(1,2) 的答案应为 `{1,0}`；空操作列表 `run()` 返回空向量；重复添加后删除一次，另一个实例仍活跃。

**7. 坑**

- 边在添加时刻生效、删除时刻失效，因此保存为半开区间 `[add,del)`；未删边为 `[add,q)`，空区间不放进树。
- 重复边按规范化端点和 LIFO 实例配对；未匹配删除被忽略。
- 类型为 `?` 的操作必须提供合法 u、v；无关字段虽不读取，也应初始化。
- `run()` 会重置答案并回滚 DSU；不要在递归 DFS 中使用带路径压缩的 DSU。
- 空操作列表不会调用 `solve`，因此时间线根上的空区间不会被访问。

**8. 一句话原理**

把边的活跃时间段分解到时间线线段树节点，DFS 子树期间临时合并，离开时回滚。

## 5.32 P2 进阶：树上莫队、Segment Tree Beats 与 LCT {#advanced-data-structure-guide}

本节分别介绍三个 P2 专题的模型、维护信息和实现流程，不含可直接提交的完整模板。

### 5.32.1 树上莫队

**1. 它是做什么的**

在树 `1-2, 1-3, 2-4` 上，颜色依次为 `A,B,C,A`，路径 `4→3` 上有三种颜色。

每次都沿路径重新数颜色，会在大量询问间反复走过同一批点。树上莫队把路径对应成括号序的一段，让相邻询问复用当前窗口，只对窗口变化的部分增删点。

**2. 变量在做什么**

普通 DFS 序中一个顶点只出现一次，树路径通常不是连续区间；括号序则让每个顶点进出各出现一次。某点在窗口中出现奇数次时保留，偶数次时抵消，选好窗口后，奇数出现的点构成要维护的集合；某些路径还需临时补入最近公共祖先。

| 名称 | 含义 |
|---|---|
| `tin[u]` | 点 `u` 第一次进入 DFS 时在长度 `2n` 括号序中的位置。 |
| `tout[u]` | 点 `u` 退出 DFS 时在括号序中的位置；每点一进一出。 |
| `euler[pos]` | 括号序位置 `pos` 对应的顶点编号。 |
| `active[u]` | 当前窗口奇数出现集合是否包含点 `u`；每次遇到都翻转。 |
| `L,R` | 当前维护的闭区间端点。 |
| `z` | 路径两端的最近公共祖先；某些区间需临时补入。 |
| `block` | 莫队排序的分块长度。 |

**3. 函数在做什么**

括号序为 `[1,2,4,4,2,3,3,1]`。询问 `4→3` 时，窗口 `[4,6]` 对应 `[4,2,3]`，奇数出现集合正是这三个点；最近公共祖先 1 不在其中，回答前临时补入 1，答案读完马上撤回。询问 `2→4` 用 `[2,3]`，窗口 `[2,4]` 已是完整路径，不补祖先。

先按 `tin` 排序端点并求 `z=LCA(u,v)`。若 `z=u`，取 `[tin[u],tin[v]]`；否则取 `[tout[u],tin[v]]` 并记下额外点 `z`。窗口移动时，每个位置都执行 toggle：若点当前不活跃则加入统计，否则删除，最后翻转活跃标记。

以下是建议的流程名，不是仓库现成 API；颜色统计函数需按题目实现。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `toggle(pos)` | 括号序位置；无返回。 | 对 `euler[pos]` 加入或删除颜色，再翻转 `active`；增删必须互逆。 |
| `moveWindow(L,R,ql,qr)` | 旧区间和目标闭区间；无返回。 | 移动端点并逐位置 toggle；初始状态对应旧区间。 |
| `pathInterval(u,v)` | 两个树点；返回区间和可选补点。 | 排序端点并求 LCA，按祖先关系选择上述区间。 |
| `answerPath(u,v)` | 两个树点；返回维护统计量。 | 移窗，临时补祖先、读答案后撤销。 |

LCA 倍增预处理 $O(n\log n)$，排序询问 $O(q\log q)$，每问求 LCA $O(\log n)$。块长约 `sqrt(2n)` 且加入/删除为 $O(1)$ 时，指针移动项为 $O((n+q)\sqrt n)$，空间 $O(n\log n+q)$；若增删更贵，移动项还要乘其代价。

**4. 怎么调用**

下面是把询问转换和维护顺序写清楚的流程伪代码，不是可直接提交的实现。仓库没有本节可直接提交的树上莫队模板；`buildEulerTour`、`lca`、`addColor`、`removeColor`、`readAnswer` 均需按所选统计量实现。示例树为 `1-2,1-3,2-4`，查询 `4→3` 时区间 `[4,6]` 需补入点 `1`。

```text
树：1-2，1-3，2-4；询问：path(4, 3)
(2n 括号序, tin, tout) = buildEulerTour(tree, root=1)
(u, v) = (4, 3)，若 tin[u] > tin[v] 则交换
z = lca(u, v) = 1
若 z == u：目标区间 = [tin[u], tin[v]]，extra = none
否则：目标区间 = [tout[u], tin[v]]，extra = z
按莫队顺序移动当前窗口到目标区间；每移动一格都 toggle(position)
若 extra != none：addColor(value[extra])
result = readAnswer()
若 extra != none：removeColor(value[extra])
assert 当前窗口统计状态仍只对应目标区间
```

**5. 要改哪里**

- 先练习手画括号序并验证窗口：覆盖祖先端点、非祖先端点、`u==v`、端点交换四种情况。
- 把普通莫队的 `add/remove` 改为对 `euler[pos]` 执行的 `toggle`，用随机小树与暴力逐点枚举路径对拍。
- 选择可增可删的路径统计量实现 `addColor/removeColor/readAnswer`；例如不同颜色数或频率平方和。若颜色有修改，再把修改时间作为第三维排序和回滚。
- 练习统计路径颜色对数时，重点校验补 LCA 后状态的恢复；树结构若动态变化，括号序和预处理均失效，应换动态树结构。参考 [OI Wiki：树上莫队](https://oi-wiki.org/misc/mo-algo-on-tree/)。

**6. 自检**

对树 `1-2,1-3,2-4` 和括号序 `[1,2,4,4,2,3,3,1]`：查询 `4→3` 的 `[4,6]` 窗口奇数集合应为 `{4,2,3}`，临时补入 `1` 后为 `{4,2,1,3}`；查询 `2→4` 的 `[2,3]` 窗口为 `{2,4}`，不补 LCA。完成一次带补点的回答后，`active` 必须恢复为仅表示窗口的状态。

**7. 坑**

- 窗口采用闭区间；非祖先情形的左端是 `tout[u]`，常见错误是误用 `tin[u]`。
- 补入 LCA 只用于读取当前答案，读取后必须撤销；否则后续询问状态被污染。
- `toggle` 必须严格按奇偶切换；把两次出现当成两次独立加入会重复计数。
- LCA 预处理和括号序针对静态树；改边后不能沿用旧序列。
- 上述复杂度依赖常数时间加入/删除及约 `sqrt n` 的块长；状态代价变化时需要重新估算。

**8. 一句话原理**

括号序中路径以外的顶点成对出现并抵消，树路径询问因此转化为区间奇偶集合的莫队维护。

### 5.32.2 Segment Tree Beats

**1. 它是做什么的**

数组 `[8,8,5,2]` 的总和为 23。把每项压到不超过 6 后是 `[6,6,5,2]`，总和变 19。

若每次更新都逐项扫描，大区间会反复访问很多元素。Segment Tree Beats 在条件满足时能整段压低最大值层；条件不够时才继续拆开看孩子。

**2. 变量在做什么**

`mx1` 是最大值，`mx2` 是严格次大值，也就是小于最大值的第二大不同值；`cnt` 是最大值出现次数。只有 `sum` 和 `mx1` 不够，因为不知道哪些元素会被压低；即使知道 `cnt`，也要知道压低后会不会碰到下一层。

| 名称 | 含义 |
|---|---|
| `sum` | 节点区间所有元素之和。 |
| `mx1` | 当前区间最大值。 |
| `mx2` | 当前区间严格次大值；全相等或单元素时为负无穷哨兵。 |
| `cnt` | 当前区间中等于 `mx1` 的元素个数。 |
| `x` | 本次 `chmin` 上限，元素改成 `min(a[i],x)`。 |
| `left/right` | 节点对应的数组闭区间。 |

**3. 函数在做什么**

对 `[8,8,5,2]`，初始 `(sum,mx1,mx2,cnt)=(23,8,5,2)`。上限为 6 时，只有最大值层的两个 8 改变：和减去 `(8-6)×2=4`，新和 19，最大值变 6，个数仍为 2。再压到 5，边界碰到原次大值，值变为 `[5,5,5,2]`，和为 17，最大值个数变成 3。

因此只有 `mx2 < x < mx1` 才能直接改：执行 `sum -= (mx1-x)*cnt` 并设 `mx1=x`。若 `x>=mx1` 不变；若 `x<=mx2` 则往孩子递归。向下前还要把父节点的最大值上限传给超标孩子，再重新合并摘要。

以下是标准流程接口约定，不代表仓库提供了现成 API。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `applyChmin(node,x)` | 节点摘要与上限；无返回。 | 仅在 `mx2 < x < mx1` 时直接覆盖。 |
| `push(node)` | 内部节点和孩子；无返回。 | 将父节点最大值约束传给最大值更大的孩子。 |
| `pull(node)` | 内部节点和孩子；无返回。 | 重算 `sum,mx1,mx2,cnt`，正确处理两侧最大值相等与否。 |
| `rangeChmin` | 节点区间、目标区间和上限；无返回。 | 不相交或 `x>=mx1` 时结束；可直接覆盖时应用，否则下推递归并合并。 |
| `rangeSum(node,l,r,ql,qr)` | 节点及目标区间；返回区间和。 | 全覆盖取 `sum`，部分覆盖先下推再合并相交孩子。 |
| `rangeMax` | 输入查询区间；返回其中的最大值。 | 完全覆盖读 `mx1`，部分覆盖先下推再取相交孩子的最大值。 |
| `rangeMaxCount` | 输入查询区间；返回其中最大值的出现次数。 | 部分覆盖时合并“最大值、次数”二元组：最大值相同则次数相加，否则只保留较大者的次数。 |

标准单向区间 `chmin` 加求和/最值查询，总时间摊还 $O((n+q)\log n)$、空间 $O(n)$；这是整体界，不保证每次更新都是 $O(\log n)$。势能分析依赖这组摘要。扩展 `chmax`、区间加或历史最值会改变字段、懒标记和证明。数组须非空，哨兵不能和合法值冲突，乘积及区间和不得溢出。

**4. 怎么调用**

这是调用次序和节点分支的流程伪代码，不是可直接提交的实现；仓库没有本节模板。示例数组 `[8,8,5,2]`，将全区间压到 `6` 后总和应为 `19`，最大值为 `6`；再压到 `5` 后总和为 `17`，最大值个数为 `3`。

```text
数组 = [8, 8, 5, 2]
build(数组)
rangeChmin([0,3], 6)
assert rangeSum([0,3]) == 19
assert rangeMax([0,3]) == 6
rangeChmin([0,3], 5)
assert rangeSum([0,3]) == 17
assert rangeMaxCount([0,3]) == 3

rangeChmin(node, ql, qr, x):
    若 node 与 [ql,qr] 不相交 或 x >= node.mx1：返回
    若 node 完全包含于 [ql,qr] 且 node.mx2 < x：applyChmin(node,x); 返回
    push(node)
    递归更新左右孩子
    pull(node)
```

**5. 要改哪里**

- 入门先写逐元素暴力 `chmin` 和区间和；再用 `[8,8,5,2]` 手算为什么需要严格次大值及最大值个数。
- 实现练习从单向 `chmin + sum/max` 开始，建立节点摘要、快速覆盖、下推与合并；不要直接扩成多种修改。
- 对拍重点包含全相等、单元素、`x=mx1`、`x=mx2`、负数、反复收紧、部分覆盖与空查询边界。
- 若题目更新后某种势能量快速下降（例如区间取模），可能也能用摊还分析，但它们不是本节模板的直接变体；先证明自己的势能界。

**6. 自检**

对 `[8,8,5,2]`，初始摘要为 `(23,8,5,2)`；`chmin(6)` 后和为 `19`、最大值为 `6`、最大值个数为 `2`；继续 `chmin(5)` 后和为 `17`、最大值个数为 `3`。用随机小数组对拍时，应逐次与逐元素执行 `min(a[i],x)` 的暴力结果核对区间和与最大值。

**7. 坑**

- `mx2` 必须是严格次大值；若把最大值重复项误作次大值，快速覆盖条件会错误。
- 快速覆盖只在 `mx2 < x < mx1` 成立；`x==mx2` 必须递归，`x==mx1` 则无变化。
- 下推时父节点的最大值上限要作用于孩子，否则父摘要与孩子摘要不一致。
- 复杂度是总操作摊还界，不能解释为每个更新最坏 $O(\log n)$。
- 哨兵、数值范围与累加乘积溢出检查属于正确性前提；扩展操作后需要重新推导复杂度。

**8. 一句话原理**

利用最大值与严格次大值之间的间隙，在只改变最大值层时批量更新；跨过间隙就递归，并以摊还分析控制总递归量。

**参考：**

- [OI Wiki：区间最值操作](https://oi-wiki.org/ds/seg-beats/)

### 5.32.3 Link-Cut Tree

**1. 它是做什么的**

森林有边 `1-2,2-3`，点权是 `[4,7,1]`，路径 `1→3` 的和为 12。删去 `2-3` 后两点断开；再加边 `1-3`，路径 `2→3` 变成 `2→1→3`，和仍为 12。

如果边会在线变化，固定的树上路径拆分会失效。Link-Cut Tree（LCT）动态组织路径信息，从而支持连边、删边与路径查询。

**2. 变量在做什么**

先知道 Splay 的基本作用：它通过旋转把指定节点调整到一棵二叉树的根。LCT 用这种辅助树组织路径顺序，树中孩子的左右关系不按原树点号大小决定。

原森林的边描述真实图；辅助 Splay 树的孩子关系用于组织路径，不等于原树父子关系。`fa[x]` 因此可能是辅助父指针，也可能是路径上的父关联，必须用 `isRoot` 区分。路径反转时辅助树左右孩子互换。

| 名称 | 含义 |
|---|---|
| `ch[x][0], ch[x][1]` | 辅助树左、右孩子。 |
| `fa[x]` | 辅助父指针或路径父关联。 |
| `rev[x]` | 延迟翻转标记。 |
| `val[x]` | 顶点自身权值。 |
| `sum[x]` | 辅助树代表路径的摘要；求和例中为路径和。 |
| `x,y` | 动态森林顶点编号。 |

**3. 函数在做什么**

对路径 `1→3`：先把 1 变成表示上的根，再暴露到 3 的路径，最后让 3 成为辅助 Splay 根。此时 3 的摘要覆盖 `1,2,3`，所以和为 `4+7+1=12`。删边 `2-3` 后查询应先发现不连通；重连 `1-3` 后再暴露 `2→3`，路径是 `2,1,3`，摘要为 12。

执行 `makeRoot(x); access(y); splay(y)` 后读取 `sum[y]`。以下是标准操作约定，不是仓库已有 API。

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `isRoot(x)` | 顶点 x；返回布尔值。 | 判断 x 是否为辅助 Splay 根。 |
| `push(x)` | 节点 x；无返回。 | 下传翻转等延迟标记。 |
| `pull(x)` | 节点 x；无返回。 | 用自身权值和孩子摘要重算维护量。 |
| `splay(x)` | 节点 x；无返回。 | 先下传标记，再旋转使 x 成为辅助树根。 |
| `access(x)` | 顶点 x；无返回。 | 暴露原树根到 x 的路径。 |
| `makeRoot(x)` | 顶点 x；无返回。 | 暴露并翻转，使 x 成为表示上的根。 |
| `connected(x,y)` | 两点；返回是否连通。 | 不连通时不得执行路径聚合。 |
| `link(x,y)` | 两点；返回是否成功。 | 仅连接不连通点，避免成环。 |
| `cut(x,y)` | 两点；返回是否成功。 | 仅删除原树中直接相邻的一条边。 |
| `pathQuery(x,y)` | 同一树两点；返回路径摘要。 | 暴露路径并读取 `y` 的摘要。 |

若要增加点权修改，先 `access(x); splay(x)` 暴露目标点，再改 `val[x]` 并执行 `pull(x)`，使辅助树摘要与新点权一致。

标准 Splay 型 LCT 的 link、cut、暴露路径和查询为摊还 $O(\log n)$，空间 $O(n)$；单次操作不保证最坏 $O(\log n)$。维护虚子树贡献或非交换路径摘要还需额外状态；反转时要同步交换正、反向摘要。

**4. 怎么调用**

下面给出操作顺序的流程伪代码，不是可直接提交的实现；仓库没有本节现成 LCT 模板。必须先实现并验证 Splay 的旋转、`push/pull` 和连通判断。点权 `[4,7,1]`，边为 `1-2,2-3`，示例中的路径和断言对应前述手算。

```text
初始化 3 个孤立点，点权分别为 [4,7,1]
assert link(1,2) == true
assert link(2,3) == true
assert connected(1,3) == true
assert pathQuery(1,3) == 12
assert cut(2,3) == true
assert connected(1,3) == false
assert link(1,3) == true
assert pathQuery(2,3) == 12
assert pathQuery(1,3) == 5

pathQuery(x,y):
    若 not connected(x,y)：返回“不连通”
    makeRoot(x)
    access(y)
    splay(y)
    返回 sum[y]
```

**5. 要改哪里**

- 学习顺序：先掌握 Splay 旋转、伸展、标记下传，再实现 LCT；先只维护路径异或或和，验证路径暴露后再扩展。
- 基础练习手算原树边与辅助 Splay 树边的区别；实现练习随机执行合法森林的连边、删边与路径查询，用 BFS 暴力对拍。
- 组合练习再加入路径懒标记；若维护非交换运算，要为翻转维护正向和反向摘要。
- 子树聚合或虚子树贡献需要额外维护与证明，不能把路径摘要直接挪用；任意图动态连通也不是动态森林问题。参考 [OI Wiki：Link Cut Tree](https://oi-wiki.org/ds/lct/)。

**6. 自检**

初始边 `1-2,2-3`、权值 `[4,7,1]` 时，`pathQuery(1,3)==12`。成功 `cut(2,3)` 后 `connected(1,3)==false`；随后 `link(1,3)`，路径 `2→1→3` 的和为 `12`，路径 `1→3` 的和为 `5`。每次 `link` 都应拒绝已经连通的端点，每次 `cut` 都应拒绝非直接相邻顶点。

**7. 坑**

- `fa[x]` 可能是原树路径父关联而非辅助树父子边，旋转前必须正确判断 `isRoot(x)`。
- 访问/旋转前要按从辅助根到目标的顺序下传翻转等懒标记；否则孩子方向与摘要可能不一致。
- `link` 必须先检查不连通，`cut` 必须验证目标边是直接边；否则森林不变量被破坏。
- LCT 的 $O(\log n)$ 是摊还界，不是单次最坏界；任意图动态连通与动态森林路径查询也不是同一个问题。
- 子树信息、非交换路径摘要需要额外维护；反向路径查询必须正确交换正反向摘要。

**8. 一句话原理**

通过 Splay 动态重排辅助路径，把原树两点间路径暴露为一棵辅助树上的连续摘要，并用摊还旋转支持森林边的在线变化。
