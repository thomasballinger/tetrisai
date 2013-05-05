Tetris ai

General todo:

* do enough research to defend the genetic algorithm approach
* read about probabilistic nodes in expectiminmax trees - think about utility


Done in c
---------

* get all valid moves for a board and a piece spec
* evaluate a move given a board, move spec, and metrics


TODO in the c
-------------

* check that moves are actually accessible, not just open
* simple choose best move for simple alg function
* make a header file
* python interface
* implement more metrics
* simulation setup
* start benchmarking so refactors can be based on data

* lookahead
  * choose k best moves to take forward
  * use a probabilistic node 
  * for each of the k moves,
    * build a new board
    * find all legal moves
    * evaluate them
    * choose k to take forward
