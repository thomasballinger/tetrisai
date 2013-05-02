// Trying no padding in this implementation
//

#include <stdio.h>
#include <stdlib.h>

#define WIDTH 10
#define HEIGHT 18

typedef int Pos[2];
typedef Pos Rotation[4];
typedef Rotation Shape1[1];
typedef Rotation Shape2[2];
typedef Rotation Shape4[4];

static Shape1 O = {0, 0, 1, 0, 0, 1, 1, 1};
static Shape2 I = {{0, 2, 1, 2, 2, 2, 3, 2},
                         {1, 0, 1, 1, 1, 2, 1, 3}};
static Shape2 S = {{0, 2, 1, 2,1, 1, 2, 1},
                         {1, 2, 0, 1, 1, 1, 0, 0}};
static Shape2 Z = {{0, 1, 1, 1, 1, 2, 2, 2},
                         {0, 2, 0, 1, 1, 1, 1, 0}};
static Shape4 J = {{2, 2, 2, 1, 1, 1, 0, 1},
                         {0, 2, 1, 2, 1, 1, 1, 0},
                         {0, 0, 0, 1, 1, 1, 2, 1},
                         {2, 0, 1, 0, 1, 1, 1, 2}};
static Shape4 L = {{0, 2, 0, 1, 1, 1, 2, 1},
                         {0, 0, 1, 0, 1, 1, 1, 2},
                         {2, 0, 2, 1, 1, 1, 0, 1},
                         {2, 2, 1, 2, 1, 1, 1, 0}};
static Shape4 T = {{0, 1, 1, 1, 1, 2, 2, 1},
                         {1, 2, 1, 1, 2, 1, 1, 0},
                         {0, 1, 1, 1, 1, 0, 2, 1},
                         {1, 0, 1, 1, 0, 1, 1, 2}};

typedef int Board[HEIGHT][WIDTH];

static Board blank;
void initialize(){
  for (int h = 0; h < HEIGHT; h++){
    for (int w = 0; w < WIDTH; w++){
      blank[h][w] = 0;
    }
  }
};

bool add_shape_to_board(Board board, int x, int y){
  return false;
};

void display_board(Board board){
  for (int h = 0; h < HEIGHT; h++){
    printf("\n");
    for (int w = 0; w < WIDTH; w++){
      printf("%d", board[h][w]);
    }
  }
  printf("\n");
};
void display_rotation(Rotation rot){
  for (int h = 0; h < HEIGHT; h++){
    printf("\n");
    for (int w = 0; w < WIDTH; w++){
      for (int p = 0; p < 4; p++){
        if (rot[p][0] == h && rot[p][1] == w){
          printf("X");
        } else {
          printf(".");
        }
      }
    }
  }
  printf("\n");
};

int main()
{
  initialize();
  Rotation *r = O;
  display_rotation(*r);
  printf("%d", 1);
  Board *b = (Board *) calloc(1, sizeof(Board));
  display_board(*b);
};
