#coding=utf-8
import wx.grid as grid

class StudentInfoGridTable(grid.PyGridTableBase):
    def __init__(self, datas):
        grid.PyGridTableBase.__init__(self)

        self.datas = datas
        self.colLabels = [u'试卷名', u'制卷人', u'制卷人账号', u'考试成绩', u'测试开始时间', u'测试结束时间', u'测试时长']

        self.odd = grid.GridCellAttr()
        self.odd.SetReadOnly(True)
        self.odd.SetBackgroundColour('yellow')
        self.even = grid.GridCellAttr()
        self.even.SetReadOnly(True)
        pass

    def GetAttr(self, row, col, kind):
        attr = [self.even, self.odd][row % 2]
        attr.IncRef()
        return attr
    def GetNumberRows(self):
        return len(self.datas)

    def GetNumberCols(self):
        return len(self.colLabels)

    def GetColLabelValue(self, col):
        return self.colLabels[col]

    def GetRowLabelValue(self, row):
        return str(row)

    def GetValue(self, row, col):
        return self.datas[row][col]


