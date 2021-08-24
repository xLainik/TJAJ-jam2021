
def valid(maze, moves, start_x, start_y):
    i = start_x
    j = start_y
    for move in moves:
        if move == "L": i -= 1
        elif move == "R": i += 1
        elif move == "U": j -= 1
        elif move == "D": j += 1
        if not(0 <= i < len(maze[0]) and 0 <= j < len(maze)):
            return False
        elif (maze[j][i] == "#"):
            return False

    return True

def findEnd(maze, moves, start_x, start_y):
    i = start_x
    j = start_y
    for move in moves:
        if move == "L": i -= 1
        elif move == "R": i += 1
        elif move == "U": j -= 1
        elif move == "D": j += 1
    if maze[j][i] == "X":
        return moves

    return False

    
