mat = [
    [1, 1, 1],
    [-1, 1, -2],
    [-3, -1, 1]
]

def fn(n):
    n = str(n)
    if len(n) == 1:
        return "  " + n
    elif len(n) == 2:
        return " " + n
    else:
        return n

def det(mat):
    print("           " +
        fn(- mat[0][2] * mat[1][1] * mat[2][0]) + " " +
        fn(- mat[0][0] * mat[1][2] * mat[2][1]) + " " +
        fn(- mat[0][1] * mat[1][0] * mat[2][2]) + " "
        #   fn(mat[0][1] * mat[1][0] * mat[2][2])
        + "= " + str((- mat[0][2] * mat[1][1] * mat[2][0]) + (- mat[0][0] * mat[1][2] * mat[2][1]) + (- mat[0][1] * mat[1][0] * mat[2][2]))
        )
    for i in range(3):
        print(f"{fn(mat[i][0])} {fn(mat[i][1])} {fn(mat[i][2])} {fn(mat[i][0])} {fn(mat[i][1])}")
    print("           " +
        fn(mat[0][0] * mat[1][1] * mat[2][2]) + " " +
        fn(mat[0][1] * mat[1][2] * mat[2][0]) + " " +
        fn(mat[0][2] * mat[1][0] * mat[2][1]) + " "
        + "= " + str((mat[0][0] * mat[1][1] * mat[2][2]) + (mat[0][1] * mat[1][2] * mat[2][0]) + (mat[0][2] * mat[1][0] * mat[2][1]))
        )
    return ((- mat[0][2] * mat[1][1] * mat[2][0]) + (- mat[0][0] * mat[1][2] * mat[2][1]) + (- mat[0][1] * mat[1][0] * mat[2][2])) + ((mat[0][0] * mat[1][1] * mat[2][2]) + (mat[0][1] * mat[1][2] * mat[2][0]) + (mat[0][2] * mat[1][0] * mat[2][1]))

d = "XYZ"

def det_ans(mat, ans):
    print(f"det a: {det(mat)}")
    for i in range(3):
        print()
        print()
        print()
        current = mat
        for j in range(3):
            current[j][i] = ans[j]
        # print(f"det b: {current}")
        # print(f"det c: {det(current)}")
        print(f"det {d[i]}: {det(current)}")



if __name__ == "__main__":
    det_ans(mat, [3, 10, 7])