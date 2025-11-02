import sys
from collections import defaultdict, deque

def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = defaultdict(set)
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)

    virus = 'a'
    result = []

    while True:
        q = deque([(virus, [])])
        visited = {virus}
        path_to_gate = None

        while q and not path_to_gate:
            node, path = q.popleft()
            for nxt in sorted(graph[node]):
                if nxt in visited:
                    continue
                visited.add(nxt)
                new_path = path + [nxt]
                if nxt.isupper():
                    path_to_gate = new_path
                    break
                q.append((nxt, new_path))

        if not path_to_gate:
            break


        if len(path_to_gate) == 1:
            gate = path_to_gate[0]
            cut = f"{gate}-{virus}"
        else:
            gate = path_to_gate[-1]
            node = path_to_gate[-2]
            if gate.islower():
                gate, node = node, gate
            cut = f"{gate}-{node}"

        result.append(cut)
        g, n = cut.split('-')
        graph[g].discard(n)
        graph[n].discard(g)


        if len(path_to_gate) > 1:
            virus = path_to_gate[0]
        else:
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
