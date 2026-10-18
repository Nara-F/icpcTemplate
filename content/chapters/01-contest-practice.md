# 1. 竞赛常用内容

## 1.1 通用代码骨架与多测清空

**问题：** 将单组逻辑放进 `solve()`，入口只负责读取测试组数并循环调用，便于复用和隔离状态。多测总成本是各组复杂度之和；优先使用局部容器，谨慎清空大型全局数组。

**思路：**

- 单测时保留 `int testCases = 1`，不要读取不存在的测试组数。
- 多测时取消读取 `testCases` 的注释；先确认题面是否给出 $T$。
- 优先把数组、图、DP 表定义为 `solve()` 内局部变量，每组自动重新构造。
- 大型全局数组只清空本组访问过的范围；时间戳法适合频繁清空布尔或编号状态。
- 每组输出格式统一在 `solve()` 内处理，题目要求时加 `Case #x:`。


```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 参数：无；从标准输入读取一组数据。返回：无。效果：计算并写出当前测试用例答案。
void solve() {
    int n;
    cin >> n;

    // 状态尽量放在 solve 内：每组测试结束后自动销毁，不会串组。
    vector<ll> a(n + 1); // 本模板约定输入下标为 1..n
    for (int i = 1; i <= n; ++i) cin >> a[i];

    // 在这里编写单组答案。
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int testCases = 1;
    // cin >> testCases; // 仅当题面明确给出测试组数时启用
    while (testCases--) solve();
    return 0;
}
```

**易错点：**

1. 把样例中的多组数据误认为题目输入含 $T$，会从第一项开始读错。
2. `vector::clear()` 只把大小变为 0；重新 `resize` 后不能假设旧内存内容有意义。
3. 全局邻接表、答案、计数器、时间戳和静态局部变量都可能跨组残留。
4. 对最大数组每组完整 `memset`，可能把本可通过的算法拖成 TLE。

**参考：**

- [OI Wiki：C++ 语法基础](https://oi-wiki.org/lang/basic/)
- [OI Wiki：常见错误](https://oi-wiki.org/contest/common-mistakes/)

## 1.2 数据范围与复杂度速判

**问题：** 依据 $n,m,W,T$ 和总和约束估算时间与峰值内存，再选择算法。清空、建图、排序、递归栈和多测开销都要计算；常数和评测机差异使经验表只能初筛。

**思路：**

- 多测必须估算 $\sum n$、$\sum m$，不能只看单组上限。
- 图算法用 $n+m$ 估算；背包看 $nW$；状压看 $n2^n$ 或 $n^22^n$。
- 内存按“元素个数 × 单元素字节数”计算，并加上容器、递归栈和多份数组。
- 约 $10^8$ 次简单整数操作已可能接近常见时限；哈希、字符串复制、堆操作常数更大。
- 用最坏数据本地计时只能辅助判断，不能替代理论复杂度。

**公式与速查：**

```text
常见候选（只作一秒级 C++ 的粗略起点）：
n <= 20          O(2^n)、O(n * 2^n)
n <= 40          O(2^(n/2)) 折半搜索
n <= 500         O(n^3) 需关注常数
n <= 5,000       O(n^2) 需关注常数和内存
n <= 200,000     O(n log n)、O(n sqrt(n)) 视常数而定
n,m <= 1,000,000 O(n)、O(n+m)

内存 MiB = 元素个数 * sizeof(元素) / 1024 / 1024
例如：2^20 * 20 个 long long 约为 160 MiB。
```

**易错点：**

1. $O(n^2)$ 的二维 `long long` 数组常先 MLE，再谈不上 TLE。
2. 把取模、平衡树、哈希或大整数运算都当成一个同常数的“基本操作”。
3. 忽略清空数组、建图、排序或输入输出，它们也计入总复杂度。
4. 只根据样例规模选算法；评测按题目给出的最大范围构造数据。

**参考：**

- [OI Wiki：复杂度简介](https://oi-wiki.org/basic/complexity/)
- [OI Wiki：常见错误](https://oi-wiki.org/contest/common-mistakes/)

## 1.3 快速输入输出

**问题：** 非交互题在首次 IO 前关闭同步并解绑 `cin`，统一使用 C++ 流、以 `\n` 换行。交互题要及时刷新；`getline` 与格式化读取混用时需处理残留换行。

**思路：**

- 在任何 IO 前调用 `ios::sync_with_stdio(false); cin.tie(nullptr);`。
- 关闭同步后统一使用 `cin/cout`，不要混用 `scanf/printf`。
- 普通换行用 `'\n'`；`endl` 会额外刷新缓冲区。
- 交互题必须在每次询问后 `cout << flush`，不能照搬非交互写法。
- 输出大量元素时先拼接或顺序写入，不要在循环中无必要地刷新。


```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false); // 必须在第一次 cin/cout 操作前调用
    cin.tie(nullptr);            // 非交互题解除 cin 对 cout 的自动刷新

    int n;
    cin >> n;
    vector<long long> a(n);
    for (long long& value : a) cin >> value;

    for (int i = 0; i < n; ++i) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\n'; // 不需要立即显示时，用换行而不是 endl
    return 0;
}
```

**易错点：**

1. 关闭同步后混用 C 与 C++ 输入或混用两套输出，顺序可能异常。
2. 交互题忘记刷新会等待超时；普通题频繁 `endl` 又可能拖慢输出。
3. `cin >> s` 跳过空白；要读取含空格整行时使用 `getline`，并处理残留换行。
4. 输入失败后变量不会得到有效新值；读到 EOF 的题应以 `while (cin >> x)` 控制。

**参考：**

- [OI Wiki：读入、输出优化](https://oi-wiki.org/contest/io/)
- [OI Wiki：C++ 输入输出](https://oi-wiki.org/lang/io/)

## 1.4 编译、运行与 Sanitizer

**用途：** 用 Python 编译并启动 C++，或直接运行 Python。先保存下方代码为 `run.py`；1.8 的 `check.py`、1.14 的 `cph.py` 均放在同一目录并导入它。需要 Python 3.10+、`g++`。

**接口：** `build(name)` 接受 `.cpp`、`.py` 或无后缀 C++ 文件名，返回子进程命令列表；C++ 每次启动时按 GNU++17 编译为同名 `.exe`，编译失败停止，不运行旧文件。`execute(cmd,data,timeout)` 供样例和对拍使用，输入输出均为字节，独立检查超时和非零退出码。直接运行脚本连接终端，不设时限，交互题可手动输入。

```python
import subprocess as s
import sys
from pathlib import Path

# 参数：.cpp/.py 路径（C++ 可省略后缀）。返回：启动命令；副作用：编译，失败立即抛异常。
def build(name):
    p = Path(name)
    if not p.suffix:
        p = p.with_suffix('.cpp')
    p = p.resolve(strict=True)
    if p.suffix == '.py':
        return [sys.executable, str(p)]
    if p.suffix != '.cpp':
        raise ValueError('expected .cpp or .py')
    exe = p.with_suffix('.exe')
    # 每次启动脚本重新编译，避免误用上次编译成功的旧程序。
    s.run(['g++', '-std=gnu++17', '-O2', '-Wall', '-Wextra',
           str(p), '-o', str(exe)], check=True)
    return [str(exe)]

# 参数：命令、输入字节和时限秒数。返回：(stdout, 错误说明)；副作用：启动子进程。
def execute(cmd, data, timeout=2):
    try:
        p = s.run(cmd, input=data, capture_output=True, timeout=timeout)
    except s.TimeoutExpired as error:
        return error.stdout or b'', 'TLE'
    error = (f'RE ({p.returncode}): ' + p.stderr.decode(errors='replace')
             if p.returncode else '')
    return p.stdout, error

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python3 run.py a.cpp | a.py')
    try:
        raise SystemExit(s.run(build(sys.argv[1])).returncode)
    except (OSError, ValueError, s.CalledProcessError) as error:
        raise SystemExit(str(error))
```

```bash
python3 run.py a          # 编译 a.cpp，随后手动输入
python3 run.py a.cpp < sample.in > actual.out
python3 run.py a.py < sample.in
# 调试版另外编译；出错后用同一反例运行，不用它评估正式时限。
g++ a.cpp -std=gnu++17 -O1 -g -DDEBUG \
  -fsanitize=address,undefined -fno-omit-frame-pointer -o a_dbg
./a_dbg < fail.in
```

**要改哪里：** 评测要求 C++20 时把 `-std=gnu++17` 改为 `-std=gnu++20`；要统一开启调试宏，在 `build` 的编译选项中加 `-DDEBUG`。`-O2` 用于普通测试；Sanitizer 用于定位非法访问和 UB，先处理第一条错误和调用栈。

**坑：** 路径相对当前工作目录解析；可执行文件会被重新编译覆盖。参数以列表传递，支持空格路径。缺编译器、源码不存在或编译失败都立即终止。程序正常退出时的 `stderr` 不参与答案比较；排查时可用 `run.py` 直接查看日志。`execute` 捕获输出，内存与输出大小成正比，适合有界的小数据。

## 1.5 调试宏与断言

**用途：** 给 `pair`、`vector` 重载输出，直接查看嵌套数据；日志写 `cerr`，用 `DEBUG` 控制，避免混入正式答案。下面是一份可独立编译的调试骨架。

```cpp
#include <bits/stdc++.h>
using namespace std;

// 参数：输出流与二元组。返回：原输出流；副作用：写入 (first,second)。
template<class A, class B>
ostream& operator<<(ostream& os, const pair<A, B>& p) {
    return os << '(' << p.first << ',' << p.second << ')';
}

// 参数：输出流与可流输出元素的 vector。返回：原输出流；副作用：写入 [x, y]。
template<class T>
ostream& operator<<(ostream& os, const vector<T>& a) {
    os << '[';
    for (size_t i = 0; i < a.size(); ++i) os << (i ? ", " : "") << a[i];
    return os << ']';
}

#ifdef DEBUG
// 参数：可流输出的任意多个值。返回：无；副作用：依次写 stderr 并换行。
template<class... Args>
void debugLog(const Args&... args) {
    ((cerr << args << ' '), ...);
    cerr << '\n';
}
#define DBG(...) debugLog(#__VA_ARGS__, "=", __VA_ARGS__)
#else
#define DBG(...) ((void)0)
#endif

// 参数：无。返回：0；副作用：DEBUG 时展示数组和边列表，否则无输出。
int main() {
    vector<int> a = {3, 1, 2};
    vector<pair<int, int>> edges = {{1, 2}, {1, 3}};
    DBG(a, edges); // stderr 包含 [3, 1, 2] 与 [(1,2), (1,3)]
    assert(a.size() == 3); // 检查真实不变量，不在 assert 内写必要操作
}
```

**调用：** 编译时加 `-DDEBUG` 开启日志；提交版不加。树/图边列表可直接 `DBG(edges)`，二维数组可逐行输出。对没有输出重载的类型（例如 `map`）先遍历、输出元素，不直接交给 `DBG`。

**坑：** `DBG(++x)` 在调试版会改变状态，关闭时不执行，避免带副作用的表达式。`NDEBUG` 会移除 `assert`；断言不能承担读入、状态转移等必要操作。大量日志可能导致 TLE；先打印错误位置附近的最小状态。提交前沿用 1.13 的检查清单。

## 1.6 随机数与数据生成

**用途：** C++ 随机数入口用于在程序内取随机整数和打乱顺序；`gen.py` 用于按固定种子生成数组、树、图等完整测试输入。

**C++ 随机数入口：** `Rand(lo,hi)` 包含两端；`shuffle` 原地打乱。生成器从命令行读取种子，便于 1.8 的对拍重现；不传种子时才取时钟。

```cpp
#include <bits/stdc++.h>
using namespace std;
mt19937_64 rng;

// 参数：闭区间 lo..hi，要求 lo<=hi。返回：随机整数；副作用：推进 rng。
long long Rand(long long lo, long long hi) {
    assert(lo <= hi);
    return uniform_int_distribution<long long>(lo, hi)(rng);
}

// 参数：可选整数种子 argv[1]。返回：0；副作用：输出 n 和随机排列，种子写 stderr。
int main(int argc, char** argv) {
    unsigned long long seed = argc > 1 ? stoull(argv[1])
        : chrono::steady_clock::now().time_since_epoch().count();
    rng.seed(seed);
    cerr << "seed = " << seed << '\n';
    int n = static_cast<int>(Rand(1, 12));
    vector<int> a(n);
    iota(a.begin(), a.end(), 1);
    shuffle(a.begin(), a.end(), rng);
    cout << n << '\n';
    for (int x : a) cout << x << ' ';
    cout << '\n';
}
```

**通用结构生成器：** 下方保存为 `gen.py`，只使用 Python 标准库。`Generator(seed)` 内部维护独立随机状态；同一种子、同一环境和相同调用顺序得到相同数据。返回的列表使用 0-based 下标，树/图点号统一为 `1..n`。调用者负责选定题目允许的规模和值域。

| 方法 | 生成结果与前提 | 时间 / 结果空间 |
|---|---|---|
| `integer(lo,hi)` | 闭区间整数 | O(1) / O(1) |
| `array(n,lo,hi,distinct=False)` | 可含重复数组；互异时要求值域至少有 n 个值 | O(n) / O(n) |
| `permutation(n)` | 1..n 的排列 | O(n) / O(n) |
| `text(n,alphabet)` | 字符集内的长度 n 字符串 | O(n) / O(n) |
| `matrix(r,c,lo,hi)` | r 行 c 列，各行独立 | O(rc) / O(rc) |
| `tree(n,shape,relabel=True)` | random/chain/star，无自环无重边，共 n-1 条边 | O(n) / O(n) |
| `graph(n,m,directed=False,connected=False,dag=False)` | 简单图；连通只用于无向图，DAG 必须有向 | O(n²) / O(n²) 候选与结果 |
| `weighted(edges,lo,hi)` | 每条已有边附加闭区间权值 | O(m) / O(m) |

```python
import random
import string
import sys

class Generator:
    # 参数：整数 seed。返回：生成器；副作用：建立独立随机状态，相同调用顺序可复现。
    def __init__(self, seed):
        self.rng = random.Random(seed)

    # 参数：闭区间 lo..hi。返回：均匀整数；副作用：推进随机状态。
    def integer(self, lo, hi):
        if lo > hi:
            raise ValueError('lo > hi')
        return self.rng.randint(lo, hi)

    # 参数：长度 n>=0、闭值域，可选互异。返回：0-based 列表；副作用：推进随机状态。
    def array(self, n, lo, hi, distinct=False):
        if n < 0 or lo > hi or (distinct and n > hi - lo + 1):
            raise ValueError('invalid array range/length')
        if distinct:
            return self.rng.sample(range(lo, hi + 1), n)
        return [self.integer(lo, hi) for _ in range(n)]

    # 参数：n>=0。返回：1..n 的随机排列（列表下标 0-based）；副作用：推进随机状态。
    def permutation(self, n):
        if n < 0:
            raise ValueError('n < 0')
        a = list(range(1, n + 1))
        self.rng.shuffle(a)
        return a

    # 参数：长度 n>=0、非空字符集。返回：字符串；副作用：推进随机状态。
    def text(self, n, alphabet=string.ascii_lowercase):
        if n < 0 or not alphabet:
            raise ValueError('invalid string length/alphabet')
        return ''.join(self.rng.choice(alphabet) for _ in range(n))

    # 参数：行列数 >=0、闭值域。返回：各行独立的二维列表；副作用：推进随机状态。
    def matrix(self, rows, cols, lo, hi):
        if rows < 0 or cols < 0 or lo > hi:
            raise ValueError('invalid matrix shape/range')
        return [self.array(cols, lo, hi) for _ in range(rows)]

    # 参数：n>=1，random/chain/star，是否打乱点号。返回：1-based 无向树边列表。
    # 副作用：推进随机状态；random 是随机接父亲树，不是均匀抽取所有标号树。
    def tree(self, n, shape='random', relabel=True):
        if n < 1 or shape not in ('random', 'chain', 'star'):
            raise ValueError('invalid tree size/shape')
        labels = self.permutation(n) if relabel else list(range(1, n + 1))
        edges = []
        for v in range(2, n + 1):
            parent = (v - 1 if shape == 'chain' else
                      1 if shape == 'star' else self.integer(1, v - 1))
            u, w = labels[parent - 1], labels[v - 1]
            edges.append((min(u, w), max(u, w)))
        self.rng.shuffle(edges)
        return edges

    # 参数：n>=1、边数 m；有向/连通/DAG 开关。返回：1-based 无重边无自环边列表。
    # connected 仅支持无向图；dag 要求 directed=True。副作用：推进随机状态。
    def graph(self, n, m, directed=False, connected=False, dag=False):
        if n < 1 or (connected and directed) or (dag and not directed):
            raise ValueError('invalid graph options')
        maximum = n * (n - 1) // (1 if directed and not dag else 2)
        if not 0 <= m <= maximum or (connected and m < n - 1):
            raise ValueError('invalid edge count')
        order = self.permutation(n) if dag else list(range(1, n + 1))
        # 枚举候选保证稠密图不会因拒绝采样卡住；仅供小规模对拍。
        candidates = [(order[i], order[j]) for i in range(n) for j in range(n)
                      if (i < j if dag or not directed else i != j)]
        edges = self.tree(n) if connected else []
        used = set(edges)
        rest = [edge for edge in candidates if edge not in used]
        edges += self.rng.sample(rest, m - len(edges))
        self.rng.shuffle(edges)
        return edges

    # 参数：已有边列表、闭权值区间。返回：(u,v,w) 列表；不改原边，推进随机状态。
    def weighted(self, edges, lo, hi):
        if lo > hi:
            raise ValueError('invalid weight range')
        return [(u, v, self.integer(lo, hi)) for u, v in edges]

# 参数：从命令行读取 seed 与可选类型。返回：无；副作用：stdout 输出单组合法输入。
def main():
    seed = int(sys.argv[1]) if len(sys.argv) >= 2 else 1
    kind = sys.argv[2] if len(sys.argv) >= 3 else 'array'
    g = Generator(seed)
    n = g.integer(1, 12)  # 小数据上限应与暴力承受范围一致
    if kind == 'ab':
        print(g.integer(-100, 100), g.integer(1, 100))
    elif kind in ('array', 'permutation', 'string', 'matrix'):
        if kind == 'matrix':
            m = g.integer(1, 8)
            print(n, m)
            for row in g.matrix(n, m, -20, 20):
                print(*row)
        else:
            print(n)
            if kind == 'string':
                print(g.text(n, 'abc'))
            else:
                print(*(g.permutation(n) if kind == 'permutation'
                        else g.array(n, -20, 20)))
    else:
        if kind in ('tree', 'chain', 'star', 'weighted-tree'):
            edges = g.tree(n, kind if kind in ('chain', 'star') else 'random')
            print(n)
        elif kind in ('graph', 'connected', 'directed', 'dag'):
            maximum = n * (n - 1) // (1 if kind == 'directed' else 2)
            m = g.integer(n - 1 if kind == 'connected' else 0, maximum)
            edges = g.graph(n, m, directed=kind in ('directed', 'dag'),
                            connected=kind == 'connected', dag=kind == 'dag')
            print(n, m)
        else:
            raise ValueError('unknown generator kind')
        if kind == 'weighted-tree':
            edges = g.weighted(edges, 1, 100)
        for edge in edges:
            print(*edge)

if __name__ == '__main__':
    main()
```

**直接使用：** 第一参数为种子，第二参数为结构；不传结构时默认数组。默认 n 在 1..12，矩阵列数在 1..8，便于暴力验证。

```bash
python3 gen.py 42 array > sample.in
python3 gen.py 42 permutation
python3 gen.py 42 string
python3 gen.py 42 matrix
python3 gen.py 42 tree
python3 gen.py 42 chain
python3 gen.py 42 star
python3 gen.py 42 weighted-tree
python3 gen.py 42 graph
python3 gen.py 42 connected
python3 gen.py 42 directed
python3 gen.py 42 dag
python3 gen.py 42 ab
```

**输入格式：** 数组/排列/字符串先输出 n，再输出一行数据；矩阵先输出 n m，再输出各行；树先输出 n，再输出 n-1 条边；图先输出 n m，再输出 m 条边。`ab` 只输出两个整数；带权树输出 u v w。多测题需自行在最外层输出 T 并循环生成，不要把这些格式直接套进任意题目。

**组合调用：** 以下是修改生成器正文时可用的片段，不是额外独立文件。

```text
g = Generator(seed)
a = g.array(10, -100, 100)              # 普通数组
b = g.array(10, 1, 100, distinct=True)  # 互异数组
increasing = sorted(a)                 # 非递减；严格递增用 sorted(b)
equal = [g.integer(-10, 10)] * 10      # 全相等边界
edges = g.tree(10, 'star')             # 星形，点号和边序均打乱
edges = g.tree(10, relabel=False)      # 每个 v 的父亲编号小于 v
weighted = g.weighted(g.graph(10, 15, connected=True), -5, 20)
```

**坑：** 随机父亲树不均匀覆盖所有标号树，应额外测链、星形和不同根；默认重标号后不能再假设父亲编号小于儿子。简单图无自环无重边，有向图允许同时存在 u→v 与 v→u，DAG 不允许环。`graph` 枚举所有候选边，仅供小数据；大规模压力测试应另写 O(n+m) 的特定构造。浮点、重边、自环、二分图、森林等需按题意扩展，不能把违反前提的随机数据当反例。随机测试不保证覆盖极值；边界构造见 1.11。

## 1.7 暴力程序与正确性基准

**用途：** 对拍沿用“生成器 / 暴力 / 被测程序”三个文件，通常命名 `a_gen.py`、`a_bf.cpp`、`a.cpp`。暴力只需支持生成器的小规模输入，但输入格式和答案定义必须与正式解相同。不要复制优化算法的核心逻辑；双方可能以同一种方式出错。

**A+B 基准：** 保存为 `a_bf.cpp`。输入两个 long long，输出两者之和；本例只用于说明文件接口，要求和落在 long long 范围内。

```cpp
#include <iostream>
using namespace std;

// 参数：标准输入两个 long long，和不溢出。返回：0；副作用：stdout 写出和。
int main() {
    long long a, b;
    if (!(cin >> a >> b)) return 1;
    cout << a + b << '\n';
}
```

**要改哪里：** 数组题可按定义枚举子数组或子集，树题逐点 BFS/DFS，图题用更慢但容易确认的算法。规模按暴力成本选择，例如枚举子集限制 n<=20 左右，O(n³) 则只造更小数据。先手算最小输入确认暴力，再接入 1.8。

**坑：** 对拍发现差异后同时检查暴力与生成器；不能默认暴力必对。多解构造题应验证输出合法性；浮点题按题面容差比较，不能沿用 token 完全相等。复杂度是暴力自身耗时加 O(输入输出大小)，不应把此程序提交为正式解。

## 1.8 自动对拍与失败保留

**用途：** 按三个程序依次执行：生成器写输入，暴力算 `.ans`，被测程序算 `.out`，不一致就停止。下方保存为 `check.py`，与 1.4 的 `run.py` 同目录；程序支持 C++ / Python 混用。文件名从参数传入，生成器接收递增种子，每次执行检查 RE/TLE，默认最多 1000 轮，避免无界循环。

```python
import subprocess as s
import sys
from pathlib import Path
from run import build, execute

# 参数：被测/暴力/生成器路径，正轮数和时限。返回：0=全过、1=失败；副作用：编译与保存失败文件。
def stress(source, brute, generator, rounds=1000, timeout=2):
    if rounds <= 0 or timeout <= 0:
        raise ValueError('rounds and timeout must be positive')
    M, B, G = build(source), build(brute), build(generator)
    for seed in range(1, rounds + 1):
        data, error = execute(G + [str(seed)], b'', timeout)
        expected, got = b'', b''
        stage = 'generator'
        if not error:
            stage = 'brute'
            expected, error = execute(B, data, timeout)
        if not error:
            stage = 'solution'
            got, error = execute(M, data, timeout)
        if error or got.split() != expected.split():
            # 每次失败覆盖旧文件；下次对拍前备份有价值的反例。
            Path('fail.in').write_bytes(data)
            Path('fail.ans').write_bytes(expected)
            Path('fail.out').write_bytes(got)
            detail = f'seed={seed}, {stage}: {error or "WA"}'
            Path('fail.txt').write_text(detail + '\n', encoding='utf-8')
            print(detail)
            return 1
        print(f'AC {seed}', flush=True)
    return 0

if __name__ == '__main__':
    if len(sys.argv) not in (4, 5):
        raise SystemExit('usage: python3 check.py a.cpp a_bf.cpp gen.py [rounds]')
    try:
        raise SystemExit(stress(*sys.argv[1:4],
                               rounds=int(sys.argv[4]) if len(sys.argv) == 5 else 1000))
    except (OSError, ValueError, s.CalledProcessError) as error:
        raise SystemExit(str(error))
```

```bash
# a_gen.py 从 argv[1] 接收 seed，stdout 只写合法题目输入。
python3 check.py a.cpp a_bf.cpp a_gen.py 1000
# 基准也可以用 Python；C++ 生成器也可用。
python3 check.py a.cpp a_bf.py a_gen.cpp 1000
# 失败后手动复现，必要时用 1.4 的 Sanitizer 版运行。
python3 run.py a.cpp < fail.in
```

**变量与文件：** `G/B/M` 为生成器/暴力/被测程序的启动命令；`seed` 从 1 递增。失败写 `fail.in`（输入）、`fail.ans`（基准输出）、`fail.out`（被测输出）、`fail.txt`（种子、阶段、错误）。若生成器或暴力先失败，后续程序不执行，对应输出为空；先修发生错误的阶段。每次失败覆盖上一份文件，重要反例应另存。

**复杂度：** 编译各一次，每轮为三个程序耗时加启动和输入输出成本；每个进程默认限时 2 秒，可在 `stress` 参数中调整。输出捕获占 O(单轮输入输出总大小) 内存。脚本在首个失败停止，不自动缩减反例；先保存，再手工删元素/边并复跑。

**坑：** `split()` 忽略空白差异，不支持浮点容差或多解等价。给生成器传 seed 不代表它一定使用 seed，应核对 1.6 的入口。对拍通过只代表这些数据一致；RE/TLE 不能按 WA 随便修改算法。并行对拍应使用不同工作目录，避免覆盖失败文件。

## 1.9 文件与标准流切换

**用途：** 三个脚本都使用标准输入输出，与题目程序解耦。优先用 shell 重定向，无需在提交代码中加入 `freopen`；确实要求文件 IO 的题目才按题面文件名修改。

```bash
# stdout 是正式答案，stderr 是日志；二者分别保留。
python3 run.py a.cpp < fail.in > actual.out 2> debug.log
./a_dbg < fail.in > actual.out 2> sanitizer.log
# 直接检查反例，不经过输出重定向，日志会显示在终端。
python3 run.py a.cpp < fail.in
```

**坑：** 文件名相对当前目录解析；`>` 覆盖文件，不能把输入路径当输出路径。`2>` 写 stderr，不参与答案比较。不要假设所有 OJ 都定义 `ONLINE_JUDGE`；提交代码保留本地 `freopen` 会读不到数据。交互题每次询问都要 flush，不能用批量样例脚本替代交互器。

## 1.10 WA、RE、TLE、MLE 与 UB 排查

**问题：** 按现象分别检查建模/边界、非法访问、渐进复杂度/常数、峰值内存和未定义行为。先用最小失败输入复现，再结合编译警告、Sanitizer 与计时定位。

**思路：**

- CE：在与评测相同标准下编译，查看第一条错误，确认提交语言和入口函数。
- WA：手算最小反例，核对输入含义、开闭区间、无解输出、取模与浮点格式。
- RE：用失败输入跑 Sanitizer，检查数组下标、递归深度、迭代器和除数。
- TLE/OLE：确认循环会推进、输出量有限，再重新计算最坏复杂度和总测试规模。
- MLE：计算峰值而非单数组大小，关注 `vector<vector<...>>`、DP 多份表和按值传参。

**排查命令。**

```bash
# 1. 带警告编译；2. 用检查版复现；3. 查看峰值时间和内存（GNU/Linux）。
g++ a.cpp -std=c++17 -O2 -Wall -Wextra -Wshadow -o a
g++ a.cpp -std=c++17 -O1 -g \
  -fsanitize=address,undefined -fno-omit-frame-pointer -o a_dbg
./a_dbg < fail.in
/usr/bin/time -v ./a < maximal.in > /dev/null
```

**易错点：**

1. 看到 RE 就盲目加大数组；根因也可能是负下标、栈溢出或除零。
2. 随机修改代码后失败样例消失，就误以为问题已修复；UB 可能只改变表现。
3. 只测样例，未覆盖最大规模、不可达、重复边、负数和空答案。
4. 诊断 TLE 时只看主算法，忽略重复清空、容器复制和调试输出。

**参考：**

- [OI Wiki：题型概述·评测结果](https://oi-wiki.org/contest/problems/)
- [OI Wiki：常见错误](https://oi-wiki.org/contest/common-mistakes/)
- [OI Wiki：编译优化·未定义行为](https://oi-wiki.org/lang/optimizations/)

## 1.11 边界数据检查清单

**问题：** 根据约束逐项构造最小、最大、重复、单调、全相等、不可达和答案极值等输入。边界测试用于验证实现假设，复杂度仍需单独证明。

**思路：**

- 规模：$n=0$（若允许）、$n=1$、最小合法值、最大 $n,m,T$、总规模上限。
- 数值：全 0、全负、全相等、最小/最大值、答案刚好越过 `int`、乘法溢出。
- 序列：递增、递减、回文、重复集中、答案在首尾、空答案和唯一答案。
- 图树：孤点、断开、重边、自环（若允许）、链、星、完全图、源点即终点。
- 区间：单点、全区间、端点相接、左右边界、开闭含义；多测检查上一组残留。

**检查清单。**

```text
[ ] 手算并通过最小合法输入
[ ] 测试空答案、无解、唯一解、多解
[ ] 测试全相等、严格递增、严格递减
[ ] 测试 0、负数、最大值与 long long 溢出边缘
[ ] 测试下标 0/1、n-1/n、区间端点和源点等于终点
[ ] 测试断开图、重边、自环、链、星（按题面允许范围）
[ ] 测试两组连续输入，第二组比第一组小
[ ] 最大数据下检查时间、内存和递归深度
[ ] 核对输出大小写、空格、换行、精度和 Case 编号
```

**易错点：**

1. 构造了题面不允许的数据并据此“修复”，反而破坏正确逻辑。
2. 只测 $n=1$，未测答案在最后一个元素或最后一条边的情形。
3. 多测只用相同大小，未发现第二组变小时的残留数组内容。
4. 随机数据代替结构数据；链、星、全相等等退化形状出现概率极低。

**参考：**

- [OI Wiki：常见错误](https://oi-wiki.org/contest/common-mistakes/)
- [OI Wiki：出题·数据与样例](https://oi-wiki.org/contest/problemsetting/)

**接入生成器：** `gen.py` 的随机模式之外，手工指定 n=1、值域端点；数组测全相等、递增、递减和重复值；树测 chain/star/random；图测 m=0、完全图、连通下界 m=n-1，以及题面允许的断开图。生成大数据前先估计 1.6 的 O(n²) 候选空间；不要拿小数据图生成器造十万点图。

## 1.12 整数溢出与浮点精度

**问题：** 根据最大中间结果选择整数类型，并在乘法前提升类型；累加、平方和及哨兵运算都要检查范围。浮点比较按误差模型选绝对/相对误差，避免随意固定 epsilon。

**思路：**

- 和、距离、计数优先用 `long long`；乘法写 `1LL * a * b`。
- 可能超过约 $9\times10^{18}$ 的整数中间值用 `__int128`，输出需自行转换。
- 无穷大取 `numeric_limits<ll>::max()/4`，加法前先排除不可达状态。
- 浮点比较用 `abs(a-b) <= eps * max(1,abs(a),abs(b))` 的混合误差。
- 输出按题意使用 `fixed << setprecision(k)`；几何 EPS 应结合坐标范围调整。


```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using i128 = __int128_t;
using u128 = __uint128_t;

// 参数：待比较实数及相对/绝对容差 eps。返回：混合误差下是否近似相等。效果：无副作用。
bool almostEqual(long double a, long double b,
                 long double eps = 1e-12L) {
    // 同时照顾接近 0 的绝对误差和大数的相对误差。
    return fabsl(a - b) <= eps * max({1.0L, fabsl(a), fabsl(b)});
}

// 参数：有符号 128 位整数。返回：十进制文本。效果：无副作用，支持最小负值。
string toString(i128 value) {
    if (value == 0) return "0";
    bool negative = value < 0;
    // 先加一再取负，避免直接对 i128 最小值取负导致溢出。
    u128 magnitude = negative ? static_cast<u128>(-(value + 1)) + 1
                              : static_cast<u128>(value);
    string result;
    while (magnitude > 0) {
        result.push_back(static_cast<char>('0' + magnitude % 10));
        magnitude /= 10;
    }
    if (negative) result.push_back('-');
    reverse(result.begin(), result.end());
    return result;
}

// 参数：两个 long long 因子。返回：精确的 128 位乘积。效果：先扩宽再相乘，避免 64 位乘法溢出。
i128 safeProduct(ll a, ll b) {
    return static_cast<i128>(a) * b; // 转换必须发生在乘法之前
}
```

**易错点：**

1. `long long product = a * b;` 中 `a,b` 为 `int` 时，乘法可能已溢出。
2. 有符号整数溢出是 UB，不能依赖“自然回绕”。
3. 用 `a == b` 判断计算所得浮点数，或所有问题固定使用同一个 EPS。
4. `NaN` 与任何数（包括自身）比较都不相等；异常值应用 `isfinite` 检查。

**参考：**

- [OI Wiki：变量·整数与浮点类型](https://oi-wiki.org/lang/var/)
- [OI Wiki：常见错误](https://oi-wiki.org/contest/common-mistakes/)
- [OI Wiki：编译优化·未定义行为](https://oi-wiki.org/lang/optimizations/)

## 1.13 赛中提交与三人协作流程

**问题：** 三人协作时约定接口、变量/编号口径和提交负责人，避免多人同时改同一文件。提交前确认编译标准、样例、边界、多测清理与输出格式，并保留可回滚版本。

**思路：**

- 开场快速读题，记录题意确定度、预估难度、算法、实现者和卡点；优先稳题。
- 维护纸面或离线状态表：未读、在读、待证明、编码、测试、已交、待修。
- 上机前写清状态、关键公式和边界；机器优先给已证明、可快速 AC 的实现。
- 提交前由另一人核对题号、语言、复杂度、清空、整数范围、样例和文件内容。
- 收到 WA/RE/TLE 后先保留版本与失败假设，再决定调试、重写或暂时换题。
- 封榜期按“通过概率 × 题目收益 ÷ 预计时间”排序，不因 sunk cost 长时间单点卡题。

**提交前检查。**

```text
[ ] 提交的是正确题号、正确文件、正确语言标准
[ ] 已删除本地 freopen，或确认评测定义 ONLINE_JUDGE
[ ] 调试信息不进入 stdout，交互题每次询问都 flush
[ ] 复杂度覆盖最大 n、m、T 和所有测试总规模
[ ] long long / __int128、INF 加法、取模和浮点精度正确
[ ] 多测状态已清空；数组、字符串、图的下标边界正确
[ ] 样例、最小数据、无解数据、手造边界均通过
[ ] 队友复述了算法并审过最危险的三处代码
```

**易错点：**

1. 三人同时围着一份代码调试，导致无人继续读题或准备下一题。
2. 未证明就抢机器编码，写完才发现模型或复杂度不成立。
3. WA 后立即重复提交同一份代码，产生无信息增益的罚时。
4. 只口头同步进度；长时间后队友不知道谁在做什么、哪题可接手。
5. 提交窗口选错题号、语言或旧文件，这是最不值得的罚时。

**参考：**

- [OI Wiki：ICPC/CCPC 赛事与赛制](https://oi-wiki.org/contest/icpc/)
- [OI Wiki：题型概述](https://oi-wiki.org/contest/problems/)

## 1.14 Python 调试与随机对拍

**土制 CPH：** 样例需自己准备，脚本不下载题目。本节集中保存批量样例脚本 `cph.py`；随机对拍统一使用 1.8 的 `check.py`，不再维护另一份题目专用对拍器。与 `run.py` 放同一目录，使用 `.in` 输入、同名 `.ans` 标准答案，实际输出写 `.out`。

```python
import subprocess as s
import sys
from pathlib import Path
from run import build, execute

# 参数：源码名、可选样例目录。返回：0=全过、1=失败；副作用：编译、运行并写 .out。
def main(source, directory=None):
    cmd = build(source)
    # a.cpp / /path/a.cpp 默认都对应当前目录 samples-A。
    directory = directory or f'samples-{Path(source).stem[0].upper()}'
    inputs = sorted(Path(directory).glob('*.in'))
    if not inputs:
        raise ValueError(f'no .in samples in {directory}')
    failed = False
    for inp in inputs:
        expected = inp.with_suffix('.ans').read_bytes()
        got, error = execute(cmd, inp.read_bytes())
        inp.with_suffix('.out').write_bytes(got)
        verdict = error or ('AC' if got.split() == expected.split() else 'WA')
        print(f'{inp}: {verdict}')
        failed |= verdict != 'AC'
    return int(failed)

if __name__ == '__main__':
    if len(sys.argv) not in (2, 3):
        raise SystemExit('usage: python3 cph.py a.cpp [samples-A]')
    try:
        raise SystemExit(main(*sys.argv[1:]))
    except (OSError, ValueError, s.CalledProcessError) as error:
        raise SystemExit(str(error))
```

```text
work/
  run.py
  cph.py
  a.cpp
  samples-A/
    1.in      # 3 5
    1.ans     # 8
    2.in      # 10 0
    2.ans     # 10
```

```bash
python3 cph.py a.cpp             # 默认 samples-A
python3 cph.py a.py samples-A    # 显式目录，不依赖题号
```

**效果：** 正确 A+B 两组均 AC；把加法写成减法时第一组 WA、第二组仍 AC。脚本每组默认 2 秒，依次显示 AC/WA/RE/TLE；全部通过返回 0，否则返回 1。没有 `.in`、缺少 `.ans` 或编译失败会报错，不会空跑后宣称通过。时间是各样例耗时和读写成本之和，内存是当前样例输入输出大小。

**本地调试速查：** `print(repr(x), file=sys.stderr)` 查看不可见字符；`assert` 检查不变量；`breakpoint()` 可交互单步，提交前移除。`itertools.product/permutations/combinations` 可写独立枚举基准，但应先估算指数/阶乘规模。浮点用题面容差，多解输出使用 validator，均需替换脚本中的 token 比较。

## 1.15 Python 运行、土制 CPH 与三程序对拍 {#practice-python-runner}

**一套文件串起来：** 先保存 1.4 的 `run.py`、1.6 的 `gen.py`、1.8 的 `check.py`、1.14 的 `cph.py` 到同一工作目录。`gen.py` 可独立运行，另两个脚本导入 `run.py`。依赖仅为 Python 标准库和 `g++`，命令从题目工作目录执行。

**A+B 演练：** 从 1.7 复制 `a_bf.cpp`，再另存 `a.cpp`。手工准备 `samples-A/1.in` 为 `3 5`、`1.ans` 为 `8`，第二组 `2.in` 为 `10 0`、`2.ans` 为 `10`。为了让对拍按 A+B 格式生成数据，将下面保存为 `a_gen.py`，不要用默认输出数组的 `gen.py` 直接对拍 A+B。

```python
import sys
from gen import Generator

if __name__ == '__main__':
    g = Generator(int(sys.argv[1]))
    print(g.integer(-100, 100), g.integer(1, 100))
```

```bash
python3 run.py a.cpp < samples-A/1.in  # 8
python3 cph.py a.cpp                  # 两组 AC
python3 check.py a.cpp a_bf.cpp a_gen.py 100  # AC 1 ... AC 100
# 故意把 a.cpp 中 a+b 改为 a-b，再执行：
python3 cph.py a.cpp                  # 第一组 WA，第二组 AC
python3 check.py a.cpp a_bf.cpp a_gen.py 100  # 首轮 WA，保存反例
python3 run.py a.cpp < fail.in        # 对照 fail.ans 定位错误
```

**改成结构题：** 只修改 `a_gen.py` 的输出格式与独立暴力；运行、样例和对拍脚本都不用改。调用 `g.array(...)`、`g.tree(...)` 或 `g.graph(...)`（见 1.6），按题面打印 n/m、点权和边。先用 1.11 的确定边界，再随机覆盖；修复后重新跑原反例、全部样例和一批随机数据。

**现场顺序：** `run.py` 先验证能编译和读入 → `cph.py` 验固定样例 → `check.py` 找小反例 → `DBG` / Sanitizer 定位 → 重新回归 → 按 1.13 核对提交。

## 1.16 一键随机造数、对拍与错误组输出 {#practice-auto-stress}

**用途：** 保存下方为 `auto.py`，与 1.4 的 `run.py`、1.6 的 `gen.py` 放在一起。一条命令自动编译被测程序和独立暴力，逐轮生成输入、运行双方、显示 AC/WA/RE/TLE，遇到第一组错误立即打印完整输入、预期输出和实际输出，并保存为可供 `cph.py` 复测的样例目录。无需手工准备 `.in/.ans`，也无需为内置结构另写生成器。

**前提：** 仍需提供符合题意的独立暴力程序；通用脚本不能自动推导任意题目的正确答案。默认输入格式来自 1.6，例如 `array` 为 n 和一行数组，`tree` 为 n 和 n-1 条边。若题目有多测、点权或其他格式，用 `--gen a_gen.py` 替换生成器；自定义生成器只接收种子参数，结构选项不再生效。

```python
import argparse
import subprocess as s
import sys
from pathlib import Path
from run import build, execute

# 参数：标题、任意输出字节。返回：无；副作用：终端打印完整内容，空内容明确标识。
def show(title, data):
    print(f'--- {title} ---')
    text = data.decode('utf-8', errors='replace')
    print(text if text else '(empty)', end='' if text.endswith('\n') else '\n')

# 参数：命令行源码、结构与测试配置。返回：0=全过、1=首组失败；副作用：编译、造数、运行、打印与保存。
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='被测 .cpp/.py')
    parser.add_argument('brute', help='独立暴力 .cpp/.py')
    parser.add_argument('--kind', default='array', choices=[
        'ab', 'array', 'permutation', 'string', 'matrix', 'tree', 'chain',
        'star', 'weighted-tree', 'graph', 'connected', 'directed', 'dag'])
    parser.add_argument('--gen', help='自定义 .cpp/.py 生成器，接收 seed')
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--rounds', type=int, default=1000)
    parser.add_argument('--timeout', type=float, default=2)
    parser.add_argument('--output', default='auto-fail')
    args = parser.parse_args()
    if args.rounds <= 0 or args.timeout <= 0:
        parser.error('rounds and timeout must be positive')
    M, B = build(args.source), build(args.brute)
    if args.gen:
        G = build(args.gen)
    else:
        generator = Path(__file__).resolve().with_name('gen.py')
        if not generator.is_file():
            raise FileNotFoundError(generator)
        G = [sys.executable, str(generator)]
    for case in range(1, args.rounds + 1):
        seed = args.seed + case - 1
        command = G + [str(seed)] + ([] if args.gen else [args.kind])
        data, error = execute(command, b'', args.timeout)
        expected, got = b'', b''
        stage = 'generator'
        if not error:
            stage = 'brute'
            expected, error = execute(B, data, args.timeout)
        if not error:
            stage = 'solution'
            got, error = execute(M, data, args.timeout)
        verdict = error or ('AC' if got.split() == expected.split() else 'WA')
        print(f'case={case} seed={seed}: {stage} {verdict}', flush=True)
        if verdict == 'AC':
            continue
        folder = Path(args.output)
        folder.mkdir(parents=True, exist_ok=True)
        for suffix, content in [('in', data), ('ans', expected), ('out', got)]:
            (folder / f'case.{suffix}').write_bytes(content)
        detail = f'case={case} seed={seed} stage={stage}\n{verdict}\n'
        (folder / 'case.txt').write_text(detail, encoding='utf-8')
        show('INPUT', data)
        show('EXPECTED (brute)', expected)
        show('ACTUAL (solution)', got)
        print(f'Saved: {folder.resolve()}')
        return 1
    print(f'PASS: {args.rounds} cases, first seed={args.seed}')
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, s.CalledProcessError) as error:
        raise SystemExit(str(error))
```

**怎么调用：** 以 1.7 的 A+B 程序另存为 `a.cpp` 和 `a_bf.cpp`，不需要样例文件或 `a_gen.py`。正确版全过；将 `a.cpp` 的 `a+b` 故意改为 `a-b` 后，首轮就输出错误组（生成器保证 b>=1）。

```bash
python3 auto.py a.cpp a_bf.cpp --kind ab --rounds 100
# 数组题：输入为 n 和一行数组；暴力与被测程序都应读取此格式。
python3 auto.py a.cpp a_bf.cpp --kind array --rounds 1000
# 树题和图题：选择与题面匹配的生成结构。
python3 auto.py a.cpp a_bf.cpp --kind tree
python3 auto.py a.cpp a_bf.cpp --kind connected
# 非标准输入格式：改用自定义生成器，仍然全自动循环。
python3 auto.py a.cpp a_bf.py --gen a_gen.py --timeout 3
# 复现失败 seed，或把保存的错误组当作固定样例再次检查。
python3 auto.py a.cpp a_bf.cpp --kind ab --seed 42 --rounds 1
python3 cph.py a.cpp auto-fail
python3 run.py a.cpp < auto-fail/case.in
```

**错误组展示：** 下例固定 `--kind ab --seed 42 --rounds 1`，被测程序故意用减法，正确暴力用加法。

```text
case=1 seed=42: solution WA
--- INPUT ---
-72 4
--- EXPECTED (brute) ---
-68
--- ACTUAL (solution) ---
-76
Saved: 当前工作目录/auto-fail
```

**文件与修改点：** `auto-fail/case.in`、`case.ans`、`case.out` 为同一组输入和双方输出，`case.txt` 记录 seed、阶段、错误信息。生成器或暴力发生 RE/TLE 时，后续程序不执行，对应输出为空；此时先修基准，不能把空答案当合法样例。更换题目主要改暴力和生成格式，规模、值域在 `gen.py` 中调整；`--output` 可为不同题目指定不同失败目录。修复后先复测保留样例，再跑新的随机种子。

**复杂度与边界：** C++ 启动时各编译一次；每轮成本为生成器、暴力和被测程序的时间加输入输出。每次执行单独限时，内存与单轮输入输出总量成正比，图生成器额外使用 O(n²) 候选空间。失败文件每次覆盖，全部通过时不清除上次留下的反例。输出按空白 token 比较；浮点、多解或严格格式题需要替换比较条件。测试小数据不能替代最大数据的时间、内存检查。
