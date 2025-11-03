import sys
from collections import defaultdict, deque


def solve(edges: list[tuple[str, str]]) -> list[str]:
    # Граф
    graph = defaultdict(set)
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)

    def shortest_path_from(start: str) -> list[str] | None:
        """
        Кратчайший путь от start до любого шлюза (A..Z),
        с лексикографическими тай-брейками:
          - сначала по букве шлюза,
          - затем по самому пути (A..Z, a..z).
        Возвращает путь как список вершин БЕЗ стартовой: [next, ..., GATE]
        или None, если шлюзы недостижимы.
        """
        q = deque([(start, [])])
        visited = {start}
        best_len = None
        paths = []

        while q:
            node, path = q.popleft()
            for nxt in sorted(graph[node]):  # лексикографический порядок соседей
                if nxt in visited:
                    continue
                visited.add(nxt)
                new_path = path + [nxt]
                if nxt.isupper():  # попали в шлюз
                    if best_len is None or len(new_path) < best_len:
                        best_len = len(new_path)
                        paths = [new_path]
                    elif len(new_path) == best_len:
                        paths.append(new_path)
                else:
                    # продолжаем искать через обычные узлы
                    q.append((nxt, new_path))

        if not paths:
            return None

        # Выбираем путь: сперва по шлюзу, затем по самому пути
        paths.sort(key=lambda p: (p[-1], p))
        return paths[0]

    virus = 'a'
    result: list[str] = []

    while True:
        # Считаем путь ДО разреза
        path = shortest_path_from(virus)
        if not path:
            break  # шлюзы недостижимы — всё, готово

        gate = path[-1]
        node = path[-2] if len(path) > 1 else virus  # сосед шлюза (всегда строчная)

        # Разрезаем
        result.append(f"{gate}-{node}")
        graph[gate].discard(node)
        graph[node].discard(gate)

        # После разреза вирус переоценивает цель и делает шаг
        new_path = shortest_path_from(virus)
        if not new_path:
            break  # больше путей к шлюзам нет
        virus = new_path[0]  # один шаг к новому ближайшему шлюзу

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        a, _, b = line.partition('-')
        edges.append((a, b))

    for cut in solve(edges):
        print(cut)


if __name__ == "__main__":
    main()
