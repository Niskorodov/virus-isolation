import sys
from collections import deque, defaultdict


def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"
    """

    # Строим граф
    graph = defaultdict(list)
    gateways = set()
    nodes = set()

    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
        nodes.add(u)
        nodes.add(v)
        # Определяем шлюзы (заглавные буквы)
        if u.isupper():
            gateways.add(u)
        if v.isupper():
            gateways.add(v)

    # Начальная позиция вируса
    virus_pos = 'a'
    result = []

    # Функция для поиска кратчайшего пути к шлюзам
    def find_virus_path(current_pos):
        # BFS для поиска кратчайшего пути до любого шлюза
        queue = deque([(current_pos, [current_pos])])
        visited = {current_pos}

        while queue:
            node, path = queue.popleft()

            # Если достигли шлюза
            if node in gateways:
                return path

            # Сортируем соседей для детерминированности
            for neighbor in sorted(graph[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    # Функция для определения следующего хода вируса
    def get_virus_move(current_pos):
        # Находим все шлюзы и их расстояния
        distances = {}
        for gateway in sorted(gateways):  # Сортируем для детерминированности
            # BFS для поиска расстояния до шлюза
            queue = deque([(current_pos, 0)])
            visited = {current_pos}
            found = False

            while queue and not found:
                node, dist = queue.popleft()
                if node == gateway:
                    distances[gateway] = dist
                    found = True
                    break

                for neighbor in sorted(graph[node]):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, dist + 1))

        if not distances:
            return None

        # Находим минимальное расстояние
        min_dist = min(distances.values())

        # Выбираем шлюз с минимальным расстоянием (лексикографически первый при равенстве)
        target_gateway = min(gw for gw, dist in distances.items() if dist == min_dist)

        # Находим следующий узел на пути к целевому шлюзу
        # BFS для построения пути
        queue = deque([(current_pos, [current_pos])])
        visited = {current_pos}

        while queue:
            node, path = queue.popleft()

            if node == target_gateway:
                # Возвращаем следующий узел после current_pos
                return path[1] if len(path) > 1 else None

            for neighbor in sorted(graph[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    # Основной цикл игры
    while True:
        # 1. Находим все возможные отключаемые коридоры (шлюз-узел)
        possible_cuts = []
        for gateway in gateways:
            for neighbor in sorted(graph[gateway]):
                if neighbor.islower():  # Только обычные узлы
                    possible_cuts.append((gateway, neighbor))

        # Сортируем для лексикографического порядка
        possible_cuts.sort()

        # 2. Пытаемся найти отключение, которое не приведет к немедленному поражению
        best_cut = None

        for gateway, node in possible_cuts:
            # Временно удаляем этот коридор
            graph[gateway].remove(node)
            graph[node].remove(gateway)

            # Проверяем, может ли вирус достичь шлюза
            path = find_virus_path(virus_pos)

            # Если вирус не может достичь шлюза или это безопасное отключение
            if path is None:
                best_cut = (gateway, node)
                # Не восстанавливаем граф - это наш выбор
                break
            else:
                # Восстанавливаем граф
                graph[gateway].append(node)
                graph[node].append(gateway)

        # Если не нашли безопасного отключения, берем первое возможное
        if best_cut is None and possible_cuts:
            best_cut = possible_cuts[0]
            gateway, node = best_cut
            graph[gateway].remove(node)
            graph[node].remove(gateway)

        if best_cut is None:
            break

        gateway, node = best_cut
        result.append(f"{gateway}-{node}")

        # 3. Вирус делает ход
        next_pos = get_virus_move(virus_pos)
        if next_pos is None:
            break  # Вирус заблокирован

        virus_pos = next_pos

        # 4. Проверяем, не достиг ли вирус шлюза
        if virus_pos in gateways:
            break

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            # Разбираем строку вида "узел1-узел2"
            parts = line.split('-')
            if len(parts) == 2:
                edges.append((parts[0], parts[1]))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()