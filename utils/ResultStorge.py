from algorithm import Tarantula
from algorithm import Crosstab
from algorithm import Jaccard
from algorithm import Ochiai

class ResultStorge:
    def __init__(self ,type):
        self.records = []
        self.single = self.singleton(type)

    def singleton(self, type):
        if(type == 1):
            print("using Tarantula......")
            return Tarantula.Tarantula()
        elif(type == 2):
            print("using Crosstab......")
            return Crosstab.Crosstab()
        elif(type == 3):
            print("using Jaccard......")
            return Jaccard.Jarrard()
        elif(type == 4):
            print("using Ochiai......")
            return Ochiai.Ochiai()

    def setFilePath(self, filepath):
        file = open(filepath)
        self.lines = len(file.readlines())

    def addrecord(self, result, record):
        temp = [result]
        temp.extend(record)
        self.records.append(temp)

    def getLineRecords(self):
        return [self.lines, self.records]

    def rankBySuspiciousness(self, CoverageList):
        return self.single.rankBySuspiciousness(CoverageList)

    def rankBySuspiciousnessBest(self, suspiciousnessRank):
        suspiciousness = []
        i = 1
        r = 1
        preitem = []
        for item in suspiciousnessRank:
            if i==1:
                suspiciousness.append([item[0], 1])
                i+=1
                preitem = item
            else:
                if preitem[1] == item[1]:
                    suspiciousness.append([item[0], r])
                else:
                    suspiciousness.append([item[0], i])
                    preitem = item
                    r = i
                i+=1
        return suspiciousness

    def rankBySuspiciousnessWorst(self, suspiciousnessRank):
        suspiciousness = []
        i = 1
        rankItem = []
        preitem = []
        for item in suspiciousnessRank:
            if i==1:
                preitem = item
            else:
                if item[1] != preitem[1]:
                    rankItem.append([i-1, i-1])
                    preitem = item
            i+=1
        rankItem.append([i,i])

        begin = 1
        for info in rankItem:
            for j in range(begin, info[0]+1):
                suspiciousness.append([j, info[1]])
                begin = j+1
        return suspiciousness

