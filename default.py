import numpy as np
import math
import plot_matrix

eps = 1e-9
A = [
    [2, 1, 0, 0, 0],
    [0, 4, 2, 0, 0],
    [0, 2, 20, 2, 0],
    [0, 1, 1, 26, 1],
    [0, 0, 0, 4, 10]
]


def calc_norm(M, types, ansnum):
    # calculate the frobenius norm when the partition is types
    n = len(types)
    m = max(types) + 1
    typesum = np.zeros(m)
    for i in range(n):
        typesum[types[i]] += ansnum[i] * ansnum[i]
    W = np.zeros((m, n))
    for i in range(n):
        W[types[i]][i] = math.sqrt(ansnum[i] * ansnum[i] / typesum[types[i]])
    L = np.dot(np.dot(W, M), W.T)
    for i in range(m):
        for j in range(i):
            L[i][j] = 0
    return np.linalg.norm(M - np.dot(np.dot(W.T, L), W), "fro")


def calc_order(types, ansnum):
    # trans the partition to optimal order
    mytypes = np.array(types)
    n = len(mytypes)
    res = []
    for i in range(n):
        cur = 0
        for j in range(n):
            if (mytypes[j] < mytypes[cur]) or ((mytypes[j] == mytypes[cur]) and (ansnum[j] > ansnum[cur])):
                cur = j
        mytypes[cur] = n + 1
        res.append(cur)
    return res


def answer_rank_default(MM, ansnum=None, normalize=None):
    # input answer-guess matrix M
    if ansnum is None:
        ansnum = []
    M = np.array(MM)
    if normalize == "all":
        M /= sum(sum(M))
    n, n = M.shape
    if not ansnum:
        ansnum = np.array([M[i][i] for i in range(n)])
    opt_uppersum = np.zeros(2 ** n, dtype=float)
    opt_last = np.zeros(2 ** n, dtype=np.int_)
    Log = dict()
    for i in range(n):
        Log.update({2 ** i: i})
    # main algorithm
    for i in range(2 ** n):
        # enumerate all subsets in a predetermined order
        opt_uppersum[i] = -1
        for j in range(n - 1, -1, -1):
            # enumerate the first answer in the ranking
            if (i >> j) & 1 == 1:
                k = i ^ (1 << j)
                uppersum = opt_uppersum[k]
                while k != 0:
                    uppersum += M[j][Log[k & -k]] * M[j][Log[k & -k]]
                    k -= k & -k
                if (uppersum > opt_uppersum[i] + eps) or (
                        (uppersum > opt_uppersum[i] - eps) and (ansnum[j] > ansnum[opt_last[i]])):
                    opt_uppersum[i] = uppersum
                    opt_last[i] = j
        if opt_uppersum[i] < 0:
            opt_uppersum[i] = 0
    k = 2 ** n - 1
    orders = []
    while k != 0:
        orders.append(opt_last[k])
        k = k ^ (1 << opt_last[k])

    return orders, calc_norm(M, calc_order(orders, ansnum), ansnum), M


result = answer_rank_default(A)
order, lack_of_fit, Matrix = result[0], result[1], result[2]
choice_list = [x + 1 for x in order]
plot_matrix.plot_matrix(matrix=np.array(A), order=choice_list, init=0)
print("思考网络高低顺序:", choice_list)
print("拟合度:", lack_of_fit)
Matrix_Transformed = []
for itag in order:
    temp_list = []
    for jtag in order:
        temp = Matrix[itag][jtag]
        temp_list.append(temp)
    Matrix_Transformed.append(temp_list)
plot_matrix.plot_matrix(matrix=np.array(Matrix_Transformed), order=choice_list, init=1)
print("结果保存成功！路径为", plot_matrix.ranked_save_path, "实验id为", plot_matrix.Lab_id)
