import sys
from collections import defaultdict, deque


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(set)
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)

    virus = 'a'
    result = []

    def bfs(start):
        q = deque([(start, [])])
        visited = {start}
        paths = []
        min_len = None

        while q:
            node, path = q.popleft()
            for nxt in sorted(graph[node]):
                if nxt in visited:
                    continue
                visited.add(nxt)
                new_path = path + [nxt]
                if nxt.isupper():
                    if min_len is None or len(new_path) < min_len:
                        min_len = len(new_path)
                        paths = [new_path]
                    elif len(new_path) == min_len:
                        paths.append(new_path)
                else:
                    q.append((nxt, new_path))
        if not paths:
            return None
        paths.sort(key=lambda p: (p[-1], p))
        return paths[0]

    while True:
        path = bfs(virus)
        if not path:
            break

        gate = path[-1]
        node = path[-2] if len(path) > 1 else virus

        result.append(f"{gate}-{node}")

        graph[gate].discard(node)
        graph[node].discard(gate)

        # вирус двигается к шлюзу, если ещё не рядом
        if len(path) > 1:
            virus = path[0]
        else:
            break

        # если нет доступных шлюзов — конец
        if not any(x.isupper() for k in graph for x in graph[k]):
            break

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        a, _, b = line.partition('-')
        edges.append((a, b))

    for res in solve(edges):
        print(res)


if __name__ == "__main__":
    main()
