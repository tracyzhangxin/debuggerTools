# coding=utf-8

from utils import CoverageUtil, JudgeResult, ResultStorge
import os
import numpy as np
import time



def printProgress(iteration, total, prefix='', suffix='', decimals=1, barLength=100):
    """
    Call in a loop to create a terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    import sys
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def generateReport(suspiciousnessRank):
    count = 0
    check = 0
    for item in suspiciousnessRank:
        if item[1] != -1:
            check = 1
    if check == 0:
        print("You must provide a test suite111 containing both successful abd failed test cases.")
    else:
        print("The most suspicious line:\n\tLine Rank")
        if len(suspiciousnessRank) >= 10:
            for item in suspiciousnessRank:
                count += 1
                print("\t{:<5}{:<5}".format(item[0],count))
                # if count == 20:
                #     break
        else:
            for item in suspiciousnessRank:
                count += 1
                print("\t{:<5}{:<5}".format(item[0],count))

def getResultList(subcode, type):
    absolutepath = os.path.abspath("../")
    sourcecode = absolutepath + "/testcase/suite/"
    testSuite = "../testcase/sort"
    coverageUtil = CoverageUtil.CoverageUtil()
    judgeResult = JudgeResult.JudgeResult()
    # type = input("please input the debugger algorithm: 1:Tarantula; 2:CrossTab; 3:Jaccard : ")
    # subcode = input("please input the sort code name: ")
    sourcecode = sourcecode + subcode

    if not os.path.isfile(sourcecode):
        print(sourcecode + "is not file")
        exit(1)

    resultStorge = ResultStorge.ResultStorge(int(type))
    coverageUtil.setPySource(sourcecode)
    f_list = os.listdir(testSuite)
    total = 0
    for filename in f_list:
        if filename.endswith(".in"):
            total = total + 1
    i = 0
    for filename in f_list:
        # suggestion: replace the last .in with .out // may be a filename containing multiple .in
        if not filename.endswith(".in"):
            continue
        # print(filename)

        resultStorge.setFilePath(testSuite + "/" + filename)
        record = coverageUtil.calCoverLine(testSuite + "/" + filename, testSuite + "/" + filename.replace(".in", ".out"))
        result = judgeResult.check(testSuite + "/" + filename, testSuite + "/" + filename.replace(".in", ".out"))
        resultStorge.addrecord(result, record)
        os.remove(testSuite + "/" + filename.replace(".in", ".out"))

        i += 1
        printProgress(i, total, prefix='Progress:', suffix='Complete', barLength=50)

    coverageUtil.clear()
    coverageList = coverageUtil.getLineCoverage(coverageUtil.lines, resultStorge.records)
    resultlist = resultStorge.rankBySuspiciousness(coverageList)
    return resultlist

def getResultInAllVersions(error_indexes, all_matrix):
    list_result = []
    for error_index, matrix in zip(error_indexes, all_matrix):
        for i in range(len(matrix)):
            if matrix[i][0] == error_index:  # 根据index找到在matrix当中的位置i
                list_result.append((i + 1) / len(matrix))  # 得到想要的结果 exam_index=m/n，并将exam_index加入list当中：list.append(exam_index);
                break
    return list_result

def getPercent(list_result):
    # 一共有versions的版本数目
    versions = len(list_result)

    percent_count = [0] * 11    # 已经初始化为0
    percent_count = np.array(percent_count)

    for i in range(0, versions):
        if((list_result[i] > 0) & (list_result[i] <= 0.05)):
            percent_count[0] += 1
        elif (list_result[i] <= 0.1):
            percent_count[1] += 1
        elif (list_result[i] <= 0.2):
            percent_count[2] += 1
        elif (list_result[i] <= 0.3):
            percent_count[3] += 1
        elif (list_result[i] <= 0.4):
            percent_count[4] += 1
        elif (list_result[i] <= 0.5):
            percent_count[5] += 1
        elif (list_result[i] <= 0.6):
            percent_count[6] += 1
        elif (list_result[i] <= 0.7):
            percent_count[7] += 1
        elif (list_result[i] <= 0.8):
            percent_count[8] += 1
        elif (list_result[i] <= 0.9):
            percent_count[9] += 1
        elif (list_result[i] <= 1):
            percent_count[10] += 1

    percent = percent_count / versions
    return percent.tolist() # 返回类似[1,2,3,4]数据

def main(type):
    # get error_indexes
    error_indexes = []
    with open('../testcase/error_rows.txt', 'r') as f:
        for line in f:
            error_indexes.append(list(line.strip('\n').split(',')))
    error_indexes = np.reshape(error_indexes, len(error_indexes), 1)
    error_indexes = error_indexes.astype(int)
    error_indexes = error_indexes.tolist()

    # get all_matrix
    absolutepath = os.path.abspath("../")
    sourcecode = absolutepath + "/testcase/suite/"
    sourceFiles = os.listdir(sourcecode)
    sourceFiles.sort() # get all files name
    all_matrix = []
    for fileName in sourceFiles:
        result = getResultList(fileName, type)
        all_matrix.append(result)

    list_result = getResultInAllVersions(error_indexes, all_matrix)
    percent_result = getPercent(list_result)
    return percent_result



if __name__ == '__main__':
    start = time.time()

    # 1:Tarantula; 2:CrossTab; 3:Jaccard :

    print(main(1))

    end = time.time()
    print("Time used:", end - start)

    # 1：[0.12, 0.2, 0.08, 0.24, 0.12, 0.12, 0.08, 0.0, 0.0, 0.0, 0.04]
    # 1：Time used: 1226.7787761688232

    # 2：[0.12, 0.2, 0.12, 0.2, 0.16, 0.08, 0.08, 0.0, 0.0, 0.0, 0.04]
    # 2：Time used: 1182.7200479507446

    # 3：[0.12, 0.24, 0.12, 0.2, 0.12, 0.08, 0.08, 0.0, 0.0, 0.0, 0.04]
    # 3：Time used: 1131.2345170974731

