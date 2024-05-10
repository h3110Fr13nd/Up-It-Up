# from collections import deque

# starting_grid = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
# ending_grid = [[6, 6, 6], [6, 0, 6], [6, 6, 6]]

# MX = 40353607

# dist = [-1] * MX
# prv = [-1] * MX

# up = {1: 3, 2: 2, 3: 6, 4: 1, 5: 5, 6: 4}
# down = {1: 4, 2: 2, 3: 1, 4: 6, 5: 5, 6: 3}
# lft = {1: 5, 2: 1, 3: 3, 4: 4, 5: 6, 6: 2}
# rgt = {1: 2, 2: 6, 3: 3, 4: 4, 5: 1, 6: 5}
# pw = [[0] * 3 for _ in range(3)]

# def precom():
#     for i in range(3):
#         for j in range(3):
#             pw[i][j] = 7 ** (i * 3 + j)

# def get_num(v):
#     cur = 0
#     for row in v:
#         for num in row:
#             cur = cur * 7 + num
#     return cur

# def get_grid(x):
#     v = [[0] * 3 for _ in range(3)]
#     for i in range(2, -1, -1):
#         for j in range(2, -1, -1):
#             v[i][j] = x % 7
#             x //= 7
#     return v

# def main():
#     precom()
#     st = get_num(starting_grid)
#     fin = get_num(ending_grid)
#     dist[st] = 0
#     prv[st] = st
#     q = deque([st])
#     while q:
#         u = q.popleft()
#         if u == fin:
#             break
#         x, y = 0, 0
#         for i in range(3):
#             for j in range(3):
#                 if (u // pw[i][j]) % 7 == 0:
#                     x, y = i, j
#         for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < 3 and 0 <= ny < 3:
#                 num = u
#                 l = (u // pw[nx][ny]) % 7
#                 num -= l * pw[nx][ny]
#                 if dx == 1:
#                     num += up[l] * pw[x][y]
#                 elif dx == -1:
#                     num += down[l] * pw[x][y]
#                 elif dy == 1:
#                     num += lft[l] * pw[x][y]
#                 else:
#                     num += rgt[l] * pw[x][y]
#                 if dist[num] == -1:
#                     dist[num] = dist[u] + 1
#                     prv[num] = u
#                     q.append(num)
#     if dist[fin] != -1:
#         print(dist[fin])
#         gg = [fin]
#         while fin != st:
#             gg.append(prv[fin])
#             fin = prv[fin]
#         gg.reverse()
#         for x in gg:
#             grid = get_grid(x)
#             print("--------------------------------------")
#             for row in grid:
#                 for num in row:
#                     if num == 1:
#                         print("1", end="")
#                     elif num == 2:
#                         print("2", end="")
#                     elif num == 3:
#                         print("3", end="")
#                     elif num == 4:
#                         print("4", end="")
#                     elif num == 5:
#                         print("5", end="")
#                     elif num == 6:
#                         print("6", end="")
#                     elif num == 0:
#                         print(".", end="")
#                     else:
#                         print("o", end="")
#                 print()
#             print("--------------------------------------")
#     else:
#         print("not found")

# if __name__ == "__main__":
#     main()


from collections import deque

starting_grid = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]  # Initial grid configuration
ending_grid = [[0, 6, 6], [6, 6, 6], [6, 6, 6]]  # Ending grid configuration

MX = 40353607  # Maximum possible states (size of dist and prv arrays)

dist = [-1] * MX  # Track distances from the starting state (-1 means unvisited) 
prv = [-1] * MX   # Track the predecessor state to reconstruct the path

# Dictionaries defining how tiles change when the blank (0) moves
up = {1: 3, 2: 2, 3: 6, 4: 1, 5: 5, 6: 4}
down = {1: 4, 2: 2, 3: 1, 4: 6, 5: 5, 6: 3}
lft = {1: 5, 2: 1, 3: 3, 4: 4, 5: 6, 6: 2}
rgt = {1: 2, 2: 6, 3: 3, 4: 4, 5: 1, 6: 5}

pw = [[0] * 3 for _ in range(3)]  # Precomputed powers of 7 for grid encoding

def precom():
    # Precalculates powers of 7 for efficient grid-number conversions
    for i in range(3):
        for j in range(3):
            pw[i][j] = 7 ** (i * 3 + j)

def get_num(v):

    # This function converts a grid into a unique numerical representation.
    # Argument (v) is a 3x3 grid represented as a list of lists.
    # This function returns (cur) an integer representing the grid configuration.

    cur = 0
    for row in v:
        for num in row:
            cur = cur * 7 + num
    print(cur)        
    return cur

def get_grid(x):

    # This function converts a numerical representation back into a grid.
    # Argument (x) is an integer representing a particular grid configuration.
    # This function returns (v) a 3x3 grid represented as a list of lists.
    
    v = [[0] * 3 for _ in range(3)]
    for i in range(2, -1, -1):
        for j in range(2, -1, -1):
            v[i][j] = x % 7
            x //= 7
    return v

def main():

    # Implements the Breadth-First Search Algorithm (BFS)
    
    precom()  # Precalculate values for efficiency 
    st = get_num(starting_grid)  # Get numerical representation of the starting grid
    fin = get_num(ending_grid)   # Get numerical representation of the target grid

    dist[st] = 0   # Distance to the starting state is 0  
    prv[st] = st   # The starting state has no predecessor
    q = deque([st])  # Initialize the queue with the starting state

    while q: 
        u = q.popleft()  # Dequeue the next state
        if u == fin:     # Check if we've reached the target state
            break

        x, y = 0, 0 
        # Find the coordinates of the blank tile (0) in the grid 
        for i in range(3):
            for j in range(3):
                if (u // pw[i][j]) % 7 == 0:
                    x, y = i, j

        # Explore possible moves from the current state
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # (down, up, right, left) 
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:  # Check if move is within the grid boundaries
                num = u 
                l = (u // pw[nx][ny]) % 7 
                num -= l * pw[nx][ny]  # Remove old tile value (where blank moves)
 
                # Apply move rules from dictionaries 
                if dx == 1:
                    num += up[l] * pw[x][y]
                elif dx == -1:
                    num += down[l] * pw[x][y]
                elif dy == 1: 
                    num += lft[l] * pw[x][y]
                else:  # dy == -1
                    num += rgt[l] * pw[x][y]

                if dist[num] == -1:  # If the new state is unvisited
                    dist[num] = dist[u] + 1 
                    prv[num] = u
                    q.append(num)

    # Path Reconstruction (If the path is found)
    if dist[fin] != -1:
        print(dist[fin])  # Print the length of the shortest path
        gg = [fin]  # Start building the path from the end 
        while fin != st:
            gg.append(prv[fin])
            fin = prv[fin]
        gg.reverse()  # Reverse the path to get it from start to end

        # Print the grid at each step of the path
        for x in gg:
            grid = get_grid(x)
            print("--------------------------------------")
            for row in grid:
                for num in row:
                    if num == 1:
                        print("1", end="")
                    elif num == 2:
                        print("2", end="")
                    elif num == 3:
                        print("3", end="")
                    elif num == 4:
                        print("4", end="")
                    elif num == 5:
                        print("5", end="")
                    elif num == 6:
                        print("6", end="")
                    elif num == 0:
                        print(".", end="")
                    else:
                        print("o", end="")
                print()
            print("--------------------------------------")
    else:
        print("Not Found")

if __name__ == "__main__":
    main()