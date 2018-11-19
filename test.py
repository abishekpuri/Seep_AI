import math

a = [[0,0.125,0.125],[0.5,0,0.125],[0.125,0,0]]
s = 0
for i in range(0,3):
    for j in range(0,3):
        x_and_y = a[i][j]
        x_given_y = a[i][j]/sum([b[j] for b in a])
        if x_and_y == 0:
            continue
        print(str(i+1),str(j+1),x_and_y,math.log(x_given_y,2))
        s += x_and_y*math.log(x_given_y,2)
print(s)
