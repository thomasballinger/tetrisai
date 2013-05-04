// Trying no padding in this implementation
//

#include <stdio.h>
#include <stdlib.h>

typedef enum { false, true } bool;
typedef char Piece;

#define WIDTH 10
#define HEIGHT 4

typedef struct {
  Piece piece;
  int r;
  int x;
  int y;
  int bag;
} Move;

typedef int Pos[2];
typedef Pos Rotation[4];
typedef Rotation Shape1[1];
typedef Rotation Shape2[2];
typedef Rotation Shape4[4];

// these {1,2,4} rotations of 4 pairs of (x, y) positions
//question Why can't I initialize these as {{1, 2}, {3, 4}, ...}?
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
typedef float (*p_Metric)(Board board);

float linear_penalty(Board board){
  int total = 0;
  for (int h = 0; h < HEIGHT; h++){
    for (int w = 0; w < WIDTH; w++){
      total += board[h][w] * (HEIGHT - h);
    }
  }
  return (float) total;
}

float num_blocks(Board board){
  int total = 0;
  for (int h = 0; h < HEIGHT; h++){
    for (int w = 0; w < WIDTH; w++){
      total += board[h][w];
    }
  }
  return (float) total;
}

static Board blank;
void initialize(){
  for (int h = 0; h < HEIGHT; h++){
    for (int w = 0; w < WIDTH; w++){
      blank[h][w] = 0;
    }
  }
};

bool rot_fits_on_board(Board board, Rotation r, int x, int y){
  //todo try using a larger board representation so we never have to bounds check, see if that's faster
  //todo try using mutable board state instead of many boards
  bool at_rest = false;
  for (int p = 0; p < 4; p++){
    int xpos = x + r[p][0];
    int ypos = y + r[p][1];
    //printf("xpos:%d", xpos);
    //printf("ypos:%d", ypos);
    //printf("WIDTH:%d", WIDTH);
    //printf("HEIGHT:%d", HEIGHT);
    if (xpos < 0 || ypos < 0 || xpos >= WIDTH || ypos >= HEIGHT){
      //printf("rot out of bounds");
      return false;
    }
    if (board[ypos][xpos]){
      //printf("board filled at position (%d, %d)", xpos, ypos);
      return false;
    }
    if (!at_rest && ypos == HEIGHT-1 && board[ypos + 1]){
      at_rest = true;
    }
  }
  //printf("rot is at rest: %d", at_rest);
  return at_rest;
};

void add_rot_to_board_unsafe(Board board, Rotation r, int x, int y){
  for (int p = 0; p < 4; p++){
    int xpos = r[p][0] + x;
    int ypos = r[p][1] + y;
    board[ypos][xpos] = 1;
  }
};

bool add_rot_to_board(Board board, Rotation r, int x, int y){
  if (rot_fits_on_board(board, r, x, y)){
    add_rot_to_board_unsafe(board, r, x, y);
    return true;
  }
  return false;
};

void remove_rot_from_board(Board board, Rotation r, int x, int y){
  for (int p = 0; p < 4; p++){
    int xpos = r[p][0] + x;
    int ypos = r[p][1] + y;
    board[ypos][xpos] = 0;
  }
};

//todo - make a move, call eval_move, unmake the move in the move_finder function
float eval_move(Board board, Move move, int num_metrics, p_Metric metrics[], int metric_weights[]){
  int num_rots = 0;
  Shape4 *p_shape;
  switch (move.piece) {
    case 'O': num_rots = 1; p_shape = (Shape4 *) &O; break;
    case 'I': num_rots = 2; p_shape = (Shape4 *) &I; break;
    case 'S': num_rots = 2; p_shape = (Shape4 *) &S; break;
    case 'Z': num_rots = 2; p_shape = (Shape4 *) &Z; break;
    case 'J': num_rots = 4; p_shape = &J; break;
    case 'L': num_rots = 4; p_shape = &L; break;
    case 'T': num_rots = 4; p_shape = &T; break;
  }
  for (int r = 0; r < num_rots; r++){
    for (int p = 0; p < 4; p++){
      int xpos = move.x + *p_shape[move.r][p][0];
      int ypos = move.y + *p_shape[move.r][p][1];
      board[ypos][xpos] = 1;
    }
  }


  float total = 0.0;
  for (int i = 0; i < num_metrics; i++){
    total += (*metrics[i]) (board);
  }
  return total;
};
// if that move clears lines, make a new board to use in the metrics

// given a board,
//   find all legal moves
//   evaluate them with eval_move
//     eval_move will build a new board to run the metrics on if lines cleared
//     todo later for efficiency maybe: return references to the new board if applicable
//   choose k moves to take forward
//   <probabilistic node here>
//   for each of the k moves,
//     build a new board
//     find all legal moves
//     evaluate them
//     choose k to take forward
//
// metrics are functions that take boards and return floats based on something or other


// moves represented as {T,0,1,0b0111111} for shape, x, y, bitmap of what's in the bag 

//Board (*get_boards(Board board, char piece)[HEIGHT];


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
  for (int h = 0; h < 4; h++){
    printf("\n");
    for (int w = 0; w < 4; w++){
      char c = '.';
      for (int p = 0; p < 4; p++){
        if (rot[p][0] == h && rot[p][1] == w){
          c = 'X';
        }
      }
      printf("%c", c);
    }
  }
  printf("\n");
};

int main()
{
  initialize();
  Rotation *p_r = &(O[0]);
  display_rotation(*p_r);
  Board *p_b = (Board *) calloc(1, sizeof(Board));
  display_board(*p_b);
  //add_rot_to_board_unsafe(*p_b, *p_r, 1, 1);
  add_rot_to_board(*p_b, *p_r, 1, HEIGHT-2);
  display_board(*p_b);

  p_Metric metrics[2];
  metrics[0] = linear_penalty;
  metrics[1] = num_blocks;
  int weights[2] = {1.0, 1.0};
  
  Move move;
  move.piece = 'O';
  move.x = 1;
  move.y = 0;
  move.bag = 0b01111111;
  move.r = 0;

  float score = eval_move(*p_b, move, 2, metrics, weights);
  printf("score: %f", score);
};
