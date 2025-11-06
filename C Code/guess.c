#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void) {
    int secret;
    int guess;

    srand((unsigned int)time(NULL));
    secret = (rand() % 100) + 1;

    printf("I'm thinking of a number between 1 and 100.\n");

    while (1) {
        printf("Enter your guess: ");
        if (scanf("%d", &guess) != 1) {
            printf("Please enter a valid integer.\n");
            int c;
            while ((c = getchar()) != '\n' && c != EOF) {
               
            }
            continue;
        }

        if (guess < secret) {
            printf("Too low!\n");
        } else if (guess > secret) {
            printf("Too high!\n");
        } else {
            printf("You got it! The number was %d.\n", secret);
            break;
        }
    }


}
