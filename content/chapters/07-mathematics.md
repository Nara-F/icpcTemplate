
# 7. 数学

本章默认整数为 `long long`，模数记为 `mod`。若无特别说明，模运算结果规范到 $[0,mod)$；乘法可能超过 `long long` 时用 `__int128`。

## 7.1 GCD 与扩展 GCD

**1. 它是做什么的**

最大公约数适用于整数；扩展欧几里得算法还会给出一组 Bézout 系数。本模板 `exgcd` 返回非负 gcd，并写出 `a*x+b*y=gcd`；`norm` 将余数规范到 `[0,mod)`。输入及递归系数乘积须能由 `long long` 表示，且不能含 `LLONG_MIN`。`exgcd` 为 $O(\log(\max(2,|a|,|b|)))$ 时间和递归栈空间；`norm` 为 $O(1)$。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `a`, `b` | 当前递归的两个整数；C++ 余数规则决定递归参数。 |
| `x`, `y` | 输出引用；函数覆盖它们，使原始输入满足 Bézout 等式。 |
| `x1`, `y1` | 递归子问题 `b*x1+(a%b)*y1=g` 的系数。 |
| `g` | 子问题返回的非负 gcd。 |
| `mod` | `norm` 的正模数；必须大于 0。 |

`exgcd(0,0)` 返回 0，并选择系数 `(1,0)`；这只是众多解中的一种。模余数的输出范围是 `[0,mod)`。

**3. 函数在做什么**

| 函数 | 参数与返回、副作用 |
|---|---|
| `exgcd(a,b,x,y)` | 输入 `a,b` 满足上述范围；返回非负 gcd，覆盖 `x,y` 为一组 Bézout 系数。 |
| `norm(x,mod)` | 要求 `mod>0`；返回 `x` 的规范余数，不修改调用者状态。 |

**4. 怎么调用**

调用扩展 GCD 后检查返回值和系数等式；`norm` 单独用于负余数归一化。

```text
long long x, y;
long long g = exgcd(30, 18, x, y);
assert(g == 6 && 30 * x + 18 * y == g);
assert(norm(-7, 5) == 3);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 输入可为负数；返回非负 gcd，并令 a*x+b*y=gcd(a,b)。系数本身不取模。
// 参数 a,b 及递归系数中间值须可由 long long 表示，不能含 LLONG_MIN；返回 gcd>=0，并覆盖 x,y 为 Bézout 系数。
ll exgcd(ll a, ll b, ll& x, ll& y) {
    if (b == 0) {
        // 选 x 的符号是为了即使 a<0，右侧仍为非负的 |a|。
        x = (a >= 0 ? 1 : -1);
        y = 0;
        return llabs(a);
    }
    ll x1, y1;
    ll g = exgcd(b, a % b, x1, y1);
    // 由 b*x1+(a%b)*y1=g 反代；若输入接近 long long 上界，乘法可能溢出。
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}

// 要求 mod>0；C++ 的负数余数可能为负，所以统一规范到 [0,mod)。
// 参数 mod>0；返回 x 的规范模余数 [0,mod)，不修改实参。
ll norm(ll x, ll mod) {
    x %= mod;
    if (x < 0) x += mod;
    return x;
}
```

**5. 要改哪里**

求方程 `a*x+b*y=c` 的整数解时，先检查 `g!=0` 且 `c%g==0`，再将 Bézout 系数乘以 `c/g`；这一步仍需检查乘法范围。若只需要 gcd，使用 `std::gcd` 并确认输入范围符合其约束。模逆元问题需额外要求 gcd 为 1，并将系数用 `norm` 归一化。需要处理 `LLONG_MIN` 或更大中间值时，须改用更宽整数或大整数实现。

**6. 自检**

`exgcd(30,18)` 应返回 6，且 `30*x+18*y==6`。`exgcd(0,0)` 返回 0；`norm(-7,5)==3`，`norm(7,5)==2`。对任意正模数，规范化结果必须落在 `[0,mod)`。

**7. 坑**

1. 返回 gcd 却忽略系数输出：调用方要用引用参数 `x,y`。
2. 将负余数直接当数组下标：先调用 `norm`。
3. 输入包含 `LLONG_MIN`：`llabs` 无法表示其绝对值，必须拒绝或换更宽类型。
4. 系数反代溢出：`(a/b)*y1` 也可能超出 `long long`，输入可表示并不自动保证中间值安全。

**8. 一句话原理**

欧几里得递归先求余数对的 gcd，再用 `a%b=a-(a/b)b` 反代恢复原输入的一组系数。

**参考：**

- [OI Wiki：最大公约数](https://oi-wiki.org/math/number-theory/gcd/)

## 7.2 快速幂

**1. 它是做什么的**

`qpow` 计算非负指数的模幂，采用二进制平方，把乘方次数降到对数级。要求 `e>=0`、`mod>0`；负底数会规范到 `[0,mod)`，`mod==1` 时返回 0，0^0 按空乘积约定返回 `1%mod`。预处理无，单次时间 $O(\log e)$，额外空间 $O(1)$。`mul_mod` 用 `__int128` 保存乘积后取模；其范围仍有限，但两个 long long 的乘积可容纳在有符号 128 位范围内。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `a` | 循环中的底数幂，始终规范到 `[0,mod)`。 |
| `e` | 尚未处理的指数；每轮右移一位。 |
| `ans` | 已处理指数位对应的累乘结果，初值 `1%mod`。 |
| `mod` | 正模数。 |
| `a`、`b`（`mul_mod`） | 乘数；返回 C++ 有符号余数，负操作数时结果也可能为负。 |

**3. 函数在做什么**

| 函数 | 参数与返回、副作用 |
|---|---|
| `mul_mod(a,b,mod)` | 要求 `mod>0`；以 `__int128` 计算乘积并返回余数，不改实参。 |
| `qpow(a,e,mod)` | 要求 `e>=0`、`mod>0`；返回 `a^e mod mod` 的规范值，不修改外部状态；每次乘法调用 `mul_mod`。 |

**4. 怎么调用**

直接给底数、非负指数和正模数；以下片段包含负底数、零指数和模数 1 的核对：

```text
assert(qpow(-2, 5, 13) == 7);
assert(qpow(9, 0, 7) == 1);
assert(qpow(123, 8, 1) == 0);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 要求 mod>0，且 a、b 已在 long long 内；用 __int128 避免乘法先溢出再取模。
// 参数 mod>0；返回 a*b 的 C++ 余数，乘积在 __int128 中求值，不改实参。
ll mul_mod(ll a, ll b, ll mod) {
    // 提升后再乘，避免两个 long long 先溢出；要求 mod>0。
    return (ll)((__int128)a * b % mod);
}

// 参数 e>=0、mod>0；返回规范化的 a^e mod mod，内部不持有可变共享状态。
ll qpow(ll a, long long e, ll mod) {
    // e 必须非负；若题目出现负指数，应先求 a 的模逆元再调用。
    a %= mod;
    if (a < 0) a += mod;
    ll ans = 1 % mod;
    while (e > 0) {
        // 不变量：ans * a^e 与原始 a^原始e 在模 mod 下同余。
        if (e & 1) ans = mul_mod(ans, a, mod);
        a = mul_mod(a, a, mod);
        e >>= 1;
    }
    return ans;
}
```

**5. 要改哪里**

- 负指数不能传入当前循环；若要算模逆幂，先求底数的模逆元，再用非负指数调用。
- 若乘数范围超出 long long，当前接口无法接收；需改参数和乘法策略。
- 需要多次对同一模数求幂时可重复调用，函数无共享可变状态；若要减少模运算，可按题目批量预处理幂表。

**6. 自检**

`qpow`(`a`,0,m)==1%m 对所有 m>0 成立；`qpow`(-2,5,13)==7；模数 1 时任何合法输入都返回 0。检查指数为 1、偶数和奇数，结果都应落在 [0,m)。

**7. 坑**

1. 把负指数传入：循环不会实现模逆，先求逆元或拒绝该输入。
2. 直接用 `a`*`b`%`mod`：乘法可能在取模前溢出，使用 `mul_mod`。
3. 模数为 0 或负数：取模无效，调用前保证 `mod>0`。
4. 误认为 `mul_mod` 对负乘数返回规范余数：其结果遵循 C++ 余数规则；`qpow` 通过规范化底数保证幂运算状态非负。

**8. 一句话原理**

按指数二进制位累乘当前底数幂，并逐轮平方底数、右移指数。

**参考：**

- [OI Wiki：快速幂](https://oi-wiki.org/math/binary-exponentiation/)

## 7.3 素数筛

**1. 它是做什么的**

`PrimeSieve(n)` 用线性筛预处理 `[0,n]`，同时生成递增质数表、最小质因子、最小质因子指数和正因数个数。构造时间与表空间均为 $O(n)$；`isPrime` 和 `countDivisors` 查询为 $O(1)$。适用于已知上界内的批量查询；只分解一个很大的数时，筛完整范围通常不划算。`countDivisors` 只接受 `1<=x<=n`；`isPrime` 对越界及小于 2 的输入返回 false。

**2. 变量在做什么**

| 成员 | 含义 |
|---|---|
| `primes` | 不超过 n 的递增质数。 |
| `minPrime[x]` | x 的最小质因子；0、1 处为 0。 |
| `minPrimeExponent[x]` | `minPrime[x]` 在 x 中的指数；0、1 处为 0。 |
| `divisorCount[x]` | x 的正因数个数；`divisorCount[1]=1`，下标 0 仅占位。 |
| `i,p,product` | 当前整数、试用质数及合数 `i*p`。 |

当 p 等于 i 的最小质因子时，指数增加一并依公式修正因数个数，然后停止内层循环；否则 p 是新因子，因数个数加倍。

**3. 函数在做什么**

| 接口 | 参数、返回与副作用 |
|---|---|
| `PrimeSieve(n)` | 要求 `n>=0`；构造并填充所有表。对象成员保存结果。 |
| `isPrime(x)` | 任意整数输入；越界或 `x<2` 返回 false，不修改对象。 |
| `countDivisors(x)` | 要求 `1<=x<=n`；返回 x 的正因数个数，只读表。 |

**4. 怎么调用**

先构造上界足够大的筛对象，再查询。示例确认素数、越界和约数个数：

```text
PrimeSieve sieve(12);
assert(sieve.isPrime(11));
assert(!sieve.isPrime(1) && !sieve.isPrime(13));
assert(sieve.countDivisors(12) == 6);
assert(sieve.countDivisors(1) == 1);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

struct PrimeSieve {
    // 数组下标就是被筛整数；0、1 的 minPrime 和 minPrimeExponent 为 0，divisorCount[0] 仅作占位。
    vector<int> primes, minPrime, minPrimeExponent, divisorCount;

    // 若 i=p^e*m 且 gcd(p,m)=1，则 d(i)=(e+1)d(m)。已有最小质因子时 d(ip)=d(i)/(e+1)*(e+2)，新增质因子时 d(ip)=2d(i)；前者先做精确整除。
    // 参数 n>=0；构造 [0,n] 筛表，填充素数、最小质因子、其指数和正因数个数；n=0/1 也有效。
    explicit PrimeSieve(int n)
        : minPrime(n + 1, 0), minPrimeExponent(n + 1, 0), divisorCount(n + 1, 0) {
        if (n >= 1) divisorCount[1] = 1;
        for (int i = 2; i <= n; ++i) {
            if (minPrime[i] == 0) {
                minPrime[i] = i;
                minPrimeExponent[i] = 1;
                divisorCount[i] = 2;
                primes.push_back(i);
            }
            for (int p : primes) {
                // 只用 p<=minPrime[i]：保证 i*p 恰由其最小质因子筛到一次。
                if (p > minPrime[i] || 1LL * i * p > n) break;
                int product = i * p;
                minPrime[product] = p;
                if (p == minPrime[i]) {
                    // 同一最小质因子指数由 e 增到 e+1，其余质因子的计数因子不变。
                    minPrimeExponent[product] = minPrimeExponent[i] + 1;
                    divisorCount[product] = divisorCount[i] /
                        (minPrimeExponent[i] + 1) * (minPrimeExponent[product] + 1);
                    break;
                }
                // p<minPrime[i] 时新增一个一次因子 p，tau 值乘 2。
                minPrimeExponent[product] = 1;
                divisorCount[product] = divisorCount[i] * 2;
            }
        }
    }

    // 参数 x 为任意整数；返回 x 是否在筛范围内且为素数，越界返回 false，不改对象。
    bool isPrime(int x) const {
        return x >= 2 && x < (int)minPrime.size() && minPrime[x] == x;
    }

    // 参数 x 满足 1<=x<minPrime.size()；返回 x 的正因数个数，读取预处理表且不修改对象。
    int countDivisors(int x) const {
        return divisorCount[x];
    }
};
```

**5. 要改哪里**

要增加其他积性函数表，需在合数生成处按最小质因子的相同/不同情况推导递推式，并保持每个合数只被其最小质因子生成。若只需要判素数，可删除指数和约数数目两张表以节省空间。若要查询超出 n 的值，必须提高上界重建对象；当前查询不会动态扩表。

**6. 自检**

`n=0` 和 `n=1` 均可构造；筛到 10 时质数应为 2、3、5、7，`countDivisors(1)=1`、`countDivisors(12)=6`。`isPrime(0)`、`isPrime(1)` 及越界值均为 false。

**7. 坑**

1. 把下标 0 的约数计数解释为数学值：它仅是占位 0。
2. 用筛表判断超出上界的数：接口按设计返回 false，不代表它在数学上不是素数。
3. 把 `i*p` 先用 int 相乘：代码先以 long long 比较上界，避免乘积比较溢出。
4. 随意移除内层停止条件：会破坏线性筛每个合数只生成一次的性质。

**8. 一句话原理**

每个合数只由最小质因子生成一次，同时根据这个因子是否重复更新其指数与约数数目。

**参考：**

- [OI Wiki：筛法](https://oi-wiki.org/math/number-theory/sieve/)

## 7.4 质因数分解

**1. 它是做什么的**

`factorize(n)` 对单个正整数试除，返回升序的“质因子、指数”对；要求 `n>=1`，输入按值传递，不改变调用者变量。`n=1` 返回空向量。最坏试除时间为 $O(\sqrt n)$，输出空间为不同质因子个数；额外工作空间同阶于输出。大量有共同上界的数可改用最小质因子筛。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `n` | 剩余待分解部分；每取出一个质因子的全部幂次就缩小。 |
| `p` | 从 2 递增尝试的除数，满足 `p<=n/p`。 |
| `e` | 当前质因子 p 的指数。 |
| `fac` | 按 p 递增追加的 `{p,e}` 结果；最后剩余的大于 1 的数是一个质因子。 |

试除上界随剩余 n 缩小，因此质因子取出后可减少后续扫描。

**3. 函数在做什么**

`factorize(ll n)` 要求正整数输入；返回 `vector<pair<ll,int>>`，每对按质因子升序排列。函数只修改自己的参数副本，不修改调用者变量；1 的分解为空。

**4. 怎么调用**

返回值可直接遍历，下面断言 360 的分解为 `2^3*3^2*5`，并检查 1：

```text
auto f = factorize(360);
assert((f == vector<pair<long long,int>>{{2,3},{3,2},{5,1}}));
assert(factorize(1).empty());
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 n>=1；返回升序 {质因子,指数}，n==1 返回空表，不改调用者数据。
vector<pair<ll, int>> factorize(ll n) {
    // 要求 n>=1；返回质因子递增的 {质因子, 指数}，不记录因子 1。
    vector<pair<ll, int>> fac;
    // 用 p<=n/p 代替 p*p<=n，避免 long long 乘法溢出；n 会随试除缩小。
    for (ll p = 2; p <= n / p; ++p) {
        if (n % p != 0) continue;
        int e = 0;
        while (n % p == 0) {
            n /= p;
            ++e;
        }
        fac.push_back({p, e});
    }
    // 此时若仍有余数，它不可能再含两个质因子，因此本身就是最后一个质因子。
    if (n > 1) fac.push_back({n, 1});
    return fac;
}
```

**5. 要改哪里**

若需要约数个数，计算各指数加一的乘积；若需约数和，可按每个质因子对应的等比和相乘，并注意乘积类型范围。需要分解很多个不超过固定上界的整数时，预处理最小质因子通常更合算。输入为 0 或负数不在本函数定义域，不能直接套用。

**6. 自检**

`factorize(1)` 为空；`factorize(13)` 为 `{{13,1}}`；`factorize(360)` 的质因子依次为 2、3、5，指数为 3、2、1。对返回结果重乘各因子幂，应还原原输入。

**7. 坑**

1. 循环写 `p*p<=n`：乘法可能溢出；使用 `p<=n/p`。
2. 试除时不缩小 n：不仅效率较差，也可能误用原数的剩余状态。
3. 漏掉循环后 `n>1` 的剩余项：它是最后一个质因子。
4. 对 `n=0` 或负数调用：超出定义域，调用前验证正数。

**8. 一句话原理**

递增试除并一次取尽每个因子的幂次，最后剩余的大于 1 的部分必为质数。

**参考：**

- [OI Wiki：质因数分解](https://oi-wiki.org/math/number-theory/pollard-rho/#%E6%9C%B4%E7%B4%A0%E7%AE%97%E6%B3%95)

## 7.5 欧拉函数

**1. 它是做什么的**

欧拉函数 `phi(n)` 统计 `1..n` 中与 n 互质的正整数个数。`eulerPhi` 单次试除，时间 $O(\sqrt n)$、额外空间 $O(1)$；`phiSieve` 一次生成 `[0,n]` 整张表，时间和空间均为 $O(n)$。单次接口要求 `n>=1`，并约定 `phi(1)=1`；筛表接受 `n>=0`，`n=0` 时返回仅含占位 `phi[0]=0` 的向量。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `n` | 当前待处理整数；试除版本会移除已处理质因子。 |
| `ans` | 起始为原 n，依次乘每个不同质因子的 `(p-1)/p`。 |
| `phi[x]` | 筛表中整数 x 的欧拉函数；0 号位为占位。 |
| `primes`、`composite` | 线性筛的质数表与合数标记。 |
| `p` | 当前试用质数；若整除 i，生成 `i*p` 后停止内层循环。 |

**3. 函数在做什么**

| 函数 | 参数、返回与副作用 |
|---|---|
| `eulerPhi(n)` | 要求 `n>=1`；返回单个欧拉函数值，不修改外部状态。 |
| `phiSieve(n)` | 要求 `n>=0`；返回长度 `n+1` 的新表，局部筛数组不会泄漏到外部。 |

**4. 怎么调用**

单点和整表接口都可独立使用；下例核对 `phi(9)=6`、`phi(1)=1` 和筛表的 `phi(10)=4`：

```text
assert(eulerPhi(9) == 6);
assert(eulerPhi(1) == 1);
auto phi = phiSieve(10);
assert(phi.size() == 11 && phi[10] == 4 && phi[0] == 0);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 n>=1；返回 phi(n)，不修改 n 或外部状态。
ll eulerPhi(ll n) {
    // 要求 n>=1；ans 始终等于原 n 乘上已处理质因子的 (p-1)/p。
    ll ans = n;
    for (ll p = 2; p <= n / p; ++p) {
        if (n % p != 0) continue;
        while (n % p == 0) n /= p;
        // p 一定整除当前 ans，先除后乘既保持精确，也降低中间溢出风险。
        ans = ans / p * (p - 1);
    }
    if (n > 1) ans = ans / n * (n - 1);
    return ans;
}

// 参数 n>=0；返回下标 [0,n] 的 phi 表，分配局部筛状态，不修改外部对象。
vector<int> phiSieve(int n) {
    // phi[x] 对应整数 x；线性筛中每个合数只由最小质因子产生一次。
    vector<int> phi(n + 1), primes;
    vector<bool> composite(n + 1, false);
    if (n >= 1) phi[1] = 1;
    for (int i = 2; i <= n; ++i) {
        if (!composite[i]) {
            primes.push_back(i);
            phi[i] = i - 1;
        }
        for (int p : primes) {
            if (1LL * i * p > n) break;
            composite[i * p] = true;
            if (i % p == 0) {
                // p 已整除 i：新增一个 p 因子，phi(i*p)=phi(i)*p，随后必须停止。
                phi[i * p] = phi[i] * p;
                break;
            }
            // gcd(i,p)=1，乘入新质因子 p 时欧拉函数乘以 p-1。
            phi[i * p] = phi[i] * (p - 1);
        }
    }
    return phi;
}
```

**5. 要改哪里**

只需单个值时用 `eulerPhi`；需要大量有界查询时用 `phiSieve`。若要计算互质计数以外的积性函数，需重推筛内递推，不能只换答案变量。欧拉定理 `a^phi(n) ≡ 1 (mod n)` 还要求 `gcd(a,n)=1`，不能把它当作对所有底数成立。

**6. 自检**

`phi(1)=1`，素数 p 的 `phi(p)=p-1`，`phi(9)=6`、`phi(10)=4`。筛到 0 返回长度 1 且 `phi[0]=0`；筛到 1 应有 `phi[1]=1`。

**7. 坑**

1. 把 `phi(1)` 设为 0：定义下它等于 1。
2. 同一质因子重复更新：先取尽 p 的所有次幂，再执行一次 `ans=ans/p*(p-1)`。
3. 乘除顺序颠倒：先整除再乘，保持精确并降低中间值风险。
4. 无条件使用欧拉定理：底数与模数必须互质。

**8. 一句话原理**

每个不同质因子 p 都将当前计数按比例乘以 `(p-1)/p`，线性筛则同时传播这一规则。

**参考：**

- [OI Wiki：欧拉函数](https://oi-wiki.org/math/number-theory/euler-totient/)

## 7.6 模逆元

**1. 它是做什么的**

`modInverse(a,mod)` 求模乘法逆元，支持质数或合数模；逆元存在当且仅当 `gcd(a,mod)=1`。要求 `mod>1`，a 可带符号，函数先规范底数。返回 `{true,x}` 时 `x∈[0,mod)` 且 `a*x≡1 (mod mod)`；不存在则返回 `{false,0}`。时间 $O(\log mod)$，递归栈空间 $O(\log mod)$。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `a` | 先取模并规范为非负值，再作为 exgcd 的一侧输入。 |
| `mod` | 大于 1 的模数。 |
| `x,y` | 扩展 GCD 写出的 Bézout 系数，满足 `a*x+mod*y=gcd(a,mod)`。 |
| `g` | 最大公约数；仅当 `g==1` 时 x 才是逆元。 |

**3. 函数在做什么**

`modInverse(a,mod)` 返回 `pair<bool,ll>`。第一项表示是否存在，第二项在成功时为规范逆元，失败时固定为 0。内部根调用为 `exgcd(a,mod,x,y)`，其中 a 已规范到 [0,mod)、b=mod；函数返回 gcd 并覆盖 x、y 为 Bézout 系数。递归系数中间值须可由 `long long` 表示。

**4. 怎么调用**

先检查存在标志，再使用逆元；以下核对模 64 的逆元及不互质情况：

```text
auto inv = modInverse(35, 64);
assert(inv.first && inv.second == 11);
assert((35 * inv.second) % 64 == 1);
auto missing = modInverse(6, 12);
assert(!missing.first && missing.second == 0);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 a,b 为非负且递归系数运算须可表示；返回 gcd 并写 Bézout 系数 x,y。
ll exgcd(ll a, ll b, ll& x, ll& y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    ll x1, y1;
    ll g = exgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - a / b * y1;
    return g;
}

// 参数 mod>1、a 可带符号；返回 {是否存在,规范逆元}，不互质时为 {false,0}。
pair<bool, ll> modInverse(ll a, ll mod) {
    // 要求 mod>1；返回 false 表示 gcd(a,mod)!=1，此时任何模除法都无定义。
    a %= mod;
    if (a < 0) a += mod;
    ll x, y;
    ll g = exgcd(a, mod, x, y);
    if (g != 1) return {false, 0};
    // Bézout 等式给出 a*x+mod*y=1，所以 x 就是逆元；规范到 [0,mod)。
    x %= mod;
    if (x < 0) x += mod;
    return {true, x};
}
```

**5. 要改哪里**

若要计算 `b/a mod m`，先求 `a` 的逆元，存在时再乘 b 并取模。若使用费马小定理 `a^(p-2)`，必须确认模数 p 为质数且 a 不被 p 整除；当前扩展 GCD 方法也支持合数模。若需要更宽输入或中间系数，需换成大整数实现。

**6. 自检**

`modInverse(35,64)` 应为 11；`modInverse(6,12)` 不存在；任何成功结果都应满足乘积模 m 等于 1。`a=0` 或 `a` 是模数倍数时无逆元。

**7. 坑**

1. 不检查存在标志就做除法：不互质时返回的 0 不是逆元。
2. 合数模数也套费马小定理：费马形式要求质数模数。
3. 结果未规范化：成功结果已保证落在 `[0,mod)`。
4. 模数取 1 或非正数：不满足函数前提。

**8. 一句话原理**

扩展 GCD 给出 `a*x+mod*y=1` 时，系数 x 正是 a 的模逆元。

**参考：**

- [OI Wiki：模逆元](https://oi-wiki.org/math/number-theory/inverse/)

## 7.7 线性同余方程

**1. 它是做什么的**

求解线性同余式 `a*x≡b (mod m)`，要求 `m>0`，系数和常数可为负。函数返回 `{exists,x0,step}`；有解时所有整数解为 `x=x0+k*step`，其中 `x0∈[0,step)`、`step=m/gcd(a,m)`。无解返回 `false,0,0`。扩展 GCD 时间和递归栈空间为 $O(\log m)$，其余工作为常数空间。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `a,b` | 先按 m 规范化的系数与常数。 |
| `m` | 正模数；保持方程的同余意义。 |
| `g` | `gcd(a,m)`；可解条件是 `g|b`。 |
| `step` | 解的周期 `m/g`。 |
| `x,y` | 扩展 GCD 得到的 Bézout 系数。 |
| `x0` | 约去 g 后求得并规范到 `[0,step)` 的一个解。 |

**3. 函数在做什么**

`solveCongruence(a,b,m)` 返回 `CongruenceSolution`。`m` 必须为正；a、b 可以带符号。`exists=false` 时其余字段为 0；成功时代表一个模 step 的剩余类。内部根调用为 `exgcd(a,m,x,y)`，其中 a 已规范到 [0,m)、b=m；函数返回 gcd 并覆盖 x、y 为 Bézout 系数，递归系数运算须可由 `long long` 表示。

**4. 怎么调用**

调用后先检查 exists；以下方程 `6x≡8 (mod 14)` 的代表解为 6、周期为 7：

```text
auto s = solveCongruence(6, 8, 14);
assert(s.exists && s.x0 == 6 && s.step == 7);
assert((6 * s.x0 - 8) % 14 == 0);
auto no = solveCongruence(4, 3, 6);
assert(!no.exists && no.x0 == 0 && no.step == 0);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 a,b 为非负；返回 gcd 并覆盖 x,y 为 Bézout 系数。
ll exgcd(ll a, ll b, ll& x, ll& y) {
    if (b == 0) { x = 1; y = 0; return a; }
    ll x1, y1;
    ll g = exgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - a / b * y1;
    return g;
}

struct CongruenceSolution {
    bool exists;
    // exists=true 时全部解为 x=x0+k*step，且 x0 位于 [0,step)。
    ll x0, step;
};

// 参数 m>0、a,b 可带符号；返回解存在标志及 x0、step，不解时三字段为 false,0,0。
CongruenceSolution solveCongruence(ll a, ll b, ll m) {
    // 要求 m>0；负系数和负常数先规范化，方程语义不变。
    a %= m;
    b %= m;
    if (a < 0) a += m;
    if (b < 0) b += m;
    ll x, y;
    ll g = exgcd(a, m, x, y);
    // ax≡b (mod m) 可解当且仅当 gcd(a,m) 整除 b。
    if (b % g != 0) return {false, 0, 0};
    ll step = m / g;
    // 约去 g 后 x 是 a/g 在模 m/g 下的逆元；乘法用 __int128 防溢出。
    ll x0 = (ll)((__int128)x * (b / g) % step);
    if (x0 < 0) x0 += step;
    return {true, x0, step};
}
```

**5. 要改哪里**

枚举模 m 内全部解时，取 `x0+k*step`，`0<=k<g`。若需最小非负解，当前 `x0` 已满足。改求其他同余方程组时可将此接口作为一步合并器；模数必须保持为正。涉及超出 long long 的乘积时，应替换 __int128/long long 的数据类型。

**6. 自检**

`6x≡8 (mod 14)` 有 2 个模 14 解：6、13，返回代表类 6 mod 7。`4x≡3 (mod 6)` 无解，因为 gcd 为 2 不整除 3。若 `a=0`，方程只有在 b 是 m 的倍数时才有解。

**7. 坑**

1. 未检查 `b%g==0`：不满足时不能继续求逆元。
2. 约去 g 后仍以 m 为周期：正确周期是 `m/g`。
3. 只检查一个代表解：返回值描述整个周期类，不是唯一整数解。
4. 忽略负输入：函数会规范化 a、b，但 m 仍须为正。

**8. 一句话原理**

先用 gcd 判定常数能否整除，再约去 gcd，把问题化为一个互质模数下的逆元求解。

**参考：**

- [OI Wiki：线性同余方程](https://oi-wiki.org/math/number-theory/linear-equation/)

## 7.8 中国剩余定理（非互质模数）

**1. 它是做什么的**

合并多条同余式 `x≡rem[i] (mod mod[i])`，允许模数不互质。要求两向量等长、每个模数为正，且逐步最小公倍数可由 `long long` 表示。成功返回 `{true,r,m}`，表示全部解 `x=r+k*m` 且 `r∈[0,m)`；矛盾返回 `{false,0,0}`。空输入按 `0 mod 1` 返回。k 条式子的时间约为 $O(k\log M)$，其中 M 是过程中模数的量级；递归栈空间 $O(\log M)$，循环变量额外空间 $O(1)$。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `rem[i],mod[i]` | 第 i 条同余式的余数和正模数。 |
| `r,m` | 已合并方程组的代表余数和周期，初值为 `0 mod 1`。 |
| `b` | 当前余数规范到 `[0,mod[i])` 后的值。 |
| `g` | `gcd(m,mod[i])`；必须整除两余数之差才能合并。 |
| `q` | 新模数除以 g；新周期为 `m*q`。 |
| `t` | 使新解满足当前同余式的步数参数。 |

**3. 函数在做什么**

`crt(rem,mod)` 要求向量等长且模数均为正；返回 `CRTResult`，矛盾时 `exists=false`。成功后 remainder 已规范，modulus 是逐步 lcm。每轮内部根调用为 `exgcd(m,mod[i],x,y)`，两个参数均为正；函数返回 gcd 并覆盖 x、y 为 Bézout 系数。递归栈占用 $O(\log M)$。中间 lcm 以 __int128 计算后转回 long long，因此输入必须保证结果可表示。

**4. 怎么调用**

传入并行的余数、模数数组。示例两式兼容，另外一组不兼容，空组具有约定结果：

```text
auto ok = crt(vector<long long>{2, 5}, vector<long long>{6, 9});
assert(ok.exists && ok.remainder == 14 && ok.modulus == 18);
auto bad = crt(vector<long long>{1, 2}, vector<long long>{4, 6});
assert(!bad.exists);
auto empty = crt(vector<long long>{}, vector<long long>{});
assert(empty.exists && empty.remainder == 0 && empty.modulus == 1);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 a,b 为正；返回 gcd 并覆盖 x,y 为 Bézout 系数，要求递归乘积不溢出。
ll exgcd(ll a, ll b, ll& x, ll& y) {
    if (b == 0) { x = 1; y = 0; return a; }
    ll x1, y1;
    ll g = exgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - a / b * y1;
    return g;
}

struct CRTResult {
    bool exists;
    // exists=true 时全部解为 x=remainder+k*modulus，余数已规范化。
    ll remainder, modulus;
};

// 参数 rem/mod 等长、每个模数正且逐步 lcm<=LLONG_MAX；返回规范解类或矛盾标志，不改输入。
CRTResult crt(const vector<ll>& rem, const vector<ll>& mod) {
    // 要求 rem.size()==mod.size() 且每个 mod[i]>0；空方程组返回 x≡0 (mod 1)。
    ll r = 0, m = 1;
    for (int i = 0; i < (int)rem.size(); ++i) {
        ll b = rem[i] % mod[i];
        if (b < 0) b += mod[i];
        ll x, y;
        ll g = exgcd(m, mod[i], x, y);
        ll diff = b - r;
        // 令新解为 r+m*t；只有 gcd(m,mod[i]) 能整除 b-r 时才可合并。
        if (diff % g != 0) return {false, 0, 0};

        ll q = mod[i] / g;
        // x 是 m/g 对模 q 的逆元；t 取最小非负剩余类即可。
        ll t = (ll)((__int128)(diff / g) * x % q);
        if (t < 0) t += q;
        __int128 newMod = (__int128)m * q;
        __int128 newR = (__int128)r + (__int128)m * t;
        // 若题目不保证最终 lcm 可放入 long long，需改用大整数。
        m = (ll)newMod;
        r = (ll)(newR % m);
        if (r < 0) r += m;
    }
    return {true, r, m};
}
```

**5. 要改哪里**

若模数保证两两互质，可使用经典 CRT，但当前算法无需该限制。若逐步 lcm 可能超出 long long，需将返回类型和中间运算全部改成大整数；只把乘法临时提升后立即窄化并不能防止最终溢出。需要报告某条冲突约束时，可扩展结果类型保存冲突位置。

**6. 自检**

`x≡2 (mod 6), x≡5 (mod 9)` 合并为 `14 mod 18`；`x≡1 (mod 4), x≡2 (mod 6)` 不相容。空方程组返回 `0 mod 1`。对成功结果，代回每条输入同余式均应成立。

**7. 坑**

1. 直接套互质模数公式：不互质时须先检查差值能否被 gcd 整除。
2. 把模数乘积当作新周期：一般新周期是 lcm，即 `m*(mod[i]/g)`。
3. 余数为负未规范：代码会先规范当前输入余数及合并结果。
4. 忽略范围约束：最终 lcm 和余数更新都不能超出 long long 可表示范围。

**8. 一句话原理**

逐条合并时先用 gcd 检查相容，再在约去公因数后的模数上解一个线性同余式。

**参考：**

- [OI Wiki：中国剩余定理](https://oi-wiki.org/math/number-theory/crt/)

## 7.9 组合数

**1. 它是做什么的**

`Combinations(N,mod)` 预处理组合数阶乘与逆阶乘，适合固定质数模数下反复查询。要求 `mod` 为大于 1 的质数且 `0<=N<mod`。构造时间 $O(N+\log mod)$，空间 $O(N)$；表内一次 `C(n,k)` 查询 $O(1)$。`n>N`、`k<0` 或 `k>n` 按约定返回 0。

**2. 变量在做什么**

| 成员 | 含义 |
|---|---|
| `mod` | 所有运算使用的质数模数。 |
| `fact[i]` | `i! mod mod`。 |
| `invFact[i]` | 阶乘 `i!` 的模逆。 |
| `n,k` | 查询的组合数参数；有效范围为 `0<=k<=n<=N`。 |

逆阶乘从 `N!` 的逆元向下推，依赖模数为质数且 `N<mod`，此时表内阶乘都非零。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `qpow(a,e,mod)` | 内部辅助，要求 `0<=a<mod`、`e>=0`、质数 `mod>1`；返回规范模幂。 |
| `Combinations(N,mod)` | 建立并持有阶乘表；要求 `0<=N<mod`、mod 为质数。 |
| `C(n,k)` | 返回 `C(n,k) mod mod`；非法 k 或超出预处理上界返回 0，不修改表。 |

**4. 怎么调用**

同一对象可回答多次查询；示例使用质数模 7 且预处理到 6：

```text
Combinations comb(6, 7);
assert(comb.C(5, 2) == 3); // 10 mod 7
assert(comb.C(6, 0) == 1);
assert(comb.C(3, 4) == 0);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 0<=a<mod、e>=0、mod>1；返回规范的 a^e 模余数，供阶乘逆元计算。
ll qpow(ll a, ll e, ll mod) {
    ll ans = 1;
    while (e > 0) {
        if (e & 1) ans = (ll)((__int128)ans * a % mod);
        a = (ll)((__int128)a * a % mod);
        e >>= 1;
    }
    return ans;
}

struct Combinations {
    ll mod;
    // fact[i]=i!，invFact[i]=(i!)^{-1}；数组下标覆盖 [0,n]。
    vector<ll> fact, invFact;

    // 参数 0<=n<mod、mod 为质数；构造并拥有 0..n 阶乘和逆阶乘表。
    Combinations(int n, ll mod) : mod(mod), fact(n + 1), invFact(n + 1) {
        // 前提：mod 为质数且 0<=n<mod，否则 fact[n] 可能为 0 且没有逆元。
        fact[0] = 1;
        for (int i = 1; i <= n; ++i)
            fact[i] = (ll)((__int128)fact[i - 1] * i % mod);
        // 费马小定理只在质数模下成立；改成任意模数时需替换整套求逆方案。
        invFact[n] = qpow(fact[n], mod - 2, mod);
        for (int i = n; i >= 1; --i)
            invFact[i - 1] = (ll)((__int128)invFact[i] * i % mod);
    }

    // 参数 n,k 为整数；返回 C(n,k) mod mod，越出预处理范围或 k 不合法时返回 0，不改表。
    ll C(int n, int k) const {
        // 返回 C(n,k) mod mod；非法 k 或超出预处理上界时约定返回 0。
        if (k < 0 || k > n || n >= (int)fact.size()) return 0;
        ll ans = (ll)((__int128)fact[n] * invFact[k] % mod);
        return (ll)((__int128)ans * invFact[n - k] % mod);
    }
};
```

**5. 要改哪里**

若 N 可能达到或超过 mod，阶乘将为 0，当前逆阶乘方案失效；需换 Lucas 定理或其他适合模数/范围的算法。若模数是合数，费马小定理求逆不可用，不能只把 mod 参数换掉。小 N 且任意模数时，可用 Pascal 递推，但单次/整体复杂度不同。

**6. 自检**

`C(5,2)=10`，模 7 得 3；`C(n,0)=C(n,n)=1`；`k>n` 返回 0。若 `N=0` 且模数满足前提，`C(0,0)=1`。

**7. 坑**

1. 将模板用于合数模：阶乘未必可逆。
2. 取 `N>=mod`：预处理阶乘可能为 0。
3. 对非法 k 访问数组：接口返回 0，应保留参数检查。
4. 每次查询重新构造对象：重复预处理会浪费时间，应复用同一表。

**8. 一句话原理**

用阶乘和逆阶乘把组合数公式拆成三次数组读取与常数次乘法。

**参考：**

- [OI Wiki：组合数学](https://oi-wiki.org/math/combinatorics/combination/)

## 7.10 容斥原理

**1. 它是做什么的**

`countDivisible(n,a)` 统计 `[1,n]` 中至少被一个给定正除数整除的整数个数。要求 `n>=0`，输入除数非负，且有效条件数少于 64；0 会忽略，重复项和冗余倍数会删除。枚举所有非空子集，设原输入长度为 `t`，清理后有效除数数目为 `k`。预处理时间为 $O(t\log t+tk)$，其中排序去重后再检查冗余倍数；枚举子集时含 gcd 的时间为 $O(2^k k\log(n+1))$，额外空间为 $O(t)$，含按值传入的副本。超出 n 的 lcm 子集贡献为 0。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `a` | 按值传入的除数副本；排序、去重和删冗余不会改调用者向量。 |
| `b` | 清理后的有效除数集合。 |
| `mask` | 当前非空子集，位 i 表示是否选中 `b[i]`。 |
| `lcm` | 当前子集交集对应的最小公倍数。 |
| `g` | 更新 lcm 时的 gcd。 |
| `ans` | 容斥累计值；奇数项加、偶数项减。 |
| `n` | 闭区间 `[1,n]` 的右端点。 |

如果已有较小除数 y 整除 x，则被 x 整除的数已经包含在 y 的集合里，x 可删。

**3. 函数在做什么**

`countDivisible(n,a)` 返回并集计数；`n>=0`、除数非负、有效数量少于 64 是调用前提。它接收向量副本并在本地清理，不修改调用者状态。lcm 超过 n 时跳过该子集。

**4. 怎么调用**

示例统计 1..20 中 2 或 3 的倍数；集合大小为 10+6-3=13：

```text
assert(countDivisible(20, vector<long long>{2, 3}) == 13);
assert(countDivisible(10, vector<long long>{2, 4, 0, 2}) == 5);
assert(countDivisible(0, vector<long long>{2, 3}) == 0);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 n>=0、a 含非负除数且有效项数<64；返回 [1,n] 并集计数，传值副本可排序删项。
ll countDivisible(ll n, vector<ll> a) {
    // 统计闭区间 [1,n]；模板假设 n>=0、除数为非负数，且有效条件数 k<64。
    sort(a.begin(), a.end());
    a.erase(remove(a.begin(), a.end(), 0), a.end());
    a.erase(unique(a.begin(), a.end()), a.end());
    vector<ll> b;
    for (ll x : a) {
        bool redundant = false;
        // 若 x 是已有 y 的倍数，“能被 x 整除”已包含于“能被 y 整除”，可删除。
        for (ll y : b) if (x % y == 0) {
            redundant = true;
            break;
        }
        if (!redundant && x <= n) b.push_back(x);
    }

    ll ans = 0;
    int k = (int)b.size();
    for (unsigned long long mask = 1; mask < (1ULL << k); ++mask) {
        // 一个子集的交集就是被这些除数的 lcm 整除；奇数个集合加，偶数个减。
        ll lcm = 1;
        bool tooLarge = false;
        for (int i = 0; i < k; ++i) if (mask >> i & 1ULL) {
            ll g = std::gcd(lcm, b[i]);
            // 一旦 lcm>n，本子集贡献为 0；先除后比较同时避免 lcm 乘法溢出。
            if (lcm > n / (b[i] / g)) { tooLarge = true; break; }
            lcm *= b[i] / g;
        }
        if (tooLarge) continue;
        if (__builtin_popcountll(mask) & 1) ans += n / lcm;
        else ans -= n / lcm;
    }
    return ans;
}
```

**5. 要改哪里**

若要统计闭区间 [L,R]，先计算不超过 R 的计数减去不超过 L-1 的计数，注意 L 的范围及减法溢出。若条件数较大，子集枚举不可行，应利用数论结构或改用其他算法。负除数不在输入约定内；先取绝对值时还要处理最小有符号整数的溢出风险。

**6. 自检**

`n=20`、除数 2 和 3 的答案为 13；除数集合含 2、4、0、2 时，清理后只剩 2，`n=10` 答案为 5。`n=0` 返回 0；空除数集合也应返回 0。

**7. 坑**

1. 容斥符号统一相加：子集大小奇数加、偶数减。
2. 直接相乘求 lcm：先约 gcd 并检查是否超过 n，避免溢出。
3. 忘记冗余项：正确性仍可成立，但会扩大指数枚举规模。
4. 有效条件数达到 64：左移掩码不再满足实现前提，且复杂度早已不可接受。

**8. 一句话原理**

把多个整除集合的并集按子集交集逐项加减，交集由所选除数的 lcm 描述。

**参考：**

- [OI Wiki：容斥原理](https://oi-wiki.org/math/combinatorics/inclusion-exclusion-principle/)

## 7.11 矩阵快速幂

**1. 它是做什么的**

`Matrix` 支持固定模数下的矩阵乘法，`matPow` 对方阵计算非负整数次幂。维度 d 的方阵幂时间 $O(d^3\log e)$，结果及中间矩阵空间 $O(d^2)$；每次乘法为 $O(r*c*k)$，其中维度为 r×k 与 k×c。适合小维线性递推和状态转移。模数须为正，矩阵乘法要求内维匹配且模数一致；幂指数非负，零次幂返回单位矩阵。写入矩阵的元素应先规范到 `[0,mod)`，否则 C++ 负余数可能产生负代表。

**2. 变量在做什么**

| 成员/变量 | 含义 |
|---|---|
| `rows,cols` | 行数和列数；元素下标从 0 开始。 |
| `mod` | 矩阵使用的正模数。 |
| `a[i][j]` | 第 i 行第 j 列元素，构造时为 0。 |
| `x,y` | 矩阵乘法左右操作数；要求 `x.cols==y.rows` 且模数相同。 |
| `ans` | 幂运算累积矩阵，初始为单位阵。 |
| `e` | 尚未处理的指数位，每轮右移。 |

**3. 函数在做什么**

| 接口 | 参数、返回与副作用 |
|---|---|
| `Matrix(r,c,mod)` | 要求非负维度、正模数；建立零矩阵。 |
| `Matrix::identity(n,mod)` | 返回 n 阶单位矩阵；不改外部状态。 |
| `operator*(x,y)` | 返回新乘积，不修改输入；需维度及模数匹配，代码未做运行时检查。 |
| `matPow(base,e)` | 按值接收矩阵并返回幂；要求方阵和 `e>=0`，不改调用者的矩阵。 |

**4. 怎么调用**

创建 2×2 Fibonacci 转移矩阵并计算五次幂，检查关键元素与零次幂单位阵：

```text
Matrix a(2, 2, 1000);
a.a[0][0] = 1; a.a[0][1] = 1;
a.a[1][0] = 1; a.a[1][1] = 0;
Matrix p = matPow(a, 5);
assert(p.a[0][0] == 8 && p.a[0][1] == 5);
Matrix id = matPow(a, 0);
assert(id.a[0][0] == 1 && id.a[0][1] == 0);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Matrix {
    int rows, cols;
    // 本模板所有元素都在同一正模数 mod 下运算；不同矩阵相乘时模数须一致。
    ll mod;
    vector<vector<ll>> a;

    // 参数 r,c>=0、mod>0；构造并拥有 r*c 个零元素。
    Matrix(int r, int c, ll mod) : rows(r), cols(c), mod(mod), a(r, vector<ll>(c)) {}

    // 参数 n>=0、mod>0；返回 n 阶模乘单位阵，不修改外部状态。
    static Matrix identity(int n, ll mod) {
        Matrix id(n, n, mod);
        for (int i = 0; i < n; ++i) id.a[i][i] = 1 % mod;
        return id;
    }
};

// 参数矩阵满足 x.cols==y.rows 且模数相同为正；返回新乘积矩阵，不改 x,y。
Matrix operator*(const Matrix& x, const Matrix& y) {
    // 前提 x.cols==y.rows；i-k-j 顺序可跳过零项，乘积用 __int128 防溢出。
    Matrix z(x.rows, y.cols, x.mod);
    for (int i = 0; i < x.rows; ++i)
        for (int k = 0; k < x.cols; ++k) if (x.a[i][k])
            for (int j = 0; j < y.cols; ++j)
                z.a[i][j] = (z.a[i][j] +
                    (__int128)x.a[i][k] * y.a[k][j]) % x.mod;
    return z;
}

// 参数 base 为正模方阵、e>=0；按值接收底矩阵并返回 base^e，实参不变。
Matrix matPow(Matrix base, long long e) {
    // 要求 base 为方阵、e>=0；列向量转移通常写 state(t)=base^t*state(0)。
    Matrix ans = Matrix::identity(base.rows, base.mod);
    while (e > 0) {
        // 不变量：ans * base^e 等于原矩阵的原指数次幂。
        if (e & 1) ans = ans * base;
        base = base * base;
        e >>= 1;
    }
    return ans;
}
```

**5. 要改哪里**

列向量状态满足 `state(t+1)=A*state(t)` 时使用 `A^t*state(0)`；行向量约定需反转乘法方向。若不需要模运算，应改乘法和数据类型并重新评估溢出；若维数大，稠密 $O(d^3)$ 乘法可能不合适，应利用稀疏结构或其他算法。不同模数的矩阵不能直接相乘。

**6. 自检**

`A^0` 必须为单位阵；`A^1=A`。对 Fibonacci 矩阵，上例五次幂左上角为 8、右上角为 5；`1×1` 矩阵也应符合普通整数模幂。

**7. 坑**

1. 转移方向不一致：先确定列向量或行向量约定。
2. 忘记维度/模数前提：模板没有断言，应由调用者保证。
3. 对负指数调用：循环不支持矩阵逆。
4. 使用 long long 直接乘矩阵元素：实现已提升乘积至 __int128，但模数和加和仍须满足表示范围。

**8. 一句话原理**

矩阵乘法组合状态转移，二进制快速幂把重复转移压缩为对数次方阵乘法。

**参考：**

- [OI Wiki：矩阵](https://oi-wiki.org/math/linear-algebra/matrix/)

## 7.12 高斯消元

**1. 它是做什么的**

`gauss` 使用部分主元消元求解有限实数系数的线性方程组。输入增广矩阵至少有一行且每行同宽；返回 0 无解、1 唯一解、2 无穷多解。`answer` 在有解时给出一组解，自由变量取 0；无解时不可使用。时间 $O(mn\min(m,n))$，空间 $O(mn)$，包括按值复制的矩阵和辅助标记。固定绝对 `EPS` 适用于尺度适合的数据，病态问题需更稳健的数值算法。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `a[i][j]` | 增广矩阵；最后一列 `a[i][n]` 为常数项。 |
| `m`,`n` | 方程数和未知数数目。 |
| `where[col]` | 列 `col` 主元所在行；-1 表示自由变量。 |
| `row`,`pivot` | 下一主元行和当前列的最大绝对值候选行。 |
| `answer` | 输出解向量；初始化为零，故自由变量取 0。 |
| `EPS` | 固定阈值 1e-12，用于判零及残差检查。 |

**3. 函数在做什么**

`gauss(a,answer)` 要求 `a` 至少有一行且每行 `n+1` 列，返回 0/1/2 状态码。函数按值接收矩阵副本并覆盖 `answer`；无解时 `answer` 不可用。输入矩阵不被调用修改。

**4. 怎么调用**

最后一列放常数项。下面解 x+y=3、x-y=1，另检查矛盾方程：

```text
vector<vector<long double>> a = {{1, 1, 3}, {1, -1, 1}};
vector<long double> answer;
assert(gauss(a, answer) == 1);
assert(fabsl(answer[0] - 2) < 1e-12L);
assert(fabsl(answer[1] - 1) < 1e-12L);
vector<vector<long double>> bad = {{1, 1, 1}, {1, 1, 2}};
assert(gauss(bad, answer) == 0);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

// 0：无解；1：唯一解；2：无穷多解。
// 参数 a 为有限数值且形状 m>0、每行 n+1；覆盖 answer，返回 0无解/1唯一/2多解。无解时 answer 不可用。
int gauss(vector<vector<long double>> a, vector<long double>& answer) {
    // a 是 m 行、n+1 列的增广矩阵；模板要求 m>0 且各行长度一致。
    // EPS 应按输入尺度调整：数值很大或病态矩阵可能需要更稳健的方法。
    const long double EPS = 1e-12L;
    int m = (int)a.size();
    int n = (int)a[0].size() - 1;
    vector<int> where(n, -1);
    // where[col] 是该未知数主元所在行；-1 表示自由变量，最终默认取 0。
    int row = 0;

    for (int col = 0; col < n && row < m; ++col) {
        int pivot = row;
        // 部分主元：选绝对值最大项，减少除以小数造成的误差放大。
        for (int i = row; i < m; ++i)
            if (fabsl(a[i][col]) > fabsl(a[pivot][col])) pivot = i;
        // 整列近似为 0 时不能制造主元，这一列成为自由变量候选。
        if (fabsl(a[pivot][col]) < EPS) continue;
        swap(a[pivot], a[row]);
        where[col] = row;

        long double div = a[row][col];
        for (int j = col; j <= n; ++j) a[row][j] /= div;
        // 消去所有其他行，直接得到简化行阶梯形；只消下方则需额外回代。
        for (int i = 0; i < m; ++i) if (i != row) {
            long double factor = a[i][col];
            if (fabsl(factor) < EPS) continue;
            for (int j = col; j <= n; ++j)
                a[i][j] -= factor * a[row][j];
        }
        ++row;
    }

    answer.assign(n, 0);
    for (int col = 0; col < n; ++col)
        if (where[col] != -1) answer[col] = a[where[col]][n];

    for (int i = 0; i < m; ++i) {
        // 用得到的一组解回代等价方程；不满足说明出现 0=非0，即无解。
        long double lhs = 0;
        for (int j = 0; j < n; ++j) lhs += a[i][j] * answer[j];
        if (fabsl(lhs - a[i][n]) > EPS) return 0;
    }
    for (int col = 0; col < n; ++col)
        if (where[col] == -1) return 2;
    return 1;
}
```

**5. 要改哪里**

若需输出所有解的参数表达式，应额外输出自由变量与主元变量的关系；当前接口只给自由变量置零的一组解。模方程组不可直接用浮点消元，应采用模逆元并处理不可逆主元。数值尺度变化时需重新评估 `EPS`，复杂病态问题应换用更稳健的分解算法。

**6. 自检**

x+y=3、x-y=1 唯一解为 (2,1)。x+y=1 与 x+y=2 无解。x+y=2 与 2x+2y=4 有无穷多解，返回的答案仍须代回成立。空矩阵不满足接口前提。

**7. 坑**

1. 无主元列并不代表无解：它是自由变量，仍需检查 0=非0。
2. 忽略返回状态：状态 0 时答案向量不可用。
3. 用精确等于 0 检查浮点数：实现使用绝对 `EPS`，尺度影响判断。
4. 输入行数为 0 或行长度不一致：调用前须保证形状合法。

**8. 一句话原理**

每列选择绝对值最大的可用主元并消去其他行，再把自由变量置零恢复一组解。

**参考：**

- [OI Wiki：高斯消元](https://oi-wiki.org/math/numerical/gauss/)

## 7.13 公平组合游戏与 SG 函数

**1. 它是做什么的**

`SGGame` 用记忆化 `mex` 计算无环公平组合游戏的 Sprague–Grundy 值；对多个彼此独立的子游戏，用 SG 值异或判断先手胜负。规则须为正常玩法，图为 0-based DAG。遍历所有可达状态的总时间为 $O(V+E)$：每条边的后继值标记一次，每个点扫描至多出度加一的 `mex` 候选。图和 `memo` 空间 $O(V+E)$，递归栈最坏 $O(V)$。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `nextState[u]` | 从状态 `u` 一步可达的后继状态编号。 |
| `memo[u]` | -1 表示未计算，否则存储 SG(`u`)。 |
| `values` | 后继状态的 SG 值，可包含重复。 |
| `seen` | 标记 `mex` 候选值是否出现，长度为后继数加一。 |
| `total` | 独立起始局面的 SG 值异或。 |

终局没有后继，`mex` 空集为 0；DAG 是递归终止条件。

**3. 函数在做什么**

| 接口 | 参数、返回、副作用 |
|---|---|
| `SGGame(graph)` | 按值接收 0-based DAG 邻接表并移入对象，初始化 `memo`；边端点必须合法。 |
| `sg(u)` | 要求合法状态且图无环；返回 SG 值并递归填充 `memo`。 |
| `firstPlayerWins(game,starts)` | `starts` 中状态合法且子游戏独立；返回 SG 异或是否非零，并修改 `game.memo`。 |

**4. 怎么调用**

将每种局面作为状态、合法操作作为有向边。2 是终局，0 可到 1、2：

```text
SGGame game({{1, 2}, {2}, {}});
assert(game.sg(2) == 0);
assert(game.sg(1) == 1);
assert(game.sg(0) == 2);
assert(firstPlayerWins(game, vector<int>{0}));
assert(!firstPlayerWins(game, vector<int>{2}));
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;

struct SGGame {
    // nextState[u] 列出局面 u 一步可达的所有局面；状态图必须是 DAG。
    vector<vector<int>> nextState;
    // memo[u]=-1 表示尚未计算，否则保存 SG(u)，使每个状态只展开一次。
    vector<int> memo;

    // 参数 graph 是 0-based DAG 邻接表；移动其内容初始化游戏和 -1 memo。
    explicit SGGame(vector<vector<int>> graph)
        : nextState(std::move(graph)), memo(nextState.size(), -1) {}

    // 参数 u 是合法状态编号；返回 SG(u)，并递归填充本对象 memo，要求图无环。
    int sg(int u) {
        if (memo[u] != -1) return memo[u];
        vector<int> values;
        values.reserve(nextState[u].size());
        for (int v : nextState[u]) values.push_back(sg(v));

        // k 个后继的 mex 至多为 k，因此只需标记 [0,k]，更大的 SG 值可忽略。
        vector<bool> seen(values.size() + 1, false);
        for (int x : values)
            if (x < (int)seen.size()) seen[x] = true;
        int mex = 0;
        while (mex < (int)seen.size() && seen[mex]) ++mex;
        return memo[u] = mex;
    }
};

// 参数 starts 是合法且互相独立的起始状态；返回 SG 异或非零，并通过 game 填充共享 memo。
bool firstPlayerWins(SGGame& game, const vector<int>& starts) {
    // starts 表示彼此独立的子游戏；普通玩法下异或和非 0 当且仅当先手必胜。
    int total = 0;
    for (int s : starts) total ^= game.sg(s);
    return total != 0;
}
```

**5. 要改哪里**

多个独立棋堆可把各自初始状态放进 `starts`；有相互作用时应构造一个联合局面，而非分开异或。若状态图含环、玩法含随机步骤，或无合法操作者获胜，需按对应博弈模型重新分析，当前 SG 递归不能直接使用。

**6. 自检**

终局值为 0；只有一个终局后继的状态值为 1；后继值集合 {0,1} 的 `mex` 为 2。两个相同 SG 值的独立子游戏异或为 0，先手不胜；空起始列表也返回 false。

**7. 坑**

1. 有环图递归：可能无限递归，先证明状态图无环。
2. 把多个子游戏的 SG 值相加：组合规则是异或。
3. 把 SG=0 当先手必胜：正常玩法下它表示后手胜。
4. 子游戏不独立仍异或：独立性是定理的前提。

**8. 一句话原理**

单个局面取后继 SG 值的 `mex`，独立局面组合取 SG 值的异或。

**参考：**

- [OI Wiki：公平组合游戏](https://oi-wiki.org/math/game-theory/impartial-game/)

## 7.14 质因数分解、约数个数与约数和

**1. 它是做什么的**

该节提供质因数分解、约数个数/约数和及正约数枚举，要求正整数 `n`，统计结果和中间幂能由 long long 表示。质因数分解最坏时间 $O(\sqrt n)$，额外空间为不同质因子数；约数统计在分解后再逐项累加等比级数，时间仍由试除主导、额外空间 $O(\omega(n))$。枚举约数扫描至平方根并排序，时间 $O(\sqrt n+d\log d)$、空间 $O(d)$，`d` 为约数数目。`n=1` 时分别返回空分解、{1,1} 统计、{1} 列表。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `f` | 升序质因子与指数对 (`p`,`e`)。 |
| `p`,`e` | 当前质因子及其在 `n` 中的指数。 |
| `count`,`sum` | 约数个数、约数和，初始乘法单位元均为 1。 |
| `term`,`power` | 当前质因子的等比和 1+`p`+...+`p^e`。 |
| `d`,`i` | 枚举列表及试除因子；`i` 和 `n/i` 成对。 |

试除循环用 `i<=n/i` 避免 `i`*`i` 溢出；若 `i` 是平方根，配对值相同，只加入一次。

**3. 函数在做什么**

| 函数 | 参数、返回与副作用 |
|---|---|
| `factorize(n)` | 要求 `n>=1`；返回升序 {`p`,`e`} 向量，`n=1` 返回空，不改外部状态。 |
| `divisorCountSum(n)` | 要求 `n>=1` 且结果及中间幂可放入 long long；返回 {约数个数,约数和}。 |
| `enumerateDivisors(n)` | 要求 `n>=1`；返回升序约数，1 返回 {1}。 |

**4. 怎么调用**

以 `n=1`2 为例，约数个数为 6、约数和为 28：

```text
auto stats = divisorCountSum(12);
assert(stats.first == 6 && stats.second == 28);
assert((enumerateDivisors(12) == vector<long long>{1,2,3,4,6,12}));
auto one = divisorCountSum(1);
assert(one.first == 1 && one.second == 1);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 参数 n>=1；返回按质因子升序的 {p,e}，1 返回空向量，不改外部状态。
vector<pair<ll,int>> factorize(ll n) {
    // 试除到 p*p>n；剩余 n>1 必为大质因子。
    vector<pair<ll, int>> f;
    for (ll p = 2; p <= n / p; ++p) {
        if (n % p != 0) continue;
        int e=0;
        do {
            n/=p;
            ++e;
        }
        while (n % p == 0);
        f.push_back({p,e});
    }
    if(n>1)f.push_back({n,1});
    return f;
}
// 参数 n>=1 且约数个数、约数和及中间幂可放进 ll；返回 {个数,总和}。
pair<ll,ll> divisorCountSum(ll n) {
    // 假设结果可放入 ll
    ll count = 1, sum = 1;
    for (auto [p, e] : factorize(n)) {
        ll term = 1, power = 1;
        for (int i = 0; i < e; ++i) {
            power *= p;
            term += power;
        }
        count*=e+1;
        sum*=term;
    }
    return {count,sum};
}
// 参数 n>=1；返回全部正约数升序列表，1 返回 {1}，不修改输入。
vector<ll> enumerateDivisors(ll n) {
    vector<ll>d;
    for (ll i = 1; i <= n / i; ++i) {
        if (n % i != 0) continue;
        d.push_back(i);
        if(i!=n/i)d.push_back(n/i);
    }
    sort(d.begin(),d.end());
    return d;
}
```

**5. 要改哪里**

需要模约数和/个数时，应在每个乘法和等比项累积处及时取模，并确保除法步骤仍然成立。大量有界整数查询可使用最小质因子筛；任意 64 位大数分解可改 Pollard–Rho。若结果可能超出 long long，需换大整数，不能只提升最后一次乘法。

**6. 自检**

`n=1` 的统计应为 (1,1)，约数列表为 {1}；`n=1`2 的约数依次为 1、2、3、4、6、12，和为 28。`n`=36 的平方根 6 只出现一次，列表无重复；各质因子指数的 (`e`+1) 乘积等于枚举结果个数。

**7. 坑**

1. 使用 `p`*`p`<=`n`：平方可能溢出，写 `p`<=`n`/`p`。
2. 平方数重复插入根：仅当 `i`!=`n/i` 时加入配对约数。
3. 忽略结果溢出：输入可表示并不代表约数和或中间幂也能表示。
4. 输入 `n`=0：0 有无限多个正约数，接口仅定义于 `n>=1`。

**8. 一句话原理**

由质因数指数分解的乘法结构，分别计算约数数量、几何级数和，或组合出所有约数。
