import sys
import heapq

DOORS = [2, 4, 6, 8]
HALL_SIZE = 11
HALL_FREE = [i for i in range(HALL_SIZE) if i not in DOORS]
COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
TARGET = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
ROOM_TYPE = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}


def parse(lines):
    rows = [l for l in lines if any(c in l for c in 'ABCD')]
    rows = [r for r in rows if len(r) > 9 and all(r[i] in 'ABCD#' for i in (3, 5, 7, 9))]
    depth = len(rows)
    if depth not in (2, 4):
        raise ValueError('Некорректный формат входных данных')
    rooms = tuple(tuple(r[j] for r in rows) for j in (3, 5, 7, 9))
    hall = tuple('.' for _ in range(HALL_SIZE))
    return hall, rooms


def is_solved(state):
    hall, rooms = state
    if any(c != '.' for c in hall):
        return False
    for i, r in enumerate(rooms):
        if any(c != ROOM_TYPE[i] for c in r):
            return False
    return True


def path_clear(hall, a, b):
    left, right = sorted((a, b))
    return all(hall[i] == '.' for i in range(left + 1, right))


def moves(state):
    hall, rooms = state
    depth = len(rooms[0])


    for ri, room in enumerate(rooms):
        target = ROOM_TYPE[ri]
        if all(c == target for c in room):
            continue
        top = next((i for i, c in enumerate(room) if c != '.'), None)
        if top is None:
            continue
        amph = room[top]
        door = DOORS[ri]
        dist_up = top + 1

        for step in (-1, 1):
            pos = door
            while 0 <= pos + step < HALL_SIZE and hall[pos + step] == '.':
                pos += step
                if pos in HALL_FREE:
                    dist = dist_up + abs(pos - door)
                    cost = dist * COSTS[amph]
                    new_hall = list(hall)
                    new_rooms = [list(r) for r in rooms]
                    new_hall[pos] = amph
                    new_rooms[ri][top] = '.'
                    yield cost, (tuple(new_hall), tuple(tuple(r) for r in new_rooms))


    for pos, amph in enumerate(hall):
        if amph == '.':
            continue
        target = TARGET[amph]
        door = DOORS[target]
        if not path_clear(hall, pos, door):
            continue
        room = rooms[target]
        if any(c not in ('.', amph) for c in room):
            continue
        d = max(i for i, c in enumerate(room) if c == '.')
        dist = abs(pos - door) + d + 1
        cost = dist * COSTS[amph]
        new_hall = list(hall)
        new_rooms = [list(r) for r in rooms]
        new_hall[pos] = '.'
        new_rooms[target][d] = amph
        yield cost, (tuple(new_hall), tuple(tuple(r) for r in new_rooms))


def solve(lines):
    start = parse(lines)
    pq = [(0, start)]
    best = {start: 0}

    while pq:
        cost, state = heapq.heappop(pq)
        if cost != best[state]:
            continue
        if is_solved(state):
            return cost
        for move_cost, nxt in moves(state):
            total = cost + move_cost
            if total < best.get(nxt, 10**12):
                best[nxt] = total
                heapq.heappush(pq, (total, nxt))
    return -1


if __name__ == '__main__':
    data = [x.rstrip('\n') for x in sys.stdin]
    print(solve(data))
