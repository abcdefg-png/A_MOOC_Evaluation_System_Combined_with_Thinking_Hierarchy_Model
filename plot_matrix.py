import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import font_manager

font = font_manager.FontProperties(fname='C:/Windows/Fonts/times.ttf')
ranked_save_path = "./实验结论/第五组/"
correct_character = "*"
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为SimHei
Lab_id = 11
origin_save_path = ranked_save_path
# 自定义颜色映射
# color_list = ['#d8f7f3', '#a4e6e1', '#7cded0',
#               '#58d4c1', '#3fbaa3', '#2b8c7b', '#1d614c']  # Green-Blue
# color_list = ['#ffffcc', '#ffeda0', '#fed976',
#               '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c']  # Red-Yellow
# color_list = ['#87b3fb', '#3d96f9', '#076ee1', '#054a97']  # Blue


# color_list = ['#f6c6d2', '#ef9ca0', '#e97b80', '#d8242d']  # Red-Pink
color_list = ['#e5c4cf', '#c0a3cf', '#aa88c4', '#8d71a4', '#884793']  # Purple


def find_max_diagonal(matrix):
    n = len(matrix)
    max_val = matrix[0][0]
    max_idx = 0
    for i in range(n):
        if matrix[i][i] > max_val:
            max_val = matrix[i][i]
            max_idx = i
    return max_idx


# 准备数据
def plot_matrix(matrix, order, init):
    """"""
    ""

    cmap = colors.ListedColormap(color_list)
    # 绘制矩阵图
    fig, ax = plt.subplots()
    ax.text(-0.4, 0.5, "Answer", fontproperties=font, fontweight='bold', transform=ax.transAxes, rotation=90,
            va='center', fontsize=40)
    ax.imshow(matrix, cmap=cmap)

    # 标注数值
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, str(matrix[i, j]), ha='center', va='center', color='black', fontsize=32)

    # 设置坐标轴标签
    if init == 0:
        # list_init = list(range(1, len(matrix) + 1))
        # list_init = ["C" + str(item) for item in list_init]]
        list_init = ["C1", "C2", "C3", "C4", "C5"]
        tag = find_max_diagonal(matrix=matrix)
        list_init[tag] = list_init[tag] + correct_character
        ax.set_xticks(np.arange(matrix.shape[1]))
        ax.set_yticks(np.arange(matrix.shape[0]))
        ax.set_xticklabels(list_init, fontproperties=font, fontsize=32)
        ax.xaxis.tick_top()
        ax.set_yticklabels(list_init, fontproperties=font, fontsize=32)
        savename = "Origin{}".format(Lab_id)
        img_title = "Prediction"
    else:
        Choice_list = ["C" + str(item) for item in order]
        Choice_list[0] = Choice_list[0] + correct_character
        ax.set_xticks(np.arange(matrix.shape[1]))
        ax.set_yticks(np.arange(matrix.shape[0]))
        ax.set_xticklabels(Choice_list, fontproperties=font, fontsize=32)
        ax.xaxis.tick_top()
        ax.set_yticklabels(Choice_list, fontproperties=font, fontsize=32)
        savename = "Ranked{}".format(Lab_id)
        img_title = "Prediction"
    # 添加标题和轴标签
    ax.set_title(img_title, fontproperties=font, fontsize=40, fontweight='bold')
    ax.set_xlabel('Answer Correctness Ranking', labelpad=20, fontproperties=font, fontsize=36)
    ax.xaxis.set_label_position('top')

    # 显示矩阵图或保存为图片
    # plt.show()
    plt.savefig(origin_save_path + savename + ".png", dpi=300, bbox_inches='tight')


def plot_matrix2(matrix, order, init):
    cmap = colors.ListedColormap(color_list)
    # 绘制矩阵图
    fig, ax = plt.subplots()
    ax.imshow(matrix, cmap=cmap)

    # 标注数值
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, str(matrix[i, j]), ha='center', va='center', color='black', fontsize=28)

    # 设置坐标轴标签
    if init == 0:
        # list_init = list(range(1, len(matrix) + 1))
        # list_init = ["C" + str(item) for item in list_init]]
        list_init = ["C3", "C5", "C6", "C4", "C1", "C2"]
        list_init[0] = list_init[0] + correct_character
        ax.set_xticks(np.arange(matrix.shape[1]))
        ax.set_yticks(np.arange(matrix.shape[0]))
        ax.set_xticklabels(list_init)
        ax.xaxis.tick_top()
        ax.set_yticklabels(list_init)
        savename = "Origin"
        img_title = "Prediction"
    else:
        Choice_list = ["C" + str(item) for item in order]
        Choice_list[0] = Choice_list[0] + correct_character
        ax.set_xticks(np.arange(matrix.shape[1]))
        ax.set_yticks(np.arange(matrix.shape[0]))
        ax.set_xticklabels(Choice_list)
        ax.xaxis.tick_top()
        ax.set_yticklabels(Choice_list)
        savename = "Ranked"
        img_title = "Prediction"
    # 添加标题和轴标签
    ax.set_title(img_title)
    ax.set_xlabel('Answer correctness ranking', labelpad=10.5)
    ax.xaxis.set_label_position('top')

    # 显示矩阵图或保存为图片
    # plt.show()
    plt.savefig(ranked_save_path + savename + ".png", dpi=300, bbox_inches='tight')
