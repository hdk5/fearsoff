from math import inf
from collections import namedtuple

# Cтруктура для частного решения
# из количества шагов вверх 'moves'
# и списка этажей 'floors'
Solution = namedtuple('Solution', ('moves', 'floors'))

# Кэш для уже посчитанных найденных частичных решений
solve_cache = dict()

level = -1


def solve(held, dropped, height, lo, hi):
    """Функция-обёртка для кэша и настоящей функции поиска решения"""
    global level
    level += 1
    print(" " * level, "Вызов с параметрами (held={held}, dropped={dropped}, height={height}, lo={lo}, hi={hi})".format(
                        held=held, dropped=dropped, height=height, lo=lo, hi=hi))
    if (held, dropped, height, lo, hi) not in solve_cache:
        solve_cache[held, dropped, height, lo, hi] = _solve(held, dropped, height, lo, hi)
    else:
        print(" " * level, "Берётся значение из кэша")
    sol = solve_cache[held, dropped, height, lo, hi]
    print(" " * level, "Возвращается значение", sol)
    level -= 1
    return sol


def _solve(held, dropped, height, lo, hi):
    """
    Функция поиска решения
    held - количество транзисторов в руках
    dropped - количество транзисторов на земле
    height - текущий этаж
    lo - известный этаж, с которого транзисторы точно не разбиваются
    hi - известный этаж, с которого тразисторы точно разбиваются
    """
    global level
    if hi == lo + 1:
        # Случай когда hi и lo - соседние этажи
        print(" " * level, "Cоседние этажи")
        return Solution(0, [])
    if held:
        # Если у профессора есть транзисторы в руках,
        # он будет их кидать с этажей от следующего за безопасным этажом
        # до последнего перед опасным этажом
        solutions = list()  # Список возможных дальнейших шагов
        for _height in range(lo + 1, hi):
            print(" " * level, "Идём на этаж", _height)
            # случай, если транзистор разбивается
            breaks = solve(held - 1, dropped, _height, lo, _height)
            # случай, если тразистор выживает
            survives = solve(held - 1, dropped + 1, _height, _height, hi)
            # выбираем худший случай
            worst = max((breaks, survives), key=lambda x: x.moves)
            print(" " * level, "Худший случай:", worst)
            solutions.append(
                Solution(
                    max(_height - height, 0) + worst.moves,
                    [_height] + worst.floors
                )
            )
        # из худших случаев выбираем лучший
        best = min(solutions, key=lambda x: x.moves, default=Solution(inf, []))
        print(" " * level, "Лучший случай из худших:", best)
        return best
    if dropped:
        # Если на руках нет транзисторов, но есть лежащие на земле,
        # то профессор спускается на первый этаж
        print(" " * level, "Спускаемся вниз")
        collect = solve(held + dropped, 0, 1, lo, hi)
        return Solution(collect.moves, [1] + collect.floors)
    # нет транзисторов - нет решений
    return Solution(inf, [])


def main():
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser()
    parser.add_argument("-f", type=FileType('r'), help="считать входные данные из файла F в формате \"{транзисторы} {этажи}\"")
    parser.add_argument("-c", help="считать входные данные из консоли", action='store_true')
    parser.add_argument("-t", type=int, help="число транзисторов")
    parser.add_argument("-s", type=int, help="число этажей")
    args = parser.parse_args()
    if bool(args.f) + bool(args.c) + (bool(args.t) + bool(args.s)) / 2 != 1:
        parser.print_help()
        parser.exit(1)
    if args.f:
        try:
            t, s = map(int, args.f.read().split()[:2])
        except ValueError:
            parser.exit(1, "Не удалось прочитать входные данные")
    elif args.t and args.s:
        t, s = args.t, args.s
    elif args.c:
        try:
            print("Число транзисторов: ", end='')
            t = int(input())
            print("Число этажей: ", end='')
            s = int(input())
        except ValueError:
            parser.exit(1, "Не удалось прочитать входные данные")
    if t <= 0 or s <= 1:
        parser.exit(1, "Входные данные должны быть натуральными числами, число этожей должно быть больше одного")
    print("Поиск решения:")
    solution = solve(t, 0, 1, 1, s)
    print("Минимальное число шагов в худшем случае:", solution.moves)
    print("Ход этажей:", solution.floors)


if __name__ == '__main__':
    main()
