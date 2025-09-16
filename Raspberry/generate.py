import random


# validating the grid
def check_valid(mesh,r,c,n):
    valid = True
    #check row and column
    for x in range(9):
        if mesh[x][c] == n:
            valid = False
            break
    for y in range(9):
        if mesh[r][y] == n:
            valid = False
            break
    row_section = r // 3
    col_section = c // 3
    for x in range(3):
        for y in range(3):
            #check if section is valid
            if mesh[row_section * 3 + x][col_section * 3 + y] == n:
                valid = False
                break
    return valid


def generatePuzzle(difficulty):
    level = difficulty
    if level=="0":
        q = random.randrange(30, 40)
    elif level=="1":
        q = random.randrange(18, 25)
    else:
        q = random.randrange(8, 15)
    #place to store the grid

    grid = [[0 for x in range(9)] for y in range(9)]
    
    # generating random values for the grid
    for i in range(q):
        row = random.randrange(9)
        col = random.randrange(9)
        num = random.randrange(1,10)
        while not check_valid(grid,row,col,num) or grid[row][col]!=0:
            row = random.randrange(9)
            col = random.randrange(9)
            num = random.randrange(1,10)
        grid[row][col]=num


    # print the grid
    stringGrid = ""
    li2 = sum(grid,[])
    stringGrid = ''.join(str(item) for innerlist in grid for item in innerlist)
    print(stringGrid)
    return stringGrid

# cnt_i = 0
# for i in range(13):
#     cnt_j = 0
#     for j in range(13):
#         if i%4==0:
#             print("+---------+---------+---------+",end="")
#             cnt_i+=1
#             break
#         elif j%4==0:
#             print("|",end="")
#             cnt_j+=1
#         else:
#             print("",grid[i-cnt_i][j-cnt_j],"" ,end="")
#     print()
