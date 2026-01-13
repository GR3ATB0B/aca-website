// Simple number guessing game.
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static int read_guess(int attempt, int max_attempts) {
    int guess;
    printf("\nAttempt %d of %d\n", attempt, max_attempts);
    printf("Enter your guess: ");
    while (scanf("%d", &guess) != 1) {
        int ch;
        printf("Please enter a number: ");
        while ((ch = getchar()) != '\n' && ch != EOF) {
        }
    }
    return guess;
}

int main(void) {
    const int max_attempts = 7;
    const int min_number = 1;
    const int max_number = 50;

    srand((unsigned)time(NULL));
    int target = (rand() % (max_number - min_number + 1)) + min_number;

    printf("=== Pookie's Guessing Game ===\n");
    printf("I'm thinking of a number between %d and %d.\n", min_number, max_number);
    printf("Can you guess it in %d tries?\n", max_attempts);

    for (int attempt = 1; attempt <= max_attempts; ++attempt) {
        int guess = read_guess(attempt, max_attempts);

        if (guess == target) {
            printf("You got it! The number was %d.\n", target);
            return 0;
        }

        if (guess < target) {
            printf("Too low!");
        } else {
            printf("Too high!");
        }

        int remaining = max_attempts - attempt;
        if (remaining > 0) {
            printf(" Try again. (%d %s left)\n", remaining, remaining == 1 ? "try" : "tries");
        } else {
            printf("\nOut of tries! The number was %d.\n", target);
        }
    }

    return 0;
}
