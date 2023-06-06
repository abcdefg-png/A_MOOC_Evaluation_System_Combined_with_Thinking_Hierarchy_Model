import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import heatmap
import algorithm


def init(allans, guessmatrix, order, ansnum=[]):
    """
    Rearrange the answer-guess matrix
    """
    n = len(allans)
    newmatrix = np.zeros([n, n])
    newans = []
    for i in range(n):
        newans.append(allans[order[i]])
        for j in range(n):
            newmatrix[i][j] = guessmatrix[order[i]][order[j]]
        if ansnum != []:
            newmatrix[i][i] = ansnum[order[i]]
    return newans, newmatrix


def print_heatmap(filename, id, allans, guessmatrix, ansnum=[], order=None, minmax=None, figsize=(3.5, 3),
                  specialname=None, method=None):
    """
    Input the answer-guess matrix, output the figure.

    filename:       the path to save the figure
    id:             the question id
    allans:         the answer list of the question
    guessmatrix:    the answer-guess matrix M
    order:          the rank of the answers. If order == None, use our algorithm to calculate the optimal rank
    """
    print("Heatmap:", filename, id, method)
    if order == None:
        order, ordernorm = algorithm.answer_rank_default(guessmatrix, ansnum=ansnum, normalize="all")
        res, resnorm = algorithm.answer_rank_variant(guessmatrix, ansnum=ansnum, normalize="all")
        order2 = algorithm.calc_order(res, ansnum)
        if method == "variant":
            order = order2
            ordernorm = resnorm
    else:
        ordernorm = algorithm.calc_norm(guessmatrix, order, ansnum)
    if specialname == None:
        specialname = "Question_" + str(id + 1)
    specialname += "_" + method
    newans, newmatrix = init(allans, guessmatrix, order, ansnum)
    if len(allans) > 10:
        figsize = (9, 8)
    fig, ax = plt.subplots(figsize=figsize)
    if minmax == None:
        minmax = [newmatrix.min(), newmatrix.max()]
    norm = matplotlib.colors.Normalize(minmax[0] + 1, minmax[1] + 1)
    im, cbar = heatmap.heatmap(newmatrix + 1, newans, newans, norm=norm, ax=ax, cmap="Blues", usecbar=False)
    fmt = matplotlib.ticker.FuncFormatter(lambda x, pos: "{:.0f}".format(x - 1))
    texts = heatmap.annotate_heatmap(im, valfmt=fmt, threshold=(sum(minmax) + 1) // 2)
    # ax.set_xlabel("lack-of-fit = %.6f" % ordernorm)
    fig.tight_layout()
    fig.savefig('output/' + filename + "/" + specialname + ".png", bbox_inches='tight', dpi=400)
    fig.savefig('output/' + filename + "/" + specialname + ".pdf", bbox_inches='tight')


def print_csv(filename, id, allans, guessmatrix, ansnum=[]):
    print("Csv:", filename, id)
    order, ordernorm = algorithm.answer_rank_default(guessmatrix, normalize="all", ansnum=ansnum)
    res, resnorm = algorithm.answer_rank_variant(guessmatrix, normalize="all", ansnum=ansnum)
    order2 = algorithm.calc_order(res, ansnum)
    return [filename, id, allans, res, order2, resnorm, order, ordernorm]
