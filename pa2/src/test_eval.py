max_row_sum = -1.0
max_col_sum = -1.0
diag_max_sum_dr = 0.0
diag_max_sum_ul = 0.0

K = 4
'''
b = (
        (1),
        (0),
        (1),
        (1),
        (2),
        (2),
        (1),
        (2),
        (2),
        (2),
        (0)
    )
'''

'''
b = (
        (1,0,0,1,2,2,1,1,1,1,2,1,2),
        (0,2,1,1,2,2,1,0,0,0,0,1,2),
        (1,2,1,2,1,2,1,2,1,2,1,2,1),
        (0,1,1,2,1,2,2,2,2,2,2,2,2),
        (1,1,1,1,1,1,1,2,2,2,2,2,2),
        (2,2,2,2,1,1,1,1,0,0,0,1,1),
        (2,2,2,2,0,0,0,0,1,1,2,1,2)
)
'''
'''
b = (
        (0,0,0,0,0,0),
        (0,0,0,0,0,0),
        (0,0,0,0,0,0),
        (0,0,0,0,0,0)
)
'''

#b = ((0,0,0,0,0,0,0))
#b = ((0,0,2),(0,2,1),(0,0,0),(1,0,0))
#b = (
      #(0,0,2,1,1,1,1,0,1,1,1,1,1,1,2,0,1,0),
      #(0,0,2,1,1,1,1,0,1,1,1,1,1,1,2,0,1,0),
      #(0,0,2,1,1,1,1,0,1,1,1,1,1,1,2,0,1,0)
      #)
b = ((0,1,1,1),
     (0,1,0,0),
     (0,1,0,1),
     (0,1,0,1))
color = 1

for x in b:
    print x

for row in b:
    cur_sum = 0
    cur_max = 0
    for it in row:
        if it == color:
            cur_sum += 1
        else:
            cur_max = max(cur_sum,cur_max)
            cur_sum = 0

    #max_row_sum = max(sum([1 for pos in row if pos==color]),max_row_sum)
    max_row_sum = max(max_row_sum, cur_max, cur_sum)

# Column search
for j in range(len(b[0])):
    cur_sum = 0
    cur_max = 0
    for i in range(len(b)):
        if b[i][j] == color:
            cur_sum += 1
        else:
            #print "cs",cur_sum,"cur_max",cur_max
            cur_max = max(cur_sum,cur_max)
            cur_sum = 0
            
    max_col_sum = max(max_col_sum, cur_max, cur_sum)

# Diag search
diag_count = len(b[0]) + len(b) - 1
diag_x_s, diag_y_s = (0,0)
x,y = (diag_x_s,diag_y_s)
# up left
for z in range(diag_count):
    cur_max = 0
    cur_sum = 0
    while(x >= 0 and y <= len(b[0]) - 1):
        if b[x][y] == color:
            cur_sum += 1
        else:
            cur_max = max(cur_max, cur_sum)
            cur_sum = 0
        x -= 1
        y += 1

    if diag_x_s < len(b) - 1:
        diag_x_s += 1
    else:
        diag_y_s += 1

    x,y = (diag_x_s,diag_y_s)
    diag_max_sum_ul = max(diag_max_sum_ul, cur_max, cur_sum)

# down right
diag_x_s, diag_y_s = (len(b[0])-1,0)
x,y = (diag_x_s,diag_y_s)
for z in range(diag_count):
    cur_sum = 0
    cur_max = 0
    while(x <= len(b[0])-1 and y <= len(b) - 1):
        if b[y][x] == color:
            cur_sum += 1
        else: 
            cur_max = max(cur_max, cur_sum)
            cur_sum = 0
        x += 1
        y += 1

    if diag_x_s > 0:
        diag_x_s -= 1
    else:
        diag_y_s += 1

    x,y = (diag_x_s,diag_y_s)
    diag_max_sum_dr = max(diag_max_sum_dr, cur_max, cur_sum)

print "k",K,"dr",diag_max_sum_dr,"ul",diag_max_sum_ul,"col",max_col_sum,"row",max_row_sum
print (float(max(diag_max_sum_dr, diag_max_sum_ul, max_col_sum, max_row_sum))/ K)
