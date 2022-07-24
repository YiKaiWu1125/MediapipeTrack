
arr = []
arr.append([[0 for i in range(2)]for j in range(3)])
arr.append([[0 for i in range(2)]for j in range(3)])
arr[0][1][0] = 5
print(arr)