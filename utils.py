def int_to_heptal(n):
    digits = []
    while n:
        n, remainder = divmod(n, 7)
        digits.append(str(remainder))
    # fix length of 9 digits
    while len(digits) < 9:
        digits.append('0')
    return ''.join(digits) or '000000000'

# moves = [up, down, lft, rgt]
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

move_mappings = {
    (1,0): up,
    (-1,0): down,
    (0,1): lft,
    (0,-1): rgt
}

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

def find_position_of_blank_tile_from_numeric_grid(u):
    # print("int_to_heptal(x)", int_to_heptal(x))
    # print("pw ", [[int_to_heptal(pw[i][j]) for j in range(3)] for i in range(3)])
    for i in range(3):
        for j in range(3):
            # print(int_to_heptal(pw[i][j])) 
            # print( "i",i,"j",j, "x",int_to_heptal(x), "x//pw[i][j]", int_to_heptal(x // pw[i][j]), "(x // pw[i][j]) % 7", (x // pw[i][j]) % 7)
            if (u // pw[i][j]) % 7 == 0:
                x, y = i, j
                # break
    return x, y