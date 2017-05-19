#include <stdio.h>
#include <time.h>

int field[70][70] = {0};
int heights[71] = {0};
int squares[24] = {0};

#ifdef VERBOSE_TO_FILE
FILE* fout;
#endif

void print_field(FILE* str)
{
    // Выводит текущее поле в поток str, внутренние квадраты обозначены латинскими буквами
    static const char codetable[] = " ABCDEFGHIJKLMNOPQRSTUVWX";
    fprintf(str, "----------------------------------------------------------------------\n");
    for (int i = 0; i < 70; ++i) {
        fprintf(str, "|");
        for (int j = 0; j < 70; ++j) {
            fprintf(str, "%c", codetable[field[i][j]]);
        }
        fprintf(str, "|\n");
    }
    fprintf(str, "----------------------------------------------------------------------\n");
}

int add_square(int x, int y, int size)
{
    // Проверяет можно ли поставить квадрат размером size на поле так, чтобы его левый верхний угол был на x, y
    // И ставит его, если это вохможно
    // Возвращает - удалось ли поставить квадрат
    if (x + size > 70 || y + size > 70) { return 0; }
    for (int i = x; i < x + size; ++i) {
        for (int j = y; j < y + size; ++j) {
            if (field[i][j] != 0) { return 0; }
        }
    }
    for (int i = x; i < x + size; ++i) {
        for (int j = y; j < y + size; ++j) {
            field[i][j] = size;
        }
    }
    squares[size - 1] = 1;
    return 1;
}

void remove_square(int x, int y, int size)
{
    // Удаляет с поля квадрат размером size, левый верхний угол которого на x, y
    for (int i = x; i < x + size; ++i) {
        for (int j = y; j < y + size; ++j) {
            field[i][j] = 0;
        }
    }
    squares[size - 1] = 0;
}

void count_heights()
{
    // Заполняет массив heights высотами каждого столбца
    int s = 0;
    for (int i = 0; i < 70; ++i) {
        if (s == 70) {
            --s;
        }
        while (s > 0 && field[s][i] == 0) {
            --s;
        }
        while (s < 70 && field[s][i] != 0) {
            ++s;
        }
        heights[i] = s;
    }
    heights[70] = 70;
}

void min_valley(int *x, int *y)
{
    // Находит наименее широкую яму, помещает координаты её левого верхнего угла в x, y
    count_heights();
    int mvw = 71, mvh = 71;
    int b = 70, c = 70;
    int bi = -1, ci = -1;
    int down = 0;
    for (int i = 0; i < 71; ++i) {
        if (heights[i] == c) {
            ci = i;
        } else if (heights[i] < c) {
            down = 1;
            b = c;
            c = heights[i];
            bi = ci;
            ci = i;
        } else {
            if (down) {
                down = 0;
                // c - top
                // bi+1 - left
                // (min(b, heights[i]) - bottom
                // i - right
                int vw = i - (bi + 1);
                if (vw <= mvw) {
                    int vh = (b < heights[i] ? b : heights[i]) - c;
                    if (vw < mvw || vh < mvh) {
                        mvw = vw;
                        mvh = vh;
                        *x = c;
                        *y = bi + 1;
                    }
                }
            }
            b = c = heights[i];
            bi = ci = i;
        }
    }
}

int solve()
{
    // Рекурсивная функция для поиска решения.
#ifdef VERBOSE_TO_FILE
    print_field(fout);
#endif
    int solved = 1;
    int x = -1, y = -1;
    min_valley(&x, &y);
    if (x == -1 || y == -1) {
        return 1;
    }
    for (int n = 24; n > 0; --n) {
        if (!squares[n - 1]) {
            solved = 0;
            if (add_square(x, y, n)) {
                if (solve()) {
                    return 1;
                }
                remove_square(x, y, n);
            }
        }
    }
    return solved;
}

int main()
{

#ifdef VERBOSE_TO_FILE
    fout = fopen("l2out_c", "w");
#endif

    time_t start_time = time(0);
    fprintf(stdout, "Program started at %s", ctime(&start_time));

    if (solve()) {
        fprintf(stdout, "Solution found:\n");
        print_field(stdout);
    } else {
        fprintf(stdout, "Solution does not exist:\n");
    }

    time_t end_time = time(0);
    fprintf(stdout, "Program ended at %s\n", ctime(&end_time));

    return 0;
}