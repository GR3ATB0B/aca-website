#include <stdio.h>

 int a;
 int b;

int main(){
    printf("a=");
    scanf("%d",&a);
    printf("b=");
    scanf("%d",&b);
    int c = a * b;
    printf("%d * %d = %d\n",a,b,c);
}