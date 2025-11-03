import sys
from collections import deque, defaultdict

def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(set)
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)

    virus = 'a'
    result = []

    def shortest_path_to_gate(start):
        """Возвращает кратчайший путь от вируса до ближайшего шлюза"""
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
                    # нашли шлюз
                    if min_len is None or len(new_path) < min_len:
                        min_len = len(new_path)
                        paths = [new_path]
                    elif len(new_path) == min_len:
                        paths.append(new_path)
                else:
                    q.append((nxt, new_path))
        if not paths:
            return None
        # выбираем путь лексикографически по последнему элементу (имени шлюза)
        paths.sort(key=lambda p: (p[-1], p))
        return paths[0]

    while True:
        path = shortest_path_to_gate(virus)
        if not path:
            break

        gate = path[-1]
        node = path[-2] if len(path) > 1 else virus

        # отключаем шлюз от узла
        cut = f"{gate}-{node}"
        result.append(cut)
        graph[gate].discard(node)
        graph[node].discard(gate)

        # если остались соединения со шлюзами — вирус двигается дальше
        if len(path) > 1:
            virus = path[0]
        else:
            break

        # если больше нет путей до шлюзов — стоп
        active = any(n.isupper() for k in graph for n in graph[k])
        if not active:
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

    res = solve(edges)
    for r in res:
        print(r)


if __name__ == "__main__":
    main()
