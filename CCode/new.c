#include <stdio.h>

int main() {
    
    int a = 0;
    double bage = 18.5;
    char val = 'x';
    

   char name[] = "nash";
   double grades[] = {90.5, 85.9, 88.7, 67, 95.6};

for (int i = 0; i < 5; i++) {
    if (grades[i] < 70) {
        printf("Failing grade: %.2f\n", grades[i]);
    }
}
}