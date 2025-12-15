

#include <stdio.h>

#define BOARD_SIZE 5
#define SHIP_COUNT 3

/* Cell meanings:
 * '.' = empty water (unknown to opponent)
 * 'S' = ship (only visible to owner when placing; hidden later)
 * 'X' = hit
 * 'O' = miss
 */

void init_board(char board[BOARD_SIZE][BOARD_SIZE]) {
    for (int r = 0; r < BOARD_SIZE; r++) {
        for (int c = 0; c < BOARD_SIZE; c++) {
            board[r][c] = '.';
        }
    }
}

void print_board(const char board[BOARD_SIZE][BOARD_SIZE], int hide_ships) {
    /* Print column headers */
    printf("   ");
    for (int c = 0; c < BOARD_SIZE; c++) {
        printf("%d ", c);
    }
    printf("\n");

    for (int r = 0; r < BOARD_SIZE; r++) {
        printf("%d: ", r);
        for (int c = 0; c < BOARD_SIZE; c++) {
            char ch = board[r][c];
            if (hide_ships && ch == 'S') {
                ch = '.';
            }
            printf("%c ", ch);
        }
        printf("\n");
    }
}

int all_ships_sunk(const char board[BOARD_SIZE][BOARD_SIZE]) {
    for (int r = 0; r < BOARD_SIZE; r++) {
        for (int c = 0; c < BOARD_SIZE; c++) {
            if (board[r][c] == 'S') {
                return 0;
            }
        }
    }
    return 1;
}

void place_ships(char board[BOARD_SIZE][BOARD_SIZE], int player) {
    int placed = 0;
    printf("\nPlayer %d: place your %d ships (single cells).\n", player, SHIP_COUNT);
    printf("Board indices are row and column from 0 to %d.\n", BOARD_SIZE - 1);
    printf("Your board:\n");
    print_board(board, 0);

    while (placed < SHIP_COUNT) {
        int row, col;
        printf("Place ship %d of %d (row col): ", placed + 1, SHIP_COUNT);
        if (scanf("%d %d", &row, &col) != 2) {
            printf("Invalid input. Exiting.\n");
            return;
        }
        if (row < 0 || row >= BOARD_SIZE || col < 0 || col >= BOARD_SIZE) {
            printf("Out of bounds. Try again.\n");
            continue;
        }
        if (board[row][col] == 'S') {
            printf("You already placed a ship there. Try again.\n");
            continue;
        }
        board[row][col] = 'S';
        placed++;
        print_board(board, 0);
    }
}

void clear_stdin_line(void) {
    int ch;
    while ((ch = getchar()) != '\n' && ch != EOF) {
        /* discard */
    }
}

void wait_for_next_player(int next_player) {
    printf("\nPass the keyboard to Player %d and press ENTER to continue...", next_player);
    clear_stdin_line();

    /* Print many newlines to "hide" the previous player's board/moves */
    for (int i = 0; i < 50; i++) {
        printf("\n");
    }
}

int main(void) {
    char board1[BOARD_SIZE][BOARD_SIZE];
    char board2[BOARD_SIZE][BOARD_SIZE];

    init_board(board1);
    init_board(board2);

    /* Ship placement */
    place_ships(board1, 1);
    clear_stdin_line(); /* clear leftover newline */
    wait_for_next_player(2);

    place_ships(board2, 2);
    clear_stdin_line();
    wait_for_next_player(1);

    int current_player = 1;
    char (*attacker_board)[BOARD_SIZE] = NULL;
    char (*defender_board)[BOARD_SIZE] = NULL;

    while (1) {
        if (current_player == 1) {
            attacker_board = board1;
            defender_board = board2;
        } else {
            attacker_board = board2;
            defender_board = board1;
        }

        printf("\n===== Player %d's turn =====\n", current_player);
        printf("Your board:\n");
        print_board(attacker_board, 0);

        printf("Opponent's board (ships hidden):\n");
        print_board(defender_board, 1);

        int row, col;
        printf("Enter coordinates to fire at (row col): ");
        if (scanf("%d %d", &row, &col) != 2) {
            printf("Invalid input. Exiting.\n");
            break;
        }

        if (row < 0 || row >= BOARD_SIZE || col < 0 || col >= BOARD_SIZE) {
            printf("That shot is out of bounds. Turn skipped.\n");
        } else {
            char *target = &defender_board[row][col];
            if (*target == 'S') {
                printf("Hit!\n");
                *target = 'X';
            } else if (*target == '.' ) {
                printf("Miss.\n");
                *target = 'O';
            } else if (*target == 'X' || *target == 'O') {
                printf("You already shot there. It stays %c.\n", *target);
            }
        }

        if (all_ships_sunk(defender_board)) {
            printf("\nAll ships of Player %d have been sunk!\n", current_player == 1 ? 2 : 1);
            printf("Player %d wins!\n", current_player);
            printf("\nFinal boards (ships visible):\n");
            printf("Player 1 board:\n");
            print_board(board1, 0);
            printf("Player 2 board:\n");
            print_board(board2, 0);
            break;
        }

        /* Switch player */
        current_player = (current_player == 1) ? 2 : 1;
        clear_stdin_line();
        wait_for_next_player(current_player);
    }

    return 0;
}


