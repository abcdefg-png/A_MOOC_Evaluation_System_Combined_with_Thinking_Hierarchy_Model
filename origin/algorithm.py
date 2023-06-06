import numpy as np
import math

eps = 1e-9


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


def answer_rank_default(MM, ansnum=[], normalize=None):
    # input answer-guess matrix M
    M = np.array(MM)
    if normalize == "all":
        M /= sum(sum(M))
    n, n = M.shape
    if ansnum == []:
        ansnum = np.array([M[i][i] for i in range(n)])
    opt_uppersum = np.zeros(2 ** n, dtype=float)
    opt_last = np.zeros(2 ** n, dtype=np.int)
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
    order = []
    while k != 0:
        order.append(opt_last[k])
        k = k ^ (1 << opt_last[k])

    return order, calc_norm(M, calc_order(order, ansnum), ansnum)


def answer_rank_variant(MM, tot_type=None, normalize=None, ansnum=[]):
    class enumerator:
        # Enumerator can enumerate all legal categories
        def __init__(self, n, cur=None):
            # n is the number of answers
            self.n = n
            if cur == None:
                self.cur = tuple([0 for i in range(n)])
            else:
                self.cur = cur
            self.prem = [self.cur[0]]
            for i in range(1, self.n):
                self.prem.append(max(self.prem[-1], self.cur[i]))

        def step(self):
            # Get the next legal category
            m = self.n - 1
            while (self.cur[m] >= self.prem[m - 1] + 1):
                m = m - 1
                if m < 1:
                    return False
            self.cur = self.cur[:m] + (self.cur[m] + 1,) + tuple([0 for i in range(self.n - m - 1)])
            for i in range(m, self.n):
                self.prem[i] = max(self.prem[i - 1], self.cur[i])
            return True

    M = np.array(MM)
    # Normalize
    n, n = M.shape
    if n <= 1:
        return [0], 0
    if ansnum == []:
        ansnum = np.array([M[i][i] for i in range(n)])

    if normalize == "all":
        M /= sum(sum(M))
    # Input answer-guess matrix M
    if tot_type == None:
        tot_type = n
    if n > 10:
        # If n > 10, the efficiency will be very low
        return
    enu = enumerator(n)

    optnorm = 1e30
    opt = list(enu.cur)
    # Initialize the optimal answer

    while True:
        cur = enu.cur
        m = enu.prem[-1] + 1
        # m is the number of typesum
        if m > tot_type:
            continue
        typesum = np.zeros(m)
        # Save the sum of squares for each type
        for i in range(n):
            typesum[cur[i]] += ansnum[i] * ansnum[i]
        W = np.zeros((m, n))
        for i in range(n):
            W[cur[i]][i] = math.sqrt(ansnum[i] * ansnum[i] / typesum[cur[i]])
        # Generate matrix W
        L = np.dot(np.dot(W, M), W.T)
        typenum = np.zeros(m)
        for i in range(n):
            typenum[cur[i]] = max(typenum[cur[i]], ansnum[i])
        # Calculate matrix L
        order, ordernorm = answer_rank_default(L, typenum)
        # Get the optimal order of L
        rank = np.zeros(m, dtype=int)
        for i in range(m):
            rank[order[i]] = i

        newcur = []
        for i in range(n):
            newcur.append(rank[cur[i]])
        # Generate new category

        norm = calc_norm(M, newcur, ansnum)
        if norm < optnorm:
            # Update optimal answer
            optnorm = norm
            opt = newcur

        if not enu.step():
            break

    return opt, optnorm
