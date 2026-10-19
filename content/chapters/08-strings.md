
# 8. 字符串

本章字符串统一使用 0-based 下标，区间统一写成左闭右开 `[l,r)`。长度为 `n` 的字符串合法字符下标为 `0..n-1`；各模板用 `int` 保存长度和下标，因此输入长度及下标表达式必须可由 `int` 表示。未特别说明时字符按字节处理，不直接支持 UTF-8 的“单个汉字”语义。

## 8.1 字符串哈希

**1. 它是做什么的**

`StringHash` 为字节串预处理前缀双哈希，之后可在常数时间取得任意子串哈希，用于快速比较子串。区间采用 0-based 半开形式 `[l,r)`，长度为 `r-l`，合法范围是 `0<=l<=r<=s.size()`；空区间哈希为 `(0,0)`。相等比较必须同时确认长度相同和双哈希相同。

构造时扫描字符串一次，计算两个模数下的前缀值与幂数组，时间 $O(n)$、空间 $O(n)$；`get(l,r)` 为 $O(1)$。固定双哈希仍有碰撞概率，不适合要求数学上零误判或可被对抗性构造的输入。该实现按 `unsigned char` 处理 `string` 字节，UTF-8 多字节字符不是单个字符。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `MOD1`、`MOD2`、`BASE` | 全部待比较对象必须一致的两个模数和哈希底数。 |
| `h1[i]`、`h2[i]` | 前缀 `s[0..i)` 的哈希值；长度数组索引，`h[0]=0`。 |
| `p1[i]`、`p2[i]` | `BASE^i` 在相应模数下的值；`p[0]=1`。 |
| `value` | 当前字节无符号值加 1，避免将字节 0 映射为零贡献。 |
| `l`、`r` | 子串左闭右开边界，哈希移除左侧前缀时使用幂 `BASE^(r-l)`。 |
| `x1`、`x2` | 从两个前缀哈希中减去左侧贡献后得到的模哈希。 |

两个模数分别运算，`get` 返回一对余数。不同起点的子串哈希可直接比较，但不同长度的字符串即便哈希对相同，也不能据此判等。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `StringHash(s)` | `const string&` 字节串；构造对象。 | 建立前缀哈希与幂数组，不修改输入；对象持有之后查询所需的全部数据。 |
| `get(l,r)` | 合法半开区间 `[l,r)`；返回 `pair<ll,ll>`。 | 返回该子串的双模哈希，不修改对象；调用者负责检查边界和比较长度。 |

两个不同对象之间也可比较，但必须使用代码中相同的底数和模数；本模板的静态常量自动保持一致。

**4. 怎么调用**

为字符串构造对象，对每个子串调用 `get(l,r)`；比较时同时比较长度和哈希对。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct StringHash {
    // 两个模数与 BASE 必须在所有待比较对象中完全一致；哈希相等仍有极小碰撞概率。
    static constexpr ll MOD1 = 1000000007;
    static constexpr ll MOD2 = 1000000009;
    static constexpr ll BASE = 911382323;
    vector<ll> h1, h2, p1, p2;

    // 参数 s 按字节读取；构造并拥有前缀哈希与幂数组，不修改 s。
    explicit StringHash(const string& s) {
        int n = (int)s.size();
        // h[i] 表示前缀 s[0..i) 的哈希，p[i]=BASE^i；两数组都按长度而非字符下标。
        h1.assign(n + 1, 0); h2.assign(n + 1, 0);
        p1.assign(n + 1, 1); p2.assign(n + 1, 1);
        // 每轮把一个字节扩展进两个前缀哈希，并同步预存下一次查询所需的幂。
        for (int i = 0; i < n; ++i) {
            int value = (unsigned char)s[i] + 1;
            h1[i + 1] = (h1[i] * BASE + value) % MOD1;
            h2[i + 1] = (h2[i] * BASE + value) % MOD2;
            p1[i + 1] = p1[i] * BASE % MOD1;
            p2[i + 1] = p2[i] * BASE % MOD2;
        }
    }

    // 返回 0-based 左闭右开子串 s[l..r) 的双哈希；要求 0<=l<=r<=s.size()。
    // 参数是 s 的 0-based 半开区间 [l,r)；返回双模哈希，调用者须保证边界合法；不改状态。
    pair<ll, ll> get(int l, int r) const {
        // h[r]-h[l]*BASE^(r-l) 消掉左侧前缀，使不同起点的等长子串可直接比较。
        ll x1 = (h1[r] - h1[l] * p1[r - l]) % MOD1;
        ll x2 = (h2[r] - h2[l] * p2[r - l]) % MOD2;
        if (x1 < 0) x1 += MOD1;
        if (x2 < 0) x2 += MOD2;
        return {x1, x2};
    }
};
```

`abracadabra` 中 `[0,4)` 与 `[7,11)` 都是 `abra`，长度与双哈希均相同：

```text
string s = "abracadabra";
StringHash hash(s);
auto first = hash.get(0, 4);
auto second = hash.get(7, 11);
int lenFirst = 4;
int lenSecond = 11 - 7;
assert(lenFirst == lenSecond && first == second);
```

**5. 要改哪里**

- 若比较对象可能来自不同实现或参数的哈希对象，必须统一底数与模数；参数不同的哈希对不能直接比较。
- 若使用场景要求零碰撞误判，用直接比较、KMP、后缀数组等确定性方法；增加模数只能降低碰撞概率，不能消除它。
- 若要按 Unicode 字符而不是字节比较，先解码成码点序列，并相应改为对整数序列建哈希。
- 若只处理单个固定长度模式，可按需只预处理相关结构；当前类为整串任意子串查询保存四个长度 `n+1` 的数组。

**6. 自检**

`abracadabra` 的 `[0,4)` 和 `[7,11)` 都为 `abra`，双哈希应相等；`[0,3)` 和 `[7,10)` 都为 `abr`，也应相等。空区间 `[k,k)` 返回 `(0,0)`。边界 `[0,s.size())` 对应整个字符串。对子串判等时若长度不同，即使哈希碰巧相同也必须判为不同。

**7. 坑**

1. 把 `[l,r)` 当作闭区间；长度和幂次都应使用 `r-l`，末端 `r` 不包含。
2. 只比较哈希对而不比较长度；不同长度哈希可能相同，判等前必须核对长度。
3. 忽略固定哈希的碰撞可能；双哈希不是绝对正确性保证，对抗场景换确定性算法。
4. `char` 当有符号值使用；实现转为 `unsigned char` 后再加 1，保持字节值一致。
5. 越界查询导致数组访问错误；`get` 不做边界检查，调用方须保证 `0<=l<=r<=s.size()`。

**8. 一句话原理**

前缀哈希减去左侧前缀乘以对应幂次，就能在常数时间得到任意半开子串的双模哈希。

**参考：**

- [OI Wiki：字符串哈希](https://oi-wiki.org/string/hash/)

## 8.2 前缀函数与 KMP

**1. 它是做什么的**

`prefixFunction` 计算字符串每个前缀的最长相等真前后缀长度；`kmpSearch` 使用该表，在文本中查找模式串的所有出现位置，允许重叠。字符串按 `std::string` 字节处理，结果位置为 0-based 起点。空模式按模板约定返回空列表；若题目另有空模式定义，需单独处理。

长度为 `m` 的模式前缀表计算时间 $O(m)$、空间 $O(m)$。在长度为 `n` 的文本中搜索总时间 $O(n+m)$，使用前缀表及输出位置占 $O(m+k)$ 空间，其中 `k` 为匹配次数；输入不修改。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `s` | `prefixFunction` 的字节串输入。 |
| `pi[i]` | 子串 `s[0..i]` 的最长相等真前后缀长度；是长度，不是末尾下标。 |
| `text`、`pattern` | 待搜索文本和模式字节串。 |
| `j` | 当前已匹配的模式前缀长度；扫描文本字符前满足 `0<=j<m`。 |
| `i` | 当前扫描到的文本下标。 |
| `positions` | 找到的 0-based 匹配起点，按扫描顺序递增。 |

失配时将 `j` 缩短为当前边界的次长候选 `pi[j-1]`，文本位置不回退。完整匹配后也回退到模式串最长真边界，使后续搜索保留可能的重叠部分。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `prefixFunction(s)` | 字节串常量引用；返回 `vector<int>`。 | 返回长度与 `s` 相同的前缀表；空串返回空表，不修改输入。 |
| `kmpSearch(text,pattern)` | 文本和模式字节串常量引用；返回 `vector<int>`。 | 返回所有匹配的 0-based 起点，包含重叠；空模式返回空向量，不修改输入。内部调用前缀函数。 |

UTF-8 字符串会按字节匹配；若要按 Unicode 码点查找，应先解码成符号序列再应用同样算法。

**4. 怎么调用**

需要前缀表时调用 `prefixFunction`；查找所有出现时调用 `kmpSearch`。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

// 参数 s 是字节串；返回与 s 等长的 pi 长度数组，空串返回空数组，不改输入。
vector<int> prefixFunction(const string& s) {
    int n = (int)s.size();
    // pi[i] 是 s[0..i] 的最长相等真前后缀“长度”，不是末尾下标。
    vector<int> pi(n, 0);
    for (int i = 1; i < n; ++i) {
        int j = pi[i - 1];
        // 失配后只可能尝试当前边界的次长边界；因此跳 pi[j-1]，文本位置 i 不回退。
        while (j > 0 && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) ++j;
        pi[i] = j;
    }
    return pi;
}

// 参数 text/pattern 是字节串；返回 pattern 的全部 0-based 起点（含重叠），空模式返回空表。
vector<int> kmpSearch(const string& text, const string& pattern) {
    // 返回 pattern 在 text 中所有 0-based 起点；空模式的语义由题目决定，这里返回空。
    vector<int> positions;
    if (pattern.empty()) return positions;
    vector<int> pi = prefixFunction(pattern);
    // 扫描 text[0..i] 前，j 表示已匹配的 pattern 前缀长度，始终有 0<=j<m。
    int j = 0;
    for (int i = 0; i < (int)text.size(); ++i) {
        while (j > 0 && text[i] != pattern[j]) j = pi[j - 1];
        if (text[i] == pattern[j]) ++j;
        if (j == (int)pattern.size()) {
            positions.push_back(i - j + 1);
            // 匹配后回到最长真边界，才能继续寻找允许重叠的下一次出现。
            j = pi[j - 1];
        }
    }
    return positions;
}
```

文本 `aaaaa` 中模式 `aaa` 出现于 0、1、2；`ababa` 的前缀表为 `[0,0,1,2,3]`：

```text
vector<int> pi = prefixFunction("ababa");
assert((pi == vector<int>{0, 0, 1, 2, 3}));
vector<int> positions = kmpSearch("aaaaa", "aaa");
assert((positions == vector<int>{0, 1, 2}));
```

**5. 要改哪里**

- 若只想判断是否出现，可在找到第一次匹配时提前返回；当前函数会扫描完整文本并收集所有位置。
- 若只要第一次出现，可返回首个起点或 `-1`，需调整返回类型和匹配后逻辑。
- 若要统计出现次数且允许重叠，可用 `positions.size()`；匹配后回退不可省略。
- 若要忽略大小写，可先将文本和模式统一大小写再运行 KMP。通配符匹配通常不满足前缀失配复用所需的相等关系，不能只替换比较符，应采用专门算法或增加相应状态。
- 若处理 Unicode 字符，先转成码点序列；当前 `string` 接口以字节为单位。

**6. 自检**

`prefixFunction("ababa")` 应为 `[0,0,1,2,3]`。`kmpSearch("aaaaa","aaa")` 返回 `[0,1,2]`，验证重叠匹配。空文本或比文本长的非空模式返回空向量；空模式也按此模板返回空向量。单字符模式在重复字符文本中应列出每个对应位置。

**7. 坑**

1. 把 `pi[i]` 当末尾下标；它存真前后缀长度，失配回退到 `pi[j-1]`。
2. 失配后将文本下标回退；KMP 只回退模式状态 `j`，文本扫描位置继续前进。
3. 找到匹配后把 `j` 清零；应回退到 `pi[j-1]`，否则会漏掉重叠匹配。
4. 对空模式访问 `pattern[0]`；模板先检测空模式并返回空结果。
5. 将 UTF-8 的字节位置当字符位置；若题目按字符计数，应先解码。

**8. 一句话原理**

前缀函数记录模式自身可复用的边界，失配时沿这些边界回退而不重扫文本，从而在线性时间内找到所有匹配。

**参考：**

- [OI Wiki：前缀函数与 KMP 算法](https://oi-wiki.org/string/kmp/)

## 8.3 Z 函数（扩展 KMP）

**1. 它是做什么的**

`zFunction(s)` 对每个位置 `i` 计算从 `s[i..]` 开始的后缀与整串的最长公共前缀长度；非空串约定 `z[0]=s.size()`，空串返回空数组。`zSearch(text,pattern)` 利用 Z 函数找出模式串在文本中的所有匹配起点，位置为 0-based，允许重叠；空模式按本模板约定返回空表。

字符串按 `std::string` 字节处理。Z 数组计算对长度 `N` 的字符串耗时 $O(N)$、空间 $O(N)$；匹配会构造长度 `|pattern|+1+|text|` 的拼接串并计算 Z 数组，时间和额外空间均为 $O(n+m)$。代码使用 `\0` 作为分隔符，因此 `text` 和非空 `pattern` 都不能包含 NUL 字节。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `z[i]` | `s` 与后缀 `s[i..]` 的 LCP 长度，范围不超过 `s.size()-i`。 |
| `l`、`r` | 当前最靠右的匹配盒 `[l,r)`；盒内子串等于从 0 开始的前缀。 |
| `i` | 当前计算 Z 值的位置。 |
| `text`、`pattern` | 待搜索文本和模式字节串。 |
| `joined` | `pattern + '\0' + text`；文本位置 `i` 在拼接串中的位置为 `m+1+i`。 |
| `m` | 模式串字节长度。 |
| `positions` | 所有匹配的文本 0-based 起点，按从小到大排列。 |

若 `i<r`，可以从镜像位置 `i-l` 的 Z 值开始复用，但最多延伸到盒子的右端 `r`；之后再直接比较扩展。拼接后某文本位置对应的 `z` 值至少为 `m`，表示整个模式与文本该后缀匹配。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `zFunction(s)` | 字节串常量引用；返回 `vector<int>`。 | 返回长度为 `s.size()` 的 Z 数组；空串返回空数组，非空时 `z[0]=size`；不修改输入。 |
| `zSearch(text,pattern)` | 不含 NUL 字节的文本和模式；返回 `vector<int>`。 | 返回所有匹配起点；空模式返回空向量，不修改输入。内部构造拼接串并调用 Z 函数。 |

**4. 怎么调用**

需要后缀 LCP 信息时调用 `zFunction`；要找模式串所有位置时调用 `zSearch`。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

// 参数 s 是字节串；返回各位置的 Z 长度，非空时 z[0]=|s|，空串返回空数组。
vector<int> zFunction(const string& s) {
    int n = (int)s.size();
    // z[i]=LCP(s, s[i..n))；所有字符与区间均为 0-based、左闭右开。
    vector<int> z(n, 0);
    if (n == 0) return z;
    z[0] = n;
    for (int i = 1, l = 0, r = 0; i < n; ++i) {
        // [l,r) 是目前右端点最远的前缀匹配段，且 s[l..r)==s[0..r-l)。
        // i 在盒内时先复用镜像 z[i-l]，但不能越过尚未验证的右端点 r。
        if (i < r) z[i] = min(r - i, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) ++z[i];
        if (i + z[i] > r) {
            l = i;
            r = i + z[i];
        }
    }
    return z;
}

// 参数 text/pattern 为字节串且均不含 '\0' 分隔符；返回 0-based 匹配起点，空模式返回空表。
vector<int> zSearch(const string& text, const string& pattern) {
    // 返回所有 0-based 起点；若字符集可能含 '\0'，需把分隔符换成确定不存在的值。
    vector<int> positions;
    if (pattern.empty()) return positions;
    string joined = pattern + '\0' + text;
    vector<int> z = zFunction(joined);
    int m = (int)pattern.size();
    // joined 中 text[i] 的下标是 m+1+i；z 值至少为 m 才覆盖整个模式串。
    for (int i = 0; i < (int)text.size(); ++i)
        if (z[m + 1 + i] >= m) positions.push_back(i);
    return positions;
}
```

`aaaaa` 中模式 `aaa` 可重叠地出现于 0、1、2；串 `aaaa` 的 Z 数组为 `[4,3,2,1]`：

```text
vector<int> z = zFunction("aaaa");
assert((z == vector<int>{4, 3, 2, 1}));
vector<int> positions = zSearch("aaaaa", "aaa");
assert((positions == vector<int>{0, 1, 2}));
```

**5. 要改哪里**

- 若字符集可能包含 `\0`，将分隔符换成保证不出现在两个输入中的字符；若不存在可靠字符分隔符，可将字节映射到整数序列并用超出字节范围的整数作分隔符。
- 若要按 Unicode 字符而不是字节匹配，先解码字符串再对符号序列计算 Z 值。
- 若只需要判断是否存在匹配，可在首次发现 `z>=m` 时提前结束；当前接口收集全部起点。
- 空模式返回空表是本模板约定。若题目把空模式视为在每个边界匹配，应调整空模式分支并明确输出位置数量。

**6. 自检**

`zFunction("aaaa")` 为 `[4,3,2,1]`。`zSearch("aaaaa","aaa")` 为 `[0,1,2]`，验证重叠匹配。模式长于文本时结果为空；空文本和非空模式结果为空；空模式按当前约定也返回空。含 NUL 字节的输入违反该匹配函数前提。

**7. 坑**

1. 维护区间 `[l,r]` 却按半开代码更新；本实现用 `[l,r)`，盒内条件是 `i<r`。
2. 混淆 `z[0]` 约定；本实现非空时令其等于整串长度。
3. 拼接分隔符出现在输入串中；这会让跨分隔符的 LCP 造成错误匹配，应使用输入中不存在的分隔符。
4. 忘记拼接串中文本偏移为 `m+1`；检查位置时访问 `z[m+1+i]`。
5. 误将 UTF-8 字节索引当字符索引；需要字符语义时先解码。

**8. 一句话原理**

用最靠右的前缀匹配盒复用已知 LCP，再向右扩展，从而在线性时间得到所有后缀与整串的匹配长度。

**参考：**

- [OI Wiki：Z 函数（扩展 KMP）](https://oi-wiki.org/string/z-func/)

## 8.4 Manacher

**1. 它是做什么的**

`manacher(s)` 在线性时间求出字节串每个位置为中心的最长奇回文半径，以及每个字符间隙为中心的最长偶回文半径。输入下标按 0-based 字节位置，空串合法；返回的两个数组都与输入等长。可由半径换算最长回文区间或长度，但函数不直接返回全局最长回文。

每个位置只会被线性次扩展或复用，时间 $O(n)$；奇偶半径数组各需 $O(n)$ 空间。`std::string` 按字节比较，UTF-8 多字节字符不视为一个字符。输入不修改。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `odd[i]` | 以字符 `i` 为中心的奇回文半径，包含中心，至少为 1。总长度 `2*odd[i]-1`，区间 `[i-odd[i]+1,i+odd[i])`。 |
| `even[i]` | 以缝隙 `i-1|i` 为中心的偶回文半径，可为 0。总长度 `2*even[i]`，区间 `[i-even[i],i+even[i])`。 |
| `l`、`r` | 当前最右回文边界；奇回文循环中区间为闭区间 `[l,r]`。 |
| `k` | 当前中心半径的临时扩展值；先复用镜像半径，再比较边界外字符。 |
| `i` | 原串位置或偶回文中心缝隙编号，范围 `0..n-1`。 |
| `ManacherResult` | 包含 `odd`、`even` 两个半径向量。 |

奇回文中心落在字符上；偶回文中心落在字符之间。`even[i]` 对应的是 `i-1` 与 `i` 之间，不是字符 `i`。空串时循环不执行，两数组为空。

**3. 函数在做什么**

| 函数/类型 | 参数与返回 | 行为及前提 |
|---|---|---|
| `ManacherResult` | 字段 `odd`、`even`，类型均为 `vector<int>`。 | 分别存奇、偶中心半径。 |
| `manacher(s)` | 字符串常量引用；返回 `ManacherResult`。 | 返回每个字节位置与间隙的最长回文半径；空串返回两个空数组，不修改输入。 |

**4. 怎么调用**

调用后可扫描两个半径数组求全局最大长度，或用公式取得中心对应的半开区间。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

struct ManacherResult {
    // odd/even 均以原串 0-based 字符位置为中心索引，数值是单侧半径而非总长度。
    vector<int> odd, even;
};

// 参数 s 是字节串；返回等长 odd/even 半径数组，空串对应两个空数组，不改输入。
ManacherResult manacher(const string& s) {
    int n = (int)s.size();
    vector<int> odd(n), even(n);

    for (int i = 0, l = 0, r = -1; i < n; ++i) {
        // [l,r] 是当前最右奇回文；盒内位置先复用关于中心的镜像半径。
        int k = (i > r ? 1 : min(odd[l + r - i], r - i + 1));
        while (i - k >= 0 && i + k < n && s[i - k] == s[i + k]) ++k;
        odd[i] = k;
        if (i + k - 1 > r) {
            l = i - k + 1;
            r = i + k - 1;
        }
    }

    for (int i = 0, l = 0, r = -1; i < n; ++i) {
        // even[i] 的中心是缝隙 i-1|i；镜像下标因此比奇回文多一个 +1。
        int k = (i > r ? 0 : min(even[l + r - i + 1], r - i + 1));
        while (i - k - 1 >= 0 && i + k < n && s[i - k - 1] == s[i + k]) ++k;
        even[i] = k;
        if (i + k - 1 > r) {
            l = i - k;
            r = i + k - 1;
        }
    }
    return {odd, even};
}
```

`abba` 的最长回文是偶回文 `[0,4)`，其中心缝隙编号 2 的半径为 2：

```text
string s = "abba";
ManacherResult result = manacher(s);
assert((result.even == vector<int>{0, 0, 2, 0}));
assert(2 * result.even[2] == 4);
string empty;
ManacherResult none = manacher(empty);
assert(none.odd.empty() && none.even.empty());
```

**5. 要改哪里**

- 若只需最长回文长度，在所有 `odd[i]` 和 `even[i]` 中分别换算长度并取最大；当前返回完整半径表，未替调用者汇总。
- 若要判断给定半开区间 `[l,r)` 是否回文，应根据长度奇偶计算中心，并检查对应半径是否覆盖该区间；边界需与上述公式一致。
- 若需要按 Unicode 字符而非字节判断回文，先将字符串解码成码点序列，再对该序列应用算法。
- 若要输出最长回文内容，记录最大长度和对应区间后从原串截取；当前接口只返回半径。

**6. 自检**

`abba` 的 `even` 为 `[0,0,2,0]`，最大偶回文长度 4。`aba` 的中心位置 1 的奇半径为 2，对应区间 `[0,3)`；全相同串 `aaaa` 的中心半径应逐步覆盖最长回文。空串返回两空向量，单字符的奇半径为 1、偶半径为 0。

**7. 坑**

1. 将奇半径直接当总长度；应换算为 `2*k-1`。
2. 认为偶半径中心是字符 `i`；它实际位于 `i-1` 与 `i` 之间。
3. 把 `even[i]` 最小值写成 1；偶回文可能不存在，最小半径为 0。
4. 区间换算把右端当闭区间；本节给出的回文区间均为半开形式 `[l,r)`。
5. 用 UTF-8 字节长度解释用户可见字符数；本实现逐字节比较，字符语义需先解码。

**8. 一句话原理**

利用当前最右回文的镜像中心复用已知半径，再向两侧扩展，从而在线性时间求出所有奇偶回文中心半径。

**参考：**

- [OI Wiki：Manacher](https://oi-wiki.org/string/manacher/)

## 8.5 Trie 字典树

**1. 它是做什么的**

`Trie` 维护只含小写 ASCII 字母 `a..z` 的字符串多重集合，支持插入、查询完整词出现次数和查询某前缀下的字符串总数。重复插入按多重集合累计；空串也可插入并在根节点计数。字符不在 `a..z` 时实现不会检查，访问孩子数组可能越界。

插入或查询长度为 `L` 的串需 $O(L)$ 时间。每个节点为 26 个字符预留孩子槽位；若插入串总长度为 `T`，节点数至多 `1+T`，空间为 $O(26T)$（字母表大小固定时写作 $O(T)$）。`pass` 和 `end` 是 `int` 计数，需保证插入数量不超过其范围。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `node` | 节点池，根固定编号 0；新节点从 1 起分配。 |
| `Node::next[c]` | 当前节点沿字母 `c` 的孩子编号；0 表示该边不存在。 |
| `Node::pass` | 有多少次插入经过该节点，重复词按次数累计。根的 `pass` 是所有插入字符串总数。 |
| `Node::end` | 有多少次插入恰好在该节点结束。 |
| `u` | 当前遍历到的 Trie 节点编号。 |
| `c` | 字符映射 `ch-'a'`，合法范围 `0..25`。 |

`pass` 与 `end` 不同：例如插入 `app` 两次、`apple` 一次，`app` 节点的 `pass` 为 3、`end` 为 2。节点号 0 既是根，也是“无孩子”哨兵，因此不能把新节点编号分配为 0。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `insert(s)` | 只含 `a..z` 的字符串；返回 `void`。 | 创建缺失路径，并递增根及路径节点的 `pass`，终点 `end` 递增；重复插入累加计数。 |
| `findNode(s)` | 小写 ASCII 字符串；返回节点编号或 `-1`。 | 查找整条前缀路径；空串返回根编号 0，不修改 Trie。 |
| `countWord(s)` | 小写 ASCII 字符串；返回 `int`。 | 返回完整词插入次数；路径不存在时为 0。 |
| `countPrefix(s)` | 小写 ASCII 字符串；返回 `int`。 | 返回以该串为前缀的插入次数；空串返回总插入数。 |

该实现没有删除接口。Trie 对象可连续插入和查询；计数反映所有历史插入。

**4. 怎么调用**

先插入词，再按需查询完整词或前缀次数。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Trie {
    struct Node {
        // next[c]=0 表示无边；根恰为 0，所以实际新节点编号必须从 1 开始。
        array<int, 26> next{};
        // pass：经过该节点的已插入字符串数；end：恰在该节点结束的字符串数。
        int pass = 0;
        int end = 0;
    };
    vector<Node> node{1};

    // 参数 s 只含 a..z；把一个词加入本 Trie，重复插入会增加 pass/end 计数。
    void insert(const string& s) {
        // 字符映射固定为 'a'..'z'；改题换字符集时同时修改 26 与 ch-'a'。
        int u = 0;
        // 根的 pass 也计数，因此 countPrefix("") 会返回插入串总数。
        ++node[u].pass;
        for (char ch : s) {
            int c = ch - 'a';
            if (node[u].next[c] == 0) {
                node[u].next[c] = (int)node.size();
                node.push_back(Node{});
            }
            u = node[u].next[c];
            ++node[u].pass;
        }
        ++node[u].end;
    }

    // 参数 s 只含 a..z；返回前缀终点节点号，缺边返回 -1；不修改 Trie。
    int findNode(const string& s) const {
        // 返回前缀终点编号；-1 是查询失败状态，与合法根节点 0 区分。
        int u = 0;
        for (char ch : s) {
            int c = ch - 'a';
            if (node[u].next[c] == 0) return -1;
            u = node[u].next[c];
        }
        return u;
    }

    // 参数 s 只含 a..z；返回完整词插入次数，未出现为 0；不修改 Trie。
    int countWord(const string& s) const {
        int u = findNode(s);
        return u == -1 ? 0 : node[u].end;
    }

    // 参数 s 只含 a..z；返回以 s 为前缀的插入次数；空串返回总插入次数。
    int countPrefix(const string& s) const {
        int u = findNode(s);
        return u == -1 ? 0 : node[u].pass;
    }
};
```

插入 `app` 两次、`apple` 一次后，完整词 `app` 出现 2 次，前缀 `app` 共匹配 3 次：

```text
Trie trie;
trie.insert("app");
trie.insert("app");
trie.insert("apple");
assert(trie.countWord("app") == 2);
assert(trie.countPrefix("app") == 3);
assert(trie.countPrefix("") == 3);
assert(trie.countWord("ap") == 0);
```

**5. 要改哪里**

- 若字符集不是小写英文字母，需同时调整 `array<int,26>` 大小和 `ch-'a'` 映射；若字符范围大且稀疏，可用映射表保存孩子。
- 若要支持删除，需沿路径递减 `pass` 和终点 `end`，并确保计数不会变负；是否回收无用节点需另行实现。
- 若只需存在性而不需重复次数，可将计数转成布尔标记；当前实现保留插入多重性。
- 若计数可能超过 `int`，将 `pass`、`end` 和查询返回类型改为更宽整数。
- 若要支持大小写或任意字节，必须定义完整字符映射，不能直接使用 `ch-'a'`。

**6. 自检**

插入 `app` 两次、`apple` 一次后，`countWord("app")=2`，`countPrefix("app")=3`，`countPrefix("")=3`。`countWord("ap")` 为 0，因为它只是前缀，不是已插入完整词。未插入的前缀查询返回 0。插入空串后，`countWord("")` 为 1，根节点的前缀计数总数也增加 1。

**7. 坑**

1. 把 `pass` 当成完整词计数；它统计经过节点的所有插入，完整词次数看 `end`。
2. 新节点编号从 0 开始；0 已表示根/无边，新节点必须从 1 开始。
3. 输入含非 `a..z` 字符；映射结果会越界，调用前校验或扩展字符映射。
4. 忽略重复插入；本模板统计次数，重复词会增加 `pass` 和 `end`。
5. 把前缀存在误认为完整词存在；路径存在不代表 `end>0`，应调用 `countWord`。

**8. 一句话原理**

把字符串逐字符映射为节点边，并沿路径维护经过次数和终点次数，从而按字符串长度完成插入与前缀查询。

**参考：**

- [OI Wiki：字典树](https://oi-wiki.org/string/trie/)

## 8.6 AC 自动机

**1. 它是做什么的**

AC 自动机在同一文本中查找多个模式串的出现次数，适用于小写 ASCII 字符串。先插入全部非空模式，保存各自的终止节点，再调用一次 `build()`，最后扫描文本统计；匹配允许重叠，重复模式对应同一终止节点并得到相同次数。空模式不受支持，文本和模式字符都必须在 `a..z`。

令 `S` 为 Trie 节点数，`T` 为文本长度，`K` 为查询的模式终止节点数。插入总模式长度为 `P` 时插入耗时 $O(P)$；固定 26 个字母下，`build()` 为 $O(26S)$，文本扫描和 fail 传播为 $O(T+S)$，返回查询结果另需 $O(K)$。节点转移空间为 $O(26S)$，计数、BFS 顺序和输出额外需 $O(S+K)$。构建会原地把缺失 Trie 边补成自动机转移，因此仅能在所有模式插入后调用一次。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `node[u].next[c]` | 字符 `c` 的转移；构建前是 Trie 边，构建后缺失边也被补为自动机跳转。 |
| `node[u].fail` | 状态 `u` 的最长真后缀状态；根为 0。 |
| `bfsOrder` | 按 Trie 深度递增记录的非根状态；逆序遍历时可先把深层访问次数汇入 fail 状态。 |
| `terminal` | 调用者保存的模式终止节点编号列表，顺序与要取回答案的模式顺序一致。 |
| `visits[u]` | 扫描中恰好落在状态 `u` 的次数；fail 逆序传播后，也包含落在其 fail 后缀的次数。 |
| `u` | 文本扫描时当前自动机状态。 |

查询先计数每个文本前缀结束时所在的状态，再沿 fail 链从深到浅累加；因此以某状态为后缀的模式也计入该状态的访问。终止节点必须来自非空模式，不能把根节点当作模式终点。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `insert(s)` | 非空小写 ASCII 模式串；返回终止节点编号。 | 向 Trie 加入路径；必须在 `build()` 前调用。 |
| `build()` | 无参数；返回 `void`。 | BFS 计算 fail 并补齐转移，改变 `next` 的语义；所有模式插入后只调用一次。 |
| `countOccurrences` | 小写文本及有效非根终点列表；返回 `vector<long long>`。 | 按 terminal 输入顺序返回各模式计数，包含重叠；可在同一已构建自动机上多次查询，局部访问计数每次重置。 |

`terminal` 中有重复节点时结果向量也保留重复项。`countOccurrences` 不修改自动机；`insert` 和 `build` 会修改内部节点状态。

**4. 怎么调用**

插入所有模式并保存终点，构建一次，然后扫描文本。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

struct AhoCorasick {
    struct Node {
        // build 前 next 是 Trie 边；build 后缺边被补为自动机转移，不能再继续 insert。
        array<int, 26> next{};
        // fail 指向当前字符串的最长真后缀状态，根及根的孩子失败时回到根 0。
        int fail = 0;
    };
    vector<Node> node{1};
    vector<int> bfsOrder;

    // 参数 s 是非空小写模式串；加入 Trie 并返回终止节点号，须在 build 前调用。
    int insert(const string& s) {
        // 返回模式串终止节点，调用者须保存它；字符集固定为小写 'a'..'z'。
        int u = 0;
        for (char ch : s) {
            int c = ch - 'a';
            if (node[u].next[c] == 0) {
                node[u].next[c] = (int)node.size();
                node.push_back(Node{});
            }
            u = node[u].next[c];
        }
        return u;
    }

    // 无参数；补全本对象转移并填 bfsOrder，改变 Trie 边语义；插入结束后仅调用一次。
    void build() {
        // 只调用一次；BFS 保证计算子节点 fail 前，其 fail 父节点的完整转移已就绪。
        queue<int> q;
        for (int c = 0; c < 26; ++c) {
            int v = node[0].next[c];
            if (v != 0) q.push(v);
        }
        while (!q.empty()) {
            int u = q.front(); q.pop();
            bfsOrder.push_back(u);
            for (int c = 0; c < 26; ++c) {
                int v = node[u].next[c];
                if (v != 0) {
                    // u 经 c 到 v，则 v 的最长可用后缀是 fail[u] 经同一字符的转移。
                    node[v].fail = node[node[u].fail].next[c];
                    q.push(v);
                } else {
                    // 补全缺边后，文本扫描每个字符只做一次数组跳转，不需 while 回退。
                    node[u].next[c] = node[node[u].fail].next[c];
                }
            }
        }
    }

    // 参数 text 是小写文本，terminal 是有效的非根模式终点列表；返回逐项出现次数（允许重叠），不改自动机。
    vector<long long> countOccurrences(
        const string& text, const vector<int>& terminal
    ) const {
        // visits[u] 先统计扫描时恰好落到 u 的次数；terminal 中存各模式的终止节点。
        vector<long long> visits(node.size(), 0), answer;
        int u = 0;
        for (char ch : text) {
            u = node[u].next[ch - 'a'];
            ++visits[u];
        }
        // fail 树上由深到浅累加：到达 u 也代表其每个 fail 后缀模式出现一次。
        for (int i = (int)bfsOrder.size() - 1; i >= 0; --i) {
            int v = bfsOrder[i];
            visits[node[v].fail] += visits[v];
        }
        for (int v : terminal) answer.push_back(visits[v]);
        return answer;
    }
};
```

模式 `a` 和 `aa` 在文本 `aaa` 中分别出现 3 次和 2 次，重叠匹配也计数：

```text
AhoCorasick ac;
int terminalA = ac.insert("a");
int terminalAA = ac.insert("aa");
ac.build();
vector<long long> count = ac.countOccurrences("aaa", {terminalA, terminalAA});
assert((count == vector<long long>{3, 2}));
```

**5. 要改哪里**

- 若字符集不是小写英文字母，调整节点孩子数组大小和字符映射；插入与扫描必须使用一致映射。
- 若要支持空模式，需在输入层定义空串出现次数（通常为文本边界数），不能把根节点计数直接当成普通非空模式结果。
- 若要查询是否出现，只需将计数与 0 比较；若需报告所有匹配位置，需在扫描过程中维护当前位置并沿输出链枚举终点，当前接口只返回次数。
- 新增模式或改变模式集合时，需重新构造自动机、插入全部模式并重新 `build()`；构建后的补全转移已覆盖原 Trie 缺边语义，不能继续插入。
- 计数类型为 `long long`，若文本/匹配数量可能超过范围，应改计数类型。

**6. 自检**

插入模式 `a`、`aa` 并扫描 `aaa`，计数应分别为 3 和 2；两个 `aa` 匹配重叠于起点 0 和 1。未匹配模式的终点计数为 0。若两次分别查询不同文本，第二次结果应只依赖第二个文本，确认 `visits` 是每次新建。插入空模式或非小写字符违反模板前提。

**7. 坑**

1. 插入模式后再调用 `build()` 多次或继续插入；构建会改写缺失转移，顺序必须是全部插入后只构建一次。
2. 统计时只数扫描直接落到的状态；后缀模式需通过 fail 逆序传播访问次数。
3. 正向传播 fail 计数；必须深层先累计到浅层，使用 BFS 顺序的逆序。
4. 忘记重叠匹配；按状态逐字符扫描并传播计数会自然计入重叠，不能跳过匹配后缀。
5. 终点列表包含根节点或字符越界；只传非空模式的终止节点，并校验所有输入字符为 `a..z`。

**8. 一句话原理**

Trie 把多模式共享前缀合并，fail 链表示可继续匹配的后缀，再把文本状态访问次数沿 fail 关系汇总给每个模式终点。

**参考：**

- [OI Wiki：AC 自动机](https://oi-wiki.org/string/ac-automaton/)

## 8.7 后缀数组

**1. 它是做什么的**

`suffixArray(s)` 将字符串所有后缀按字典序排列，返回它们在原串中的 0-based 起点。`lcpArray(s,sa)` 返回排序后相邻后缀的最长公共前缀长度。输入按 `std::string` 字节比较；空串的后缀数组和 LCP 数组均为空。

后缀数组用倍增法，每轮按两个 rank 组成的键对 `n` 个后缀进行比较排序；轮数 $O(\log n)$、每轮排序 $O(n\log n)$，总时间 $O(n\log^2 n)$、空间 $O(n)$。Kasai 算法构造相邻 LCP 为 $O(n)$ 时间和 $O(n)$ 空间。此实现适合中等长度；大规模输入可改用计数排序优化的倍增或线性/近线性构造法。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `sa[i]` | 字典序第 `i` 小的后缀在 `s` 中的起点，范围 `0..n-1`。 |
| `rk[i]` | 当前轮后缀 `s[i..]` 的排序等级。 |
| `tmp[i]` | 按新 rank 对后缀排序后生成的下一轮等级。 |
| `k` | 当前倍增长度；按 `(rk[i], rk[i+k])` 排序，越界第二关键字视作 `-1`。 |
| `rankPair(i)` | lambda：返回后缀起点 `i` 对应的两个排序键。 |
| `lcp[i]` | `sa[i]` 与 `sa[i+1]` 的 LCP 长度，因此数组长度为 `max(0,n-1)`。 |
| `rk`（LCP 中） | 后缀起点到其 `sa` 排名的逆映射。 |
| `h` | Kasai 复用前一个起点的 LCP 下界；每轮结束后至多减 1。 |

初始 rank 是单字节值（按 unsigned byte 读取）；每轮把已知长度扩展到约两倍。`lcpArray` 先建立逆排名，再扫描原串起点并复用前一个 LCP，避免每对后缀从头比较。

**3. 函数在做什么**

| 函数 | 参数与返回 | 行为及前提 |
|---|---|---|
| `suffixArray(s)` | 字符串常量引用；返回 `vector<int>`。 | 返回后缀起点的字典序排列；空串返回空向量，不修改输入。 |
| 内部 `rankPair(i)` lambda | 后缀起点 `0<=i<n`；返回当前轮的两个 rank 键。 | 用于 `sort` 比较，捕获当前 `rk`、`k`，不修改它们。 |
| `lcpArray(s,sa)` | 字符串及其后缀数组；返回 `vector<int>`。 | 要求 `sa` 是 `[0,n)` 的合法排列且按后缀字典序排列；返回相邻后缀 LCP，输入不修改。空串或单字符字符串均返回空 LCP 表。 |

**4. 怎么调用**

先构造 `sa`，再把同一字符串与 `sa` 传给 LCP 函数。模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

// 参数 s 是字节串；返回按字典序排列的后缀起点，空串返回空表，不改输入。
vector<int> suffixArray(const string& s) {
    // 倍增按两个 rank 排序，越界第二关键字视为 -1。
    int n = s.size();
    vector<int> sa(n), rk(n), tmp(n);
    iota(sa.begin(), sa.end(), 0);
    for (int i = 0; i < n; ++i) rk[i] = (unsigned char) s[i];
    // k 逐次翻倍，rank 对应长度 2k 的前缀；所有后缀按新 rank 重排。
    for (long long k = 1; k < n; k <<= 1) {
        // 参数 i 是 0..n-1 的后缀起点；返回当前 2k 长度排序键，只读捕获的 rk/k。
        auto rankPair = [&](int i) {
            return pair{rk[i], i + k < n ? rk[i + k] : -1};
        };
        // 比较器参数是两个后缀起点；按 rankPair 严格升序比较，不改捕获状态。
        sort(sa.begin(), sa.end(), [&](int i, int j) {
            return rankPair(i) < rankPair(j);
        });
        if (n) tmp[sa[0]] = 0;
        for (int i = 1; i < n; ++i) {
            int a = sa[i - 1], b = sa[i];
            tmp[b] = tmp[a] + (rankPair(a) < rankPair(b));
        }
        rk=tmp;
        if (n && rk[sa.back()] == n - 1) break;
    }
    return sa;
}
// 参数 sa 必须是按后缀字典序排列的 [0,|s|) 起点排列；返回相邻后缀 LCP，长度 max(0,n-1)，不改输入。
vector<int> lcpArray(const string& s, const vector<int>& sa) {
    int n = s.size();
    vector<int> rk(n), lcp(max(0, n - 1));
    for (int i = 0; i < n; ++i) rk[sa[i]] = i;
    // Kasai 复用相邻后缀的公共前缀，向右移动起点后最多只需少比较一个字符。
    for (int i = 0, h = 0; i < n; ++i) {
        int r = rk[i];
        if (r == n - 1) {
            h = 0;
            continue;
        }
        int j = sa[r + 1];
        while (i + h < n && j + h < n && s[i + h] == s[j + h]) ++h;
        lcp[r] = h;
        if (h) --h;
    }
    return lcp;
}
```

`banana` 的后缀起点排序为 `[5,3,1,0,4,2]`，相邻 LCP 为 `[1,3,0,0,2]`：

```text
string s = "banana";
vector<int> sa = suffixArray(s);
assert((sa == vector<int>{5, 3, 1, 0, 4, 2}));
vector<int> lcp = lcpArray(s, sa);
assert((lcp == vector<int>{1, 3, 0, 0, 2}));
assert(suffixArray(string{}).empty());
```

**5. 要改哪里**

- 若要查找模式串出现位置，可在后缀数组上二分比较模式与后缀前缀；当前两个函数只构造 SA 和相邻 LCP。
- 若要最长重复子串，可取 `lcp` 最大值并结合对应相邻起点恢复区间；当前接口只返回 LCP 数组。
- 若输入规模导致 `O(n log² n)` 超时，需将每轮比较排序替换为基数/计数排序等线性轮次排序；仅优化 LCP 不会降低主要构造成本。
- 若按 Unicode 字符而非字节排序，先解码成整数符号序列并相应调整实现；当前后缀位置是字节下标。
- `lcpArray` 不校验传入 `sa`；若排序数组不合法，结果没有定义，应使用与同一 `s` 对应的正确排列。

**6. 自检**

`banana` 的后缀序列依次为 `a, ana, anana, banana, na, nana`，起点 `[5,3,1,0,4,2]`，相邻 LCP 为 `[1,3,0,0,2]`。空串返回空 SA 和 LCP；单字符字符串 SA 为 `[0]`、LCP 为空；重复字符 `aaaa` 的 SA 应为 `[3,2,1,0]`，LCP 为 `[1,2,3]`。

**7. 坑**

1. 混淆后缀起点与排名；`sa[rank]` 给起点，逆映射 `rk[start]` 才给排名。
2. 把 `lcp[i]` 当作后缀 `sa[i]` 与原串的 LCP；它表示排序相邻的 `sa[i]` 和 `sa[i+1]`。
3. 用倍增比较排序却按 $O(n\log n)$ 估算；本实现每轮 `sort`，实际为 $O(n\log^2 n)$。
4. 给 `lcpArray` 传入未经排序或不是排列的 `sa`；该函数要求正确后缀数组，不会验证。
5. 把字节位置当 Unicode 字符位置；`string` 中的排序和 LCP 都按字节进行。

**8. 一句话原理**

倍增排序逐轮扩展已知后缀前缀排名，Kasai 再复用相邻后缀 LCP 的重叠部分在线性时间生成 LCP 表。
