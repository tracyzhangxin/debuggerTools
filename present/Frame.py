# coding=utf-8


import wx
import time
import threading
from utils import CoverageUtil, JudgeResult, ResultStorge
import os
import wx.grid
import sys

class MyFrame(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'DebuggerTool', size=(600, 400))
        # 创建面板
        panel = wx.Panel(self)

        # 创建open，reset按钮
        self.bt_open = wx.Button(panel, label='start')
        self.bt_reset = wx.Button(panel, label='reset')

        # 创建文本，左对齐，注意这里style=wx.TE_LEFT，不是wx.ALIGN_LEFT ，表示控件中的输入光标是靠左对齐。
        self.st_tips = wx.StaticText(panel, 0, "please select algorithm and suite:", style=wx.TE_LEFT)
        #self.st_tips2 = wx.StaticText(panel, 0, "文件路径:", style=wx.TE_LEFT)
        #self.text_filename = wx.TextCtrl(panel, style=wx.TE_LEFT)

        # 创建下拉选项1
        list1 = ['Tarantula', 'Crosstab']
        self.ch1 = wx.ComboBox(panel, 0, choices=list1, style=wx.TE_READONLY)

        # 创建下拉选项2
        list2 = ["bubble_sort_1.py", "insert_sort_1.py"]
        self.ch2 = wx.ComboBox(panel, 0, choices=list2, style=wx.TE_READONLY)

        # 创建文本内容框，多行，垂直滚动条
        #self.text_contents = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY)

        # 创建表格
        # self.list = wx.ListCtrl(panel, style= wx.LC_REPORT)
        # self.list.InsertColumn(0, 'Line', width=100)
        # self.list.InsertColumn(1, 'Rank', width=100)
        self.grid = wx.grid.Grid(panel, -1)
        self.grid.CreateGrid(0, 2)
        self.grid.SetColLabelValue(0, "Line")
        self.grid.SetColLabelValue(1, "Rank")
        #self.grid.AppendRows(1, False)
        #self.grid.SetCellValue(0,0, "1")



        # 添加容器，容器中控件按横向并排排列
        bsizer_top = wx.BoxSizer(wx.VERTICAL)

        # 添加容器，容器中控件按纵向并排排列
        bsizer_center = wx.BoxSizer(wx.HORIZONTAL)
        bsizer_bottom = wx.BoxSizer(wx.HORIZONTAL)

        # 在容器中添加st_tips控件，proportion=0 代表当容器大小变化时，st_tips控件的大小不
        # flag = wx.EXPAND|wx.ALL中，wx.ALL代表在st_tips控件四周都增加宽度为x的空白，x取border参数的值，本例是border=5
        # wx.EXPAND代表st_tips控件占满可用空间。
        bsizer_top.Add(self.st_tips, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        # proportion=1 代表当容器大小变化时，st_tips2控件的大小变化，变化速度为1
        bsizer_center.Add(self.ch1, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT, border=5)
        # proportion=2 代表当容器大小变化时，text_filename控件的大小变化，变化速度为2
        bsizer_center.Add(self.ch2, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)
        bsizer_center.Add(self.bt_open, proportion=1, flag=wx.ALL, border=5)
        bsizer_center.Add(self.bt_reset, proportion=0, flag=wx.ALL, border=5)
        #bsizer_bottom.Add(self.text_contents, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        bsizer_bottom.Add(self.grid, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        #bsizer_bottom.Add(self.list, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        # wx.VERTICAL 横向分割
        bsizer_all = wx.BoxSizer(wx.VERTICAL)

        # 添加顶部sizer，proportion=0 代表bsizer_top大小不可变化
        bsizer_all.Add(bsizer_top, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        bsizer_all.Add(bsizer_center, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        # 添加顶部sizer，proportion=1 代表bsizer_bottom大小变化
        bsizer_all.Add(bsizer_bottom, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.onStart, self.bt_open)
        self.Bind(wx.EVT_BUTTON, self.reSet, self.bt_reset)
        # self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        panel.SetSizer(bsizer_all)

    def onStart(self, event):
        dialog = wx.ProgressDialog('Doing debug', 'Please wait...')
        self.start(self.doDebug, dialog)

    def doDebug(self, dialog):  # put your logic here

        absolutepath = os.path.abspath("../")
        sourcecode = absolutepath + "/testcase/suite/"
        testSuite = "../testcase/sort"
        coverageUtil = CoverageUtil.CoverageUtil()
        judgeResult = JudgeResult.JudgeResult()

        type = self.ch1.GetValue()
        map = {"Tarantula":1, "Crosstab":2}
        subcode = self.ch2.GetValue()
        sourcecode = sourcecode + subcode

        if not os.path.isfile(sourcecode):
            print(sourcecode + "is not file")
            #self.text_contents.AppendText(sourcecode + "is not file")

        resultStorge = ResultStorge.ResultStorge(map[type])
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
            wx.CallAfter(dialog.Update, i)

        coverageUtil.clear()
        coverageList = coverageUtil.getLineCoverage(coverageUtil.lines, resultStorge.records)
        resultlist = resultStorge.rankBySuspiciousness(coverageList)

        #self.text_contents.AppendText(str(resultlist));
        self.generateReport(resultlist)
        wx.CallAfter(dialog.Destroy)

    def generateReport(self, suspiciousnessRank):
        count = 0
        check = 0
        str1 = ""
        #self.text_contents.SetValue("")
        #self.list.ClearAll()
        for item in suspiciousnessRank:
            if item[1] != -1:
                check = 1
        if check == 0:
            #self.text_contents.AppendText("You must provide a test suite containing both successful abd failed test cases.")
            #self.list.ClearAll()
            print(1)
        else:
            #self.text_contents.AppendText("The suspiciousness result of program:\n")
            #self.text_contents.AppendText("\tLine\tRank\n")
            if len(suspiciousnessRank) >= 10:
                for item in suspiciousnessRank:
                    count += 1
                    #str1 = str1 + str("\t{:<1}\t{:<1}\n".format(item[0], count))
                    self.grid.AppendRows(1, False)
                    if count ==20:
                       break
            else:
                for item in suspiciousnessRank:
                    count += 1
                    #str1 = str1 + str("\t{:<1}\t{:<1}\n".format(item[0], count))
                    self.grid.AppendRows(1, False)
        #print(str1)
        #self.text_contents.AppendText(str1)


    def start(self, func, *args):  # helper method to run a function in another thread
        thread = threading.Thread(target=func, args=args)
        thread.setDaemon(True)
        thread.start()

    def reSet(self, event):
        #self.text_contents.flush()
        #self.text_contents.SetValue("")
        #self.list.ClearAll()
        print(1)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(parent=None, id=-1)
    frame.Show()
    frame.Center()
    app.MainLoop()