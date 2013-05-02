#DEFINE UNKNOWN 0
#DEFINE PLAYER1 1
#DEFINE PLAYER1 2
#DEFINE TIE 3


class TicTacToe{
  public:
    TicTacToe();
    bool make_move(int x, int y, int player);
    int winner();
    void display();
  private:
    static int width;
    static int height;
    static int wins[24];
    int board[9];
    int turn;
};

TicTacToe::TicTacToe(): width(3), height(3), turn(0), board(){}

bool make_move(int x, int y, int player){
  if (x < 0 || x > 2){ return false; }
  if (y < 0 || y > 2){ return false; }
  if (player != turn){ return false; }
  if (board[y*3+x] == 0){
    board[y*3+x] = player;
    turn = turn % 2 + 1;
  } else {
    return false;
  }
}
int winner(){
  return 0;
}
void display(){
  for (int i = 0; i<8; i++) {
    for (int p = 0; p < 2; p++) {
      int player = {PLAYER1, PLAYER2}[p];
      int sum = 0;
      for (int s = 0; s < 3; s++) {
        if (player == board[pos]

  }
}

