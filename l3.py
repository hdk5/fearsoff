from math import inf
from collections import namedtuple

# Cтруктура для частного решения
# из количества шагов вверх 'moves'
# и списка этажей 'floors'
Solution = namedtuple('Solution', ('moves', 'floors'))
inf_sol = Solution(inf, [])
zero_sol = Solution(0, [])

level = 0
verbose = False


def solve(held, dropped, height, lo, hi, current, uplim):
    global level
    level += 1
    if verbose:
        print(" " * level, "Вызов с параметрами (held={held}, dropped={dropped}, height={height}, lo={lo}, hi={hi}, uplim={uplim})"
                           .format(held=held, dropped=dropped, height=height, lo=lo, hi=hi, uplim=uplim))
    sol = _solve(held, dropped, height, lo, hi, current, uplim)
    if verbose:
        print(" " * level, "Возвращается значение", sol)
    level -= 1
    return sol


def _solve(held, dropped, height, lo, hi, current, uplim):
    """
    Функция поиска решения
    held - количество транзисторов в руках
    dropped - количество транзисторов на земле
    height - текущий этаж
    lo - известный этаж, с которого транзисторы точно не разбиваются
    hi - известный этаж, с которого тразисторы точно разбиваются
    current – текущий путь
    uplim – верхняя граница для отсеивания плохих ветвей
    """
    if current.moves > uplim:
        return inf_sol
    if hi == lo + 1:
        # Случай когда hi и lo - соседние этажи
        if verbose:
            print(" " * level, "Cоседние этажи")
        return current
    if held:
        solutions = list()  # Список возможных дальнейших шагов
        for _height in range(lo + 1, hi):
            if verbose:
                print(" " * level, "Идём на этаж", _height)
            # случай, если транзистор разбивается
            breaks = solve(held - 1, dropped, _height, lo, _height,
                           Solution(
                               max(_height - height, 0) + current.moves, current.floors + [_height]
                           ), uplim
                           )
            # случай, если тразистор выживает
            survives = solve(held - 1, dropped + 1, _height, _height, hi,
                             Solution(
                                 max(_height - height, 0) + current.moves, current.floors + [_height]
                             ), uplim
                             )
            # выбираем худший случай
            worst = max((breaks, survives), key=lambda x: x.moves)
            if verbose:
                print(" " * level, "Худший случай:", worst)
            # uplim = min(worst.moves, uplim)
            if worst.moves < uplim:
                uplim = worst.moves
                if verbose:
                    print(" " * level, "Новая верхняя граница:", uplim)
            solutions.append(worst)
        # из худших случаев выбираем лучший
        best = min(solutions, key=lambda x: x.moves, default=Solution(inf, []))
        if verbose:
            print(" " * level, "Лучший случай из худших:", best)
            # uplim = min(best.moves, uplim)
        if best.moves < uplim:
            uplim = best.moves
            if verbose:
                print(" " * level, "Новая верхняя граница:", uplim)
        return best
    if dropped:
        return solve(held + dropped, 0, 1, lo, hi, Solution(current.moves, current.floors + [1]), uplim)
    return inf_sol


def main():
    from argparse import ArgumentParser, FileType
    parser = ArgumentParser()
    parser.add_argument("-f", type=FileType('r'), help="считать входные данные из файла F в формате \"{транзисторы} {этажи}\"")
    parser.add_argument("-c", help="считать входные данные из консоли", action='store_true')
    parser.add_argument("-v", help="выводить ход решения", action='store_true')
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
    global verbose
    verbose = args.v
    print("Поиск решения:")
    solution = solve(t, 0, 1, 1, s, zero_sol, inf)
    print("Минимальное число шагов в худшем случае:", solution.moves)
    print("Ход этажей:", solution.floors)


if __name__ == '__main__':
    main()
