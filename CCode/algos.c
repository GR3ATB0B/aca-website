#include <stdio.h>

void first() {
    for (int i = 0; i <= 10; i++) {
        printf("%d\n", i);
    }
}
void second() {
    for (int i = 2; i <= 20; i++) {
        printf("%d\n", i);
    }
}
void third() {
    for (int i = 4; i <= 40; i++) {
        if (i % 2 == 0)
            printf("%d\n", i);
    }
}
void fourth() {
    for (int i = 101; i <= 303; i++) {
        if (i % 2 != 0)
            printf("%d\n", i);
    }
}
void fith() {
    for (int i = 0; i <= 4; i++) {
        for (int i = 0; i <= 9; i++) {
            int j = i * 7;
                printf("%d\n", j);
    }
    }
}
void sixth() {
    int arr[85] = {0};
}

void seventh() {
    int matrix[20][20];
   
    }
void eighth() {
    int arr[85];
    for (int i = 0; i < 85; i++) {
        arr[i] = i;
    }
}
void ninth() {
    int rows = 5, cols = 5;
    int arr[rows][cols];
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            arr[i][j] = i * cols + j;
            printf("(%d,%d)\n", i, j);
        }
    }
}




int main() {
    first();
    second();
    third();
    fourth();
    fith();
    sixth();
    seventh();
    eighth();
    ninth();
}