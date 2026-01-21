#include <stdio.h>
#include <math.h>
 
int main() {
   double array[100];
   for(int i = 0; i <= 100; i++) { 
       array[i] = sqrt(i);
         printf("%f\n", array[i]);
    }
}