# coding=utf-8
from utils import CoverageUtil, JudgeResult, ResultStorge
import os
import xlwt


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


# 设置表格样式
def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


# 写Excel
def write_excel():
    f = xlwt.Workbook() #创建工作簿
    sheet1 = f.add_sheet('学生', cell_overwrite_ok=True)#创建工作表
    row0 = ["姓名", "年龄", "出生日期", "爱好"] #标题栏
    colum0 = ["张三", "李四", "恋习Python", "小明", "小红", "无名"]
    # 写第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))
    # 写第一列
    for i in range(0, len(colum0)):
        sheet1.write(i + 1, 0, colum0[i], set_style('Times New Roman', 220, True))

    sheet1.write(1, 3, '2006/12/12')
    sheet1.write_merge(6, 6, 1, 3, '未知')  # 合并行单元格
    sheet1.write_merge(1, 2, 3, 3, '打游戏')  # 合并列单元格
    sheet1.write_merge(4, 5, 3, 3, '打篮球')

    f.save('test.xls')


def generateReport(suspiciousnessRank):
    count = 0
    check = 0
    for item in suspiciousnessRank:
        if item[1] != -1:
            check = 1
    if check == 0:
        print("You must provide a test suite containing both successful abd failed test cases.")
    else:
        print("The most suspicious line:\n\tLine Rank")
        # if len(suspiciousnessRank) >= 10:
        for item in suspiciousnessRank:
            count += 1
            print("\t{:<5}{:<5}".format(item[0], count))
            # if count == 20:
            #     break
        # else:
        #     for item in suspiciousnessRank:
        #         count += 1
        #         print("\t{:<5}{:<5}".format(item[0],count))
    return suspiciousnessRank;


def main():
    absolutepath = os.path.abspath("../")
    sourcecode = absolutepath + "/testcase/suite/"
    testSuite = "../testcase/sort"
    coverageUtil = CoverageUtil.CoverageUtil()
    judgeResult = JudgeResult.JudgeResult()
    type = raw_input("please input the debugger algorithm: 1:Tarantula; 2:CrossTab; 3:Jaccard : ")
    subcode = raw_input("please input the sort code name: ")
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
        record = coverageUtil.calCoverLine(testSuite + "/" + filename,
                                           testSuite + "/" + filename.replace(".in", ".out"))
        result = judgeResult.check(testSuite + "/" + filename, testSuite + "/" + filename.replace(".in", ".out"))
        resultStorge.addrecord(result, record)
        os.remove(testSuite + "/" + filename.replace(".in", ".out"))

        i += 1
        printProgress(i, total, prefix='Progress:', suffix='Complete', barLength=50)

    coverageUtil.clear()
    coverageList = coverageUtil.getLineCoverage(coverageUtil.lines, resultStorge.records)
    resultlist = resultStorge.rankBySuspiciousness(coverageList)
    print(resultlist)  # 所有测试集的结果
    suspiciousnessRank = generateReport(resultlist)  # 生成排名的函数


if __name__ == '__main__':
    main()
