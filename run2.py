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

                    if min_len is None or len(new_path) == min_len:
                        min_len = len(new_path)
                        paths.append(new_path)
                    elif len(new_path) < min_len:
                        min_len = len(new_path)
                        paths = [new_path]
                else:
                    q.append((nxt, new_path))

        if not paths:
            break


        paths.sort(key=lambda p: (p[-1], p))
        path_to_gate = paths[0]


        gate = path_to_gate[-1]
        node = path_to_gate[-2] if len(path_to_gate) > 1 else virus
        if gate.islower():
            gate, node = node, gate
        cut = f"{gate}-{node}"

        result.append(cut)
        g, n = cut.split('-')
        graph[g].discard(n)
        graph[n].discard(g)


        virus = path_to_gate[0] if len(path_to_gate) > 1 else virus


        if not any(c.isupper() for c in graph[virus]):
            if not any(any(x.isupper() for x in graph[k]) for k in graph if k.islower()):
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
