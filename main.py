import sys

def main():
    case_num = 1
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            break
        c = int(line)
        if c == 0:
            break

        country_names = []
        country_cities = [[] for _ in range(c)]
        city_to_country = [[-1] * 11 for _ in range(11)]
        for i in range(c):
            parts = sys.stdin.readline().strip().split()
            name = parts[0]
            xl, yl, xh, yh = map(int, parts[1:])
            country_names.append(name)
            for x in range(xl, xh + 1):
                for y in range(yl, yh + 1):
                    city_to_country[x][y] = i
                    country_cities[i].append((x, y))


        coins = [[[0 for _ in range(c)] for _ in range(11)] for _ in range(11)]
        for i in range(c):
            for x, y in country_cities[i]:
                coins[x][y][i] = 1000000

        city_complete_day = [[-1] * 11 for _ in range(11)]
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        day = 0


        for x in range(1, 11):
            for y in range(1, 11):
                if city_to_country[x][y] == -1:
                    continue
                if all(coins[x][y][m] >= 1 for m in range(c)):
                    city_complete_day[x][y] = day

        all_complete = all(city_complete_day[x][y] != -1
                           for x in range(1, 11)
                           for y in range(1, 11)
                           if city_to_country[x][y] != -1)

        while not all_complete:
            next_coins = [[[0 for _ in range(c)] for _ in range(11)] for _ in range(11)]
            for x in range(1, 11):
                for y in range(1, 11):
                    if city_to_country[x][y] == -1:
                        continue
                    for m in range(c):
                        cnt = coins[x][y][m]
                        if cnt == 0:
                            continue
                        portion = cnt // 1000
                        if portion == 0:
                            next_coins[x][y][m] += cnt
                            continue
                        neigh = 0
                        for dx, dy in dirs:
                            nx, ny = x + dx, y + dy
                            if 1 <= nx <= 10 and 1 <= ny <= 10 and city_to_country[nx][ny] != -1:
                                next_coins[nx][ny][m] += portion
                                neigh += 1
                        next_coins[x][y][m] += cnt - portion * neigh
            coins = next_coins
            day += 1


            for x in range(1, 11):
                for y in range(1, 11):
                    if city_to_country[x][y] == -1 or city_complete_day[x][y] != -1:
                        continue
                    if all(coins[x][y][m] >= 1 for m in range(c)):
                        city_complete_day[x][y] = day

            all_complete = all(city_complete_day[x][y] != -1
                               for x in range(1, 11)
                               for y in range(1, 11)
                               if city_to_country[x][y] != -1)


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