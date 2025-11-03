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
        """Возвращает список путей до всех шлюзов минимальной длины"""
        q = deque([(start, [])])
        visited = {start}
        gates = []
        min_len = None

        while q:
            node, path = q.popleft()
            for nxt in sorted(graph[node]):
                if nxt in visited:
                    continue
                visited.add(nxt)
                new_path = path + [nxt]
                if nxt.isupper():
                    # нашли шлюз
                    if min_len is None or len(new_path) < min_len:
                        min_len = len(new_path)
                        gates = [new_path]
                    elif len(new_path) == min_len:
                        gates.append(new_path)
                else:
                    q.append((nxt, new_path))
        return gates

    while True:
        paths = bfs(virus)
        if not paths:
            break

        # выбираем ближайший шлюз и путь лексикографически
        paths.sort(key=lambda p: (p[-1], p))
        path = paths[0]

        gate = path[-1]
        if len(path) == 1:
            node = virus
        else:
            node = path[-2]

        if gate.islower():
            gate, node = node, gate

        cut = f"{gate}-{node}"
        result.append(cut)

        # отключаем коридор
        graph[gate].discard(node)
        graph[node].discard(gate)

        # если есть путь — вирус движется на следующий узел
        if len(path) > 1:
            virus = path[0]
        else:
            break

        # если больше нет соединений с шлюзами — стоп
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
