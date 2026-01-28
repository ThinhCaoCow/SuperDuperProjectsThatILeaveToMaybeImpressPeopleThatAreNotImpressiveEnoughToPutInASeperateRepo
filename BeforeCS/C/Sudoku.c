#include <stdio.h> // includes standard input and output functions such as print and scan
#include <stdlib.h> // important for variable/memory control with commands such as malloc or abs for memory allocation
#include <string.h> // string data manipulation such as strcpy and strlen
#include <math.h> // complex math functions such as sin and sqrt
#include <time.h> // time & date functionalitys
#include <assert.h> // data diagnostics through assert
//Basic C libaries that are included  

//  Day one of refreshing my C memory by solving sudoku
// Sudoku is a math-related game in which a player must fill a 9x9 grid
// in which, each column and row would contain the digits from 1 to 9.
// The Grid would be partially compeleted, allowing for the player to start filling 
// numbers when appropiate.

// To start, i will be attempting to use brute force techniques to solve, mainly using recursion.
// There will be 3 objectives, Scan the grid, adding a scaling number, and removing/backtracking. 
// I'd Suggest that the program would have 4 functions, excluding the main sudoku function
// read_grid, find_empty, check_add_remove, and solve.

void read_grid(int board[9][9])
{
    for (int i = 0; i < 9; i++)
    {
        for(int j = 0; j < 9; j++)
        {
            scanf("%d", &board[i][j]);
        }
    }
}

// the read_grid function has 2 for statments, which represents the row and columun respectivly
// it would then check for all points of the submitted data, scanning for all 9*9 values. 
// this would be later checked by the find_empty to check for whether the certain arrary(s) has the value of 0.

int find_empty(int board[9][9], int *row, int *col)
{
    for(*row = 0; *row < 9; (*row)++)
    {
        for(*col = 0; *col < 9; (*col)++) //I MISSED THE BRACKETS JUST ADDED THEM
        {
            if (board[*row][*col] == 0)
            {
                return 1;
            }
        }
    }
    return 0;
}

// the find_empty function also has 2 for statements as the read_grid to read all points and their values.
// this checks whether the values are true to 0, which returns a 1 to be later read by the last re
// This may seem redundant but it will be used later to verify if the board had been completed.
// 30minutes later I REALISED THAT THE PROGRAM DIDNT SOLVE PROPERLY BECAUSE THE POINTER ROW AND COL WAS NOT BRACKETED, CAUSING IT TO FREEZe DUE TO INVALID MEMORY ADDRESS HANDELING. Im more fitt to go to a mcd and work tbh.

int check_add_remove(int board[9][9], int row, int col, int num)
{
    for(int x = 0; x< 9; x++)
    {
        if (board[row][x] == num)
        return 0;
    }
    for(int y = 0; y < 9; y++)
    {
        if (board[y][col] == num)
        return 0;
    }
    int startrow = row - row % 3;
    int startcol = col - col % 3;
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            if (board[i + startrow][j + startcol] == num)
            return 0;
        }
    }
    return 1;
}

// the check_add_remove function may seem off, checking for each individual row/col with num but
// this part is essential as it individually checks each row if the num added is valid, and vic versa
// with the column.
// the startrow and startcol continues with the valid check to find whether the same number appears in the 3x3 grid
// as the final check by subtracting the base row number with the remain of 3 (to isolate the 5 3x3 grids without repipition)

void printBF(int board[9][9])
{
    printf("\n Bruteforcing \n");
    for (int i = 0; i < 9; i++)
    {
        for (int j = 0; j < 9; j++)
        {
            if (board[i][j] == 0)
                printf(".");
            else
                printf("%d", board[i][j]);
        }
        printf("\n");
    }
    fflush(stdout);
}

//was not orignally planned, but i wanted to see the brute force progress so i used the 2 for loops as usual to register the values, making a . for every 0 instead.
// this would be used to print the board for every solve or backtracked, which will be used in the solve function. 
// fflush(stdout) is used to slow down the output a bit for visualisation.

int solve(int board[9][9])
{
    int row,col;
    if (!find_empty(board, &row, &col)) //I keep forgeting this but the ! qcan be used as a ture or false statement, where in this case, if no empty cells are found, and returns a true value, then the grid would be solved, returning a true value
    {
        return 1;
    }
    for (int num = 1; num <= 9; num++)
    {
        if (check_add_remove(board, row, col, num))
        {
            board[row][col] = num;
            printBF(board);
            if (solve(board))
            {
                return 1;
            }
            board[row][col] = 0;
            printBF(board);
        }
    }
    return 0;
}
// In Solve, we reset row, and col, while also using the find_empty function each check to check whether it had been solved
// before the add/remove/check function can process the next value.
// after that, a for statement had been added, counting the num which would loop each time it reached 9 (starting from 1), causing it to contiuously bruteforce 
// with the assistance of the false output, which backtracks the value. 
// Now that im thinking about it, the bruteforce method resembles a depth first search, DFS, which starts at the origin and countinues with its route
// until it reaches the end, which then moves to the closest route.

int main()
{
    int board[9][9];
    printf("Enter The Grid, Seperate with Space (0 represents no number)\n");
    for (int i = 0; i < 9; i++)
    {
        for (int j = 0; j < 9; j++) //Im lwk a DumbA**, the program didnt start since my scanf
        {
            scanf("%d", &board[i][j]);
        }
                
    }
    if(solve(board))
    {
        printf("solved Board\n");
        for (int i = 0; i < 9; i++)
        {
            for(int j = 0; j < 9; j++)
            {
                printf("%d", board[i][j]); //there was a segmentation fault that occured, which was the fault where i did for(int j = 0; j < 9; i++) where the i was supposed to be the j. THe error caused the program to attempt to access memory outside of the allocated arrary. oops
                
            }
            printf("\n");
        }
    }
    else
    {
        printf("No Solution\n");
    }
    return 0;
}

//in main, the board data structure is made beforehand for organisation purposed (dont ask why it wasnt done with the rest)
// main handles the scaning of data structures rather than a function as it was not as needed (comapred to the visual effects :>) by using the for loops to scan for all values in each arrary point
// once done, the solve function is put in a true/false statment, where it would recursively call the check_add_remove function until it is solved, based on the find_empty and read_grid functions

// In this excersise i learnt that i still have a long awy ahead if i wanted to get into low-level systems, so i will go into more indepth c programing instead of simple logic excerices next. mabye after python though lol. 
//Completed January 29th 2026 1 am 7+

// Sample Input 
// 5 3 0 0 7 0 0 0 0
// 6 0 0 1 9 5 0 0 0
// 0 9 8 0 0 0 0 6 0
// 8 0 0 0 6 0 0 0 3
// 4 0 0 8 0 3 0 0 1
// 7 0 0 0 2 0 0 0 6
// 0 6 0 0 0 0 2 8 0
// 0 0 0 4 1 9 0 0 5
// 0 0 0 0 8 0 0 7 9

// Sample Output
//534678912
//672195348
//198342567
//859761423
//426853791
//713924856
//961537284
//287419635
//345286179
// possible to add space but atp, its more work to scroll up than to write this.