#include <stdio.h>
#include <time.h>

int field[70][70] = {0};
int squares[24] = {0};

int verbose = 0;
FILE* fout = NULL;


void print_field(FILE* str)
{
    // Выводит текущее поле в поток str, внутренние квадраты обозначены латинскими буквами
    static const char codetable[] = " ABCDEFGHIJKLMNOPQRSTUVWX";
    fprintf(str, "------------------------------------------------------------------------\n");
    for (int i = 0; i < 70; ++i) {
        fprintf(str, "|");
        for (int j = 0; j < 70; ++j) {
            fprintf(str, "%c", codetable[field[i][j]]);
        }
        fprintf(str, "|\n");
    }
    fprintf(str, "------------------------------------------------------------------------\n");
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
    if (verbose) {
        print_field(fout);
    }
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
    if (verbose) {
        print_field(fout);
    }
}


void min_valley(int *x, int *y)
{
    // Находит наименее широкую яму, помещает координаты её левого верхнего угла в x, y
    int height = 0;
    int minwidth = 71;
    int depth = 70;
    int border_i = -1;
    int down = 0;
    for (int i = 0; i < 71; ++i) {
        if (i == 70) {
            height = 70;
        } else {
            if (height == 70) {
                --height;
            }
            while (height > 0 && field[height][i] == 0) {
                --height;
            }
            while (height < 70 && field[height][i] != 0) {
                ++height;
            }
        }
        if (height < depth) {
            down = 1;
            depth = height;
            border_i = i - 1;
        } else if (height > depth) {
            if (down) {
                down = 0;
                // depth - top
                // border_i+1 - left
                // (min(border, height) - bottom
                // i - right
                int width = i - (border_i + 1);
                if (width < minwidth) {
                    minwidth = width;
                    *x = depth;
                    *y = border_i + 1;
                }
            }
            depth = height;
            border_i = i;
        }
    }
}


int solve()
{
    // Рекурсивная функция для поиска решения.
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


int main(int argc, char const *argv[])
{

    if (argc == 2 && argv[1][0] == 'v') {
        verbose = 1;
        fout = fopen("l2out_c.txt", "w");
    }

    time_t start_time = time(0);
    fprintf(stdout, "Program started at %s", ctime(&start_time));

    if (verbose) {
        print_field(fout);
    }

    if (solve()) {
        fprintf(stdout, "Solution found:\n");
        print_field(stdout);
    } else {
        fprintf(stdout, "Solution does not exist\n");
    }

    time_t end_time = time(0);
    fprintf(stdout, "Program ended at %s\n", ctime(&end_time));

    return 0;
}