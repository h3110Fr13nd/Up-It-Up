from collections import deque

MAX_STATE = 40353607


def int_to_heptal(n):
    digits = []
    while n:
        n, remainder = divmod(n, 7)
        digits.append(str(remainder))
    return ''.join(reversed(digits)) or '0'



dist = [-1] * MAX_STATE
prv = [0] * MAX_STATE

ending_grid = [ 
    [(1, 4), (1, 4), (1, 4)],  # ((0,0) represents the empty cell)
    [(1, 4), (0, 0), (1, 4)],  
    [(1, 4), (1, 4), (1, 4)]   
] 

starting_grid = [ 
    [(6,2),(6,2),(6,2)],  # ((0,0) represents the empty cell)
    [(6,2),(0,0),(6,2)],  
    [(6,2),(6,2),(6,2)]   
]

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
      (6,2):(2,1), (6,3):(3,1), (6,4):(4,1), (6,5):(5,1)} 

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
      (6,2):(3,1), (6,3):(5,3), (6,4):(2,4), (6,5):(4,5) }

pw = [[0] * 3 for _ in range(3)]  

def precompute():
    # Precalculates powers of 7 for efficient grid-number conversions
    for i in range(3):
        for j in range(3):
            pw[i][j] = 7 ** (i * 3 + j)
#     print('Precompute',pw)        


def get_num(v):

    # This function converts a grid into a unique numerical representation.
    # Argument (v) is a 3x3 grid represented as a list of lists.
    # This function returns (cur) an integer representing the grid configuration.
    cur1, cur2 = 0, 0
    for i in range(len(v)):
        for k in v[i]:
            cur1 = cur1 * 7 + k[0]
            cur2 = cur2 * 7 + k[1]
#     print('Cur1, Cur2',cur1,cur2)
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

import pickle


def main():

    # Implements the Breadth-First Search Algorithm (BFS)
    
    precompute()  # Precalculate values for efficiency 
    st = get_num(starting_grid)  # Get numerical representation of the starting grid -> (top, front)
    fin = get_num(ending_grid)   # Get numerical representation of the target grid -> (top, front)
    
    # Convert the state tuple to an index
    # index = hash(st) % MAX_STATE
    s1 = st[0] 
    f = fin[0]
    # Set the distance of the state to 0
    dist[s1]= 0

    # Set the previous state of st as st
    prv[s1] = s1

    # Initialize the queue with st as its first element
    q = deque([st])
    q_copy = {}

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
        if len(q) >= 10000000:
            with open('queue2', 'wb') as f:
                pickle.dump(q, f)
                break
                

        # print('q',list(map(lambda x: (int_to_heptal(x[0]), int_to_heptal(x[1])),list(q))))
        q1 = q.popleft()

        # if q1 in q_copy:
        #     continue

        u = q1[0]  # Dequeue the next state
        u1 = q1[1]

        # print('q',q)
        # print('i1',i1)
      #   print('u',u)
      #   print('u1',u1)

        if u == fin[0]:
            print("Solution Found")   # Check if we've reached the target state
            break
        
        x, y = 0, 0 
        # Find the coordinates of the blank tile (0) in the grid 
        for i in range(3):
            for j in range(3):
                if (u // pw[i][j]) % 7 == 0:
                    x, y = i, j
                    # print(x,y)

        # Explore possible moves from the current state
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # (down, up, right, left) 
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:  # Check if move is within the grid boundaries
                num = u 
                num1 = u1
                l = (u // pw[nx][ny]) % 7
                l1 = (u1 // pw[nx][ny]) % 7
            #     print('l, l1',l,l1)

                num -= l * pw[nx][ny]  # Remove old tile value (where blank moves)
                num1 -= l1 * pw[nx][ny]

                # Apply move rules from dictionaries 
                if dx == 1:
                    k1 = up[(l, l1)]
                    num += k1[0] * pw[x][y]
                    num1 += k1[1] * pw[x][y]
                    st1=(num,num1)

                elif dx == -1:
                    k2 = down[(l, l1)]
                    num += k2[0] * pw[x][y]
                    num1 += k2[1] * pw[x][y]   
                    st1=(num,num1)

                elif dy == 1: 
                    k3 = lft[(l, l1)]
                    num += k3[0] * pw[x][y]
                    num1 += k3[1] * pw[x][y]
                    st1=(num,num1)

                else:  # dy == -1
                    k4 = rgt[(l, l1)]
                    num += k4[0] * pw[x][y]
                    num1 += k4[1] * pw[x][y]
                    st1=(num,num1)
                
                # print(st1 in q_copy)
                if st1 not in q_copy:
                    q_copy[st1] = (u,u1)
                    q.append(st1)
                    # print('q',list(map(lambda x: (int_to_heptal(x[0]), int_to_heptal(x[1])),list(q))))



                if dist[num] == -1:  # If the new state is unvisited
                # if (num,num1) not in q_copy:
                    dist[num] = dist[u] + 1 
                    prv[num] = u
                    q.append(st1)


    print('q',list(map(lambda x: (int_to_heptal(x[0]), int_to_heptal(x[1])),list(q))))
    # print('q_copy',list(map(lambda x: (int_to_heptal(x[0]), int_to_heptal(x[1])),list(q_copy))))
    print(len(q_copy))
    print(q_copy)

    
    # Path Reconstruction (If the path is found)
    print(fin[0])
    print(dist[fin[0]])
    
    if dist[fin[0]] != -1:
        print(dist[fin[0]])  # Print the length of the shortest path
        gg = [fin[0]]  # Start building the path from the end 
    #   #   print('gg',gg)
    #   #   print('Fin', fin[0])
    #   #   print('st[0]',st[0])
    #   #   print (prv[a1])
        
        count = 0
        while (f != st[0]):
            gg.append(prv[f])
            f = prv[f]
            # print(a1)

            count+=1
            # if (count==50):
                # break
            
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

