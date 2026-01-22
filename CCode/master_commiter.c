#include <stdio.h>
#include <math.h>
 
int main() {
   float array[100];
   float num;
   for(int i = 0; i <= 100; i++) { 
       array[i] = sqrt(i);
        printf("%.2f", array[i]);
         printf("\n");
    }

    printf("enter the number you want to search for\n");
    scanf("%f", &num);

    for(int i = 0; i <= 100; i++) {
        if(array[i] == num) {
            printf("Number found at index %d\n", i);
        }
    }
    printf("Number not found in the array\n");
}