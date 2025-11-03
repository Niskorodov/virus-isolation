import sys
from collections import defaultdict, deque


def solve(edges: list[tuple[str, str]]) -> list[str]:
    # --- строим граф ---
    graph = defaultdict(set)
    gateways = set()
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)
        if a.isupper():
            gateways.add(a)
        if b.isupper():
            gateways.add(b)
    virus = 'a'
    # --- BFS расстояния от вируса ---
    dist = {virus: 0}
    q = deque([virus])
    while q:
        u = q.popleft()
        for v in sorted(graph[u]):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    # --- собираем все пары шлюз-узел ---
    candidates = []
    for g in sorted(gateways):
        for n in sorted(graph[g]):
            d = dist.get(n, float('inf'))  # если узел нед
            candidates.append((d, g, n))
    # --- сортировка ---
    candidates.sort(key=lambda x: (x[0], x[1], x[2]))
    # --- вывод ---

    return [f"{g}-{n}" for d, g, n in candidates]


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