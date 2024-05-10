from collections import deque
from utils import int_to_heptal, up, down, lft, rgt, pw, move_mappings, precompute, get_num, get_grid, get_single_grid, find_position_of_blank_tile_from_numeric_grid

dist_front = {}
prev_front = {}
dist_back = {}
prev_back = {}
grid_1 = [ 
    [(1, 4), (1, 4), (1, 4)],  # ((0,0) represents the empty cell)
    [(1, 4), (0, 0), (1, 4)],  
    [(1, 4), (1, 4), (1, 4)]   
] 
grid_2 = [ 
    [(6,2),(6,2),(6,2)],  
    [(6,2),(0,0),(6,2)],  
    [(6,2),(6,2),(6,2)]   
]


def main():
    precompute()
    start_front = get_num(grid_1)
    end_front = get_num(grid_2)
    start_back = end_front
    end_back = start_front

    start_front_top = start_front[0]
    end_front_top = end_front[0]

    start_back_top = start_back[0]
    end_back_top = end_back[0]

    dist_front[start_front] = 0
    prev_front[start_front] = start_front

    dist_back[start_back] = 0
    prev_back[start_back] = start_back

    queue_front = deque([start_front])
    queue_back = deque([start_back])
    common_set = set(list(dist_front.keys()) + list(dist_back.keys()))
    # print("Common Set",common_set)


    meet = False
    meet_state = None
    # print([[int_to_heptal(j) for j in i] for i in pw])
    while not meet and (queue_front or queue_back):
        if queue_front:
            cur_front = queue_front.popleft()
            # print("Cur Front",int_to_heptal(cur_front[0]), int_to_heptal(cur_front[1]))
            cur_front_top = cur_front[0]
            cur_front_front = cur_front[1]
            if cur_front_top == end_front_top:
                meet = True
                break
            x_front, y_front = find_position_of_blank_tile_from_numeric_grid(cur_front_top)
            # print("x_front",x_front,"y_front",y_front)

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                # print("dx",dx,"dy",dy)
                nx_front, ny_front = x_front + dx, y_front + dy
                # print("nx_front",nx_front,"ny_front",ny_front)
                if 0 <= nx_front < 3 and 0 <= ny_front < 3:
                    num_front_top = cur_front_top
                    num_front_front = cur_front_front
                    # print("Num Front",int_to_heptal(num_front_top), int_to_heptal(num_front_front))
                    # print(int_to_heptal(cur_front_top // pw[nx_front][ny_front]), int_to_heptal(cur_front_front // pw[nx_front][ny_front]))
                    l = (cur_front_top // pw[nx_front][ny_front]) % 7
                    l1 = (cur_front_front // pw[nx_front][ny_front]) % 7
                    # print("l",l,"l1",l1)

                    num_front_top -= l * pw[nx_front][ny_front]
                    num_front_front -= l1 * pw[nx_front][ny_front]

                    k1 = move_mappings[(dx, dy)][(l, l1)]
                    num_front_top += k1[0] * pw[x_front][y_front]
                    num_front_front += k1[1] * pw[x_front][y_front]

                    if (num_front_top, num_front_front) not in dist_front:
                        dist_front[(num_front_top, num_front_front)] = dist_front[cur_front] + 1
                        prev_front[(num_front_top, num_front_front)] = cur_front
                        queue_front.append((num_front_top, num_front_front))

                    if (num_front_top, num_front_front) in dist_back:
                        meet = True
                        meet_state = (num_front_top, num_front_front)
                        # print("Num Front",int_to_heptal(num_front_top), int_to_heptal(num_front_front))
                        break
                    # else:
                    #     common_set.add((num_front_top, num_front_front))
                        # print("Common Set", set(map(lambda x: (int_to_heptal(x[0]), int_to_heptal(x[1])), common_set)))




        if queue_back:
            cur_back = queue_back.popleft()
            cur_back_top = cur_back[0]
            cur_back_front = cur_back[1]
            if cur_back_top == end_back_top:
                meet = True
                break
            x_back, y_back = find_position_of_blank_tile_from_numeric_grid(cur_back_top)

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx_back, ny_back = x_back + dx, y_back + dy
                if 0 <= nx_back < 3 and 0 <= ny_back < 3:
                    num_back_top = cur_back_top
                    num_back_front = cur_back_front

                    l = (cur_back_top // pw[nx_back][ny_back]) % 7
                    l1 = (cur_back_front // pw[nx_back][ny_back]) % 7

                    num_back_top -= l * pw[nx_back][ny_back]
                    num_back_front -= l1 * pw[nx_back][ny_back]

                    k1 = move_mappings[(dx, dy)][(l, l1)]
                    num_back_top += k1[0] * pw[x_back][y_back]
                    num_back_front += k1[1] * pw[x_back][y_back]

                    if (num_back_top, num_back_front) not in dist_back:
                        dist_back[(num_back_top, num_back_front)] = dist_back[cur_back] + 1
                        prev_back[(num_back_top, num_back_front)] = cur_back
                        queue_back.append((num_back_top, num_back_front))
                        

                    if (num_back_top, num_back_front) in dist_front:
                        meet = True
                        meet_state = (num_back_top, num_back_front)
                        # print("Num Back",num_back_top, num_back_front)
                        break
                    # else:
                    #     common_set.add((num_back_top, num_back_front))
                        # print("Common Set", set(map(lambda x: (int_to_heptal(x[0]), int_to_heptal(x[1])), common_set)))

        # print(not meet, queue_front, queue_back)


    if meet:
        print(int_to_heptal(meet_state[0]), int_to_heptal(meet_state[1]))
        path = []
        cur = meet_state
        while cur != start_front:
            path.append(cur)
            cur = prev_front[cur]
        path.append(start_front)
        path = path[::-1]
        print([(int_to_heptal(i[0]), int_to_heptal(i[1])) for i in path])
        print('Length:', len(path))
        print([[(i[0].find("0")//3)+1,(i[0].find("0")%3)+1] for i in [(int_to_heptal(i[0]), int_to_heptal(i[1])) for i in path]])


        cur = meet_state
        while cur != start_back:
            cur = prev_back[cur]
            path.append(cur)

        print('Path:', path)
        print('Length:', len(path) - 1)
        print([(int_to_heptal(i[0]), int_to_heptal(i[1])) for i in path])
        print([[(i[0].find("0")//3)+1,(i[0].find("0")%3)+1] for i in [(int_to_heptal(i[0]), int_to_heptal(i[1])) for i in path]])
    else:
        print('No path exists')

if __name__ == '__main__':
    main()
    
