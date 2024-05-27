from collections import deque

MAX_STATE = 40353607
# MAX_STATE = 40353607  # 7^9 = 40353607
# Considering the front and top its 7**9 * 7**9
# 7 ** 9 * 4 = 282475249

TOTAL_NUMBER_OF_STATES = (6 * 4 + 1) * 9



dist = [-1] * MAX_STATE
prv = [0] * MAX_STATE

starting_grid = [
    [(6,2),(6,2),(6,2)],  # ((0,0) represents the empty cell)
    [(6,2),(0,0),(6,2)],
    [(6,2),(6,2),(6,2)]
]

# ('402446663', '603625231')
ending_grid = [
    [(4,6), (0,0), (2,3)],  # ((0,0) represents the empty cell)
    [(4,6), (4,2), (6,5)],
    [(6,2), (6,3), (3,1)]
]

# starting_grid = [
#     [(1, 4), (1, 4), (1, 4)],  # ((0,0) represents the empty cell)
#     [(1, 4), (0, 0), (1, 4)],
#     [(1, 4), (1, 4), (1, 4)]
# ]

# ending_grid = [
#     [(6,0),(6,0),(6,0)],  # ((0,0) represents the empty cell)
#     [(6,0),(0,0),(6,0)],
#     [(6,0),(6,0),(6,0)]
# ]

up = {(1,2):(2,6), (1,3):(3,6), (1,4):(4,6), (1,5):(5,6),
      (2,1):(1,5), (2,3):(3,5), (2,4):(4,5), (2,6):(6,5),
      (3,1):(1,4), (3,2):(2,4), (3,5):(5,4), (3,6):(6,4),
      (4,1):(1,3), (4,2):(2,3), (4,5):(5,3), (4,6):(6,3),
      (5,1):(1,2), (5,3):(3,2), (5,6):(6,2), (5,4):(4,2),
      (6,2):(2,1), (6,3):(3,1), (6,4):(4,1), (6,5):(5,1) }

down = {(1,2):(5,1), (1,3):(4,1), (1,4):(3,1), (1,5):(2,1),
      (2,1):(6,2), (2,3):(4,2), (2,4):(3,2), (2,6):(1,2),
      (3,1):(6,3), (3,2):(5,3), (3,5):(2,3), (3,6):(1,3),
      (4,1):(6,4), (4,2):(5,4), (4,5):(2,4), (4,6):(1,4),
      (5,1):(6,5), (5,3):(4,5), (5,6):(1,5), (5,4):(3,5),
      (6,2):(5,6), (6,3):(4,6), (6,4):(3,6), (6,5):(2,6) }

lft =  {(1,2):(3,2), (1,3):(5,3), (1,4):(2,4), (1,5):(4,5),
      (2,1):(4,1), (2,3):(1,3), (2,4):(6,4), (2,6):(3,6),
      (3,1):(2,1), (3,2):(6,2), (3,5):(1,5), (3,6):(5,6),
      (4,1):(5,1), (4,2):(1,2), (4,5):(6,5), (4,6):(2,6),
      (5,1):(3,1), (5,3):(6,3), (5,6):(4,6), (5,4):(1,4),
      (6,2):(4,2), (6,3):(2,3), (6,4):(5,4), (6,5):(3,5) }

rgt = {(1,2):(4,2), (1,3):(2,3), (1,4):(5,4), (1,5):(3,5),
      (2,1):(3,1), (2,3):(6,3), (2,4):(1,4), (2,6):(4,6),
      (3,1):(5,1), (3,2):(1,2), (3,5):(6,5), (3,6):(2,6),
      (4,1):(2,1), (4,2):(6,2), (4,5):(1,5), (4,6):(5,6),
      (5,1):(4,1), (5,3):(1,3), (5,6):(3,6), (5,4):(6,4),
      (6,2):(3,2), (6,3):(5,3), (6,4):(2,4), (6,5):(4,5) }

pw = [[0] * 3 for _ in range(3)]

def precompute():
    # Precalculates powers of 7 for efficient grid-number conversions
    for i in range(3):
        for j in range(3):
            pw[i][j] = 7 ** (i * 3 + j)
#     print('Precompute',pw)

def int_to_heptal(n):
    digits = []
    while n:
        n, remainder = divmod(n, 7)
        digits.append(str(remainder))
    return ''.join(reversed(digits)) or '0'

def get_num(v):

    # This function converts a grid into a unique numerical representation.
    # Argument (v) is a 3x3 grid represented as a list of lists.
    # This function returns (cur) an integer representing the grid configuration.
    cur1, cur2 = 0, 0
    for i in range(len(v)):
        for k in v[i]:
            print('K',k)
            cur1 = cur1 * 7 + k[0]
            cur2 = cur2 * 7 + k[1]
    print("heptal",int_to_heptal(cur1),int_to_heptal(cur2))
    return (cur1, cur2)


def get_grid(x):

    # This function converts a numerical representation back into a grid.
    # Argument (x) is an integer representing a particular grid configuration.
    # This function returns (v) a 3x3 grid represented as a list of lists.
    v = []
    for i in range(3):
        row = []
        for j in range(3):
            n1, n2 = 0, 0
            n1 = x[0] % 7
            x[0] //= 7
            n2 = x[1] % 7
            x[1] //= 7

            row.append((n1, n2))
        v.append(row)
      #   print('Grid',v)
    return v

def get_single_grid(x):
    
    v = [[0] * 3 for _ in range(3)]
    for i in range(2, -1, -1):
        for j in range(2, -1, -1):
            v[i][j] = x % 7
            x //= 7
    return v

def find_position_of_blank_tile_from_numeric_grid(x):
    print("int_to_heptal(x)", int_to_heptal(x))
    print("pw ", [[int_to_heptal(pw[i][j]) for j in range(3)] for i in range(3)])
    for i in range(3):
        for j in range(3):
            print(int_to_heptal(pw[i][j])) 
            print( "i",i,"j",j, "x",int_to_heptal(x), "x//pw[i][j]", int_to_heptal(x // pw[i][j]), "(x // pw[i][j]) % 7", (x // pw[i][j]) % 7)
            if (x // pw[i][j]) % 7 == 0:
                x, y = 3 - i, 3 - j
                # break
    return x, y



def main():
    # Implements the Breadth-First Search Algorithm (BFS)
    precompute()  # Precalculate values for efficiency
    st = get_num(starting_grid)  # Get numerical representation of the starting grid
    fin = get_num(ending_grid)   # Get numerical representation of the target grid

    # Convert the state tuple to an index
    index = hash(st) % MAX_STATE

    # Set the distance of the state to 0
    dist[index] = 0

    # Set the previous state of st as st
    prv[index] = st

    # Initialize the queue with st as its first element
    q = deque([st])

    # dist[st] = 0   # Distance to the starting state is 0
    # prv[st] = st   # The starting state has no predecessor
    # q = deque([st])  # Initialize the queue with the starting state

#     print('Dist[st[0]]',dist[st[0]])
#     print('Prv[st[0]]',prv[st[0]])
#     print('Dist',dist)
#     print('Prv',prv)
#     print('q',q)
#     print('q1',q1)
#     print('Fin',fin[0])
#     print('St', st)


    while q:
        q1 = q.popleft()
        i1 = hash(q1) % MAX_STATE

        u = q1[0]  # Dequeue the next state
        u1 = q1[1]

        if u == fin[0]:
            print("Solution Found")   # Check if we've reached the target state
            break

        x,y = find_position_of_blank_tile_from_numeric_grid(u)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # (up, down, left, right)
            print('X',x , 'Y',y)
            print(dx,dy)
            nx, ny = x + dx, y + dy
            print(nx,ny)
            if 0 <= nx < 3 and 0 <= ny < 3:  # Check if move is within the grid boundaries
                num = u
                num1 = u1
                print(int_to_heptal(num),int_to_heptal(num1), nx, ny, dx, dy, pw[nx][ny])
                print(int_to_heptal(u // pw[nx][ny]))
                l = ((u // pw[nx][ny]) % 7)
                print(int_to_heptal(u1 // pw[nx][ny]))
                l1 = ((u1 // pw[nx][ny]) % 7) 
                print('L',l)
                print('L1',l1)
                num -= (l) * pw[nx][ny]  # Remove old tile value (where blank moves)
                num1 -= (l1) * pw[nx][ny]
                print(int_to_heptal(num),int_to_heptal(num1))

                # Apply move rules from dictionaries
                if dx == 1:
                    k1 = up[(l, l1)]
                    num += k1[0] * pw[x][y]
                    num1 += k1[1] * pw[x][y]
                    st1=(num,num1)
                    i2 = hash(st1) % MAX_STATE

                elif dx == -1:
                    k2 = down[(l, l1)]
                    num += k2[0] * pw[x][y]
                    num1 += k2[1] * pw[x][y]
                    st1=(num,num1)
                    i2 = hash(st1) % MAX_STATE

                elif dy == 1:
                    k3 = lft[(l, l1)]
                    num += k3[0] * pw[x][y]
                    num1 += k3[1] * pw[x][y]
                    st1=(num,num1)
                    i2 = hash(st1) % MAX_STATE

                else:  # dy == -1
                    k4 = rgt[(l, l1)]
                    num += k4[0] * pw[x][y]
                    num1 += k4[1] * pw[x][y]
                    st1=(num,num1)
                    i2 = hash(st1) % MAX_STATE
                print("After",int_to_heptal(num),int_to_heptal(num1))
                # u = num
                # u1 = num1

                if dist[i2] == -1:  # If the new state is unvisited
                    dist[i2] = dist[i1] + 1
                    prv[i2] = q1
                    q.append(st1)


    # Path Reconstruction (If the path is found)
    # print(fin[0])
    # print(dist[fin[0]])
    if dist[i1] != -1:
        print(dist[i1])  # Print the length of the shortest path
        gg = [q1[0]]  # Start building the path from the end
    #   #   print('gg',gg)
    #   #   print('Fin', fin[0])
    #   #   print('st[0]',st[0])
        a1 = q1[0]
        a2 = st[0]
        print(a1)
    #   #   print (prv[a1])
        count = 0

        while (a1 != a2):
            i3 = hash(q1) % MAX_STATE
            q1 = prv[i3]
            a1 = q1[0]
            gg.append(a1)

            # print(a1)

            count+=1
            if (count==50):
                break

        gg.reverse()  # Reverse the path to get it from start to end

        # Print the grid at each step of the path
        for x in gg:
            grid = get_single_grid(x)
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

