// Trying no padding in this implementation
//

// moves represented as {T,0,1,0b0111111} for shape, x, y, bitmap of what's in the bag 
//metrics are functions that take boards and return floats based on something or other
//Board (*get_boards(Board board, char piece)[HEIGHT];

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

void display_board(Board board);

Rotation *p_rot_from_move(Move move){
  Shape4 *p_shape;
  int num_rots = 0;
  switch (move.piece) {
    case 'O': num_rots = 1; p_shape = (Shape4 *) &O; break;
    case 'I': num_rots = 2; p_shape = (Shape4 *) &I; break;
    case 'S': num_rots = 2; p_shape = (Shape4 *) &S; break;
    case 'Z': num_rots = 2; p_shape = (Shape4 *) &Z; break;
    case 'J': num_rots = 4; p_shape = &J; break;
    case 'L': num_rots = 4; p_shape = &L; break;
    case 'T': num_rots = 4; p_shape = &T; break;
  }
  Rotation *p_rot = &(*p_shape)[move.r];
  //printf("rotation: %d", (*p_rot)[0][0]);
  return p_rot;
};

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

//TODO figure out which of these is better, and just use that one
bool move_fits_on_board(Board board, Move move){
  //todo try using a larger board representation so we never have to bounds check, see if that's faster
  //todo try using mutable board state instead of many boards
  Rotation *p_r = p_rot_from_move(move);
  bool at_rest = false;
  for (int p = 0; p < 4; p++){
    int xpos = move.x + (*p_r)[p][0];
    int ypos = move.y + (*p_r)[p][1];
    if (xpos < 0 || ypos < 0 || xpos >= WIDTH || ypos >= HEIGHT){
      //printf("rot out of bounds");
      return false;
    }
    if (board[ypos][xpos]){
      return false;
    }
    if (!at_rest && (ypos == HEIGHT-1 || board[ypos + 1][xpos])){
      at_rest = true;
    }
  }
  return at_rest;
};

void add_move_to_board_unsafe(Board board, Move move){
  Rotation *p_r = p_rot_from_move(move);
  for (int p = 0; p < 4; p++){
    int xpos = (*p_r)[p][0] + move.x;
    int ypos = (*p_r)[p][1] + move.y;
    board[ypos][xpos] = 1;
  }
};

bool add_move_to_board(Board board, Move move){
  if (move_fits_on_board(board, move)){
    add_move_to_board_unsafe(board, move);
    return true;
  }
  return false;
};

float eval_move(Board board, Move move, int num_metrics, p_Metric metrics[], int metric_weights[]){
  //todo benchmark creating new arrays conditionally vs always
  int num_rots = 0;
  //question do I really need to cast here?
  Board *p_use_board = (Board *) board;
  Rotation *p_rot = p_rot_from_move(move);
  bool lines_affected[HEIGHT] = { 0 }; //missing entries will be filled in with zeros apparently?
  bool lines_cleared[HEIGHT] = { 0 };
  for (int p = 0; p < 4; p++){
    //todo work through why the parens are needed around *p_shape) here
    int xpos = move.x + (*p_rot)[p][0];
    int ypos = move.y + (*p_rot)[p][1];
    //printf("placing block at %d %d\n", xpos, ypos);
    lines_affected[ypos] = true;
    board[ypos][xpos] = 1;
  }
  bool need_copy = false;
  for (int h = HEIGHT - 1; h >= 0; h--){
    if (!lines_affected[h]){continue;}
    for (int w = 0; w < WIDTH; w++){
      if (!board[h][w]){break;}
      if (w == WIDTH - 1){
        need_copy = true;
        lines_cleared[h] = 1;
      }
    }
  }

  // undoing line clears seems like hard work, so use a temp board if we need it,
  // but otherwise don't bother using a new grid for efficiency
  // TODO find out if this is true, it complicates the code a bit
  // to do this conditional temp board thing
  if (need_copy){
    p_use_board = malloc(sizeof(Board));
    memcpy(p_use_board, &board, sizeof(Board));
  }
  // TODO later for efficiency maybe: return references to the new board if applicable

  int row_to_move_to = HEIGHT;
  for (int h = HEIGHT - 1; h >= 0; h--){
    if (lines_cleared[h]){
      continue;
    } else {
      row_to_move_to--;
    }
    if (row_to_move_to == h){
      continue;
    }
    for (int w = 0; w < WIDTH; w++){
      //since we're careful about never reading the same row after it's been written, this is ok
      (*p_use_board)[row_to_move_to][w] = board[h][w];
    }
  }
  row_to_move_to--;
  while (row_to_move_to >= 0){
    for (int w = 0; w < WIDTH; w++){
      (*p_use_board)[row_to_move_to][w] = 0;
    }
    row_to_move_to--;
  }
        
  float total = 0.0;
  for (int i = 0; i < num_metrics; i++){
    total += (*metrics[i]) (*p_use_board);
  }

  // fixing up the board to be in its previous state
  for (int p = 0; p < 4; p++){
    int xpos = move.x + (*p_rot)[p][0];
    int ypos = move.y + (*p_rot)[p][1];
    board[ypos][xpos] = 0;
  }
  return total;
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

static Board *p_board_for_move_generator;
static int x_for_move_generator;
static int y_for_move_generator;
static int r_for_move_generator;
static Move move_for_move_generator;
static Board allowedMoves[4]; // indexed by [rotation][row][column]
void use_board_for_move_generator(Board *p_board, Piece piece){
  p_board_for_move_generator = p_board;
  move_for_move_generator.piece = piece;
  move_for_move_generator.x = -1;
  move_for_move_generator.y = 0;
  move_for_move_generator.r = 0;
  for (h = 0; h < HEIGHT; h++){
    for (w = 0; w < WIDTH; w++){
      for (r = 0; r < 4; r++){
        allowedMoves[r][h][w] = 0;
      }
    }
  }
}

Move next_move(){
  move_for_move_generator.x++;
  if (move_for_move_generator.x == WIDTH){
    move_for_move_generator.x = 0;
    move_for_move_generator.y++;
  }
  if (move_for_move_generator.y >= HEIGHT){
    move_for_move_generator.piece = '-';
  }
  return move_for_move_generator;
};

Move next_valid_move(){
  Move move;
  while (true){
    next_move();
    if (move_for_move_generator.piece == '-'){
      return move_for_move_generator;
    }
    if (!move_fits_on_board(*p_board_for_move_generator, move_for_move_generator)){
      continue;
    }
    // all pieces start at 4 over, 2 down, r 0


      return move_for_move_generator;
    }
    //printf("move not valid: %c, r:%d, (%d, %d)\n", move_for_move_generator.piece, move_for_move_generator.r, move_for_move_generator.x, move_for_move_generator.y);
  }
};

int main()
{
  Rotation *p_r = &(O[0]);
  display_rotation(*p_r);
  Board *p_b = (Board *) calloc(1, sizeof(Board));
  display_board(*p_b);
  (*p_b)[HEIGHT-1][2] = 1;
  (*p_b)[HEIGHT-2][2] = 1;
  (*p_b)[HEIGHT-1][3] = 1;
  (*p_b)[HEIGHT-1][4] = 1;
  display_board(*p_b);

  p_Metric metrics[2];
  metrics[0] = linear_penalty;
  metrics[1] = num_blocks;
  int weights[2] = {1.0, 1.0};
  
  float score;
  use_board_for_move_generator(p_b, 'O');
  Move m;
  while (true){
    m = next_valid_move();
    //printf("next valid move: %c, r:%d, (%d, %d)\n", m.piece, m.r, m.x, m.y);
    if (m.piece == '-'){
      break;
    }
    score = eval_move(*p_b, m, 2, metrics, weights);
    printf("score of move %c, r:%d, (%d, %d): %f\n", m.piece, m.r, m.x, m.y, score);
  }
};
