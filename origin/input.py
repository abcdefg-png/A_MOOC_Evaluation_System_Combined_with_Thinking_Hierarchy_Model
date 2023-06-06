import os
import numpy as np

info = 6
perc = 0.03
# Ignore answers that are less than 3%
split1 = '\t'
split2 = ','
outfile = 'output/'
infile = 'input/'


def csv_input(filename):
    print("Input: " + filename)
    # input from csv file
    f = open(infile + filename, 'r', encoding='utf-8')
    spl = filename.split('.')
    filename = spl[0]
    if spl[1] == 'mat':
        return mat_input(filename, f)

    if not os.path.exists(outfile + filename):
        os.mkdir(outfile + filename)
    lis = f.readlines()
    data = []
    for i in range(len(lis)):
        data.append(lis[i].rstrip('\n').split(split1))
    # print(data[0])
    n = (len(data[0]) - info) // 2
    m = len(data) - 1
    ignore = max(perc * m, 1)
    ret = []
    for i in range(n):
        dic = dict()
        for j in range(1, m + 1):
            if data[j][info + i * 2] in dic:
                dic.update({data[j][info + i * 2]: dic[data[j][info + i * 2]] + 1})
            else:
                dic.update({data[j][info + i * 2]: 1})
        allans = []
        dic1 = dict()
        for key in sorted(dic, key=dic.__getitem__):
            if (dic[key] > ignore) and (key != "不知道"):
                allans.append(key)
                dic1.update({key: len(allans) - 1})
        guessmatrix = np.zeros([len(allans), len(allans)])
        ansnum = np.zeros(len(allans))
        for j in range(1, m + 1):
            if data[j][info + i * 2] in dic1:
                jid = dic1[data[j][info + i * 2]]
                guess = data[j][info + i * 2 + 1].split(split2)
                for k in range(len(guess)):
                    if (guess[k] in dic1):
                        guessmatrix[jid][dic1[guess[k]]] += 1
                # guessmatrix[jid][jid] += 1
                ansnum[jid] += 1
        ret.append({
            'filename': filename,
            'questionname': data[0][info + i * 2],
            'allans': allans,
            'guessmatrix': guessmatrix,
            'ansnum': ansnum,
        })
    for i in range(len(ret)):
        ret[i].update({'id': i})
    return ret


def txt_input(filename):
    print("Input: " + filename)
    if not os.path.exists(outfile + filename):
        os.mkdir(outfile + filename)
    ret = []
    for root, dirs, files in os.walk(infile + filename):
        for fil in files:
            f = open(os.path.join(root, fil), 'r')
            lis = f.readlines()
            m = len(lis)
            data = []
            ignore = max(perc * m, 1)
            for j in range(m):
                tmp = lis[j].rstrip('\n').split(' ')
                if (len(tmp) == 1):
                    tmp = lis[j].rstrip('\n').split('\t')
                data.append(tmp)
            # print(data)
            dic = dict()
            for j in range(m):
                if data[j][0] in dic:
                    dic.update({data[j][0]: dic[data[j][0]] + 1})
                else:
                    dic.update({data[j][0]: 1})
            allans = []
            dic1 = dict()
            for key in sorted(dic, key=dic.__getitem__):
                if (dic[key] > ignore) and (key != "不知道"):
                    allans.append(key)
                    dic1.update({key: len(allans) - 1})
            guessmatrix = np.zeros([len(allans), len(allans)])
            ansnum = np.zeros(len(allans))
            for j in range(m):
                if data[j][0] in dic1:
                    jid = dic1[data[j][0]]
                    guess = data[j][1].split(split2)
                    for k in range(len(guess)):
                        if (guess[k] in dic1):
                            guessmatrix[jid][dic1[guess[k]]] += 1
                    ansnum[jid] += 1
            ret.append({
                'filename': filename,
                'questionname': fil,
                'allans': allans,
                'guessmatrix': guessmatrix,
                'ansnum': ansnum,
                'specialname': fil.split('.')[0]
            })
    for i in range(len(ret)):
        ret[i].update({'id': i})
    return ret


def mat_input(filename, f):
    lis = f.readlines()
    data = []
    for i in range(len(lis)):
        data.append(lis[i].rstrip('\n').split(split1))
    intdata = [list(map(int, data[i][1:])) for i in range(1, len(data))]
    ansnum = np.zeros(len(data[0][1:]))
    for i in range(len(data[0][1:])):
        ansnum[i] = intdata[i][i]

    # print(np.array(intdata))
    return [{
        'id': 0,
        'filename': filename,
        'questionnaire': filename,
        'allans': data[0][1:],
        'guessmatrix': np.array(intdata),
        'ansnum': ansnum,
    }]


def input():
    ret = []
    allfile = os.listdir(infile)
    for fil in allfile:
        if '.' in fil:
            ret.append(csv_input(fil))
        else:
            ret.append(txt_input(fil))
    return ret
