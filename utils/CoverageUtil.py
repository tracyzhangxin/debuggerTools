import os, shutil
from subprocess import check_output

class CoverageUtil:

    def setPySource(self, pyfile):
        absolutepath = os.path.abspath("../")
        self.pyfile = absolutepath + "/utils/sorts.py"
        shutil.copyfile(pyfile, self.pyfile)
        file = open(self.pyfile)
        self.lines = len(file.readlines())

    def calCoverLine(self, inputpath, outputpath):
        result = os.popen("coverage run " + self.pyfile + " < \"" + inputpath + "\" > \"" + outputpath + "\"")
        res = result.read()
        for line in res.splitlines():
            pass

        Report = check_output("coverage report -m " + self.pyfile, shell=True).decode()
        ReportList = Report.split("\n")  # Analyze information in the Report information
        ReportInfo = ReportList[2].split(" ")
        ReportInfo = [x.replace('\r', '') for x in ReportInfo if x != '']
        ReportInfo = [x.replace(',', '') for x in ReportInfo]
        Totlength = int(ReportInfo[1])
        MissingLine = []
        CoverLine = []
        if len(ReportInfo) > 4:
            for i in range(4, len(ReportInfo)):
                if '-' in ReportInfo[i]:
                    RInfoList = ReportInfo[i].split('-')
                    L = RInfoList[0]
                    R = RInfoList[1]
                    for i in range(int(L), int(R) + 1):
                        MissingLine.append(i)
                else:
                    MissingLine.append(int(ReportInfo[i]))
        for i in range(1, Totlength + 1):
            if i not in MissingLine:
                CoverLine.append(i)
        return CoverLine

    def getLineCoverage(self, linenum, testCoverageList):
        testNum = len(testCoverageList)
        ncf = [0] * linenum
        ncs = [0] * linenum
        ns = 0
        nf = 0
        for testCoverage in testCoverageList:
            if testCoverage[0]:
                ns += 1
                for i in range(1, len(testCoverage)):
                    ncs[testCoverage[i] - 1] += 1
            else:
                nf += 1
                for i in range(1, len(testCoverage)):
                    ncf[testCoverage[i] - 1] += 1
        nuf = []
        nus = []
        for i in range(0, linenum):
            nuf.append(nf - ncf[i])
            nus.append(ns - ncs[i])

        lineCoverage = [ncf, ncs, nuf, nus]
        lineCoverage = list(map(list, zip(*lineCoverage)))
        return lineCoverage

    def getLineCoverageMatrix(swlf, linenum, testCoverageList):
        # print(lineNum)
        # print(testCoverageList)
        CoverageLabel = [0] * (len(testCoverageList))
        CoverageMatrix = []
        for i in range(len(testCoverageList)):
            CoverageMatrix.append([0] * linenum)
        for i in range(len(testCoverageList)):
            if testCoverageList[i][0]:
                CoverageLabel[i] += 1
            for j in range(1, len(testCoverageList[i])):
                CoverageMatrix[i][testCoverageList[i][j] - 1] = CoverageMatrix[i][testCoverageList[i][j] - 1] + 1
        return CoverageMatrix, CoverageLabel

    def clear(self):
        os.remove(self.pyfile)
        os.remove(".coverage")

if __name__ == '__main__':
    baseDir = "../testcase/"
    infile = input("please input infile:")
    outfile = input("please input outfile:")
    infile = baseDir + infile
    outfile = baseDir + outfile
    sortfile = baseDir + "sorts.py"
    coverageUtil = CoverageUtil()
    coverageUtil.setPySource(sortfile)
    coverLine = coverageUtil.calCoverLine(infile, outfile)
    print(coverLine)



