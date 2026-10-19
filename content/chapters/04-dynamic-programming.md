# 4. 动态规划

## 4.1 DP 入门：状态、转移与顺序

**1. 它是做什么的**

本例解决“从一列数中选若干个，不能选相邻位置，求最大和”的问题。输入 `value[1..n]`，输出最大和及一组达到最大和的 1-based 下标。允许一个都不选，因此所有数为负时答案为 0。模板只适用于相邻约束和加法权值这一具体模型；其他题目需重新定义状态和转移。

令 `dp[i]` 表示只看前 `i` 个位置、允许空选时的最大和。对位置 `i`，要么不选它，答案沿用 `dp[i-1]`；要么选它，此时 `i-1` 不能选，候选值是 `dp[i-2]+value[i]`。初始化 `dp[0]=0`，`dp[1]=max(0,value[1])`。计算每个状态花费 $O(1)$，总时间 $O(n)$，保存 DP 表及输入需要 $O(n)$ 空间；恢复下标另需至多 $O(n)$ 时间和空间。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `value` | 1-based 权值数组，`value[1]` 是第一个数；`value[0]` 不使用。 |
| `n` | 由 `value.size()-1` 得到的元素数；空输入约定为仅含占位的 `{0}`。 |
| `dp[i]` | 前 `i` 个位置允许空选时的最大总和，不是“必须选第 `i` 个”的最优值。 |
| `chosen` | 回溯过程中收集的 1-based 下标；最终反转为递增顺序。 |
| `maximumSum` | `dp[n]`，即允许空选的最大和。 |

状态初始化为 0 表示空选可行。若多个方案同样最优，回溯遇到 `dp[i]==dp[i-1]` 时固定跳过 `i`，所以只保证返回其中一组，不保证特定的字典序或元素数最少。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `maximumNonAdjacentSum` | `value[1..n]` 的 `long long` 权值；返回 `LineDPResult`。 | 返回最大和及一组互不相邻的 1-based 下标。允许空选；空输入 `{0}` 返回和 0、空下标。输入向量不修改。 |

`LineDPResult` 包含 `maximumSum` 和 `chosenIndices`。函数每次调用都新建 DP 表，状态不会跨调用保留。

**4. 怎么调用**

准备一个首位占位的向量，调用函数，再读取总和和下标。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct LineDPResult {
    ll maximumSum;
    vector<int> chosenIndices; // 1-based
};

// 参数：value[1..n] 的 long long 权值。返回：最大和与一组 1-based 互不相邻下标；允许空选。效果：O(n) 时间、空间。
LineDPResult maximumNonAdjacentSum(const vector<ll>& value) {
    // value 使用 1-based；dp[i] 表示前 i 个位置允许空选时的最大和。
    int n = static_cast<int>(value.size()) - 1; // value[1..n]
    vector<ll> dp(n + 1, 0);
    if (n >= 1) dp[1] = max(0LL, value[1]);
    for (int i = 2; i <= n; ++i) {
        // 不选 i 继承 dp[i-1]；选 i 时前一个可选前缀只能到 i-2。
        dp[i] = max(dp[i - 1], dp[i - 2] + value[i]);
    }

    vector<int> chosen;
    // 从 dp[n] 逆推一组最优下标；相等时固定选择“不取 i”。
    for (int i = n; i >= 1;) {
        if (i == 1) {
            if (dp[i] > 0) chosen.push_back(1);
            break;
        }
        if (dp[i] == dp[i - 1]) {
            --i;
        } else {
            chosen.push_back(i);
            i -= 2;
        }
    }
    reverse(chosen.begin(), chosen.end());
    return {dp[n], chosen};
}
```

可在业务函数中直接使用以下输入和断言：权值 `[5,1,4]` 时选择位置 1 和 3，总和为 9。

```text
vector<ll> value = {0, 5, 1, 4};
LineDPResult result = maximumNonAdjacentSum(value);
assert(result.maximumSum == 9);
assert((result.chosenIndices == vector<int>{1, 3}));
```

**5. 要改哪里**

- 若允许空选，应保留当前 `max(0LL, value[1])` 初始化；若必须至少选一个，`dp` 不能全置 0，需用不可达哨兵并重写边界与恢复逻辑。
- 若不能相邻的限制改成至少间隔 `k` 个位置，选择 `i` 时依赖的前缀会改变为 `i-k-1`，同时处理下标越界的基例。
- 若要统计最优方案数，状态需同时维护最优值和方案数，并在两条转移相等时累加计数。
- 若只要最大和且不恢复方案，可用常数个变量滚动保存前两状态；当前接口返回下标，仍需保留 DP 信息或改用前驱记录。

**6. 自检**

输入 `[5,1,4]`，最优选择 `{1,3}`，和为 9。单元素 `[−3]` 返回 0 和空下标；单元素 `[6]` 返回 6 和 `{1}`。全负序列允许空选，答案仍为 0。重复权值 `[2,2,2]` 的最大和为 4，返回的一组下标应互不相邻且总权值确为 4。

**7. 坑**

1. 把 `dp[i]` 误解为“必须选 i”；这会导致初始化和回溯条件不匹配，先固定状态定义再写转移。
2. 允许空选却把 `dp[1]` 设成负数；全负输入会产生错误答案，应将其与 0 取最大。
3. 输入按 0-based 提供却直接传入；函数约定首位是占位，真实元素从下标 1 开始。
4. 只按 `dp[i]` 值恢复却忽略相等情况；平局时本实现跳过当前位置，得到的仍是最优方案。

**8. 一句话原理**

每个位置只需比较“不选它”和“选它并接上前一个不相邻前缀”的最优值，再沿同一转移回溯方案。

**参考：**

- [OI Wiki：动态规划基础](https://oi-wiki.org/dp/basic/)
- [OI Wiki：记忆化搜索](https://oi-wiki.org/dp/memo/)

## 4.2 0-1 背包

**1. 它是做什么的**

给定 `n` 件物品，每件有非负整数重量与 `long long` 价值，且每件最多选一次，求容量不超过 `capacity` 时的最大价值。模板另提供恰好装满版本：返回能恰好达到容量的最大价值，无解时返回空 `optional`。重量和价值数组按 0-based 下标对应，长度必须相同；容量非负且 `O(n*capacity)` 的时间和 `O(capacity)` 的内存可接受。

普通版本允许不装满，空选价值为 0；恰好版本只把重量 0 设为可达。处理每件物品时容量倒序，防止当前物品在同一轮被重复使用。两种接口每件物品最多更新 `capacity+1` 个状态，时间 $O(nC)$、额外空间 $O(C)$，其中 `C=capacity`。返回值和状态运算须能放入 `long long`；exact 版所有可达状态的最优值还须严格大于 `NEG_INF`，否则应另设可达标记。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `weight[i]`、`value[i]` | 第 `i` 件物品的重量和值，`i` 从 0 到 `n-1`；两向量必须一一对应。 |
| `capacity` | 容量上限或恰好要求的重量，必须非负。 |
| `dp[j]`（普通版） | 处理过的物品中，总重量不超过 `j` 的最大价值。所有状态初值 0，表示可以不选。 |
| `dp[j]`（恰好版） | 当前恰好组成重量 `j` 的最大价值；仅 `dp[0]=0` 初始可达，其余用 `NEG_INF` 标记不可达。 |
| `NEG_INF` | 安全的负哨兵；不可达状态参与加法会产生虚假方案，所以转移前先判断。 |

倒序遍历的关键是更新 `dp[j]` 时，`dp[j-weight[i]]` 仍是处理第 `i` 件物品之前的状态。重量为 0 时，每个 `j` 仍只处理当前物品一次；正价值可加一次，负价值可不选。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `zeroOneKnapsack` | 平行的重量和值数组、非负容量；返回 `ll`。 | 返回重量不超过容量的最大价值，允许不装满；数组长度须相等，重量非负。 |
| `exactZeroOneKnapsack` | 同上；返回 `optional<ll>`。 | 求恰好装满的最大价值；无法凑出容量时返回 `nullopt`。 |

两个函数都不改输入，每次调用都重新建 DP 数组。重量必须为非负整数；若某个重量大于容量，它在对应转移循环中自然不会被选中。容量数组大小和计算结果须在可用整数范围内。

**4. 怎么调用**

准备平行数组并调用所需版本。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 参数：平行的重量/价值数组与容量；每件至多取一次。返回：不超过容量的最大价值。效果：O(nC)，要求容量非负。
ll zeroOneKnapsack(const vector<int>& weight,
                   const vector<ll>& value,
                   int capacity) {
    // 物品为 0-based；dp[j] 表示总重量不超过 j 的最大价值。
    vector<ll> dp(capacity + 1, 0);
    for (int i = 0; i < static_cast<int>(weight.size()); ++i) {
        // 容量倒序保证右侧 dp[j-weight[i]] 尚未使用当前物品。
        for (int j = capacity; j >= weight[i]; --j) {
            dp[j] = max(dp[j], dp[j - weight[i]] + value[i]);
        }
    }
    return dp[capacity];
}

// 恰好装满时的最大价值；不可达返回 nullopt。
// 参数：平行的重量/价值数组及非负容量；每件至多取一次。返回：恰好装满的最大价值，无解为空。效果：O(nC)。
optional<ll> exactZeroOneKnapsack(const vector<int>& weight,
                                  const vector<ll>& value,
                                  int capacity) {
    const ll NEG_INF = numeric_limits<ll>::lowest() / 4;
    // 除 dp[0] 外均不可达，因而该版本要求最终重量恰好为 capacity。
    vector<ll> dp(capacity + 1, NEG_INF);
    dp[0] = 0;
    for (int i = 0; i < static_cast<int>(weight.size()); ++i) {
        for (int j = capacity; j >= weight[i]; --j) {
            // 不可达状态不能参与加法，否则会制造不存在的方案。
            if (dp[j - weight[i]] != NEG_INF) {
                dp[j] = max(dp[j], dp[j - weight[i]] + value[i]);
            }
        }
    }
    if (dp[capacity] == NEG_INF) return nullopt;
    return dp[capacity];
}
```

以下输入中两件物品分别为 `(重量2,价值3)`、`(重量3,价值4)`。容量不超过 3 的最优价值为 4；恰好装满 3 也为 4；恰好装满 4 无解。

```text
vector<int> weight = {2, 3};
vector<ll> value = {3, 4};
assert(zeroOneKnapsack(weight, value, 3) == 4);
auto exact = exactZeroOneKnapsack(weight, value, 3);
assert(exact.has_value() && *exact == 4);
assert(!exactZeroOneKnapsack(weight, value, 4).has_value());
```

**5. 要改哪里**

- 若只需要最大价值且容量允许空余，调用普通版本；若必须刚好达到给定总重，调用 exact 版本，不能把两种初始化混用。
- 若问题变成完全背包（物品可重复选），状态转移方向需改为容量正序；只改循环方向会改变每件物品的使用次数语义。
- 若只问是否可行，可把价值状态换成布尔状态并用逻辑或转移；若还要求方案数，应改变状态聚合方式。
- 若要恢复具体选取物品，需要额外保存前驱/选择信息，当前接口只返回价值，不返回方案。
- 若重量可为负数或容量极大，当前按整数容量逐格枚举的表示不适用，应改用其他建模或算法。

**6. 自检**

物品 `(2,3)`、`(3,4)` 且容量 3 时，普通版和 exact 版都得到 4；容量 4 的 exact 版无解。容量为 0 且没有零重量物品时，两个版本均返回 0。单件零重量、价值 5 时，容量 0 的两版都只能把它选一次，答案为 5；这也可检查倒序循环在零重量时没有无限循环或重复选取。负价值物品不会提升普通版答案，因为允许不选。

**7. 坑**

1. 0-1 背包容量正序遍历；会让当前物品被重复使用，应倒序更新。
2. exact 版本把所有状态初始化为 0；这会把无法达到的重量误当成可达，除 `dp[0]` 外应使用不可达哨兵。
3. 对不可达状态直接加价值；先判断来源状态不等于 `NEG_INF`。
4. 误以为普通版本必须装满；它求的是重量不超过容量，空选可行。
5. 重量和值数组错位或长度不同；第 `i` 项必须代表同一件物品，并确保两数组等长。

**8. 一句话原理**

逐件物品倒序更新容量状态，让每次转移只使用上一轮结果，从而保证每件物品至多进入方案一次。

**参考：**

- [OI Wiki：背包 DP](https://oi-wiki.org/dp/knapsack/)

## 4.3 完全背包与多重背包

**1. 它是做什么的**

完全背包允许每种物品取任意非负件，多重背包给每种物品一个数量上限。两个接口都求总重量不超过 `capacity` 时的最大价值，允许空选。重量、价值数组按 0-based 对应；多重背包另有同长度的非负数量数组。完全背包要求重量为正，否则正价值零重物品可被无限取，最优值无界。所有重量和容量为非负整数，数组长度需匹配。

完全背包用容量正序转移，时间 $O(nC)$、额外空间 $O(C)$。多重背包将每类数量拆成若干 0-1 组，再倒序更新。令 `K` 为拆出的组数，时间为 $O(CK+n+K)$，空间为 $O(C+K)$（代码显式保存所有拆分组），其中 `K=O(\sum_i \log(count[i]+1))`。拆分组的重量和值以及 DP 结果都须在整数类型范围内。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `weight[i]`、`value[i]` | 第 `i` 类物品单件重量和值，按 0-based 对应。 |
| `count[i]` | 多重背包中第 `i` 类最多可取的件数，必须非负。 |
| `capacity` | 总重量上限，必须非负。 |
| `dp[j]` | 已处理物品下，重量不超过 `j` 时的最大价值；初值 0 表示可留空。 |
| `items` | 多重背包二进制拆分后形成的 `(组重量, 组价值)` 列表；每组只能选一次。 |
| `remaining`、`group`、`take` | 拆分当前物品时的剩余数量、当前二进制组大小，以及本轮实际取出的数量。 |

完全背包的正序让 `dp[j-weight[i]]` 可包含当前物品，因此允许重复取；拆分后的组则必须倒序，避免同一组被重复使用。多重背包每类的组数量之和恰好等于其上限，最后一组取完剩余数量。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `completeKnapsack` | 平行重量/价值数组及容量；返回 `ll`。 | 求不超过容量的最大价值；重量须为正，两个数组长度相同。每次调用重新建 DP，不修改输入。 |
| `multipleKnapsack` | 平行重量/价值/数量数组及容量；返回 `ll`。 | 每类最多取 `count[i]` 件，通过二进制分组转成 0-1 物品后求最大价值；三数组长度相同，重量、数量非负。每次调用重建状态。 |

**4. 怎么调用**

根据物品是否可重复选择调用对应函数。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 参数：平行重量/价值数组与容量；每件可无限取。返回：不超过容量的最大价值。效果：O(nC)，重量须为正。
ll completeKnapsack(const vector<int>& weight,
                    const vector<ll>& value,
                    int capacity) {
    // weight 必须为正；dp[j] 表示容量上限为 j 的最大价值。
    vector<ll> dp(capacity + 1, 0);
    for (int i = 0; i < static_cast<int>(weight.size()); ++i) {
        // 正序使 dp[j-weight[i]] 可含当前物品，从而允许重复选择。
        for (int j = weight[i]; j <= capacity; ++j) {
            dp[j] = max(dp[j], dp[j - weight[i]] + value[i]);
        }
    }
    return dp[capacity];
}

// 参数：重量、价值、数量上限数组与容量。返回：不超过容量的最大价值。效果：二进制拆分，O(CΣlog count)。
ll multipleKnapsack(const vector<int>& weight,
                    const vector<ll>& value,
                    const vector<int>& count,
                    int capacity) {
    // 每个二进制组视为一件只能选择一次的 0-1 物品。
    vector<pair<int, ll>> items;
    for (int i = 0; i < static_cast<int>(weight.size()); ++i) {
        int remaining = count[i];
        for (int group = 1; remaining > 0; group <<= 1) {
            // 最后一组取全部 remaining，确保拆分数量之和恰为 count[i]。
            int take = min(group, remaining);
            items.push_back({weight[i] * take, value[i] * take});
            remaining -= take;
        }
    }

    vector<ll> dp(capacity + 1, 0);
    for (auto [groupWeight, groupValue] : items) {
        // 拆分后的每组只能使用一次，因此容量必须倒序。
        for (int j = capacity; j >= groupWeight; --j) {
            dp[j] = max(dp[j], dp[j - groupWeight] + groupValue);
        }
    }
    return dp[capacity];
}
```

以下两类物品分别为 `(重量2,价值3)` 和 `(重量3,价值4)`。完全背包容量 6 可取三件第一类，重量 6、价值 9，比两件第二类的价值 8 更优。多重背包若第一类最多 2 件、第二类最多 1 件，容量 7 时可全取，价值 10。

```text
vector<int> weight = {2, 3};
vector<ll> value = {3, 4};
assert(completeKnapsack(weight, value, 6) == 9);
vector<int> count = {2, 1};
assert(multipleKnapsack(weight, value, count, 7) == 10);
```

**5. 要改哪里**

- 物品可无限使用时用完全背包；有有限数量上限时用多重背包；每件最多一次时应使用 0-1 背包。
- 完全背包重量必须为正。若重量 0 且价值为正，问题无有限最优值；若价值非正可忽略该类，但本模板没有为此作特殊处理。
- 多重背包只支持非负件数；`count[i]=0` 表示该类不进入拆分列表。
- 若容量很大而总价值较小，可改为“价值为状态、最小重量为状态值”的 DP；需重写状态和转移，不能仅调整循环方向。
- 要恢复选取数量，需要记录每个拆分组是否选中并将结果映射回原类别；当前接口只返回最大价值。

**6. 自检**

完全背包中重量和值分别为 `(2,3)`、`(3,4)`，容量 6 时取三件第一类，得到 9；这能区分完全背包与 0-1 背包。多重背包数量 `{2,1}`、容量 7 时三件都可选，重量 7、价值 10。数量全为 0 时答案为 0；容量为 0 时正重量物品均不能选。完全背包如传入零重量应判为输入违反前提，不应期待有限答案。

**7. 坑**

1. 完全背包容量倒序，导致每类只取一次；它应正序，以复用本轮状态。
2. 多重背包拆分后容量正序，导致单个分组可被重复用；拆分组是 0-1 物品，应倒序。
3. 拆分时遗漏最后的剩余件数；每轮 `take=min(group,remaining)`，才能让各组总数等于上限。
4. 完全背包允许零重量正价值物品；可无限取使答案无界，需排除此输入或另行定义。
5. 拆分后 `weight*take`、`value*take` 或累计结果溢出；按题目范围选择足够宽的类型并预先核算上界。

**8. 一句话原理**

完全背包用正序让当前物品参与后续状态，多重背包先把有限件数拆成 0-1 组再倒序更新。

**参考：**

- [OI Wiki：背包 DP](https://oi-wiki.org/dp/knapsack/)

## 4.4 最长上升子序列（LIS）

**1. 它是做什么的**

给定可比较序列，求一条最长严格递增子序列并返回它在原序列中的下标。子序列保持原有先后次序，但不要求连续。输入下标为 0-based；空输入返回空下标向量。模板用 `lower_bound` 实现严格递增，若要非下降子序列则需改变查找规则。

算法为每个元素二分查找一次，时间 $O(n\log n)$；前驱、尾值和尾下标数组共需 $O(n)$ 空间，输出也至多 $O(n)$。要求元素可由 `<` 严格弱序比较；模板不修改输入。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `a[i]` | 输入第 `i` 个元素，`i` 从 0 开始。 |
| `tailValue[len]` | 当前已见元素中，长度为 `len+1` 的严格递增子序列所能达到的最小末值。 |
| `tailIndex[len]` | 对应 `tailValue[len]` 在原序列中的下标。 |
| `previous[i]` | 以 `a[i]` 结尾的当前构造链中，前一个元素的原数组下标；不存在时为 `-1`。 |
| `position` | `a[i]` 在 `tailValue` 中第一个不小于它的位置，也是它更新的递增子序列长度减一。 |
| `indices` | 从最终尾下标沿 `previous` 逆向收集、再反转得到的答案。 |

`tailValue` 不是最终子序列：替换某个末值只是在保留该长度的更优延伸可能。实际方案通过 `tailIndex` 和 `previous` 追溯，因此输出下标严格递增，且对应值严格递增。

**3. 函数在做什么**

| 函数 | 参数、返回与行为 |
|---|---|
| `longestIncreasingSubsequenceIndices<T>` | 任意可严格比较的只读向量；返回 `vector<int>`。 返回一条最长严格递增子序列的 0-based 下标；输入不改，空向量返回空向量。相同长度的多种答案中返回哪一条由更新和平局顺序决定。 |
| `lower_bound` | 在已排序的 `tailValue` 中查找首个 `>= a[i]` 的位置。 `tailValue` 按严格递增维护；相等值会替换末尾而不增加长度，因此得到严格递增序列。 |

**4. 怎么调用**

将可比较序列传给模板，按返回下标读取元素。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

template <class T>
// 参数：可严格比较序列。返回：一个最长严格递增子序列的 0-based 下标。效果：无副作用，O(n log n)。
vector<int> longestIncreasingSubsequenceIndices(const vector<T>& a) {
    // a 与返回下标均为 0-based；本模板恢复严格上升子序列。
    int n = static_cast<int>(a.size());
    // tailValue[len] 是长度 len+1 的严格上升子序列的最小末值。
    vector<T> tailValue;
    // tailIndex 与 tailValue 同步，保存该末值来自的原数组下标。
    vector<int> tailIndex;
    vector<int> previous(n, -1);

    for (int i = 0; i < n; ++i) {
        // lower_bound 找首个 >= a[i] 的位置；改成 upper_bound 即求非下降。
        int position = static_cast<int>(lower_bound(tailValue.begin(),
                                                   tailValue.end(), a[i])
                                        - tailValue.begin());
        if (position == static_cast<int>(tailValue.size())) {
            tailValue.push_back(a[i]);
            tailIndex.push_back(i);
        } else {
            tailValue[position] = a[i];
            tailIndex[position] = i;
        }
        // 记录长度少一的最优末尾下标，供最终方案沿前驱恢复。
        if (position > 0) previous[i] = tailIndex[position - 1];
    }

    vector<int> indices;
    if (!tailIndex.empty()) {
        for (int i = tailIndex.back(); i != -1; i = previous[i]) {
            indices.push_back(i);
        }
        reverse(indices.begin(), indices.end());
    }
    return indices;
}
```

以下序列 `[3,1,2,2,4]` 的实现会返回 `{1,3,4}`，对应值 `{1,2,4}`，长度为 3：

```text
vector<int> a = {3, 1, 2, 2, 4};
vector<int> indices = longestIncreasingSubsequenceIndices(a);
assert((indices == vector<int>{1, 3, 4}));
assert(a[indices[0]] < a[indices[1]] && a[indices[1]] < a[indices[2]]);
```

**5. 要改哪里**

- 若要求非下降子序列，将 `lower_bound` 换成 `upper_bound`，允许相等值接在已有序列后面。
- 若只需要 LIS 长度，可不保存 `tailIndex` 和 `previous`，只维护尾值数组；当前接口需要恢复下标，不能删掉前驱记录。
- 若要返回值而不是下标，可用返回下标在原数组中取值；若需自定义“递增”关系，必须让二分比较和尾值维护采用一致的严格弱序。
- 若需要统计 LIS 方案数或所有 LIS，单个最小末值状态不足，需要改成更丰富的 DP/数据结构状态。

**6. 自检**

对 `[3,1,2,2,4]`，输出下标应严格递增，值为严格递增的 `{1,2,4}`，长度 3。空序列返回空；单元素 `[7]` 返回一个有效下标 `{0}`。全相同的 `[5,5,5]` 的严格 LIS 长度应为 1；若把查找改为 `upper_bound`，则对应的非下降版本长度为 3。

**7. 坑**

1. 把子序列误当成连续子数组；LIS 可跳过中间元素，但下标必须递增。
2. 严格递增使用 `upper_bound`；相等值会被错误地接到序列末尾，应使用 `lower_bound`。
3. 直接把 `tailValue` 当作答案；它是各长度的最小末值集合，未必能对应同一条链，应沿前驱恢复。
4. 将返回下标当成 1-based；本函数输入与输出都按 0-based。
5. 输入类型没有一致的严格比较关系；二分查找要求比较规则有效且与尾值顺序一致。

**8. 一句话原理**

维护每种长度可达到的最小末值来二分更新，并用前驱下标把最优长度对应的真实子序列链接回来。

**参考：**

- [OI Wiki：最长上升子序列](https://oi-wiki.org/dp/basic/#%E6%9C%80%E9%95%BF%E4%B8%8A%E5%8D%87%E5%AD%90%E5%BA%8F%E5%88%97)

## 4.5 最长公共子序列（LCS）

**1. 它是做什么的**

给定两个序列，求一个最长公共子序列：结果元素按原顺序同时出现在两个输入中，但不要求连续。函数返回其中一条实际元素序列；存在多条最优解时不保证选哪一条。输入可以是任意支持相等比较的类型，空序列也合法。

令 `n=a.size()`、`m=b.size()`。二维 DP 填表需 $O(nm)$ 时间和 $O(nm)$ 空间，回溯方案另需 $O(n+m)$ 时间；输入不修改。模板返回序列本身，不能只把 DP 压成一行而仍按当前方式恢复方案。若只求长度，才可改用滚动数组压到 $O(\min(n,m))$ 空间。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `a`、`b` | 两个 0-based 输入序列。 |
| `n`、`m` | 两个输入长度。 |
| `dp[i][j]` | `a` 的前 `i` 项与 `b` 的前 `j` 项的 LCS 长度；多开一行一列表示空前缀，初值为 0。 |
| `result` | 回溯时逆序收集的公共元素，最后反转成原顺序。 |
| `i`、`j` | 回溯中当前前缀长度；对应比较的是 `a[i-1]` 与 `b[j-1]`。 |

若末项相等，模板将它们一起匹配并接在 `dp[i-1][j-1]` 的解后；否则在两种舍弃一个末项的可能中沿 DP 值不减小的一侧前进。相等时优先向上，因此并列 LCS 的选择受这一规则影响。

**3. 函数在做什么**

| 函数 | 参数、返回与行为 |
|---|---|
| `longestCommonSubsequence<T>` | 两个支持 `==` 的只读向量；返回 `vector<T>`。 返回一个最长公共子序列，元素顺序与两输入一致；空输入时返回空向量，不修改输入。元素类型还需可复制以写入结果。 |
| `reverse` | 反转已收集的结果。 将从末尾回溯得到的逆序元素恢复为正序；模板内部使用。 |

**4. 怎么调用**

直接传入两个同类向量，按返回序列读取。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

template <class T>
// 参数：支持相等比较的两序列。返回：一个最长公共子序列。效果：无副作用，O(nm) 时间与空间。
vector<T> longestCommonSubsequence(const vector<T>& a, const vector<T>& b) {
    // a、b 为 0-based；dp[i][j] 表示两序列前 i、j 个元素的 LCS 长度。
    int n = static_cast<int>(a.size());
    int m = static_cast<int>(b.size());
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
    // i、j 递增，保证左、上、左上三个依赖状态已经计算。
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (a[i - 1] == b[j - 1]) {
                // 最优公共子序列可把这对相同末字符一起接到左上状态。
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                // 末字符不同时，至少舍弃一侧末字符，取两种可能的较优值。
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    vector<T> result;
    // 从右下角逆推；值相等走左上，否则走不减小 dp 的一侧。
    for (int i = n, j = m; i > 0 && j > 0;) {
        if (a[i - 1] == b[j - 1]) {
            result.push_back(a[i - 1]);
            --i;
            --j;
        } else if (dp[i - 1][j] >= dp[i][j - 1]) {
            --i;
        } else {
            --j;
        }
    }
    reverse(result.begin(), result.end());
    return result;
}
```

以下字符串序列用字符向量表示，公共子序列为 `a,c,e`：

```text
vector<char> a = {'a', 'b', 'c', 'd', 'e'};
vector<char> b = {'a', 'c', 'e'};
vector<char> result = longestCommonSubsequence(a, b);
assert((result == vector<char>{'a', 'c', 'e'}));
```

**5. 要改哪里**

- 若只需 LCS 长度，可仅保留两行 DP，并根据依赖滚动更新；当前代码需要完整表来回溯具体序列。
- 若题目要求最长公共子串（连续片段），相等时的状态需从 `dp[i-1][j-1]` 延续，不等时应清零，不能使用本模板的取最大转移。
- 若需统计最优方案数或枚举所有 LCS，当前一个长度值和单一路径回溯不足，须改变状态及恢复方式。
- 若两输入类型不同，需将模板改为适当的比较器或统一元素类型；当前接口要求两个参数都是同一 `T` 类型的向量并支持 `==`。

**6. 自检**

`a=[a,b,c,d,e]`、`b=[a,c,e]` 时，LCS 是 `[a,c,e]`，长度 3。任一输入为空时返回空；两个序列完全相同则返回该序列；两个序列没有共同元素时也返回空。对重复元素输入，结果仍须是两边都能按顺序找到的序列，不能只检查长度。

**7. 坑**

1. 把 LCS 当成连续子串；子序列允许跳过元素，子串不允许。
2. DP 下标混淆前缀长度与原数组下标；状态 `[i][j]` 比较的是 `a[i-1]`、`b[j-1]`。
3. 不相等时直接令当前值为 0；LCS 应取上方和左方最大值。
4. 只返回 DP 长度却以为拿到了方案；当前函数返回的是元素序列，长度可用 `result.size()` 取得。
5. `n*m` 二维表过大导致内存不足；只需长度时改成滚动数组，若需恢复则考虑适合的分治恢复算法。

**8. 一句话原理**

用两个前缀的 LCS 长度作状态，按末元素是否相同递推，再从右下角沿保持最优值的方向恢复一条序列。

**参考：**

- [OI Wiki：动态规划基础](https://oi-wiki.org/dp/basic/)

## 4.6 区间 DP

**1. 它是做什么的**

本模板解决链上相邻石子合并：每次把相邻两堆合为一堆，代价等于这两堆总重量，求合成一堆的最小总代价。输入为 0-based 权值向量，输出最小费用；空输入或只有一堆时返回 0。若题目允许环形合并、合并代价不同或要求其他目标，需调整建模与转移。

`dp[left][right]` 表示闭区间合成一堆的最小代价。枚举区间内最后一次切分位置，左右分别先合并，再加上当前区间总和。前缀和构造为 $O(n)$；区间长度、起点和分割点三重循环，时间 $O(n^3)$；二维 DP 与前缀和共需 $O(n^2)$ 空间。实现使用 `long long` 和 `INF` 哨兵，需保证前缀和、候选费用不溢出且有效答案小于 `INF`。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `stones[i]` | 第 `i` 堆的初始权值，`i` 从 0 到 `n-1`。 |
| `prefix[i]` | 前 `i` 堆的权值和；`prefix[0]=0`。 |
| `dp[left][right]` | 合并连续闭区间 `[left,right]` 为一堆的最小总代价；单点区间初值为 0。 |
| `length` | 当前枚举区间长度，从 2 增至 `n`。 |
| `split` | 最后一次合并前左右区间的分界，范围 `left..right-1`。 |
| `intervalSum` | 当前区间权值和，也就是把左右两堆最后合并时的新增费用。 |
| `INF` | 初始化尚未求出的多元素区间的候选最小值。 |

按长度递增保证 `[left,split]` 与 `[split+1,right]` 已经算好。前缀和用 `prefix[right+1]-prefix[left]` 在常数时间取区间权值。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `minimumMergeCost(stones)` | `long long` 权值向量；返回 `ll`。 | 返回链式相邻合并的最小总费用。输入不修改；空向量和单元素向量返回 0。中间前缀和及 DP 值须可由 `ll` 表示，且有效费用不能与 `INF` 哨兵冲突。 |

函数每次调用都重新构建前缀和与 DP 表；模板没有返回合并顺序或树形结构的接口。

**4. 怎么调用**

把初始堆权值放入向量并调用函数。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = numeric_limits<ll>::max() / 4;

// 参数：相邻合并权值序列。返回：每次合并相邻段、代价为段和时的最小总费用。效果：O(n^3)，空/单元素费用为 0。
ll minimumMergeCost(const vector<ll>& stones) {
    // stones 使用 0-based；dp[left][right] 表示闭区间合成一堆的最小代价。
    int n = static_cast<int>(stones.size());
    if (n == 0) return 0;
    vector<ll> prefix(n + 1, 0);
    for (int i = 0; i < n; ++i) prefix[i + 1] = prefix[i] + stones[i];

    // dp[i][i]=0；按长度递增保证转移所需的两个子区间已经算完。
    vector<vector<ll>> dp(n, vector<ll>(n, 0));
    for (int length = 2; length <= n; ++length) {
        // 所有长度更短的区间都已完成，当前转移可直接读取子区间。
        for (int left = 0; left + length <= n; ++left) {
            int right = left + length - 1;
            dp[left][right] = INF;
            ll intervalSum = prefix[right + 1] - prefix[left];
            // split 将 [left,right] 分成 [left,split] 与 [split+1,right]。
            for (int split = left; split < right; ++split) {
                dp[left][right] = min(dp[left][right],
                    dp[left][split] + dp[split + 1][right] + intervalSum);
            }
        }
    }
    return dp[0][n - 1];
}
```

输入 `[1,2,3,4]` 的最优费用为 19：先合并 `1+2=3`，再合并 `3+3=6`，最后合并 `6+4=10`，总费用 `3+6+10`。

```text
vector<ll> stones = {1, 2, 3, 4};
assert(minimumMergeCost(stones) == 19);
assert(minimumMergeCost(vector<ll>{}) == 0);
```

**5. 要改哪里**

- 若求最大总代价，将区间状态的初值改为负无穷并将 `min` 改成 `max`；还需核对代价定义是否仍是区间和。
- 若合并代价不是当前区间权值和，替换 `+ intervalSum` 为题目定义的代价函数。
- 环形石子合并可将序列复制一遍，在长度至多为原 `n` 的区间中枚举起点，并在所有合法起点结果中取最优；当前函数只计算线性链。
- 若题目具备可证明的四边形不等式/决策单调性，可进一步优化分割点枚举；不能仅因状态形似就跳过 `split` 范围。
- 若需要输出合并顺序，应另存每个区间的最优 `split` 并递归恢复；当前接口只返回费用。

**6. 自检**

`[1,2,3,4]` 的最小费用为 19。空序列和单堆 `[8]` 均为 0。两堆 `[2,5]` 只能合并一次，答案为 7。三堆 `[1,2,3]` 可先合并 `1+2`，费用 `3+6=9`；也可先合并 `2+3`，费用 `5+6=11`，因此答案为 9。检查小规模时可枚举所有相邻合并顺序作对照。

**7. 坑**

1. 区间长度未从小到大枚举；转移读取的子区间可能尚未计算。
2. 分割点写到 `right`；右侧 `[split+1,right]` 将为空，合法范围应为 `left <= split < right`。
3. 把区间 DP 当成任意子集合并；题意要求相邻合并，状态必须是连续闭区间。
4. 前缀和右端写成 `prefix[right]`；`prefix[t]` 表示前 `t` 项，闭区间和应减 `prefix[left]`、取 `prefix[right+1]`。
5. 数值范围超出 `long long` 或答案碰到 `INF`；需依据输入上界选择安全类型/哨兵，并确保加法不溢出。

**8. 一句话原理**

将每个连续区间的最后一次合并位置作为分割点，组合已求出的左右最优值并加上整段合并费用。

**参考：**

- [OI Wiki：区间 DP](https://oi-wiki.org/dp/interval/)

## 4.7 树形 DP

**1. 它是做什么的**

本模板求无向树的最大权独立集：选出的节点中任意两点不能有边相连，最大化所选权值之和。输入是 1-based 连通无环树 `tree` 和 `weight[1..n]`，可指定根；返回根状态中的最大值。允许空集，因此若所有权值为负，答案为 0。若输入是森林，当前函数只遍历指定根所在连通分量。

每个节点在 DFS 中处理一次，每条树边被访问两次，时间 $O(n)$；DP 数组和递归调用栈共需 $O(n)$ 空间。递归深度最坏可达 `n`，长链可能超过运行环境的栈限制。要求根在 `1..n`，邻接表和权值数组至少有 `n+1` 个元素。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `tree[u]` | 与节点 `u` 相邻的节点编号；无向边两端都需记录。 |
| `weight[u]` | 节点 `u` 的权值，编号从 1 开始，0 号位不用。 |
| `root` | DFS 的起点，默认是 1。 |
| `dp[u][0]` | 在 `u` 的子树中不选 `u` 时，最大独立集权值。 |
| `dp[u][1]` | 在 `u` 的子树中选 `u` 时，最大独立集权值。 |
| `parent` | DFS 中 `u` 的父节点；跳过这条边，避免在无向树中返回祖先。 |

转移为 `dp[u][0]=Σmax(dp[v][0],dp[v][1])`、`dp[u][1]=weight[u]+Σdp[v][0]`，其中 `v` 是孩子。DFS 后序保证先得到孩子状态，再合并到父节点。

**3. 函数在做什么**

| 函数 | 参数、返回与行为 |
|---|---|
| `maximumWeightIndependentSet` | 1-based 邻接表、权值向量、合法根（默认 1）；返回 `ll`。 返回根覆盖的整棵树上的最大权值独立集和；允许空集，不改输入。输入必须是连通无向树，数组需覆盖 `1..n`。 |
| 内部递归 `dfs(u,parent)` | 当前节点与父节点；返回 `void`。 后序遍历并写入 `dp[u][0/1]`；只遍历根所在连通分量，正常由公开函数启动。 |

函数每次调用都会新建 DP 状态。权值及状态累加必须能放入 `long long`。

**4. 怎么调用**

用 `n+1` 大小的邻接表和权值数组，按无向边双向加边，然后调用函数。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 参数：1..n 编号无向树。返回：不选相邻点时的最大权值和。效果：O(n)，权值按本函数参数约定给出。
ll maximumWeightIndependentSet(const vector<vector<int>>& tree,
                               const vector<ll>& weight,
                               int root = 1) {
    // tree 与 weight 均为 1-based；输入应为一棵连通无向树。
    int n = static_cast<int>(tree.size()) - 1;
    vector<array<ll, 2>> dp(n + 1, {0, 0});

    // 参数：当前点与父点。返回：无。效果：递归聚合子树状态到 dp[u]。
    function<void(int, int)> dfs = [&](int u, int parent) {
        // dp[u][0/1]：u 不选/选时，其整棵子树内可取得的最大权值。
        dp[u][0] = 0;
        dp[u][1] = weight[u];
        for (int v : tree[u]) {
            if (v == parent) continue;
            dfs(v, u); // 后序处理保证子树状态先于父状态完成
            // 不选 u 可自由选孩子最优状态；选 u 时所有孩子都必须不选。
            dp[u][0] += max(dp[v][0], dp[v][1]);
            dp[u][1] += dp[v][0];
        }
    };

    dfs(root, 0);
    return max(dp[root][0], dp[root][1]);
}
```

三节点树中，1 与 2、3 相连，权值分别为 `5,4,3`。选两个叶子得到 7，比只选根的 5 大：

```text
vector<vector<int>> tree(4);
tree[1] = {2, 3};
tree[2] = {1};
tree[3] = {1};
vector<ll> weight = {0, 5, 4, 3};
assert(maximumWeightIndependentSet(tree, weight) == 7);
```

**5. 要改哪里**

- 若节点权值改变，修改 `weight` 即可重新计算；此实现每次从头运行，不维护动态更新。
- 若要恢复选中的节点，需要记录每个节点状态下孩子取了哪个状态，再从根沿记录回溯；当前接口只返回最优和。
- 若改成“相邻必须满足某种代价/状态约束”，需扩展 DP 状态和孩子合并规则，不能只替换权值。
- 若输入是森林，需对每个连通分量分别调用或改成遍历所有根，并把各分量最优值相加；当前只启动一次根 DFS。
- 若树可能是极深链且递归栈不可靠，应将 DFS 改为显式栈后序处理。

**6. 自检**

三节点星形树权值 `[5,4,3]` 得 7。单节点正权 `[6]` 得 6；单节点负权 `[-6]` 因允许空集得 0。链 `1-2-3` 权值 `[4,10,4]` 时应选两端，得到 8，而不能选相邻的中间点与端点。每条无向边只建立一次逻辑连接但需在邻接表两端各记录一次。

**7. 坑**

1. 无向 DFS 没有跳过父节点；会沿边递归回去，应传 `parent` 并跳过。
2. 选了 `u` 仍给孩子取 `max(dp[v][0],dp[v][1])`；孩子必须不选，只能加 `dp[v][0]`。
3. 将权值/树按 0-based 构造；模板从节点 1 开始，0 号位是哨兵。
4. 输入含多个连通分量却只调用一次；未访问分量不会进入结果，需按森林处理。
5. 长链递归栈溢出；若约束允许深度达 `n`，考虑迭代后序遍历。

**8. 一句话原理**

把每个子树分成“根不选”和“根选”两种状态，利用选根时孩子必须不选这一约束自底向上合并。

**参考：**

- [OI Wiki：树形 DP](https://oi-wiki.org/dp/tree/)

## 4.8 状态压缩 DP

**1. 它是做什么的**

本模板求有向或无向带权图中的旅行商回路：从指定起点出发，每个节点恰好访问一次，最后回到起点，返回最小费用。`cost[u][v]` 是从 `u` 到 `v` 的边权；缺边必须用 `INF` 表示。无可行回路时返回 `INF`。节点和起点均为 0-based，要求 `n>=1`、起点在范围内、矩阵为 `n×n`。

用位掩码表示访问集合，状态数约 `n*2^n`。转移枚举当前终点和下一个未访问点，时间 $O(n^2 2^n)$；DP 空间 $O(n2^n)$，另有输入矩阵 $O(n^2)$。`1<<n` 必须在 `int` 位宽内且数组内存可分配；实际可处理规模通常更受内存限制。所有有效状态费用须小于 `INF`，相加中间值不能溢出 `long long`。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `cost[u][v]` | 从节点 `u` 到 `v` 的费用；有向图可不对称，无边用 `INF`。 |
| `start` | 起点下标，默认 0；位掩码的初始集合只含该点。 |
| `mask` | 位集合；第 `u` 位为 1 表示节点 `u` 已访问。 |
| `dp[mask][u]` | 从 `start` 出发，访问集合恰为 `mask` 并停在 `u` 的最小路径费用。 |
| `nextMask` | 将未访问节点 `v` 加入后得到的新集合。 |
| `all` | `1<<n`，所有掩码的数量；完整访问集合是 `all-1`。 |
| `INF` | 无边和不可达状态哨兵；代码仅将恰好等于它的值视作不可达。 |

初始化仅 `dp[1<<start][start]=0`。转移只扩展未访问节点；最后从完整集合的每个终点补上回到起点的边。无向图需在矩阵两方向都填边权；有向图按方向填值。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `travelingSalesmanCycle` | 方阵 `cost` 和合法 0-based 起点（默认 0）；返回 `ll`。 | 返回最小回路费用；不存在完整回路时返回 `INF`。输入不修改。矩阵至少有 `n` 行且每行 `n` 列，`n>=1`。 |

函数每次调用都会新建全部 DP 状态。对于 `n=1`，实现会把 `cost[0][0]` 当作回起点的边；若该项为 `INF` 则返回 `INF`。

**4. 怎么调用**

建立方阵，缺边位置设成 `INF`，再给出起点。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = numeric_limits<ll>::max() / 4;

// 参数：方阵 cost 与起点下标。返回：从起点出发访问每点一次并回起点的最小费用；无可行环返回 INF。效果：O(2^n n^2)，n 须较小。
ll travelingSalesmanCycle(const vector<vector<ll>>& cost, int start = 0) {
    // 节点为 0-based；cost[u][v] 可表示有向边，无边必须设为 INF。
    int n = static_cast<int>(cost.size());
    int all = 1 << n;
    // dp[mask][u]：从 start 出发，恰好访问 mask 中节点并停在 u 的最小代价。
    vector<vector<ll>> dp(all, vector<ll>(n, INF));
    dp[1 << start][start] = 0;

    for (int mask = 0; mask < all; ++mask) {
        if (!(mask & (1 << start))) continue;
        for (int u = 0; u < n; ++u) {
            // u 必须已访问且状态可达；INF 状态不能参与加法。
            if (!(mask & (1 << u)) || dp[mask][u] == INF) continue;
            for (int v = 0; v < n; ++v) {
                if (mask & (1 << v)) continue;
                if (cost[u][v] == INF) continue;
                // 只向未访问 v 扩展，因此每个节点在路径中恰好出现一次。
                int nextMask = mask | (1 << v);
                dp[nextMask][v] = min(dp[nextMask][v],
                                      dp[mask][u] + cost[u][v]);
            }
        }
    }

    ll answer = INF;
    // 最后补上 u -> start；若仍为 INF，表示不存在哈密顿回路。
    for (int u = 0; u < n; ++u) {
        if (dp[all - 1][u] != INF && cost[u][start] != INF) {
            answer = min(answer, dp[all - 1][u] + cost[u][start]);
        }
    }
    return answer;
}
```

下面的有向图中，最优回路 `0→1→2→0` 的费用为 `1+2+3=6`：

```text
vector<vector<ll>> cost = {
    {INF, 1, 10},
    {10, INF, 2},
    {3, 10, INF}
};
assert(travelingSalesmanCycle(cost, 0) == 6);
```

**5. 要改哪里**

- 若只求访问全部节点的最短路径、不要求回起点，最终在 `dp[all-1][u]` 中取最小值，不补 `cost[u][start]`。
- 若起点可任选，需分别以每个起点计算或修改初始化和终点闭合规则；当前默认固定从 `start` 出发。
- 若图是无向的，构造 `cost[u][v]` 时同时设置 `cost[v][u]`；当前转移本身按有向费用读取。
- 若要恢复访问顺序，需记录每个 `dp[nextMask][v]` 的前驱状态/终点，当前函数只返回费用。
- 若 `n` 稍大到 `2^n*n` 不可存储，换用剪枝搜索、近似算法或利用问题的特殊结构；改成更宽位掩码只能解决移位范围，不能降低指数级内存。

**6. 自检**

示例矩阵的最优环 `0→1→2→0` 费用为 6，反方向路线费用为 30。若删去 `2→0` 边，则没有闭合回路，结果为 `INF`。`n=1` 时结果等于对角边费用；空图不合法。再检查所用 `INF` 大于所有合法路线费用且累加过程不溢出。

**7. 坑**

1. 缺边用 0 表示；0 可能是合法边权，模板约定缺边必须用 `INF`。
2. 把终点最小路径当作回路；必须确认最后一条 `u→start` 边存在并计入费用。
3. 对 `INF` 状态直接加边权；先跳过不可达状态和缺边，避免溢出伪造可达值。
4. 位掩码移位超出 `int` 范围；约束需保证 `1<<n` 有效且状态数组可分配。
5. 估算内存时只看 `2^n`；还要乘终点数 `n`，并考虑 DP 单元大小和输入矩阵。

**8. 一句话原理**

用集合掩码和当前终点描述已走过的路径，对每个未访问点扩展一次，最后把完整路径闭合回起点。

**参考：**

- [OI Wiki：状压 DP](https://oi-wiki.org/dp/state/)

## 4.9 数位 DP

**1. 它是做什么的**

本模板统计闭区间 `[left,right]` 中，十进制数位和等于 `targetSum` 的非负整数个数。`countDigitSumUpTo(n,s)` 统计 `[0,n]`，负上界或负目标和返回 0；区间函数要求 `0<=left<=right`。数字按普通十进制表示，前导零只用于补齐递归位数，不改变数位和，也不会把同一整数重复计数。

设上界有 `D` 位，目标和为 `S`。每个位置、已用和与上界限制状态至多计算一次，每个状态枚举至多 10 个数字，时间 $O(D(S+1)\cdot10)$；记忆表空间 $O(D(S+1))$，递归深度 $O(D)$。计数用 `long long`，若题目要求取模或计数可能超出类型范围，须修改转移。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `digits` | `n` 的十进制字符串，从最高位到最低位处理。 |
| `position` | 当前处理的位下标，范围 `0..length`。 |
| `sum` | 已处理位的数位和；大于 `targetSum` 时可剪枝。 |
| `tight` | 当前已选前缀是否仍等于上界前缀；为真时当前位最大只能取上界数字。 |
| `memo[position][sum]` | 仅针对 `tight=false` 状态缓存的补全方案数；受限状态随上界前缀变化，不共用该缓存。 |
| `upper` | 当前位可选择的最大数字：受限时为上界当前位，否则为 9。 |
| `answer` | 当前状态所有合法下一位选择的计数总和。 |

到达末位后，只有累计和恰好等于目标才贡献 1。下一位仍受限的条件是“原状态受限且当前数字取到了原上界位”。前导零自然作为普通的 0 转移，因此数字 0 被计入：当目标和为 0 时，`[0,n]` 至少包含数字 0。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `countDigitSumUpTo` | `long long` 上界和整数目标和；返回 `ll`。 | 返回 `[0,n]` 中符合条件的个数。`n<0` 或目标和负时返回 0；每次调用新建 memo。 |
| 内部递归 `dfs(position,sum,tight)` | 当前位、已用数位和、上界限制标记；返回 `ll`。 | 递归枚举本位可选数字，并只缓存不受限状态；由前缀函数内部调用。 |
| `countDigitSumInRange` | 非负闭区间及目标和；返回 `ll`。 | 用两个前缀计数相减得到区间计数；要求 `0<=left<=right`，函数自身不校验区间顺序。 |

这两个函数不修改输入。`countDigitSumInRange` 会各调用一次前缀计数，复杂度为两次同阶计算。

**4. 怎么调用**

统计 `[0,n]` 用前缀函数；统计闭区间用范围函数。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

// 参数：非负上界 n 与目标数位和。返回：[0,n] 中数位和等于目标的整数个数。效果：O(位数×targetSum)。
ll countDigitSumUpTo(ll n, int targetSum) {
    // 统计闭区间 [0,n]；n<0 或目标和为负时统一返回 0。
    if (n < 0 || targetSum < 0) return 0;
    string digits = to_string(n);
    int length = static_cast<int>(digits.size());
    vector<vector<ll>> memo(length, vector<ll>(targetSum + 1, -1));

    // position 从最高位向低位；tight 表示当前前缀是否仍贴住 n 的上界。
    // 参数：当前数位位置、已用数位和及是否受上界限制。返回：满足目标数位和的补全数。效果：写入 memo，避免重复状态计算。
    function<ll(int, int, bool)> dfs = [&](int position, int sum, bool tight) -> ll {
        if (sum > targetSum) return 0;
        if (position == length) return sum == targetSum;
        // 仅非受限状态与更高位选择无关，可以跨路径复用记忆化值。
        if (!tight && memo[position][sum] != -1) return memo[position][sum];

        int upper = tight ? digits[position] - '0' : 9;
        ll answer = 0;
        for (int digit = 0; digit <= upper; ++digit) {
            // 只有原状态受限且本位取到当前上界，下一位才继续受限。
            answer += dfs(position + 1, sum + digit,
                          tight && digit == upper);
        }
        if (!tight) memo[position][sum] = answer;
        return answer;
    };

    return dfs(0, 0, true);
}

// 参数：非负闭区间 [left,right] 与目标数位和。返回：区间内符合条件的整数个数。效果：调用两次 countDigitSumUpTo。
ll countDigitSumInRange(ll left, ll right, int targetSum) {
    // 用前缀计数相减得到闭区间 [left,right]；left-1 由前缀函数处理负数。
    return countDigitSumUpTo(right, targetSum)
         - countDigitSumUpTo(left - 1, targetSum);
}
```

`[0,20]` 中数位和为 2 的数是 `2、11、20`，共 3 个；`[10,22]` 中是 `11、20`，共 2 个。

```text
assert(countDigitSumUpTo(20, 2) == 3);
assert(countDigitSumInRange(10, 22, 2) == 2);
assert(countDigitSumInRange(0, 0, 0) == 1);
```

**5. 要改哪里**

- 若统计范围是 `[left,right]`，保留前缀相减，但确保边界非负且 `left<=right`。
- 若约束涉及相邻位、是否出现过某数字或数字长度，需增加相应状态维度；当前 `position,sum,tight` 只记录数位和与上界关系。
- 若前导零对约束有影响（例如统计实际位数或禁止前导模式），需加入 `started` 状态，区分尚未开始构造数字与数字中的 0。本模板的数位和统计不需要该状态。
- 若结果要求模 `M`，在每次累加后取模，并确保 memo 的未计算标记不与合法值混淆。
- 若计数上界超出 `long long` 可表示范围或目标和过大导致表无法分配，应改用更宽计数/字符串上界或重新设计状态范围。

**6. 自检**

`[0,20]` 中数位和为 2 的数只有 `2、11、20`，结果 3。`[10,22]` 中只有 `11、20`，结果 2。`[0,0]` 且目标和 0 返回 1，说明零会计入；目标和大于上界十进制位数乘 9 时返回 0。单点区间 `[7,7]` 的目标和 7 返回 1，目标和 6 返回 0。

**7. 坑**

1. `tight` 更新写成只看当前数字是否等于 `upper`；当原来不受限时不能重新变受限，条件必须保留原 `tight`。
2. 把受限状态写进只按 `(position,sum)` 索引的 memo；不同上界前缀可能有不同上界位，代码只缓存 `tight=false`。
3. 把前导零当作实际数位限制；数位和下前导零无影响，但相邻位等条件通常需要 `started` 状态。
4. 区间减法使用 `left-1` 却未处理 0；此实现的前缀函数对负上界返回 0，故 `left=0` 正常。
5. 忘记 0 是否计数；本实现统计 `[0,n]`，目标和为 0 时数字 0 会被计入。

**8. 一句话原理**

从高位向低位枚举数字，用已用数位和与是否贴住上界描述状态，并复用所有不再受上界约束的子问题。

**参考：**

- [OI Wiki：数位 DP](https://oi-wiki.org/dp/digit/)

## 4.10 DAG 上的 DP

**1. 它是做什么的**

给定 1-based 有向无环图和源点，函数求源点到每个节点的最长路权值。边权可以为负，也可有重边；无向边不适用。不可达节点的结果为 `NEG_INF`；若图中任意位置存在有向环，拓扑序无法覆盖全部节点，函数返回空向量表示失败。

构造入度并拓扑排序遍历每条边一次，松弛也遍历每条边一次，时间 $O(V+E)$。辅助的入度、队列、拓扑序和距离数组占 $O(V)$ 额外空间；输入邻接表另占 $O(V+E)$。点编号为 `1..n`，要求 `graph` 有 `n+1` 个槽位，源点和每条边终点均合法。距离累加须在 `long long` 范围内，所有有限最长距离须严格大于 `NEG_INF`。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `graph[u]` | 从 `u` 出发的有向边列表，每条 `Edge` 存 `to` 和 `weight`。 |
| `indegree[v]` | 进入 `v` 的边数；重边按多条边计数，出队处理时逐条减回。 |
| `q`、`order` | 入度为 0 的节点队列及其拓扑序。 |
| `source` | 最长路起点，初始距离为 0。 |
| `distance[u]` | 当前已确定的源点到 `u` 最长路；`NEG_INF` 表示尚不可达。 |
| `edge` | 当前待处理有向边，松弛候选为 `distance[u]+edge.weight`。 |
| `NEG_INF` | 不可达哨兵；不可达节点不能参与边权加法。 |

代码把所有入度为 0 的点都加入队列，所以即使 DAG 有多个连通部分也能检查全图是否有环。拓扑排序长度不足 `n` 时直接失败；若图合法，未从源点可达的其他分量仍保留 `NEG_INF`。

**3. 函数在做什么**

| 函数/类型 | 参数与返回 | 行为及前提 |
|---|---|---|
| `Edge` | 字段 `to`（终点）和 `weight`（边权）。 | 表示一条有向边；`to` 必须为 `1..n`。 |
| `longestPathInDAG` | 1-based 邻接表及合法源点；返回 `vector<ll>`。 | 合法 DAG 时返回长度 `n+1` 的距离表，0 号位不用；有环返回空向量。输入不修改。 |

本函数不返回具体路径，只返回每点最长距离。每次调用重建拓扑序和距离状态；图必须整体是 DAG，即使环与源点不连通也会失败。

**4. 怎么调用**

按方向建立邻接表，用 `Edge{终点,权值}` 表示边，调用后先检查结果是否为空，再读取距离。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll NEG_INF = numeric_limits<ll>::lowest() / 4;

struct Edge {
    int to;
    ll weight;
};

// 参数：1..n 编号 DAG 邻接表与源点。返回：各点最长路权值；不可达为 NEG_INF。效果：O(V+E)，图必须无环。
vector<ll> longestPathInDAG(const vector<vector<Edge>>& graph, int source) {
    // graph 与节点为 1-based、有向、可含重边和负权，但必须无环。
    int n = static_cast<int>(graph.size()) - 1;
    vector<int> indegree(n + 1, 0);
    for (int u = 1; u <= n; ++u) {
        for (const auto& edge : graph[u]) ++indegree[edge.to];
    }

    queue<int> q;
    // 所有入度为 0 的点同时入队，保证断开的 DAG 也能完成拓扑排序。
    for (int u = 1; u <= n; ++u) {
        if (indegree[u] == 0) q.push(u);
    }
    vector<int> order;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (const auto& edge : graph[u]) {
            if (--indegree[edge.to] == 0) q.push(edge.to);
        }
    }
    // 拓扑序不含全部节点说明存在有向环；用空数组作为失败状态。
    if (static_cast<int>(order.size()) != n) return {};

    // distance[u] 为 source 到 u 的最长距离；NEG_INF 表示不可达。
    vector<ll> distance(n + 1, NEG_INF);
    distance[source] = 0;
    for (int u : order) {
        // 不可达点不能松弛出边，否则负无穷参与加法会产生伪状态。
        if (distance[u] == NEG_INF) continue;
        for (const auto& edge : graph[u]) {
            distance[edge.to] = max(distance[edge.to],
                                    distance[u] + edge.weight);
        }
    }
    return distance;
}
```

下例中最长路到节点 4 为 `1→3→4`，长度 7；孤立节点 5 不可达，距离为 `NEG_INF`：

```text
vector<vector<Edge>> graph(6);
graph[1] = {{2, 3}, {3, 2}};
graph[2] = {{4, 4}};
graph[3] = {{4, 5}};
vector<ll> distance = longestPathInDAG(graph, 1);
assert(distance.size() == 6);
assert(distance[4] == 7);
assert(distance[5] == NEG_INF);
```

**5. 要改哪里**

- 求 DAG 最短路时，将初值哨兵改为正无穷并把 `max` 松弛改成 `min`；仍须跳过不可达状态。
- 若只需从源点可达部分且想容忍图其他区域有环，需改变环检测范围；当前拓扑排序检查整张图。
- 若要返回具体路径，松弛成功时记录 `edge` 的前驱节点，再从终点反向恢复；当前接口不存前驱。
- 若要统计路径数或最优路径数，状态聚合不再是单个最大距离，需额外维护计数并明确并列最优时的合并规则。
- 若图有环，不能直接使用 DAG DP；可按题意缩点、处理强连通分量，或选择适用于有环图的算法。

**6. 自检**

示例中 `1→2→4` 权值 7，`1→3→4` 权值 7? 其中第二条为 `2+5=7`，两条并列，结果到 4 为 7。节点 5 无入边但从源点不可达，仍为 `NEG_INF`。若增加边 `4→2`，图出现环，函数应返回空向量；若源点出发的边权是负数，可达节点的距离应保留该负值，不能误当作不可达或 0。

**7. 坑**

1. 按节点编号直接松弛而非拓扑顺序；后继可能先于前驱处理，应遍历 `order`。
2. 把不可达初始化为 0；负权路径会被错误压过，使用 `NEG_INF` 并跳过不可达点。
3. 只检测源点所在部分是否有环；实现检查全图，任何环都会导致空结果。
4. 将无向边只存一侧或将有向边自动补反向；邻接表必须忠实表达图方向。
5. 把返回空向量当作“所有点不可达”；它表示图不是 DAG，合法 DAG 的不可达节点仍在长度 `n+1` 的结果中并取 `NEG_INF`。

**8. 一句话原理**

按拓扑序确保所有前驱先完成，再把每条边的最长距离候选传播到后继。

**参考：**

- [OI Wiki：DAG 上的 DP](https://oi-wiki.org/dp/dag/)

## 4.11 编辑距离

**1. 它是做什么的**

本函数计算把字符串 `a` 变成 `b` 所需的最少操作数，每次插入、删除或替换一个字符的代价都是 1。输入是两个 `std::string`，返回 `int` 距离。实现按 `string` 的 `char` 单位比较；UTF-8 多字节字符会被当作多个字节处理，若题目按 Unicode 字符计数需先解码。

设长度为 `n`、`m`，每个前缀状态只做常数次转移，时间 $O(nm)$。滚动数组保存第二个字符串的各前缀，额外空间为 $O(m)$；代码不会交换字符串以压缩到较短一侧。输入不修改。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `a`、`b` | 源字符串与目标字符串，比较下标为 0-based。 |
| `dp[j]` | 当前已处理的 `a` 前缀与 `b` 的前 `j` 个字节之间的编辑距离。 |
| `i`、`j` | 当前源前缀长度和目标前缀长度；字符下标分别为 `i-1`、`j-1`。 |
| `diagonal` | 覆写当前格之前的左上旧值，即前一行的 `dp[j-1]`。 |
| `oldAbove` | 覆写前的上方旧值，即前一行的 `dp[j]`。 |
| `dp[j-1]` | 本行已更新的左侧状态。 |

初始化 `dp[j]=j` 表示空串变成 `b` 的前 `j` 个字符需要 `j` 次插入；每行开头将 `dp[0]=i`，表示将 `a` 的前 `i` 个字符删空。字符相同直接继承左上值；否则从删除、插入、替换三种操作中取最小值并加 1。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `editDistance(a,b)` | 两个只读 `string`；返回 `int`。 | 返回单位插入/删除/替换代价下的最小编辑次数；空字符串合法，不改输入。 |

函数每次调用都新建滚动数组。字符串长度和最终距离需能由 `int` 表示。

**4. 怎么调用**

直接传入源字符串与目标字符串，返回值是最少操作次数。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

// 参数：两字符串。返回：插入、删除、替换代价均为 1 的最小编辑次数。效果：O(|a||b|) 时间、O(|b|) 空间。
int editDistance(const string& a, const string& b) {
    // dp[j] 表示当前 a 前缀与 b 的前 j 个字符之间的编辑距离。
    vector<int> dp(b.size() + 1);
    iota(dp.begin(), dp.end(), 0); // 空串变成 b 前 j 字符需要 j 次插入

    for (int i = 1; i <= static_cast<int>(a.size()); ++i) {
        int diagonal = dp[0]; // 覆盖前保存左上角的旧状态
        dp[0] = i; // b 为空时只能删除 a 的 i 个字符
        for (int j = 1; j <= static_cast<int>(b.size()); ++j) {
            int oldAbove = dp[j];
            if (a[i - 1] == b[j - 1]) {
                dp[j] = diagonal;
            } else {
                dp[j] = 1 + min({oldAbove, dp[j - 1], diagonal});
            }
            diagonal = oldAbove;
        }
    }
    return dp[b.size()];
}
```

`kitten` 变为 `sitting` 至少需要 3 次操作；空串变为 `abc` 需要 3 次插入：

```text
assert(editDistance("kitten", "sitting") == 3);
assert(editDistance("", "abc") == 3);
assert(editDistance("abc", "abc") == 0);
```

**5. 要改哪里**

- 若插入、删除、替换代价不同，转移应分别加上对应代价，不再统一 `+1`。
- 若只允许插入/删除，可将问题转为最长公共子序列长度 `|a|+|b|-2*LCS(a,b)`；当前实现还允许替换。
- 若要输出具体编辑脚本或对齐方案，需保存前驱/完整 DP 表；滚动版本只返回距离。
- 若要处理 UTF-8 文本并按字符计算，先将字符串解码为码点序列，再在该序列上运行等价 DP。

**6. 自检**

`kitten` 到 `sitting` 的距离为 3。相同字符串距离为 0；空串到长度为 `k` 的字符串距离为 `k`，反向也为 `k`。单字符 `a` 到 `b` 距离为 1。可用对称性检查交换两输入后距离不变，因为这三种单位操作的代价对称。

**7. 坑**

1. 更新 `dp[j]` 前没保存旧值；上方旧值和本行左值混用会破坏转移，需用 `oldAbove` 与 `diagonal` 保存状态。
2. 空前缀初始化为 0；`dp[j]=j` 与每行 `dp[0]=i` 分别代表插入和删除代价。
3. 把 `dp[j-1]` 当成左上旧值；它已是本行新值，左上值应单独保存在 `diagonal`。
4. 期望 UTF-8 字符按一个字符处理；本函数实际比较字节，须先解码。
5. 认为长字符串也适合本算法；空间虽为线性，时间仍是 $O(nm)$，大输入可能过慢。

**8. 一句话原理**

滚动维护两个前缀的编辑距离，并在每个字符对上从删除、插入、替换三种最后操作中取最小代价。

## 4.12 树形 DP 与换根

**1. 它是做什么的**

本模板计算无权树中每个顶点到所有顶点的距离和。顶点编号为 `1..n`，边无方向且每条边长度视为 1；`solve()` 返回长度 `n+1` 的向量，`answer[u]` 位于下标 `u`，0 号位不用。要求 `n>=1`，输入恰为一棵树。

先以 1 为根做 DFS，计算子树大小和根 1 的距离和；再沿每条父子边换根一次。每个点和边处理常数次，构造及添加 `n-1` 条边为 $O(n)$，`solve()` 为 $O(n)$；邻接表、状态数组和递归栈共需 $O(n)$ 空间。答案最大可达 $O(n^2)$，使用 `long long` 存储。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `n` | 树的顶点数，节点编号为 `1..n`。 |
| `graph[u]` | 无向邻接表；每条输入边在两个端点各记录一次。 |
| `subtreeSize[u]` | 初次以 1 为根时，`u` 子树中的节点数，包含 `u`。 |
| `answer[u]` | 以 `u` 为根时到全体顶点的距离和。 |
| `depth` | 第一遍 DFS 中节点到固定根 1 的边数。 |
| `parent` | DFS 父节点；跳过该邻接点以免沿树边返回。 |

从父节点 `u` 换根到孩子 `v` 时，`v` 子树内的 `subtreeSize[v]` 个点距离减 1，其余 `n-subtreeSize[v]` 个点距离加 1，因此 `answer[v]=answer[u]+n-2*subtreeSize[v]`。第一遍累加得到 `answer[1]`，第二遍沿树逐个转移。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `RerootDistanceSum(n)` | 正顶点数；构造对象。 | 分配 1-based 邻接表及状态数组，答案初值为 0。 |
| `addEdge(u,v)` | 树中两个合法相邻端点；返回 `void`。 | 将无向边加入邻接表两端；所有边须在 `solve` 前添加，输入需保持为树。 |
| 内部 `firstDfs(u,parent,depth)` | 当前点、父点和深度；返回 `void`。 | 填子树大小并累加根 1 的距离和；由 `solve()` 调用。 |
| 内部 `rerootDfs(u,parent)` | 当前根候选及父点；返回 `void`。 | 根据子树大小把父答案转移到孩子，遍历全部节点；由 `solve()` 调用。 |
| `solve()` | 无参数；返回 `vector<ll>`。 | 运行两遍 DFS 并返回内部答案副本。每个对象仅调用一次；重复调用会再次累加 `answer[1]`，结果错误。 |

`addEdge` 不检查端点、重复边或环；调用者须提供合法树。递归深度最坏为 `n`。

**4. 怎么调用**

构造对象，加入所有无向边，再调用一次 `solve()` 并用节点编号访问结果。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct RerootDistanceSum {
    int n;
    vector<vector<int>> graph;
    vector<int> subtreeSize;
    vector<ll> answer;

    // 参数：树的顶点数 n>=1。返回：清零的换根 DP 对象。效果：分配 1..n 邻接表及状态数组。
    explicit RerootDistanceSum(int n)
        : n(n), graph(n + 1), subtreeSize(n + 1), answer(n + 1, 0) {}

    // 参数：树中相邻顶点 u、v。返回：无。效果：向无向邻接表加入一条边。
    void addEdge(int u, int v) {
        graph[u].push_back(v);
        graph[v].push_back(u); // 无向树
    }

    // 参数：当前点、父点和深度。返回：无。效果：计算子树大小与初始根答案。
    void firstDfs(int u, int parent, int depth) {
        subtreeSize[u] = 1;
        answer[1] += depth; // 第一遍累加以 1 为根的距离和
        for (int v : graph[u]) {
            if (v == parent) continue;
            firstDfs(v, u, depth + 1);
            subtreeSize[u] += subtreeSize[v];
        }
    }

    // 参数：当前根及其父点。返回：无。效果：将父点答案转移到子点并遍历整棵树。
    void rerootDfs(int u, int parent) {
        for (int v : graph[u]) {
            if (v == parent) continue;
            answer[v] = answer[u] + n - 2LL * subtreeSize[v];
            rerootDfs(v, u);
        }
    }

    // 参数：无；须已加入全部树边且仅对新对象调用一次。返回：answer[1..n] 的各根距离和。效果：O(n)，写入并返回内部答案副本。
    vector<ll> solve() {
        firstDfs(1, 0, 0);
        rerootDfs(1, 0);
        return answer; // answer[1..n] 有效
    }
};
```

路径 `1-2-3` 的三个距离和依次为 3、2、3：

```text
RerootDistanceSum solver(3);
solver.addEdge(1, 2);
solver.addEdge(2, 3);
vector<ll> answer = solver.solve();
assert(answer.size() == 4);
assert(answer[1] == 3 && answer[2] == 2 && answer[3] == 3);
```

**5. 要改哪里**

- 若边 `(u,v)` 长度为 `w`，跨边转移改为 `answer[v]=answer[u]+w*(n-2*subtreeSize[v])`。若按节点权重求加权距离和，则应将子树节点数替换为子树权重总和，并用全树权重总和替换 `n`。
- 若要统计每点距离平方和或其他距离函数，通常需扩展子树聚合量及转移式；当前状态只支持无权距离和。
- 若要对森林求结果，需分别处理每个连通分量并设定每个分量的节点数；当前以节点 1 启动，要求整图连通。
- 多组数据应为每组新建对象；不要在同一对象上再次 `solve()`，也不要在第一次求解后继续加边。
- 若树很深且递归栈有限，将两遍 DFS 改为迭代遍历并按逆序完成子树聚合。

**6. 自检**

路径 `1-2-3` 的距离和是 `[3,2,3]`。单节点树 `n=1` 返回 `answer[1]=0`。星形树中心 1 连三个叶子时，中心答案为 3，每个叶子的答案为 5。可检查总距离和对称：所有 `answer[u]` 之和应为所有无序点对距离总和的两倍。

**7. 坑**

1. 无向边只加入一侧；DFS 会漏点或结果错误，每条边应调用一次 `addEdge(u,v)`，由接口负责双向记录。
2. 误用 0-based 节点；对象的有效下标为 `1..n`，`answer[0]` 不代表节点。
3. 在同一对象重复 `solve()`；第一遍会再次累加根 1 的距离和，须每个对象只求解一次。
4. 把无权换根公式用于加权树；边长改变后必须重新推导跨边增量。
5. 输入含环或不连通；DFS 只跳父节点，非树输入可能递归循环或遗漏分量。

**8. 一句话原理**

先算一个根的全树距离和与各子树大小，再用跨边时“子树内减一、子树外加一”在线性时间传播到所有根。

## 4.13 概率与期望 DP

**1. 它是做什么的**

模型是每次独立、等概率地抽取 `n` 种卡片之一，抽到已收集种类仍会继续抽，求集齐全部种类所需抽取次数的期望。输入为正整数 `n`，返回 `double`。它不处理不同种类概率不等、依赖历史的抽取过程或其他一般状态转移问题。

状态 `e[i]` 表示已集齐 `i` 种后还需抽取次数的期望。下一次抽取必消耗 1 次，并以 `(n-i)/n` 概率进入 `i+1`；若抽到旧种则留在 `i`，将这一项移至等式左边得到 `e[i]=(1+pNew*e[i+1])/pNew`。循环计算 `n` 个状态，时间 $O(n)$；保存 `n+1` 个双精度值，空间 $O(n)$。期望使用浮点数近似，需按题目精度比较或输出。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `n` | 卡片种类数，调用者必须保证 `n>0`。 |
| `e[i]` | 已收集 `i` 种之后的剩余抽取次数期望；边界 `e[n]=0`。 |
| `i` | 当前已收集种类数，从 `n-1` 递减到 0。 |
| `pNew` | 下一次抽到一种尚未收集种类的概率 `(n-i)/n`，在循环范围内严格大于 0。 |

状态只依赖 `e[i+1]`，从集齐状态向空集状态倒推。抽到旧种的概率为 `i/n`，其期望仍是 `e[i]`，解方程时已被吸收到分母中，不能再简单把旧种情况丢掉。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `couponCollectorExpectation` | 正整数种类数；返回 `double`。 | 返回独立均匀抽取直到集齐的期望次数；不修改外部状态。调用者需保证 `n>0`，函数本身不检查。 |

函数内部新建期望数组，因此每次调用互不影响。较大的 `n` 下，结果为近似浮点数而非精确分数。

**4. 怎么调用**

传入种类数，按题目要求设置浮点输出精度。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

// 参数：不同卡片种类数 n>0。返回：等概率独立抽取直到集齐的期望次数。效果：O(n) 时间、空间。
double couponCollectorExpectation(int n) {
    // e[i] 是已收集 i 种时还需抽取次数的期望，边界 e[n]=0。
    vector<double> e(n + 1, 0.0);
    for (int i = n - 1; i >= 0; --i) {
        double pNew = static_cast<double>(n - i) / n;
        // 一步必然消耗，再以 pNew 前进；重复抽到旧种的概率已移项。
        e[i] = (1.0 + pNew * e[i + 1]) / pNew;
    }
    return e[0];
}
```

只有一种卡片时必抽一次；两种卡片时期望为 `2 + 1 = 3`：

```text
assert(fabs(couponCollectorExpectation(1) - 1.0) < 1e-9);
assert(fabs(couponCollectorExpectation(2) - 3.0) < 1e-9);
```

**5. 要改哪里**

- 若每种卡片的抽取概率不相等，仅记录已收集种类数 `i` 不足以确定下一步概率；状态需记录具体已收集集合（或能区分剩余种类概率的等价信息），再按该状态的新增概率写方程并处理自环。
- 若一次抽取可能得到多种卡片、或抽取结果依赖历史，需重新定义状态和概率转移。
- 若要求方差等更高阶统计量，需为状态增加相应的二阶矩/统计量转移；当前函数只输出期望。
- 若需查询多个种类数 `n` 的答案，当前表只对应一个固定 `n`，不能直接跨 `n` 复用。可预处理调和数 `H[n]=H[n-1]+1/n`，再用 `n*H[n]` 回答各个 `n`。

**6. 自检**

`n=1` 时期望为 1；`n=2` 时先抽到第一种必花 1 次，之后抽到另一种平均再花 2 次，总期望 3。递推也等价于 `e[i]=n/(n-i)+e[i+1]`，因此 `e[0]=n(1+1/2+...+1/n)`。输入必须为正；`n=0` 不符合模型，不能把函数返回 0 当作有意义答案。

**7. 坑**

1. 直接计算 `1+pNew*e[i+1]` 而不除以 `pNew`；会忽略抽到已收集种类后仍要继续的自环期望。
2. 忘记边界 `e[n]=0`；集齐后不再需要抽取。
3. 用整数类型保存期望或中间概率；会截断小数，应使用 `double`。
4. 输入概率不均匀仍套用 `(n-i)/n`；此概率只适用于每种等可能。
5. 用精确相等比较浮点结果；验证和判题应使用容差或按题目要求格式化输出。

**8. 一句话原理**

对每个已收集种类数写出一步期望方程，将停留在当前状态的自环概率移项后从满集向空集递推。
