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

