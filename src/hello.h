class Shape {
  public:
    Shape();
    int get_size();
    int *get_matrix(int rot);
  protected:
    int size;

    // an array[4] of pointers to arrays of ints
    int *rotation_matrices[4];
};

class Board {
  public:
    Board(int width, int height, int shape_max_size);
    bool is_occupied(int x, int y);
    bool valid_locations(Shape *shape);
    int place_shape(Shape *shape, int x, int y, int rot);
  private:
   static int width;
   static int height;
   int board[];
};

class IShape : public Shape {
  public:
    IShape();
  private:
    static int rot1[16];
    static int rot2[16];
};
