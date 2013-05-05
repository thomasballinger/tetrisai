from cffi import FFI

ffi = FFI()

ffi.cdef("""
        int printf(const char *format, ...);
""")

C = ffi.dlopen(None)
arg = ffi.new("char[]", "world")
C.printf("hi there, %s\n", arg)


# Gist: I want the ability to try out ai techniques, using c functions for representing boards and such
# the functions I want in c:
#   - try these metrics on this move on this board
#   - get all possible moves from this board
#   - get top k moves from this board
#   - going n levels deep, using chance nodes and bag state, get best move
#   

