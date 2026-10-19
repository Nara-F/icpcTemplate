
# 9. 计算几何

本章要求浮点输入为有限值，并采用两套明确的数值约定：含交点、距离、投影时使用 `long double` 和绝对误差 `EPS = 1e-12L`；坐标尺度变化明显时应按题目精度调整 EPS，或采用相对误差。整数输入只判断方向、求凸包或平方距离时，输入用 `long long`、运算前提升到 `__int128`；坐标差、乘积、叉积、面积和平方距离的中间量都必须落在 signed `__int128` 范围内，否则需增加坐标限制或使用大整数。浮点数不能直接用于有序容器的“近似相等”比较。

## 9.1 点、向量与基本运算

**1. 它是做什么的**

本节用 `Point` 表示二维实数坐标点，也将其当作向量；提供加减、缩放、点积、叉积、长度与逆时针旋转。各运算为 $O(1)$。浮点类型为 `long double`，判号 `sgn` 使用绝对 `EPS=1e-12`；坐标尺度过大时此容差可能不合适。除法标量须非零，`rotate` 的角度单位为弧度。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `x`,`y` | `Point` 的横纵坐标；向量按同一坐标差解释。 |
| `EPS` | 绝对误差判零阈值。 |
| `PI` | 由反余弦计算出的圆周率常量。 |
| `a`,`b` | 点积/叉积中的向量；`cross(a,b)>0` 表示 b 位于 a 的逆时针侧。 |
| `angle` | 旋转弧度，正值为逆时针。 |

**3. 函数在做什么**

`Point` 的 +、-、*、/ 运算符返回新对象，不改操作数；除法要求除数非零。`dot` 返回点积，`cross` 返回有向面积标量，`norm2` 返回平方长度，`length` 返回非负长度，`rotate` 返回旋转后的新向量。`sgn(x)` 返回 -1/0/1，按绝对 `EPS` 判定。

**4. 怎么调用**

用两个向量验证点积、叉积和 90 度旋转：

```text
Point a{1, 0}, b{0, 1};
assert(dot(a, b) == 0);
assert(sgn(cross(a, b)) == 1);
Point r = rotate(a, PI / 2);
assert(fabsl(r.x) < 1e-12L && fabsl(r.y - 1) < 1e-12L);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ld = long double;

const ld EPS = 1e-12L;
const ld PI = acosl(-1.0L);

// 这是绝对误差判号；若坐标尺度极大，应按题目误差要求调整 EPS 或改用相对误差。
// 参数 x 为 long double；按绝对 EPS 返回 -1/0/1，不修改全局容差。
int sgn(ld x) {
    if (x > EPS) return 1;
    if (x < -EPS) return -1;
    return 0;
}

struct Point {
    // 浮点点也作为向量使用；b-a 表示从 a 指向 b，坐标下标不涉及点编号。
    ld x = 0, y = 0;
    // 参数 p 是另一向量；返回逐坐标相加的新点，不改两操作数。
    Point operator+(const Point& p) const { return {x + p.x, y + p.y}; }
    // 参数 p 是被减向量；返回 this-p 的新向量，不改两操作数。
    Point operator-(const Point& p) const { return {x - p.x, y - p.y}; }
    // 参数 k 为实数缩放因子；返回缩放后的新向量，不改 this。
    Point operator*(ld k) const { return {x * k, y * k}; }
    // 参数 k 必须非零；返回逐坐标除以 k 的新向量，不改 this。
    Point operator/(ld k) const { return {x / k, y / k}; }
};

// 参数 a,b 为向量；返回点积标量，不修改输入。
ld dot(Point a, Point b) { return a.x * b.x + a.y * b.y; }
// cross(a,b)>0 表示从向量 a 逆时针转到 b；绝对值是平行四边形面积。
// 参数 a,b 为向量；返回有向叉积标量，不修改输入。
ld cross(Point a, Point b) { return a.x * b.y - a.y * b.x; }
// 参数 a 为向量；返回平方长度，不开方且不修改输入。
ld norm2(Point a) { return dot(a, a); }
// 参数 a 为向量；返回非负欧氏长度，不修改输入。
ld length(Point a) { return sqrtl(norm2(a)); }

// 参数 a 为向量、angle 为弧度；返回逆时针旋转后的新向量，不改输入。
Point rotate(Point a, ld angle) {
    // angle 使用弧度，正值按数学坐标系逆时针旋转；屏幕 y 轴向下时视觉方向相反。
    ld c = cosl(angle), s = sinl(angle);
    return {a.x * c - a.y * s, a.x * s + a.y * c};
}
```

**5. 要改哪里**

角度制输入先乘 `PI`/180 转成弧度。若坐标尺度变化显著，应重新设计 `EPS` 或使用相对误差判定；不可仅把阈值机械调小。若参与除法的量可能为零，调用前处理退化情况。整数精确判向可使用 9.2 的整点叉积模板。

**6. 自检**

(1,0) 点乘 (0,1) 为 0，叉积为 1；旋转 (1,0) 逆时针 π/2 后近似为 (0,1)。零向量的长度为 0；对任意向量 v，`norm2`(v) 应非负。

**7. 坑**

1. 把角度制直接传入 `rotate`：接口用弧度。
2. 浮点值直接与 0 比较：使用 `sgn` 或明确误差界。
3. 零向量参与除法：先检查长度或除数。
4. 坐标很大仍使用固定绝对 `EPS`：误差尺度不匹配，需调整模型。

**8. 一句话原理**

把点的坐标差当作向量，用点积、叉积和三角函数表达二维几何关系。

**参考：**

- [OI Wiki：二维计算几何基础](https://oi-wiki.org/geometry/2d/)

## 9.2 叉积与方向判断

**1. 它是做什么的**

整点模板用叉积精确判断左转、右转、共线及点是否落在闭线段上。单次操作 $O(1)$。点坐标是 `long long`，三点叉积先提升到 signed __int128 再相减；坐标差和最终叉积仍须能由 signed __int128 表示。`onSegment` 包含端点。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `IPoint` 的 `x`,`y` | 整数点坐标，不代表数组下标。 |
| `a`,`b` | `cross` 的向量，或三点重载中的起点和第二点。 |
| `c` | 三点叉积中的第三点，计算 `(b-a)x(c-a)`。 |
| `p` | 待测点。 |
| `value` | 有向叉积；正左转、负右转、零共线。 |

**3. 函数在做什么**

`cross(a,b)` 返回两个整数向量叉积；`cross(a,b,c)` 返回 `(b-a)x(c-a)`，两者均返回 `i128`。`orientation` 将符号映射为 1/0/-1。`onSegment(a,b,p)` 仅在共线且 `p` 落在两坐标轴包围盒内时返回 true，端点包含；均不修改输入。

**4. 怎么调用**

以水平线段及其两侧点检查方向和闭区间端点：

```text
IPoint a{0, 0}, b{4, 0}, p{2, 0}, above{2, 1};
assert(orientation(a, b, above) == 1);
assert(onSegment(a, b, p));
assert(onSegment(a, b, a));
assert(!onSegment(a, b, above));
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using i128 = __int128_t;

struct IPoint {
    ll x = 0, y = 0;
};

// 两向量叉积；整数坐标下精确判号，乘法提升到 i128 以避免 long long 溢出。
// 参数 a,b 为整数向量；返回叉积，结果须可由 signed i128 表示。
i128 cross(IPoint a, IPoint b) {
    return (i128)a.x * b.y - (i128)a.y * b.x;
}

// 参数 a,b,c 为整数点；返回 (b-a)x(c-a)，精确结果须在 signed i128 范围内。
i128 cross(IPoint a, IPoint b, IPoint c) {
    // 返回 (b-a)x(c-a)：正为 a->b 到 a->c 左转，负为右转，零为共线。
    i128 abx = (i128)b.x - a.x, aby = (i128)b.y - a.y;
    i128 acx = (i128)c.x - a.x, acy = (i128)c.y - a.y;
    return abx * acy - aby * acx;
}

// 参数为三点；返回左转 1、共线 0、右转 -1，不修改输入。
int orientation(IPoint a, IPoint b, IPoint c) {
    i128 value = cross(a, b, c);
    return (value > 0) - (value < 0);
}

// 参数 a,b 定义闭线段、p 为查询点；共线且在包围盒内（含端点）时返回 true。
bool onSegment(IPoint a, IPoint b, IPoint p) {
    // 闭线段判定：共线还不够，还要落在两端点的横纵坐标包围盒内；端点算在线。
    return orientation(a, b, p) == 0 &&
           min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x) &&
           min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y);
}
```

**5. 要改哪里**

浮点坐标需采用 EPS 判号与范围判断，不能直接把浮点值传入整数模板。若要判断线段相交，可由方向值和 `onSegment` 组合；若要计算交点坐标，则使用直线/线段交点算法。坐标范围接近 `long long` 极限时，差值和叉积可能超出 `i128`，应改用更宽/大整数。

**6. 自检**

`a`=(0,0), `b`=(4,0) 时 above=(2,1) 左转为 1，below=(2,-1) 右转为 -1，共线点 (2,0) 在闭段上，端点也在线段上；共线点 (5,0) 不在线段上。

**7. 坑**

1. 将共线误认为在线段上：还要检查横纵包围盒。
2. 交换 `b`、`c` 后仍期待原符号：交换顺序会改变方向。
3. 在提升前先做坐标减法：要在 signed `i128` 中求差。
4. 认为 `i128` 没有范围限制：极端坐标下叉积仍会溢出。

**8. 一句话原理**

叉积符号给出转向，叉积为零时再用坐标范围检查线段包含。

**参考：**

- [OI Wiki：极坐标与叉积](https://oi-wiki.org/geometry/2d/)

## 9.3 直线交点与线段相交

**1. 它是做什么的**

浮点模板求两条无限直线的唯一交点，并判断两条闭线段是否有公共点；端点接触和共线重叠都算相交。每次操作 $O(1)$。直线方向须非零，交点计算以绝对 `EPS=1e-12` 判断分母；绝对误差适用于尺度合适的数据。`lineIntersection` 对平行或重合返回 false 且不改 `out`。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `p`,`v` | 第一条直线的起点和方向，参数式 `p`+`t`*`v`。 |
| `q`,`w` | 第二条直线的起点和方向，参数式 `q`+s*`w`。 |
| `denominator` | `cross(v,w)`；近零表示平行或重合，无唯一交点。 |
| `t` | 第一条直线交点参数。 |
| `a`,`b`,`c`,`d` | 两条闭线段的端点。 |
| `c1`..`c4` | 各端点相对另一条有向直线的方向符号。 |

**3. 函数在做什么**

`sgn` 按绝对 `EPS` 返回符号；`Point` 的 +、-、* 返回新向量。`cross` 有向量和三点两个重载。`lineIntersection` 要求 `v`、`w` 非零，成功写出 `out` 并返回 true；平行/重合返回 false，`out` 保持原值。`onSegment(a,b,p)` 的参数 `a`、`b` 为线段端点、`p` 为查询点；共线且在包围盒内（含端点）时为 true，退化段按当前容差作点附近判定。`segmentsIntersect` 返回两闭线段是否共享点，含端点及共线重叠；退化线段按当前容差作点附近判定。

**4. 怎么调用**

两条交叉直线交于 (0.5,0.5)，两段端点相接也算相交：

```text
Point out{9, 9};
bool ok = lineIntersection(Point{0,0}, Point{1,1},
                           Point{0,1}, Point{1,-1}, out);
assert(ok && fabsl(out.x - 0.5L) < 1e-12L);
assert(fabsl(out.y - 0.5L) < 1e-12L);
assert(segmentsIntersect(Point{0,0}, Point{1,0},
                         Point{1,0}, Point{2,0}));
assert(segmentsIntersect(Point{0,0}, Point{2,0},
                         Point{1,0}, Point{3,0}));
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ld = long double;
const ld EPS = 1e-12L;

// EPS 是绝对误差阈值；整数输入且只判相交时应改用 i128 叉积以得到精确结果。
// 参数 x 为浮点量；按本节绝对 EPS 返回 -1/0/1。
int sgn(ld x) { return (x > EPS) - (x < -EPS); }

struct Point {
    ld x = 0, y = 0;
    // 参数 p 为向量；返回坐标和的新值，不改操作数。
    Point operator+(Point p) const { return {x + p.x, y + p.y}; }
    // 参数 p 为向量；返回 this-p 的新值，不改操作数。
    Point operator-(Point p) const { return {x - p.x, y - p.y}; }
    // 参数 k 为实数；返回按 k 缩放的新向量，不改 this。
    Point operator*(ld k) const { return {x * k, y * k}; }
};

// 参数 a,b 为向量；返回浮点有向叉积，不修改输入。
ld cross(Point a, Point b) { return a.x * b.y - a.y * b.x; }
// 参数为三点；返回 (b-a)x(c-a)，供方向判定使用。
ld cross(Point a, Point b, Point c) { return cross(b - a, c - a); }

// 参数给出 p+t*v、q+s*w 且方向非零；成功写 out 返回 true，平行/重合返回 false 且 out 不变。
bool lineIntersection(Point p, Point v, Point q, Point w, Point& out) {
    // 两条无限直线分别是 p+t*v、q+s*w；v、w 必须是非零方向向量。
    ld denominator = cross(v, w);
    // 叉积近零包含“平行不重合”和“整条重合”，二者都没有唯一交点。
    if (sgn(denominator) == 0) return false;
    // 由 (q-p)xw=t*(v x w) 解出参数 t；交换叉积顺序会把符号写反。
    ld t = cross(q - p, w) / denominator;
    out = p + v * t;
    return true;
}

// 参数 a,b 定义闭线段，p 为查询点；按绝对 EPS 判断是否在线段上，包含端点，退化段按容差判定点附近。
bool onSegment(Point a, Point b, Point p) {
    // 使用带容差的闭区间判定；a==b 时坐标乘积仍使用 EPS，不能当作精确点相等。
    return sgn(cross(a, b, p)) == 0 &&
           sgn((p.x - a.x) * (p.x - b.x)) <= 0 &&
           sgn((p.y - a.y) * (p.y - b.y)) <= 0;
}

// 参数为两条闭线段端点；返回是否共享一点，端点接触和共线重叠都算相交。
bool segmentsIntersect(Point a, Point b, Point c, Point d) {
    // c1、c2 是 c、d 相对有向直线 a->b 的方向；异号才是严格跨越。
    int c1 = sgn(cross(a, b, c)), c2 = sgn(cross(a, b, d));
    int c3 = sgn(cross(c, d, a)), c4 = sgn(cross(c, d, b));
    if (c1 * c2 < 0 && c3 * c4 < 0) return true;
    return (c1 == 0 && onSegment(a, b, c)) ||
           (c2 == 0 && onSegment(a, b, d)) ||
           (c3 == 0 && onSegment(c, d, a)) ||
           (c4 == 0 && onSegment(c, d, b));
}
```

**5. 要改哪里**

若只判断整数线段相交，改用 9.2 的精确 i128 方向判断。若要区分“严格穿越”与接触/重叠，应在闭段相交结果外单独规定退化与共线规则。坐标尺度变化时调整 `EPS`；需要输出平行重合的关系时，应另增分类结果，当前接口只报告没有唯一交点。

**6. 自检**

两条非平行直线应写出唯一交点；平行和重合直线都返回 false 且 `out` 不变。线段端点接触为 true，共线不重叠为 false。零长度线段仅在它所在点落在另一段上时相交，但不能作为无限直线方向。

**7. 坑**

1. 把 `lineIntersection` 的 false 当成没有公共点：它也可能表示直线重合。
2. 只检查端点异侧：共线端点需额外用 `onSegment` 判断。
3. 忽略端点接触：本函数采用闭线段语义。
4. 用零方向求直线交点：方向非零是前提。

**8. 一句话原理**

叉积符号判断两端相对方向，唯一直线交点则通过解参数方程求出。

**参考：**

- [OI Wiki：直线与线段相关](https://oi-wiki.org/geometry/2d/)

## 9.4 距离与投影

**1. 它是做什么的**

本节计算点到无限直线或闭线段的投影点及距离，单次时间 $O(1)$。坐标采用 `long double`；线段长度平方小于 `EPS*EPS` 时按退化点处理。无限直线接口要求 `a`、`b` 不同，线段接口会把退化段当作点 `a`。`EPS` 为绝对阈值，尺度不合适时要调整。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `p` | 查询点。 |
| `a`,`b` | 直线或线段端点。 |
| `v=b-a` | 方向向量。 |
| `length2` | `v` 的平方长度；小于 `EPS*EPS` 时线段退化。 |
| `t` | 投影参数 `dot(p-a,v)/|v|²`；截到 [0,1] 后对应线段最近点。 |

**3. 函数在做什么**

`dot` 返回点积，`norm2` 返回平方长度，`distance` 返回欧氏距离。`projectionOnLine` 要求 `a!=b`，返回无限直线垂足；`distanceToLine` 返回点到直线距离。`closestPointOnSegment` 对短于 `EPS` 的段返回 `a`，否则将投影参数截到 [0,1]。`distanceToSegment` 返回 `p` 到最近点的距离。

**4. 怎么调用**

`p`=(2,2)，线段端点 (-1,0),(1,0)，无限直线垂足是 (2,0)，线段最近点为 (1,0)：

```text
Point p{2,2}, a{-1,0}, b{1,0};
Point foot = projectionOnLine(p, a, b);
assert(fabsl(foot.x - 2) < 1e-12L && fabsl(foot.y) < 1e-12L);
Point near = closestPointOnSegment(p, a, b);
assert(fabsl(near.x - 1) < 1e-12L && fabsl(near.y) < 1e-12L);
assert(fabsl(distanceToSegment(p, a, b) - sqrtl(5.0L)) < 1e-12L);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ld = long double;
const ld EPS = 1e-12L;

struct Point {
    ld x = 0, y = 0;
    // 参数 p 为向量；返回坐标和的新值，不改操作数。
    Point operator+(Point p) const { return {x + p.x, y + p.y}; }
    // 参数 p 为向量；返回 this-p 的新值，不改操作数。
    Point operator-(Point p) const { return {x - p.x, y - p.y}; }
    // 参数 k 为缩放因子；返回新向量，不改 this。
    Point operator*(ld k) const { return {x * k, y * k}; }
};

// 参数 a,b 为向量；返回点积标量。
ld dot(Point a, Point b) { return a.x * b.x + a.y * b.y; }
// 参数 a 为向量；返回平方长度。
ld norm2(Point a) { return dot(a, a); }
// 参数为两点；返回非负欧氏距离，平方量以 long double 计算。
ld distance(Point a, Point b) { return sqrtl(norm2(a - b)); }

// 参数 p 为查询点、a!=b 定义无限直线；返回垂足，不限制投影参数。
Point projectionOnLine(Point p, Point a, Point b) {
    // 求无限直线参数 t；前提 a!=b，否则 norm2(b-a)=0。线段版本在下方单独处理退化。
    Point v = b - a;
    return a + v * (dot(p - a, v) / norm2(v));
}

// 参数 p 为查询点、a!=b 定义直线；返回到无限直线的非负距离。
ld distanceToLine(Point p, Point a, Point b) {
    return distance(p, projectionOnLine(p, a, b));
}

// 参数 p 为查询点、a,b 为线段端点；返回最近点，EPS² 内退化段返回 a。
Point closestPointOnSegment(Point p, Point a, Point b) {
    Point v = b - a;
    ld length2 = norm2(v);
    // EPS^2 与平方长度同量纲；退化或极短线段按单点 a 处理。
    if (length2 < EPS * EPS) return a;
    ld t = dot(p - a, v) / length2;
    // 无限直线投影参数截到 [0,1]，分别对应端点 a、b 和线段内部。
    t = max((ld)0, min((ld)1, t));
    return a + v * t;
}

// 参数 p 为查询点、a,b 为闭线段端点；返回非负距离，退化段按点 a 计算。
ld distanceToSegment(Point p, Point a, Point b) {
    return distance(p, closestPointOnSegment(p, a, b));
}
```

**5. 要改哪里**

若要最近点在射线而非线段上，将投影参数限制为 `t`>=0；无限直线则不截断。若输入为整数且只比较点到直线距离，可避免开方但仍需设计足够宽的精确类型。短线段的 `EPS*EPS` 规则取决于坐标尺度，应与其他几何判定保持一致。

**6. 自检**

垂足落在线段内部时两种投影一致；垂足在线段外时最近点应为相邻端点。`a`=`b` 时 `closestPointOnSegment` 返回 `a`，`distanceToSegment` 等于点距；`projectionOnLine` 对同样输入不合法。

**7. 坑**

1. 将直线投影误当线段最近点：线段参数必须截在 [0,1]。
2. 直接除以 `norm2(v)`：退化线段会除零，直线接口要求端点不同。
3. 用平方长度与线性 `EPS` 比较：退化阈值要用 `EPS*EPS`。
4. 需要比较距离却反复开方：可比较平方距离，但要确认所有量同尺度。

**8. 一句话原理**

沿方向向量求投影参数，直线保留原参数，线段将其夹到闭区间 [0,1]。

**参考：**

- [OI Wiki：距离](https://oi-wiki.org/geometry/distance/)

## 9.5 多边形面积

**1. 它是做什么的**

`signedDoubleArea` 用鞋带公式计算按边界顺序给出的简单整数多边形有向二倍面积，时间 $O(n)$、额外空间 $O(1)$。输入点坐标为 `long long`；坐标差、单项叉积及总和都必须可由 `signed __int128` 表示。首点无需重复在末尾；空输入、少于三个点或共线退化时返回 0。逆时针结果为正，顺时针为负。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `IPoint` 的 `x`,`y` | 整数顶点坐标。 |
| `polygon` | 按多边形边界顺序排列的顶点；不是无序点集。 |
| `n` | 顶点数。 |
| `i` | 当前边的起点下标。 |
| `(i+1)%n` | 当前边终点；最后一项自动连接回首点。 |
| `sum` | 所有边叉积之和，即有向二倍面积。 |

**3. 函数在做什么**

`signedDoubleArea(polygon)` 返回 `signed __int128`，不修改输入。顶点按边界顺序给出且不重复首点；空输入、少于三个点或共线退化时返回 0。对简单多边形取绝对值再除以 2 得到普通面积；自交顶点列的有向叉积和不代表通常的覆盖面积。

**4. 怎么调用**

单位正方形逆时针的有向二倍面积为 2，反向则为 -2：

```text
vector<IPoint> ccw{{0,0},{1,0},{1,1},{0,1}};
vector<IPoint> cw{{0,1},{1,1},{1,0},{0,0}};
assert(signedDoubleArea(ccw) == 2);
assert(signedDoubleArea(cw) == -2);
assert(signedDoubleArea(vector<IPoint>{}) == 0);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using i128 = __int128_t;

struct IPoint { ll x = 0, y = 0; };

// 单项叉积提升到 i128；若坐标约在 1e18 量级，多个叉积之和仍可能超过 i128。
// 参数 a,b 为整数位置向量；返回叉积，signed i128 须容纳乘积差。
i128 cross(IPoint a, IPoint b) {
    return (i128)a.x * b.y - (i128)a.y * b.x;
}

// 参数为按边界顺序且首点不重复的顶点列；返回有向二倍面积，逆时针为正，不改输入。
i128 signedDoubleArea(const vector<IPoint>& polygon) {
    // 顶点须按边界顺序给出且不重复首点；返回有向二倍面积，逆时针为正。
    i128 sum = 0;
    int n = (int)polygon.size();
    // (i+1)%n 自动补上末点到首点的闭合边；n<3 时自然得到退化面积 0。
    for (int i = 0; i < n; ++i)
        sum += cross(polygon[i], polygon[(i + 1) % n]);
    return sum;
}
```

**5. 要改哪里**

要返回非负面积，可在调用端对结果取绝对值并除以 2；若二倍面积为奇数，真实面积含 .5。输入必须提供真实多边形边界顺序；只有题目要求凸包面积时才先求凸包，不能将一般凹多边形替换成凸包。若坐标范围增大，应重新证明差值、叉积和累加总和均不溢出；提升到 `i128` 并不代表无限精度。

**6. 自检**

逆时针单位正方形返回 2，顺时针返回 -2；少于 3 点和共线顶点序列返回 0。交换顶点遍历方向会改变符号但绝对值不变。

**7. 坑**

1. 忘记结果是二倍面积：最后需除以 2。
2. 输入无序点集：鞋带公式要求沿边界顺序。
3. 漏掉末点到首点边：模板通过取模补齐闭合边。
4. 只提升乘法、不考虑总和：单项及累加值都要可放入 `i128`。

**8. 一句话原理**

沿边界把相邻顶点叉积求和，得到有向二倍面积。

**参考：**

- [OI Wiki：多边形面积](https://oi-wiki.org/geometry/2d/)

## 9.6 点在多边形内

**1. 它是做什么的**

给定按边界顺序排列的简单浮点多边形和查询点，射线奇偶法判断点在外部、边界还是内部。多边形顶点可顺时针或逆时针，首点无需重复；空顶点列返回 `OUTSIDE`。单次时间 $O(n)$，除输入外额外空间 $O(1)$。自交多边形不适用。代码使用绝对 `EPS=1e-12`，坐标尺度很大或很小时可能需要调整；退化的 1、2 点顶点列不代表通常的简单多边形，应按题意自行定义语义。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `Point{x,y}` | 长双精度坐标点；减法返回向量差。 |
| `polygon[i]` | 边界顺序第 `i` 个顶点，向量下标为 0-based。 |
| `a`, `b` | 当前边的起点及下一顶点；最后一点连接回第 0 点。 |
| `p` | 查询点。 |
| `cross(a,b)` | 两向量有向叉积，符号表示相对方向。 |
| `inside` | 射线与边界交点数的奇偶状态；跨过一个右侧交点就翻转。 |
| `EPS` | 绝对容差，`sgn` 将 `[-EPS,EPS]` 视为 0。 |

函数先用 `onSegment` 判断边界，再用半开高度条件检查边是否跨过点的水平射线，避免顶点重复计数。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `sgn(x)` | 返回 `-1/0/1`，按绝对 `EPS` 判断符号。 |
| `Point::operator-(p)` | 返回当前点减 `p` 的向量，不改操作数。 |
| `cross(a,b)` | 返回两个向量的有向叉积标量。 |
| `onSegment(a,b,p)` | 若 `p` 按当前 EPS 判断在线段闭区间上则返回 `true`，含端点；不修改输入。 |
| `pointInPolygon(polygon,p)` | 参数为简单多边形顶点列和查询点；返回 `OUTSIDE`、`BOUNDARY` 或 `INSIDE`，不修改输入。 |

**4. 怎么调用**

按顺序提供多边形顶点，调用后根据枚举值分支。正方形示例验证内部、边界、外部和空多边形：

```text
vector<Point> square = {{0, 0}, {2, 0}, {2, 2}, {0, 2}};
assert(pointInPolygon(square, {1, 1}) == INSIDE);
assert(pointInPolygon(square, {2, 1}) == BOUNDARY);
assert(pointInPolygon(square, {3, 1}) == OUTSIDE);
assert(pointInPolygon({}, {0, 0}) == OUTSIDE);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ld = long double;
const ld EPS = 1e-12L;

// 参数 x 为浮点量；按本节绝对 EPS 返回 -1/0/1。
int sgn(ld x) { return (x > EPS) - (x < -EPS); }
struct Point {
    ld x = 0, y = 0;
    // 参数 p 为向量；返回 this-p 的新值，不改操作数。
    Point operator-(Point p) const { return {x - p.x, y - p.y}; }
};
// 参数 a,b 为向量；返回有向叉积标量。
ld cross(Point a, Point b) { return a.x * b.y - a.y * b.x; }

// 参数 a,b 定义闭边、p 为点；共线且落在包围盒内（含端点）时返回 true。
bool onSegment(Point a, Point b, Point p) {
    // 边界优先单独判定，避免射线与水平边或顶点重合时归属不明确。
    return sgn(cross(b - a, p - a)) == 0 &&
           sgn((p.x - a.x) * (p.x - b.x)) <= 0 &&
           sgn((p.y - a.y) * (p.y - b.y)) <= 0;
}

enum PointLocation { OUTSIDE, BOUNDARY, INSIDE };

// 参数是按边界顺序的简单多边形和查询点；返回 OUTSIDE/BOUNDARY/INSIDE，不修改输入。
PointLocation pointInPolygon(const vector<Point>& polygon, Point p) {
    // 适用于顶点按边界排列的简单多边形；返回值明确区分边界与内部。
    bool inside = false;
    int n = (int)polygon.size();
    for (int i = 0; i < n; ++i) {
        Point a = polygon[i], b = polygon[(i + 1) % n];
        if (onSegment(a, b, p)) return BOUNDARY;
        // 半开高度条件保证射线经过顶点时只让相邻两边中的一条计数。
        bool straddles = (a.y > p.y) != (b.y > p.y);
        if (straddles) {
            ld intersectionX = a.x + (b.x - a.x) *
                (p.y - a.y) / (b.y - a.y);
            // 只统计查询点右侧交点；每跨过一次边界就翻转内外奇偶性。
            if (intersectionX > p.x + EPS) inside = !inside;
        }
    }
    return inside ? INSIDE : OUTSIDE;
}
```

**5. 要改哪里**

- 若需整数坐标精确判定，应将叉积及方向运算改为足够宽的整数类型，并在减法前扩宽；`__int128` 也有取值范围。
- 若输入是自交多边形，必须先定义奇偶规则或非零绕数规则，再选对应算法；当前接口假设简单多边形。
- 若坐标范围变化明显，需重新评估 `EPS` 对叉积、坐标乘积和交点比较的影响；该实现使用统一绝对阈值，不具尺度不变性。

**6. 自检**

正方形 `[0,2]×[0,2]` 中 `(1,1)` 为内部，边 `(2,0)-(2,2)` 上的 `(2,1)` 为边界，`(3,1)` 在外部。空点列返回外部。再检查水平边上的点和顶点本身均返回边界；顶点附近相差小于 EPS 的点可能受容差影响，坐标尺度需与 EPS 匹配。

**7. 坑**

- 射线过顶点时奇偶翻转两次：使用半开高度条件，不能简单判断两端是否跨过。
- 边界点被判内或外：先调用 `onSegment` 并单独返回 `BOUNDARY`。
- 浮点几何在不同尺度下误判：固定绝对 EPS 不随坐标缩放，按输入尺度调整并测试近边界点。
- 用于自交轮廓：内部定义不唯一或规则不同，需换成题目要求的判定方法。

**8. 一句话原理**

先识别边界，再数查询点向右射线与简单多边形的交点奇偶性。

**参考：**

- [OI Wiki：判断一个点是否在多边形内部](https://oi-wiki.org/geometry/2d/)

## 9.7 凸包

**1. 它是做什么的**

Andrew 单调链从无序整数点集中构造凸包，返回按逆时针排列且不重复首点的顶点；本实现删除边上中间的共线点。重复输入点可有；空集返回空，单点保留，全共线时只返回两个端点。排序需 $O(n\log n)$，扫描为 $O(n)$，总时间 $O(n\log n)$；按值接收输入并建立凸包，空间 $O(n)$。坐标差和叉积都必须能由 signed `__int128` 表示；提升到 `__int128` 能避免 `long long` 减法先溢出，但乘积及其差仍有有限范围。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `IPoint{x,y}` | 64 位整数点；按 `x` 再按 `y` 字典序排序，坐标相等视为同一点。 |
| `points` | 函数的输入副本；先排序，再去重。 |
| `hull` | 当前构造的下凸壳和上凸壳拼接序列。 |
| `lowerSize` | 下凸壳完成后的长度，作为逆序扫描上凸壳的边界。 |
| `cross(a,b,c)` | `(b-a)×(c-a)`；正值左转，零共线，负值右转。 |

返回 vector 是 0-based；首点为字典序最小点，不再在末尾重复首点。判断转向前坐标先扩宽到 `i128`，但若输入极值使叉积超出 signed `__int128` 仍会溢出。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `IPoint::operator<(p)` | 按 `x`、`y` 字典序比较，用于排序。 |
| `IPoint::operator==(p)` | 两坐标完全相等时返回 `true`，供 `unique` 去重。 |
| `cross(a,b,c)` | 返回有向叉积；坐标差、乘积及最终差均须处于 signed `__int128` 范围。 |
| `convexHull(points)` | 按值接收任意顺序整数点（可重复）；返回逆时针凸包，不修改调用者向量。边界共线中间点会删除。 |

**4. 怎么调用**

提供点集并调用即可。正方形去重后仍按逆时针返回四角；共线点集只保留极端两点：

```text
vector<IPoint> points = {{1, 1}, {0, 0}, {1, 0}, {0, 1}, {1, 1}};
vector<IPoint> hull = convexHull(points);
assert(hull == vector<IPoint>({{0, 0}, {1, 0}, {1, 1}, {0, 1}}));
vector<IPoint> line = convexHull({{0, 0}, {1, 1}, {2, 2}, {1, 1}});
assert(line == vector<IPoint>({{0, 0}, {2, 2}}));
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using i128 = __int128_t;

struct IPoint {
    ll x = 0, y = 0;
    // 参数 p 为另一整数点；按 x 再 y 严格字典序比较，用于排序，不改点。
    bool operator<(const IPoint& p) const { return tie(x, y) < tie(p.x, p.y); }
    // 参数 p 为另一整数点；仅两坐标完全相等时返回 true。
    bool operator==(const IPoint& p) const { return x == p.x && y == p.y; }
};

// 参数为整数点；返回 (b-a)x(c-a)，坐标差和乘积差须在 signed i128 范围。
i128 cross(IPoint a, IPoint b, IPoint c) {
    // (b-a)x(c-a)>0 是严格左转；整数 i128 判号不需要 EPS。
    i128 abx = (i128)b.x - a.x, aby = (i128)b.y - a.y;
    i128 acx = (i128)c.x - a.x, acy = (i128)c.y - a.y;
    return abx * acy - aby * acx;
}

// 参数 points 按值接收，可乱序/重复；返回逆时针凸包且不重复首点，删去边上中间共线点。
vector<IPoint> convexHull(vector<IPoint> points) {
    // 输入可无序且可重复；输出 0-based vector 中按逆时针排列，不重复首点。
    sort(points.begin(), points.end());
    points.erase(unique(points.begin(), points.end()), points.end());
    if (points.size() <= 1) return points;

    vector<IPoint> hull;
    for (const IPoint& p : points) {
        // 维护下凸壳连续三点严格左转；<=0 会同时删除右转和边上共线中间点。
        // 若题目要求保留边界共线点，改为 <0，并额外处理全部共线的输入。
        while (hull.size() >= 2 &&
               cross(hull[hull.size() - 2], hull.back(), p) <= 0)
            hull.pop_back();
        hull.push_back(p);
    }
    size_t lowerSize = hull.size();
    // 逆序扫描构造上凸壳；lowerSize 是边界，防止弹掉已完成的整条下凸壳。
    for (int i = (int)points.size() - 2; i >= 0; --i) {
        const IPoint& p = points[i];
        while (hull.size() > lowerSize &&
               cross(hull[hull.size() - 2], hull.back(), p) <= 0)
            hull.pop_back();
        hull.push_back(p);
    }
    // 最后压入的是起点副本，删除它以保持“首点不重复”的返回约定。
    hull.pop_back();
    return hull;
}
```

**5. 要改哪里**

- 若要保留凸包边上的所有共线点，可将弹栈条件 `<= 0` 改为 `< 0`，并单独处理全部共线输入，避免重复端点。
- 若坐标范围可能超过 `long long` 差值或 `__int128` 叉积范围，需更宽的精确表示或限制输入范围；不能只因用了 `i128` 就视为无限安全。
- 若需要顺时针输出，可在得到凸包后反转非首点部分，保持起点约定。
- 若要算面积或周长，可在返回点列上循环 `(i+1)%hull.size()`；空集和单点要单独处理。

**6. 自检**

示例正方形应得到 `(0,0),(1,0),(1,1),(0,1)`，首点不重复；重复输入点不改变结果。全共线的 `(0,0),(1,1),(2,2)` 应只返回两端点；单点返回自身，空集返回空。对凸包相邻三点检查叉积应为正；输入有极大坐标时先核对差值与乘积范围。

**7. 坑**

- 同一点重复进入链：先按字典序排序并去重。
- 共线点保留策略不符：`<=0` 删除中间共线点，改 `<0` 会改变输出且须处理全共线情况。
- 把末点重复首点当作结果：模板已删除重复首点，遍历闭合边时使用 `(i+1)%n`。
- 叉积溢出：减法前转 `i128`，同时保证乘积和最终减法仍在其范围内。

**8. 一句话原理**

按字典序分别扫描下、上链，遇到非左转就回退，保留包住全部点的最外层转折点。

**参考：**

- [OI Wiki：凸包](https://oi-wiki.org/geometry/convex-hull/)

## 9.8 旋转卡壳：凸包直径

**1. 它是做什么的**

给定按逆时针排列、无重复首点的严格凸包，旋转卡壳求最远点对的欧氏距离平方。输入点型为 `IPoint`，坐标为 `long long`；叉积、绝对值和平方距离均须在 signed `__int128` 范围内。若凸包有 0 或 1 个点返回 0，2 点返回唯一平方距离；其余情况时间 $O(h)$，额外空间 $O(1)$，其中 `h` 为凸包顶点数。若先从 `n` 个原始点构造凸包，总时间为 $O(n\log n)$。不直接接受未排序原始点或含边上共线中间点的轮廓。组合使用 9.7 时，应共用或合并 `IPoint`、`cross` 等公共定义，不能原样拼接两份含同名定义的完整代码块。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `IPoint{x,y}` | 整数坐标点；沿用凸包章节的点字段。 |
| `hull` | 逆时针严格凸包，首点不重复；内部下标 0-based。 |
| `i`, `nextI` | 当前凸包边的起点和下一个顶点，`nextI=(i+1)%n`。 |
| `j` | 与当前边对应的对踵点指针，只沿凸包前进。 |
| `cross` | 边到候选点的有向面积；凸包方向已知，代码取绝对值比较面积。 |
| `answer` | 已检查点对的最大平方距离，类型为 `i128`。 |

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `cross(a,b,c)` | 返回 `(b-a)×(c-a)`；差值、乘积和最终减法均须适配 signed `i128`。 |
| `distanceSquared(a,b)` | 返回两点欧氏距离平方；坐标差及平方和须适配 signed `i128`。 |
| `abs128(x)` | 返回 `|x|`；输入不能是 signed `i128` 最小值。 |
| `convexDiameterSquared(hull)` | 输入严格逆时针凸包且首点不重复；返回最大距离平方，0/1 点为 0、2 点直接计算。 |
| `toString(x)` | 将非负 `i128` 转成十进制字符串；负数不受支持。 |

**4. 怎么调用**

传入严格凸包；若已有原始点，先用 9.7 的 Andrew 凸包算法处理。下例矩形对角线平方为 `4²+3²=25`，两点退化输入也直接返回平方距离：

```text
vector<IPoint> hull = {{0, 0}, {4, 0}, {4, 3}, {0, 3}};
i128 d2 = convexDiameterSquared(hull);
assert(d2 == 25 && toString(d2) == "25");
assert(convexDiameterSquared({{0, 0}, {3, 4}}) == 25);
assert(convexDiameterSquared({{7, 9}}) == 0);
assert(convexDiameterSquared({}) == 0);
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using i128 = __int128_t;

struct IPoint {
    ll x = 0, y = 0;
};

// 参数为整数点；返回有向叉积，调用者保证差值和乘积在 signed i128 范围。
i128 cross(IPoint a, IPoint b, IPoint c) {
    i128 abx = (i128)b.x - a.x, aby = (i128)b.y - a.y;
    i128 acx = (i128)c.x - a.x, acy = (i128)c.y - a.y;
    return abx * acy - aby * acx;
}

// 参数为两整数点；返回平方距离，坐标差、平方和须可由 signed i128 表示。
i128 distanceSquared(IPoint a, IPoint b) {
    // 差值和平方均在 i128 中完成；返回平方距离，避免开方误差。
    i128 dx = (i128)a.x - b.x;
    i128 dy = (i128)a.y - b.y;
    return dx * dx + dy * dy;
}

// 参数 x 不得是 signed i128 最小值；返回 |x|，不修改外部状态。
i128 abs128(i128 x) { return x < 0 ? -x : x; }

// 参数是逆时针且不重复首点凸包；返回最远平方距离，0/1 点为 0、2 点为点距。
i128 convexDiameterSquared(const vector<IPoint>& hull) {
    // 前提：hull 是逆时针严格凸包且不重复首点；可直接接 convexHull 的输出。
    int n = (int)hull.size();
    if (n <= 1) return 0;
    if (n == 2) return distanceSquared(hull[0], hull[1]);

    i128 answer = 0;
    int j = 1;
    for (int i = 0; i < n; ++i) {
        int nextI = (i + 1) % n;
        // 固定有向边 i->nextI，面积随对踵点前进先增后减，因此 j 全程只向前转。
        // 使用严格 > 可停在面积平台任一端；随后同时检查边的两个端点与 j。
        while (abs128(cross(hull[i], hull[nextI], hull[(j + 1) % n])) >
               abs128(cross(hull[i], hull[nextI], hull[j]))) {
            j = (j + 1) % n;
        }
        answer = max(answer, distanceSquared(hull[i], hull[j]));
        answer = max(answer, distanceSquared(hull[nextI], hull[j]));
    }
    return answer;
}

// 参数 x>=0；返回十进制字符串，仅转换非负距离值，不修改输入。
string toString(i128 x) {
    // 本章仅用它输出非负平方距离；若复用于有向面积，需先处理负号和最小值。
    if (x == 0) return "0";
    string s;
    while (x > 0) {
        s.push_back(char('0' + x % 10));
        x /= 10;
    }
    reverse(s.begin(), s.end());
    return s;
}
```

**5. 要改哪里**

- 若要返回最远点对，在每次更新 `answer` 时同步保存对应下标；返回点坐标时再映回 `hull`。
- 若要输出实际距离，可将非负平方值转为 `long double` 后开方；若输出整数平方距离，使用 `toString`，不能直接用 `cout` 输出 `i128`。
- 若输入点集未经凸包处理，先求凸包；若凸包保留大量共线边界点，先按本算法前提规整或改写指针逻辑。
- 坐标极大时需证明坐标差、叉积、绝对值和平方和都未超出 `i128`，不能只检查最终答案。

**6. 自检**

矩形的最远点是对角顶点，平方距离应为 25。两点 `(0,0),(3,4)` 返回 25；单点和空凸包返回 0。对正方形应得到边长平方的两倍；输入应为逆时针且不重复首点。叉积平台出现时，代码以严格 `>` 停在平台端点，再检查当前边两端与该对踵点。

**7. 坑**

- 直接把无序点集传入：指针单调性依赖凸包按逆时针顺序排列。
- 首点重复或边上保留大量共线点：不符合严格凸包前提，可能破坏指针前进规则。
- 输出整数平方值乱码或编译失败：标准流不直接格式化 `__int128`，使用 `toString`。
- 认为 `i128` 不会溢出：乘法与平方和仍有有限范围；绝对值也不能对最小值取负。

**8. 一句话原理**

沿凸包边旋转并单调移动对踵点，只检查相邻边端与对踵点构成的候选直径。

**参考：**

- [OI Wiki：旋转卡壳](https://oi-wiki.org/geometry/rotating-calipers/)

## 9.9 圆与直线、圆与圆

**1. 它是做什么的**

本节提供无限直线与圆、两圆交点计算，坐标和半径为 `long double`，采用绝对 `EPS=1e-12`。每次计算时间 $O(1)$，返回至多两个 `Point`，结果容器空间 $O(1)$。直线由点 `p` 和方向向量 `v` 表示，要求 `dot(v,v)>EPS`；近零方向返回空。圆半径须非负。两圆圆心距离 `d<=EPS` 时（包括重合圆有无穷交点的情形）返回空；相切返回一个点，分离或包含而不相切返回空。浮点误差与坐标尺度有关，阈值需结合输入调整。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `Circle{o,r}` | 圆心 `o` 和非负半径 `r`。 |
| `p`, `v` | 直线上一点及非零方向向量；`v` 不要求单位化。 |
| `vv` | `dot(v,v)`，方向向量长度平方。 |
| `foot` | 圆心在直线上的垂足。 |
| `h2` | 从垂足到交点的偏移距离平方；小于 `-EPS` 判无交，接近 0 判切点。 |
| `dvec`, `d` | 两圆心的位移向量和距离。 |
| `base`, `perp`, `off` | 两交点弦中点、单位垂直方向及偏移向量。 |
| `EPS` | 绝对误差阈值；代码将长度平方、平方距离差等量也与同一个 EPS 比较。 |

依赖第 9.1 节的 `Point`、`dot`、`length`、`EPS` 和 `Point` 的加减、数乘操作。直线偏移按 `v * sqrt(h2/dot(v,v))` 计算，因此方向向量长度不限。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `lineCircleIntersections(p,v,c)` | 返回无限直线与圆的 0、1 或 2 个交点；近零方向向量返回空。要求圆半径非负，依赖第 9.1 节几何定义。 |
| `circleIntersections(a,b)` | 返回两圆的 0、1 或 2 个交点；半径须非负。圆心近同（`d<=EPS`）时一律返回空，包括重合圆。 |

相切时两个接口都只返回一个点；返回点顺序按各自计算方向，不应依赖顺序代表特定语义。

**4. 怎么调用**

先提供第 9.1 节的几何基础定义，再调用函数。浮点结果用误差比较；下例直线与单位圆相交于 `(-1,0),(1,0)`，两个单位圆相切于 `(1,0)`：

```text
// near(a,b) 比较两个 long double 的绝对误差是否小于 1e-10，不修改状态。
auto near = [](long double a, long double b) { return fabsl(a - b) < 1e-10L; };
Circle unit{{0, 0}, 1};
auto lineHits = lineCircleIntersections({-2, 0}, {1, 0}, unit);
assert(lineHits.size() == 2);
assert(near(lineHits[0].x, -1) && near(lineHits[1].x, 1));
auto circleHits = circleIntersections(unit, Circle{{2, 0}, 1});
assert(circleHits.size() == 1 && near(circleHits[0].x, 1));
assert(lineCircleIntersections({0, 0}, {0, 0}, unit).empty());
```

模板如下：

```cpp
struct Circle {
    Point o;
    long double r;
};
// 参数 p,v 定义直线且 dot(v,v)>EPS，圆半径非负；返回 0/1/2 交点，近零方向返回空。
vector<Point> lineCircleIntersections(Point p,Point v,Circle c) {
    long double vv=dot(v,v);
    if (vv <= EPS) return {};
    Point foot=p+v*(dot(c.o-p,v)/vv);
    long double h2=c.r*c.r-dot(foot-c.o,foot-c.o);
    if (h2 < -EPS) return {};
    if (h2 <= EPS) return {foot};
    Point off=v*(sqrtl(max((long double)0,h2)/vv));
    return {foot-off,foot+off};
}
// 参数是半径非负的两圆；返回 0/1/2 交点，`d<=EPS` 的近同心情形（含重合圆）返回空，切点只返一次。
vector<Point> circleIntersections(Circle a,Circle b) {
    // 先判相离、包含、同心等退化，再计算垂足与偏移。
    Point dvec=b.o-a.o;
    long double d=length(dvec);
    if(d<=EPS) {
        return {};
    }
    // 同心：无交点或无穷多交点，均返回空
    if (d > a.r + b.r + EPS || d < fabsl(a.r - b.r) - EPS) return {};
    long double x = (a.r * a.r - b.r * b.r + d * d) / (2 * d);
    long double h2 = a.r * a.r - x * x;
    Point base = a.o + dvec * (x / d);
    if (h2 <= EPS) return {base};
    Point perp{-dvec.y / d, dvec.x / d};
    Point off = perp * sqrtl(max((long double) 0, h2));
    return {base - off, base + off};
}
```

**5. 要改哪里**

- 若输入的是线段而非无限直线，需在求交后检查交点参数是否落在线段参数区间；当前函数不限制直线参数。
- 若同心且重合圆需表示“无限多个交点”，应换用能区分有限点集和重合状态的返回类型；当前统一返回空。
- 若要处理半径为负的输入，应在调用前拒绝或规范化；模板要求非负半径。
- 若要求更强数值稳定性或坐标尺度跨度大，应改用尺度相关容差/稳健几何判定，并重新审查每个平方量的阈值。

**6. 自检**

直线 `y=0` 与单位圆的交点横坐标应为 `-1`、`1`。单位圆心距 2 时相切并只返回一点；圆心距大于半径和时无交点，小于半径差且不同心时一圆包含另一圆、返回空。零方向向量返回空；同心相等圆因有无穷多个交点也按接口约定返回空。

**7. 坑**

- 把零方向向量当成直线：`dot(v,v)<=EPS` 时接口返回空。
- 把直线结果当线段结果：当前没有限制交点参数范围。
- 重合圆返回空却当作无交点：它表示近同心情形统一空，不区分无交与无限交。
- 直接比较浮点坐标或根号内负值：应按 EPS 分类；根号前代码将近零负值截到 0。
- EPS 对不同量纲一概使用：当前实现对长度平方等量也使用绝对 EPS，坐标尺度可能改变判定效果。

**8. 一句话原理**

先投影求垂足或两圆弦中点，再根据剩余平方距离决定无交、相切或两个对称交点。

## 9.10 整数几何方向模板

**1. 它是做什么的**

模板用整数精确判断三点方向、叉积符号，以及点是否落在包含端点的闭线段上。点坐标为 `long long`，中间差值和叉积使用 signed `__int128`；乘积和最终相减仍须在其范围内。三项操作时间均为 $O(1)$，额外空间 $O(1)$，不使用浮点 EPS。距离平方不是本模板接口，另行计算时也必须检查平方和范围。

**2. 变量在做什么**

| 名称 | 含义 |
|---|---|
| `IPoint{x,y}` | 整数坐标点，字段为 `long long`。 |
| `a,b,c` | 方向判断所用三点；`crossInt(a,b,c)` 计算 `(b-a)×(c-a)`。 |
| `p,a,b` | 线段判定中的查询点和两个端点。 |
| `abx,aby,acx,acy` | 先扩宽到 `__int128` 后再做坐标差，避免 `long long` 减法溢出。 |
| 叉积符号 | 正值表示 `a->b` 转向 `a->c` 为逆时针，负值为顺时针，0 为共线。 |

线段判定先要求叉积为 0，再检查两个坐标都落在端点闭区间内。若 `a==b`，只有 `p==a` 时返回真。

**3. 函数在做什么**

| 函数 | 契约 |
|---|---|
| `crossInt(a,b,c)` | 返回三点有向叉积；坐标差、乘积和相减结果必须适配 signed `__int128`。 |
| `signInt(x)` | 对 signed `__int128` 返回 `-1`、`0` 或 `1`，不修改输入。 |
| `onSegmentInt(p,a,b)` | 若 `p` 在线段 `ab` 的闭区间上返回 `true`，包括端点；叉积不得溢出。 |

**4. 怎么调用**

整数坐标直接传入，不需 EPS。下例中 `c` 在 `a->b` 左侧，`p` 在水平线段上，而更外侧点不在线段内：

```text
IPoint a{0, 0}, b{4, 0}, c{1, 1}, p{2, 0};
assert(signInt(crossInt(a, b, c)) == 1);
assert(onSegmentInt(p, a, b));
assert(!onSegmentInt({5, 0}, a, b));
assert(onSegmentInt({2, 2}, {2, 2}, {2, 2}));
```

模板如下：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct IPoint {
    ll x,y;
};
// 参数为整数点；返回 (b-a)x(c-a)，坐标差和叉积须在 signed i128 范围。
__int128 crossInt(IPoint a, IPoint b, IPoint c) {
    // 转换发生在减法之前，避免 long long 坐标差先溢出。
    __int128 abx = (__int128)b.x - a.x, aby = (__int128)b.y - a.y;
    __int128 acx = (__int128)c.x - a.x, acy = (__int128)c.y - a.y;
    return abx * acy - aby * acx;
}
// 参数 x 为 signed i128；返回 -1/0/1，不修改输入。
int signInt(__int128 x) {
    return (x>0)-(x<0);
}
// 参数 p 为查询点、a,b 为线段端点；闭线段含端点判定，crossInt 不得溢出。
bool onSegmentInt(IPoint p,IPoint a,IPoint b) {
    return crossInt(a, b, p) == 0
        && min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x)
        && min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y);
}
```

**5. 要改哪里**

- 要判断严格位于线段内部，可在 `onSegmentInt` 的共线和包围盒条件外再排除 `p==a`、`p==b`。
- 要计算距离平方，应先把坐标转为 `__int128` 再相减、平方；平方和可能超出 signed `__int128`，需按坐标范围另作保证。
- 要判断线段相交，可组合四次方向符号判断，并单独处理共线重叠；本模板没有直接提供相交接口。
- 需要非整数交点时，交点坐标可能是分数，应改用有理数或浮点表示，不能强行存入 `IPoint`。

**6. 自检**

`(0,0)->(4,0)` 与 `(1,1)` 的叉积为 4，符号为正；`(2,0)` 在线段上，`(5,0)` 共线但在端点范围外。退化线段 `(2,2)-(2,2)` 只包含同一点。坐标取极端 `long long` 时，减法扩宽仍不代表叉积乘积一定安全。

**7. 坑**

- 先用 `long long` 相减再转换：溢出已发生；必须像模板一样在减法前扩宽。
- 只检查共线不检查范围：会把整条直线上的点都判在线段上。
- 对整数几何套 EPS：整数叉积可直接比较 0，不需要浮点容差。
- 将 `__int128` 当无限精度或直接流输出：它有范围，输出时需自行转换成十进制字符串。

**8. 一句话原理**

用精确叉积判断共线和转向，再用坐标闭区间检查确认点落在线段范围内。
