import sys

# ====================== КОНСТАНТИ (Зауваження 2) ======================
MAX_COINS = 1_000_000          # початкова кількість монет у кожному місті
GRID_SIZE = 10                 # розмір сітки (1..10)
PORTION_DIVISOR = 1000         # 1 монета на кожні 1000
MAX_DAYS = 20000               # максимальна кількість днів (захист від нескінченного циклу)

def main():
    """
    Головна функція програми Euro Diffusion.
    Моделює розповсюдження монет по Європі та визначає день завершення обігу для кожної країни.
    """
    case_num = 1
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            break
        c = int(line)
        if c == 0:
            break

        # --- Ініціалізація країн ---
        country_names = []
        country_cities = [[] for _ in range(c)]
        city_to_country = [[-1] * (GRID_SIZE + 1) for _ in range(GRID_SIZE + 1)]

        for i in range(c):
            parts = sys.stdin.readline().strip().split()
            name = parts[0]
            xl, yl, xh, yh = map(int, parts[1:])
            country_names.append(name)
            for x in range(xl, xh + 1):
                for y in range(yl, yh + 1):
                    city_to_country[x][y] = i
                    country_cities[i].append((x, y))

        # --- Ініціалізація монет ---
        coins = [[[0 for _ in range(c)] for _ in range(GRID_SIZE + 1)] for _ in range(GRID_SIZE + 1)]
        for i in range(c):
            for x, y in country_cities[i]:
                coins[x][y][i] = MAX_COINS

        city_complete_day = [[-1] * (GRID_SIZE + 1) for _ in range(GRID_SIZE + 1)]
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        day = 0

        # Початкова перевірка (день 0)
        for x in range(1, GRID_SIZE + 1):
            for y in range(1, GRID_SIZE + 1):
                if city_to_country[x][y] == -1:
                    continue
                if all(coins[x][y][m] >= 1 for m in range(c)):
                    city_complete_day[x][y] = day

        all_complete = all(
            city_complete_day[x][y] != -1
            for x in range(1, GRID_SIZE + 1)
            for y in range(1, GRID_SIZE + 1)
            if city_to_country[x][y] != -1
        )

        # === Основний цикл симуляції (виправлено Зауваження 3) ===
        while not all_complete:
            if day > MAX_DAYS:
                print(f"WARNING: Досягнуто максимум {MAX_DAYS} днів. Можливо країни не з'єднані.")
                break

            next_coins = [[[0 for _ in range(c)] for _ in range(GRID_SIZE + 1)] for _ in range(GRID_SIZE + 1)]

            for x in range(1, GRID_SIZE + 1):
                for y in range(1, GRID_SIZE + 1):
                    if city_to_country[x][y] == -1:
                        continue
                    for m in range(c):
                        cnt = coins[x][y][m]
                        if cnt == 0:
                            continue
                        portion = cnt // PORTION_DIVISOR
                        if portion == 0:
                            next_coins[x][y][m] += cnt
                            continue

                        neigh = 0
                        for dx, dy in dirs:
                            nx, ny = x + dx, y + dy
                            if 1 <= nx <= GRID_SIZE and 1 <= ny <= GRID_SIZE and city_to_country[nx][ny] != -1:
                                next_coins[nx][ny][m] += portion
                                neigh += 1
                        next_coins[x][y][m] += cnt - portion * neigh

            coins = next_coins
            day += 1

            # Перевірка після переміщення
            for x in range(1, GRID_SIZE + 1):
                for y in range(1, GRID_SIZE + 1):
                    if city_to_country[x][y] == -1 or city_complete_day[x][y] != -1:
                        continue
                    if all(coins[x][y][m] >= 1 for m in range(c)):
                        city_complete_day[x][y] = day

            all_complete = all(
                city_complete_day[x][y] != -1
                for x in range(1, GRID_SIZE + 1)
                for y in range(1, GRID_SIZE + 1)
                if city_to_country[x][y] != -1
            )

        # --- Вивід результату ---
        country_days = []
        for i in range(c):
            max_d = max((city_complete_day[x][y] for x, y in country_cities[i]), default=0)
            country_days.append((max_d, country_names[i]))

        country_days.sort(key=lambda t: (t[0], t[1]))

        print(f"Case Number {case_num}")
        for d, name in country_days:
            print(name, d)
        case_num += 1


if __name__ == "__main__":
    main()
