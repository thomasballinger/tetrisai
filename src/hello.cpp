#include <iostream>
#include "hello.h"

// questions for later
// how do c++ classes work? Are insteances always on the heap?
// how do superclass constructors get called?
// why public?
// how does const apply to nested (complicated) datatypes?
// ok to return arrays of undetermined length? how to do this?

Shape::Shape(): rotation_matrices(), size(0){}

int Shape::get_size(){
    return size;
}

int (*Shape::get_matrix(int rot)){
    if (rot < 0 || rot > 3){
        return 0;
    }
    return rotation_matrices[rot];
}

int IShape::rot1[] = {0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0};
int IShape::rot2[] = {0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0};
IShape::IShape(){
    size = 4;
    rotation_matrices[0] = rot1;
    rotation_matrices[1] = rot2;
    rotation_matrices[2] = rot1;
    rotation_matrices[3] = rot2;
}

Board::Board(): 

int main()
{
    IShape s;
    //std::cout << "size%s\n";
    printf("%d", s.get_size());
    int *matrix;
    matrix = s.get_matrix(2);
    printf("\n");
    for (int i = 0, size = s.get_size(); i < size; i++){
        for (int j = 0; j < size; j++){
            printf("%d", matrix[i*size+j]);
        }
        printf("\n");
    }
}
