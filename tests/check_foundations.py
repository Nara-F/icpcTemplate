#!/usr/bin/env python3
"""Compile every C++17 fenced example in chapters 01–04 independently."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = [
    ROOT / "content/chapters/01-contest-practice.md",
    ROOT / "content/chapters/02-cpp-stl.md",
    ROOT / "content/chapters/03-basic-search.md",
    ROOT / "content/chapters/04-dynamic-programming.md",
]


def compile_cpp(compiler: str, source_text: str, directory: Path, name: str) -> Path:
    source = directory / f"{name}.cpp"
    executable = directory / name
    source.write_text(source_text + "\n", encoding="utf-8")
    result = subprocess.run(
        [compiler, "-std=c++17", "-O0", str(source), "-o", str(executable)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"could not compile smoke fixture {name}:\n{result.stderr}")
    return executable



def local_tools() -> dict[str, str]:
    """Extract the exact scripts printed in chapter 1, including the A+B adapter."""
    chapter = CHAPTERS[0].read_text(encoding="utf-8")
    result = {}
    for number, name in [(4, 'run.py'), (6, 'gen.py'), (8, 'check.py'),
                         (14, 'cph.py'), (15, 'a_gen.py'), (16, 'auto.py')]:
        section = re.split(rf'^## 1\.{number} ', chapter, flags=re.M)[1]
        section = re.split(r'^## ', section, maxsplit=1, flags=re.M)[0]
        result[name] = re.findall(r'```python\s*\n(.*?)\n```', section, re.DOTALL)[0]
    return result


def smoke_local_runner(compiler: str, temp: Path) -> None:
    """Check A+B workflow, stale binary rejection, RE/TLE stages and saved bytes."""
    folder = temp / 'local runner with spaces'
    folder.mkdir()
    for name, code in local_tools().items():
        (folder / name).write_text(code, encoding='utf-8')
    fixture = '#include <iostream>\nint main(){long long a,b;std::cin>>a>>b;std::cout<<a+b;}\n'
    (folder / 'a.cpp').write_text(fixture)
    (folder / 'a_bf.cpp').write_text(fixture)
    (folder / 'correct.py').write_text('a,b=map(int,input().split());print(a+b)\n')
    (folder / 'wrong.py').write_text('a,b=map(int,input().split());print(a-b)\n')
    (folder / 'exit.py').write_text('raise SystemExit(7)\n')
    (folder / 'slow.py').write_text('import time;time.sleep(3)\n')
    samples = folder / 'samples-A'
    samples.mkdir()
    (samples / '1.in').write_text('3 5\n')
    (samples / '1.ans').write_text('8\n')
    cases = [
        (['run.py', 'a'], '8', 0),
        (['run.py', 'correct.py'], '8', 0),
        (['cph.py', 'a.cpp'], 'AC', 0),
        (['cph.py', 'wrong.py', 'samples-A'], 'WA', 1),
        (['cph.py', 'exit.py', 'samples-A'], 'RE (7)', 1),
        (['cph.py', 'slow.py', 'samples-A'], 'TLE', 1),
        (['cph.py', 'a.cpp', 'missing'], 'no .in', 1),
        (['check.py', 'a.cpp', 'a_bf.cpp', 'a_gen.py', '3'], 'AC 3', 0),
        (['check.py', 'wrong.py', 'correct.py', 'a_gen.py'], 'solution: WA', 1),
        (['check.py', 'correct.py', 'exit.py', 'a_gen.py'], 'brute: RE (7)', 1),
        (['check.py', 'correct.py', 'correct.py', 'exit.py'], 'generator: RE (7)', 1),
        (['check.py', 'exit.py', 'correct.py', 'a_gen.py'], 'solution: RE (7)', 1),
        (['check.py', 'slow.py', 'correct.py', 'a_gen.py'], 'solution: TLE', 1),
        (['check.py', 'correct.py', 'correct.py', 'a_gen.py', '0'], 'positive', 1),
    ]
    for args, expected, status in cases:
        proc = subprocess.run([sys.executable, *args], cwd=folder, input='3 5\n',
                              text=True, capture_output=True, timeout=30)
        assert proc.returncode == status, (args, proc.stdout, proc.stderr)
        assert expected in proc.stdout + proc.stderr, (args, proc.stdout, proc.stderr)
        if expected == 'solution: WA':
            a, b = map(int, (folder / 'fail.in').read_text().split())
            assert (folder / 'fail.ans').read_text().split() == [str(a + b)]
            assert (folder / 'fail.out').read_text().split() == [str(a - b)]
            assert 'seed=1' in (folder / 'fail.txt').read_text()
    # An old valid executable must not be run after a failed compilation.
    (folder / 'a.cpp').write_text('invalid C++')
    proc = subprocess.run([sys.executable, 'run.py', 'a.cpp'], cwd=folder,
                          input='3 5\n', text=True, capture_output=True, timeout=30)
    assert proc.returncode != 0 and '8' not in proc.stdout
    (samples / '1.ans').unlink()
    proc = subprocess.run([sys.executable, 'cph.py', 'correct.py', 'samples-A'],
                          cwd=folder, text=True, capture_output=True, timeout=5)
    assert proc.returncode != 0
    print('Local tools: A+B, C++/Python, samples, stress, CE, RE, TLE, WA and failure files passed.')


def smoke_auto_runner(compiler: str, temp: Path) -> None:
    """Check built-in structures, exact printed counterexample, custom gen and stage failures."""
    folder = temp / 'auto workflow'
    folder.mkdir()
    for name, code in local_tools().items():
        (folder / name).write_text(code, encoding='utf-8')
    fixture = '#include <iostream>\nint main(){long long a,b;std::cin>>a>>b;std::cout<<a+b;}\n'
    (folder / 'a.cpp').write_text(fixture)
    (folder / 'a_bf.cpp').write_text(fixture)
    (folder / 'correct.py').write_text('a,b=map(int,input().split());print(a+b)\n')
    (folder / 'wrong.py').write_text('a,b=map(int,input().split());print(a-b)\n')
    (folder / 'tokens.py').write_text('import sys;print(sum(map(int,sys.stdin.read().split())))\n')
    (folder / 'echo.py').write_text('import sys;sys.stdout.write(sys.stdin.read())\n')
    (folder / 'exit.py').write_text('raise SystemExit(7)\n')
    (folder / 'slow.py').write_text('import time;time.sleep(1)\n')
    (folder / 'custom.cpp').write_text('#include <iostream>\nint main(){std::cout<<"3 5";}\n')

    def invoke(args, status, needle):
        proc = subprocess.run([sys.executable, 'auto.py', *args], cwd=folder,
                              capture_output=True, text=True, timeout=30)
        assert proc.returncode == status, (args, proc.stdout, proc.stderr)
        assert needle in proc.stdout + proc.stderr, (args, proc.stdout, proc.stderr)
        return proc.stdout

    invoke(['a.cpp', 'a_bf.cpp', '--kind', 'ab', '--rounds', '3'], 0, 'PASS: 3')
    assert not (folder / 'auto-fail').exists()
    output = invoke(['wrong.py', 'correct.py', '--kind', 'ab', '--seed', '42',
                     '--rounds', '1'], 1, 'solution WA')
    # Verify the full example printed in the board, including input and both answers.
    for text in ('case=1 seed=42:', '--- INPUT ---\n-72 4\n',
                 '--- EXPECTED (brute) ---\n-68\n', '--- ACTUAL (solution) ---\n-76\n'):
        assert text in output, output
    failure = folder / 'auto-fail'
    assert (failure / 'case.in').read_text().split() == ['-72', '4']
    assert (failure / 'case.ans').read_text().split() == ['-68']
    assert (failure / 'case.out').read_text().split() == ['-76']
    assert 'seed=42' in (failure / 'case.txt').read_text()
    # The saved error group is directly usable as a CPH sample after fixing the program.
    result = subprocess.run([sys.executable, 'cph.py', 'correct.py', 'auto-fail'], cwd=folder,
                            capture_output=True, text=True, timeout=5)
    assert result.returncode == 0 and 'AC' in result.stdout
    for kind in ('array', 'permutation', 'matrix', 'tree', 'chain', 'star',
                 'weighted-tree', 'graph', 'connected', 'directed', 'dag', 'string'):
        invoke(['echo.py', 'echo.py', '--kind', kind, '--rounds', '2'], 0, 'PASS: 2')
    invoke(['correct.py', 'correct.py', '--gen', 'a_gen.py', '--rounds', '2'], 0, 'PASS: 2')
    invoke(['correct.py', 'correct.py', '--gen', 'custom.cpp', '--rounds', '2'], 0, 'PASS: 2')
    for source, brute, extra, needle in [
        ('correct.py', 'correct.py', ['--gen', 'exit.py'], 'generator RE (7)'),
        ('correct.py', 'exit.py', [], 'brute RE (7)'),
        ('exit.py', 'correct.py', [], 'solution RE (7)'),
        ('slow.py', 'correct.py', ['--timeout', '0.2'], 'solution TLE'),
    ]:
        invoke([source, brute, '--kind', 'ab', '--rounds', '1', *extra], 1, needle)
        assert needle.split()[0] in (failure / 'case.txt').read_text()
    invoke(['wrong.py', 'correct.py', '--kind', 'ab', '--rounds', '1',
            '--output', 'other failure'], 1, 'Saved:')
    assert (folder / 'other failure' / 'case.in').is_file()
    invoke(['correct.py', 'correct.py', '--rounds', '0'], 2, 'positive')
    print('Auto workflow: C++/Python, all built-in structures, custom gen, printed/saved WA, CPH replay and RE/TLE stages passed.')


def smoke_debug_and_cpp_random(compiler: str, temp: Path) -> None:
    """Check the actual printed container logger and C++ seeded generator."""
    chapter = CHAPTERS[0].read_text(encoding="utf-8")
    for number in (5, 6):
        section = re.split(rf'^## 1\.{number} ', chapter, flags=re.M)[1]
        section = re.split(r'^## ', section, maxsplit=1, flags=re.M)[0]
        code = re.findall(r'```cpp\s*\n(.*?)\n```', section, re.DOTALL)[0]
        if number == 5:
            for enabled in (False, True):
                prefix = '#define DEBUG\n' if enabled else ''
                exe = compile_cpp(compiler, prefix + code, temp, f'logger-{enabled}')
                result = subprocess.run([str(exe)], capture_output=True, text=True, check=True)
                assert result.stdout == ''
                if enabled:
                    assert '[3, 1, 2]' in result.stderr and '[(1,2), (1,3)]' in result.stderr
                else:
                    assert result.stderr == ''
        else:
            exe = compile_cpp(compiler, code, temp, 'cpp-generator')
            first = subprocess.run([str(exe), '42'], capture_output=True, text=True, check=True)
            second = subprocess.run([str(exe), '42'], capture_output=True, text=True, check=True)
            assert first.stdout == second.stdout and 'seed = 42' in first.stderr
            values = list(map(int, first.stdout.split()))
            assert sorted(values[1:]) == list(range(1, values[0] + 1))
    print('C++ debug containers and seeded random generator passed.')


def smoke_generators() -> None:
    """Check structure invariants over seeds and exact generator CLI formats."""
    namespace = {'__name__': 'generator_test'}
    exec(compile(local_tools()['gen.py'], 'chapter-01-gen.py', 'exec'), namespace)
    Generator = namespace['Generator']
    for seed in range(40):
        g = Generator(seed)
        for n in (1, 2, 12):
            a = g.array(n, -5, 5)
            assert len(a) == n and all(-5 <= x <= 5 for x in a)
            assert len(set(g.array(n, 1, n, distinct=True))) == n
            assert sorted(g.permutation(n)) == list(range(1, n + 1))
            assert set(g.text(n, 'abc')) <= set('abc')
            matrix = g.matrix(n, 3, -2, 2)
            assert len(matrix) == n and all(len(row) == 3 for row in matrix)
            assert all(-2 <= x <= 2 for row in matrix for x in row)
            assert len({id(row) for row in matrix}) == n
            for shape in ('random', 'chain', 'star'):
                edges = g.tree(n, shape)
                assert len(edges) == n - 1
                degrees = [0] * (n + 1)
                parent = list(range(n + 1))
                for u, v in edges:
                    assert 1 <= u < v <= n
                    degrees[u] += 1
                    degrees[v] += 1
                    ru, rv = u, v
                    while parent[ru] != ru:
                        ru = parent[ru]
                    while parent[rv] != rv:
                        rv = parent[rv]
                    assert ru != rv
                    parent[ru] = rv
                if shape == 'chain':
                    assert max(degrees) <= 2
                if shape == 'star':
                    assert max(degrees) == n - 1
            for directed, dag in ((False, False), (True, False), (True, True)):
                maximum = n * (n - 1) // (1 if directed and not dag else 2)
                for m in sorted({0, maximum // 2, maximum}):
                    edges = g.graph(n, m, directed=directed, dag=dag)
                    assert len(edges) == len(set(edges)) == m
                    assert all(1 <= u <= n and 1 <= v <= n and u != v for u, v in edges)
                    if not directed:
                        assert all(u < v for u, v in edges)
                    if dag:
                        indegree = [0] * (n + 1)
                        for u, v in edges:
                            indegree[v] += 1
                        queue = [u for u in range(1, n + 1) if indegree[u] == 0]
                        for u in queue:
                            for x, v in edges:
                                if x == u:
                                    indegree[v] -= 1
                                    if indegree[v] == 0:
                                        queue.append(v)
                        assert len(queue) == n
            for m in sorted({n - 1, n * (n - 1) // 2}):
                edges = g.graph(n, m, connected=True)
                assert len(edges) == len(set(edges)) == m
                seen = {1}
                for _ in range(n):
                    for u, v in edges:
                        if u in seen or v in seen:
                            seen.update((u, v))
                assert len(seen) == n
            weighted = g.weighted(g.tree(n), -5, 0)
            assert len(weighted) == n - 1 and all(-5 <= w <= 0 for _, _, w in weighted)
        assert Generator(seed).tree(12) == Generator(seed).tree(12)
        assert Generator(seed).graph(8, 12, dag=True, directed=True) == Generator(seed).graph(8, 12, dag=True, directed=True)
    g = Generator(1)
    assert g.array(0, 1, 1) == [] and g.permutation(0) == [] and g.text(0) == ''
    for method, args, kwargs in [
        ('array', (2, 1, 1), {'distinct': True}), ('array', (-1, 1, 2), {}),
        ('matrix', (1, -1, 0, 1), {}), ('tree', (0,), {}),
        ('tree', (3, 'bad'), {}), ('text', (2, ''), {}),
        ('graph', (3, 4), {}), ('graph', (3, 1), {'connected': True}),
        ('graph', (3, 2), {'dag': True}),
        ('graph', (3, 2), {'connected': True, 'directed': True}),
    ]:
        try:
            getattr(g, method)(*args, **kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError((method, args, kwargs))
    with tempfile.TemporaryDirectory(prefix='icpcboard-gen-') as name:
        script = Path(name) / 'gen.py'
        script.write_text(local_tools()['gen.py'])
        for kind in ('array', 'permutation', 'string', 'matrix', 'tree', 'chain',
                     'star', 'weighted-tree', 'graph', 'connected', 'directed', 'dag', 'ab'):
            cmd = [sys.executable, str(script), '42', kind]
            first = subprocess.check_output(cmd, text=True)
            assert first == subprocess.check_output(cmd, text=True)
            lines = first.splitlines()
            header = list(map(int, lines[0].split()))
            if kind == 'ab':
                assert len(header) == 2 and len(lines) == 1
                continue
            n = header[0]
            assert 1 <= n <= 12
            if kind in ('array', 'permutation', 'string'):
                assert len(lines) == 2
                assert (len(lines[1]) if kind == 'string' else len(lines[1].split())) == n
            elif kind == 'matrix':
                assert len(lines) == n + 1
                assert all(len(row.split()) == header[1] for row in lines[1:])
            else:
                count = n - 1 if kind in ('tree', 'chain', 'star', 'weighted-tree') else header[1]
                assert len(lines) == count + 1
                assert all(len(row.split()) == (3 if kind == 'weighted-tree' else 2)
                           for row in lines[1:])
    print('Generators: arrays, permutations, strings, matrices, trees, graphs, DAGs, weights, seeds and invalid inputs passed.')


def smoke_constructive_example(compiler: str, temp: Path) -> None:
    chapter = (ROOT / "content/chapters/03-basic-search.md").read_text(encoding="utf-8")
    section = chapter.split("## 3.13 常用构造题思路", 1)[1]
    blocks = re.findall(r"```cpp\s*\n(.*?)\n```", section, re.DOTALL)
    if not blocks:
        raise RuntimeError("chapter 3.13 has no runnable construction example")
    executable = compile_cpp(compiler, blocks[0], temp, "constructive-example")
    result = subprocess.run([str(executable)], capture_output=True, text=True, timeout=5)
    if result.returncode != 0:
        raise RuntimeError(f"constructive example assertions failed: {result.stderr}")
    print("Construction example exhaustive assertions passed.")


def smoke_sliding_window_edges(compiler: str, temp: Path) -> None:
    chapter = (ROOT / "content/chapters/03-basic-search.md").read_text(encoding="utf-8")
    section = chapter.split("## 3.4 双指针与滑动窗口", 1)[1].split("## 3.5", 1)[0]
    blocks = re.findall(r"```cpp\s*\n(.*?)\n```", section, re.DOTALL)
    if not blocks:
        raise RuntimeError("chapter 3.4 has no runnable sliding-window example")
    checks = r'''
int main() {
    assert(minLengthAtLeast({}, 0) == 0);
    assert(minLengthAtLeast({1, 2}, 0) == 1);
    assert(minLengthAtLeast({1, 2, 3}, 4) == 2);
    assert(minLengthAtLeast({1, 2}, 5) == 0);
}
'''
    executable = compile_cpp(compiler, blocks[0] + checks, temp, "sliding-window-edges")
    result = subprocess.run([str(executable)], capture_output=True, text=True, timeout=5)
    if result.returncode != 0:
        raise RuntimeError(f"sliding-window edge assertions failed: {result.stderr}")
    print("Sliding-window edge assertions passed.")


def main() -> int:
    compiler = shutil.which("g++")
    if compiler is None:
        print("g++ is required for the C++17 snippet check", file=sys.stderr)
        return 2

    failures: list[str] = []
    total = 0
    with tempfile.TemporaryDirectory(prefix="icpcboard-foundations-") as temp_name:
        temp = Path(temp_name)
        for chapter in CHAPTERS:
            text = chapter.read_text(encoding="utf-8")
            blocks = re.findall(r"```cpp\s*\n(.*?)\n```", text, re.DOTALL)
            chapter_passes = 0
            for index, code in enumerate(blocks, start=1):
                source = temp / f"{chapter.stem}-{index}.cpp"
                source.write_text(code + "\n", encoding="utf-8")
                result = subprocess.run(
                    [compiler, "-std=c++17", "-fsyntax-only", str(source)],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                total += 1
                if result.returncode == 0:
                    chapter_passes += 1
                else:
                    failures.append(
                        f"{chapter.relative_to(ROOT)} block {index}:\n"
                        f"{result.stderr.strip()}"
                    )
            print(f"{chapter.relative_to(ROOT)}: {chapter_passes}/{len(blocks)} passed")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"All {total} C++17 snippets passed syntax checks.")
    try:
        with tempfile.TemporaryDirectory(prefix="icpcboard-smoke-") as smoke_name:
            smoke_temp = Path(smoke_name)
            smoke_local_runner(compiler, smoke_temp)
            smoke_auto_runner(compiler, smoke_temp)
            smoke_generators()
            smoke_debug_and_cpp_random(compiler, smoke_temp)
            smoke_constructive_example(compiler, smoke_temp)
            smoke_sliding_window_edges(compiler, smoke_temp)
    except Exception as error:
        print(f"Foundation smoke check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
