# $LAN=PYTHON$
# Python 3.10.7
# 中山大學資訊工程所 M113040019 余承叡
# 執行方法: 在虛擬環境下安裝pyqt5，在虛擬環境中執行 python main.py


#程式原始碼合併檔

#============================================================main.py=======================================================================

from PyQt5 import QtWidgets
from MainWidget import MainWidget


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWidget()
    window.show()
    sys.exit(app.exec_())

#==========================================================================================================================================

#=============================================================MainWidget.py=================================================================

from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtCore import Qt
from PaintBoard import PaintBoard
from Voronoi import Voronoi
from Voronoi import Edge

class MainWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.board = PaintBoard(self)
        self.voronoi = Voronoi()
        self.data_list = []                     #從file拿出來的資料存放區域
        self.complete_data = []                 #只會有一個陣列有值，所以當一個陣列設值時另一個陣列要清空
        self.point = []                         #要畫在畫板上的點
        self.line = []                          #要畫在畫板上的縣
        self.convex_line = []
        self.step_by_step_now = 0
        self.now = 0                            #
        self.mode = ""
        self.main_view()
        self.contorl_view()

    def main_view(self):
        self.resize(600,600)
        self.setWindowTitle("Midterm")
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.addWidget(self.board)

    def contorl_view(self):
        control_layout = QVBoxLayout()
        control_layout.setContentsMargins(10, 10, 10, 10) 
        splitter = QSplitter(self) #佔位符
        control_layout.addWidget(splitter)

        self.run_button = QPushButton("Run")
        self.run_button.setParent(self)
        self.run_button.clicked.connect(self.click_run)
        control_layout.addWidget(self.run_button)

        self.step_by_step_button = QPushButton("Step_by_step")
        self.step_by_step_button.setParent(self)
        self.step_by_step_button.clicked.connect(self.click_step_by_step)
        control_layout.addWidget(self.step_by_step_button)

        self.laod_file_button = QPushButton("Load_file")
        self.laod_file_button.setParent(self)
        self.laod_file_button.clicked.connect(self.click_load_file)
        control_layout.addWidget(self.laod_file_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setParent(self)
        self.clear_button.clicked.connect(self.click_clear)
        control_layout.addWidget(self.clear_button)

        self.display_button = QPushButton("Display")
        self.display_button.setParent(self)
        self.display_button.clicked.connect(self.click_Display)
        control_layout.addWidget(self.display_button)

        splitter = QSplitter(self)
        control_layout.addWidget(splitter)
        self.layout.addLayout(control_layout)
    

    def click_run(self):
        self.mode = self.board.check_mode()
        #print(self.mode)
        with open('test1.txt','a+') as f:
            f.truncate(0)
        self.step_by_step_now = 0
        self.voronoi.reset()
        print("=================================================================")
        if self.mode == "file":
            print(self.data_list)
            if len(self.data_list)!=0:
                if len(self.data_list[self.now]) == 1:                 
                    self.num = int(self.data_list[self.now][0])                      #檢查這筆資料有幾行
                    self.point = []
                    self.line = []
                    self.convex_line = []
                    convex_points = []
                    self.board.Clear()
                    for i in range(self.num):
                        print(self.now)
                        self.now += 1
                        self.point.append((int(self.data_list[self.now][0]),
                                                int(self.data_list[self.now][1])))
                    # self.board.point_accessor(self.point,self.line,clear=True)
                    self.board.update_mode(self.mode)
                    print("POINTS:",self.point)
                    edge_list = Edge()
                    self.point, edge_list,_,self.convex_line  = self.voronoi.calu_run(self.point)
                    if len(edge_list) != 0:
                        #print("important:",edge_list[0].mid_line)
                        print("len:",len(edge_list))
                        for edge in edge_list:
                            self.line.append(edge.mid_line)
                            #print("edge",edge.mid_line)
                    else:
                        self.line = []
                    self.board.point_accessor(self.point,self.line,self.convex_line,self.convex_line[-2:],clear=False)
                    # self.board.point_accessor(self.point,tmp_test,self.convex_line,self.convex_line[-2:],clear=False)
                else:
                    self.close()
                self.now = self.now + 1
        else:
            #print("points:",self.board.point)
            self.mode = self.board.mode
            edge_list = Edge()
            self.point, edge_list,_,self.convex_line = self.voronoi.calu_run(self.board.point)
            #self.point.append(mid_points)
            #print("after",self.point)
            # print("len:",len(edge_list))
            for edge in edge_list:
                self.line.append(edge.mid_line)
                #print(edge.mid_line)
            self.board.point_accessor(self.point,self.line,self.convex_line,self.convex_line[-2:],clear=False)
            # self.board.point_accessor(self.point,tmp_test,self.convex_line,self.convex_line[-2:],clear=False)
            self.board.update_mode(self.mode)
            #print("Point: ",self.board.object_point)
            #print("Line: ",self.board.object_line)
        self.save_data()

    def click_step_by_step(self):
        h = []              #hpyer plane
        L_m = []              #mid line
        R_m = []
        cL = []              #convex hull
        cR = []
        cT = []
        p = []
        path = 'test1.txt'
        with open(path, 'r', encoding='utf-8') as f:
            for i,line in enumerate(f.readlines()):
                print("i:",i," ",self.step_by_step_now)
                print("outer line",line)
                if i >= self.step_by_step_now:
                    print("line",line)
                    if line[0] == '\n':
                        break
                    else:
                        tmp_line = line[2:]
                        tmp_string = tmp_line.rstrip('\n')
                        tmp_list = tmp_string.split()
                        tmp_list = list(map(int, tmp_list))
                        print('tmp_list:',tmp_list)
                        if line[0] == 'h':
                            h.append(tmp_list)
                        elif line[0:2] == 'Lm':
                            L_m.append(tmp_list)
                        elif line[0:2] == 'Rm':
                            L_m.append(tmp_list)
                        elif line[0:2] == 'cL':
                            cL.append(tmp_list)
                        elif line[0:2] == 'cR':
                            cL.append(tmp_list)
                        elif line[0:2] == 'cT':
                            cL.append(tmp_list)
                        elif line[0] == 'p':
                            p.append(tmp_list)
                        elif line[0] == 'r':
                            self.board.Clear()
                    self.step_by_step_now += 1
        self.step_by_step_now += 1
        print("send before:",cL)
        self.board.step_point_accessor(p,L_m,R_m,[],cL,cR,cT,h)                              
                #self.step_by_step_now
                
                
                # print()
        print("I")

    def click_load_file(self):
        fname, _ = QFileDialog.getOpenFileName(self,"open File","","All Files (*);;Text Files (*.txt)")

        if len(fname) == 0:
            print("\nCancel!!!")
            return 
        self.mode = "file"
        self.board.update_mode(self.mode)
        self.load_data_from_file(fname)

    def load_data_from_file(self,fname):
        self.now = 0
        self.data_list = []
        self.complete_data = []
        path = fname
        with open(path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                    if line[0] == '#' or line[0] == "\n":
                        continue
                    tmp_string = line.rstrip('\n')
                    tmp_list = tmp_string.split()
                    if line[0] == 'P' or line[0] == 'E':            #讀取已做完的數據畫成圖
                        self.complete_data.append(tmp_list)
                    else:
                        self.data_list.append(tmp_list)             #讀取未計算的點
                    
    def click_clear(self):
        self.line = []
        self.point = []
        self.board.Clear()

    def click_Display(self):
        self.board.Clear()
        for _, data in enumerate(self.complete_data):
            if data[0] == 'P':
                self.point.append([int(data[1]),int(data[2])])
            else:
                self.line.append([int(data[1]),int(data[2]),
                                    int(data[3]),int(data[4])])
        self.board.ChangePenColor("red")
        self.board.point_accessor(self.point,self.line,[],[],clear=True)
        self.board.update_mode(self.mode)

    def save_data(self):
        points = self.point
        lines = self.line
        points.sort(key=lambda x: (x[0],x[1]))
        lines.sort(key=lambda x:[x[0],x[1],x[2],x[3]])
        with open('output.txt','w') as f:
            for point in points:
                f.write("P ")
                for element in point:
                    f.write(str(element)+" ")
                f.write("\n")
        with open('output.txt','a') as f:
            for line in lines:
                f.write("E ")
                for element in line:
                    f.write(str(element)+" ")
                f.write("\n")
        
#===============================================================================================================================================



#===========================================================PaintBoard.py======================================================================


from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import QPixmap, QPainter, QPoint, QPaintEvent, QMouseEvent, QPen,\
    QColor, QSize,QLine
from PyQt5.QtCore import Qt

color = [QColor("black"),QColor("red"),QColor("blue"),QColor("yellow")
        ,QColor("magenta"),QColor("cyan"),QColor("gray")]
class PaintBoard(QWidget):


    def __init__(self, Parent=None):
        '''
        Constructor
        '''
        super().__init__(Parent)

        self.__InitData() #先初始化資料，再初始化介面
        self.__InitView()
        self.mode = ""

    def __InitData(self):

        self.__size = QSize(600,600)

        #新建QPixmap作為畫板，尺寸為__size
        self.__board = QPixmap(self.__size)
        self.__board.fill(Qt.white) #用白色填充畫板

        self.__IsEmpty = True #預設為空畫板 
        #self.pen = QPen(Qt.red, 5, Qt.SolidLine)
        self.__penColor = QColor("black")#設定預設畫筆顏色為黑色
        self.object_point = []
        self.object_line = []
        self.two_lines = []
        self.point = []
        self.line = []
        self.convex_line = []
        self.cL = []
        self.cR = []
        self.cT = []
        self.L_line = []
        self.R_line = []
        self.hyperplane = []

    def __InitView(self):
        #設定介面的尺寸為__size
        self.setFixedSize(self.__size)

    def Clear(self):
        #清空畫板
        print("clear")
        #self.__board.fill(Qt.white)
        self.object_point = []
        self.object_line = []
        self.point = []
        self.line = []
        self.L_line = []
        self.R_line = []
        self.convex_line = []
        self.two_lines = []
        self.cL = []
        self.cR = []
        self.cT = []
        self.hyperplane = []
        self.update()
        self.__IsEmpty = True


    def IsEmpty(self):
        #返回畫板是否為空
        return self.__IsEmpty
    
    def check_mode(self):
        return self.mode

    def GetContentAsQImage(self):
        #獲取畫板內容（返回QImage）
        image = self.__board.toImage()
        return image

    def paintEvent(self, paintEvent):
        #繪圖事件
        #繪圖時必須使用QPainter的例項，此處為__painter
        #繪圖在begin()函式與end()函式間進行
        #begin(param)的引數要指定繪圖裝置，即把圖畫在哪裡
        #drawPixmap用於繪製QPixmap型別的物件
        #self.__painter = QPainter()#新建繪圖工具
        self.__painter = QPainter()#新建繪圖工具
        self.__painter.begin(self)
        #self.__painter1.begin(self)
        # 0,0為繪圖的左上角起點的座標，__board即要繪製的圖
        self.__painter.setPen(QPen(self.__penColor, 4, Qt.SolidLine))
        self.__painter.drawPixmap(0,0,self.__board)
        self.__painter.drawPoints(self.object_point)
        #if len(self.line):
        self.__painter.setPen(QPen(color[0], 4, Qt.SolidLine))
        self.__painter.drawLines(self.object_line)
        self.__painter.drawLines(self.L_line)

        self.__painter.setPen(QPen(color[1], 4, Qt.SolidLine))
        self.__painter.drawLines(self.convex_line)

        self.__painter.setPen(QPen(color[3], 4, Qt.SolidLine))
        self.__painter.drawLines(self.two_lines)

        self.__painter.setPen(QPen(color[4], 4, Qt.SolidLine))
        self.__painter.drawLines(self.cL)

        self.__painter.setPen(QPen(color[5], 4, Qt.SolidLine))
        self.__painter.drawLines(self.hyperplane)
        # self.__painter.setPen(QPen(color[4], 4, Qt.SolidLine))
        self.__painter.drawLines(self.cR)
        self.__painter.setPen(QPen(color[2], 4, Qt.SolidLine))
        self.__painter.drawLines(self.R_line)
        # self.__painter.setPen(QPen(color[6], 4, Qt.SolidLine))
        self.__painter.drawLines(self.cT)
        self.__painter.setPen(QPen(color[2], 4, Qt.SolidLine))
        self.__painter.drawLines(self.two_lines)
        self.update()
        self.__painter.end()

    def mousePressEvent(self, mouseEvent):
        #滑鼠按下時，獲取滑鼠的當前位置儲存為上一次位置
        x = mouseEvent.pos().x()
        y = mouseEvent.pos().y()
        self.mode = "dot"
        self.object_point.append(QPoint(x,y))
        self.point.append((x,y))
        self.__IsEmpty = False

    def update_mode(self,mode):
        self.mode = mode

    def point_accessor(self,point,line,convex,two_lines,clear):
        if clear == False:
            print("no clean")
        if clear == True:
            self.Clear()
            # self.obect_point = []
            # self.object_line = []
        if len(point)!=0:
            for time, num in enumerate(point):
                self.object_point.append(QPoint(num[0],num[1]))
                self.point.append((num[0],num[1]))
        if len(line)!=0:
            for time,num in enumerate(line):   
                self.object_line.append(QLine(num[0],num[1],
                                        num[2],num[3]))
        if len(convex)!=0:
            for time,num in enumerate(convex):   
                self.convex_line.append(QLine(num[0],num[1],
                                        num[2],num[3]))
        if len(two_lines)!=0:
            #print("Two_lines:",two_lines)
            for time,num in enumerate(two_lines):   
                self.two_lines.append(QLine(num[0],num[1],
                                        num[2],num[3]))
    def ChangePenColor(self, color="black"):
        #改變畫筆顏色
        self.__penColor = QColor(color)

    def step_point_accessor(self,point,L_line,R_line,two_lines,cL,cR,cT,hyperplane):
        # if clear == False:
        #     print("no clean")
        # if clear == True:
        #     self.Clear()
            # self.obect_point = []
            # self.object_line = []
        if len(point)!=0:
            for time, num in enumerate(point):
                self.object_point.append(QPoint(num[0],num[1]))
                self.point.append((num[0],num[1]))
        if len(L_line)!=0:
            for time,num in enumerate(L_line):   
                self.L_line.append(QLine(num[0],num[1],
                                        num[2],num[3]))
        if len(R_line)!=0:
            for time,num in enumerate(R_line):   
                self.R_line.append(QLine(num[0],num[1],
                                        num[2],num[3]))

        if len(two_lines)!=0:
            #print("Two_lines:",two_lines)
            for time,num in enumerate(two_lines):   
                self.two_lines.append(QLine(num[0],num[1],
                                        num[2],num[3]))
        if len(cL)!=0:
            #print("Two_lines:",two_lines)
            for time,num in enumerate(cL):   
                self.cL.append(QLine(num[0],num[1],
                                        num[2],num[3]))
        print(self.cL)
        if len(cR)!=0:
            #print("Two_lines:",two_lines)
            for time,num in enumerate(cR):   
                self.cR.append(QLine(num[0],num[1],
                                        num[2],num[3]))
        if len(cT)!=0:
            #print("Two_lines:",two_lines)
            for time,num in enumerate(cT):   
                # self.cT.append((QPoint(num[0],num[1])))
                # self.cT.append((QPoint(num[2],num[3])))
                self.cT.append(QLine(num[0],num[1],
                                        num[2],num[3]))
        if len(hyperplane)!=0:
            #print("Two_lines:",two_lines)
            for time,num in enumerate(hyperplane):   
                self.hyperplane.append(QLine(num[0],num[1],
                                        num[2],num[3]))


#============================================================================================================================================


#===============================================================Voronoi.py===================================================================


import math
import numpy as np
import itertools

class Edge():
    def __init__(self) -> None:
        self.length = 0
        self.vector = []
        self.slope = 0
        self.mid_point = []
        self.order_point = []
        self.mid_line = []                                      #mid_line = voronoi edge
    def reset(self):
        self.slope = 0
        self.length = 0
        self.vector = []
        self.mid_point = []
        self.order_point = []


class Voronoi():
    def __init__(self):
        self.edge_list = []
        self.points = []
        self.lines = []
        self.outer_center = []
        #convex_hull_edge = []
        self.mid_lines = []

    def calu_run(self,points,line=[]):
        output_points = []
        mid_lines = []
        mid_lines11 = []
        output_points1 = []
        convex_hull_edge = []
        convex_hull_edge1 = []
        convex_points = []
        intersec_two_edges = []                                                 #!!!!!!!!!!之後要刪掉
        self.reset()
        points = list(set(points))                                              #將所有重複地點去除
        points.sort(key=lambda x: (x[0],x[1]))
        #print("points:",points)
        if len(points) == 1:                                                    #一點
            return points,self.edge_list,convex_points,convex_hull_edge
        elif len(points) <= 3:
            order_points = list(itertools.combinations(points,2))
            #print("ORDER_POINTS:",order_points)
            collinear = self.check_collinear(order_points)
            convex_points = self.convex_hull(points)
            if collinear == True:                                                   #三點共線
                order_points = []
                order_points.append((points[0],points[1]))
                order_points.append((points[1],points[2]))

            for i,order_point in enumerate(order_points):                           #主要都是在初始與計算所有邊的資訊(兩點同時會在這處理完)
                edge = Edge()
                # print("order_point:",order_point)
                tmp_mid_point = self.calu_mid_point(order_point)
                #print("mid_point:",tmp_mid_point)
                slope = self.mid_line(tmp_mid_point, order_point)
                length = self.calu_two_point_lengh(order_point)
                #print("length:",length)
                edge.length = length
                edge.slope = slope                                                  #中垂線的斜率
                edge.mid_point = tmp_mid_point
                edge.order_point = order_point
                self.points.append([tmp_mid_point[0], tmp_mid_point[1]])
                self.edge_list.append(edge)
            for point in points:
                output_points.append(point)
            if len(points) > 2:                                                     #三點
                if collinear == False:
                    self.outer_center = self.get_line_cross_point(self.lines[0],self.lines[1])
                    print("outer:",self.outer_center)
                    angle, max_index  = self.check_obtuse_angle()                                       #確認是否鈍角
                    self.calu_vector()
                    if angle == 1:                                                                      #鈍角
                        self.edge_list[max_index].vector[0] = -self.edge_list[max_index].vector[0]
                        self.edge_list[max_index].vector[1] = -self.edge_list[max_index].vector[1]
                    elif angle == 2:                                                                    #等腰直角三角形
                        tmp_index, tmp_vector = self.isosceles_right(points)
                        self.edge_list[tmp_index].vector[0] = tmp_vector[0]
                        self.edge_list[max_index].vector[1] = tmp_vector[1]
                    self.line_bound()
                    #convex_points = self.convex_hull(points)

            #print("self.lines:",self.lines)
            for i,order_point in enumerate(order_points):                                               #放回要傳回的陣列主要紀錄所有線段的都在self.lines
                mid_lines.append([int(self.lines[i][0][0]), int(self.lines[i][0][1])
                                ,int(self.lines[i][1][0]),int(self.lines[i][1][1])])
                self.edge_list[i].mid_line = [int(self.lines[i][0][0]), int(self.lines[i][0][1])
                                            ,int(self.lines[i][1][0]),int(self.lines[i][1][1])]

            for i,point in enumerate(convex_points):
                second = (i+1) % len(convex_points)
                convex_hull_edge.append([int(point[0]),int(point[1]),int(convex_points[second][0]),int(convex_points[second][1])])
            # print("voronoi output:",mid_lines)
        else:
            sub_size = len(points) / 2
            #print("sub_size:",sub_size)
            if sub_size % 1 != 0:
                sub_size = int(sub_size) + 1
                print("in")
            sub_size = int(sub_size)
            tmp = points[0:sub_size]
            tmp1 = points[sub_size:]
            #print("tmp:",tmp)
            #print("tmp1:",tmp1)
            total_edge_list = []
            output_points, edge_list1, convex_points,_ = self.calu_run(tmp)              #mid_lines就是voronoi edges
            output_points1, edge_list2, convex_points1,_= self.calu_run(tmp1)          
            total_points,total_edge_list,convex_points,convex_hull_edge = self.merge(edge_list1, edge_list2, tmp, tmp1)
            output_points = total_points
            self.edge_list = total_edge_list
        return output_points, self.edge_list, convex_points, convex_hull_edge


    def merge(self,edge_list1,edge_list2,L_points,R_points):
        path = 'test1.txt'
        f = open(path,'a')
        total_points = []
        #convex_points
        total_mid_lines = []
        total_edge_list = []
        for line in edge_list1:
            total_mid_lines.append(line.mid_line)
        for line in edge_list2:
            total_mid_lines.append(line.mid_line)
        for point in R_points:
            total_points.append(point)
            print('p',point[0],point[1],file=f)
        for point in L_points:
            total_points.append(point)
            print('p',point[0],point[1],file=f)
        print('',file=f)
        for edge in edge_list1:
            total_edge_list.append(edge)
            print('Lm',edge.mid_line[0],edge.mid_line[1],edge.mid_line[2],edge.mid_line[3],file=f)
        print('',file=f)
        for edge in edge_list2:
            total_edge_list.append(edge)
        #     print('Rm',edge.mid_line[0],edge.mid_line[1],edge.mid_line[2],edge.mid_line[3],file=f)
        # print('',file=f)
        original_len = len(total_edge_list)
        big_convex_hull_edges = []
        L_convex_hull_edges = []
        R_convex_hull_edges = []
        intersec_two_edges = []
        top = []
        bottom = []
        merge_order_point = []
        #print("convex_points:",total_points)
        L_convex_hull_points = self.convex_hull(L_points)
        R_convex_hull_points = self.convex_hull(R_points)
        for i,L_convex_hull_point in enumerate(L_convex_hull_points):
            second = (i+1) % len(L_convex_hull_points)
            L_convex_hull_edges.append([int(L_convex_hull_point[0]),int(L_convex_hull_point[1]),int(L_convex_hull_points[second][0]),int(L_convex_hull_points[second][1])])
            print('cL',int(L_convex_hull_point[0]),int(L_convex_hull_point[1]),int(L_convex_hull_points[second][0]),int(L_convex_hull_points[second][1]),file=f)
        print('',file=f)
        for edge in edge_list2:
            print('Rm',edge.mid_line[0],edge.mid_line[1],edge.mid_line[2],edge.mid_line[3],file=f)
        print('',file=f)
        for i,R_convex_hull_point in enumerate(R_convex_hull_points):
            second = (i+1) % len(R_convex_hull_points)
            R_convex_hull_edges.append([int(R_convex_hull_point[0]),int(R_convex_hull_point[1]),int(R_convex_hull_points[second][0]),int(R_convex_hull_points[second][1])])
            print('cR',int(R_convex_hull_point[0]),int(R_convex_hull_point[1]),int(R_convex_hull_points[second][0]),int(R_convex_hull_points[second][1]),file=f)
        print('',file=f)
        big_convex_hull_points = self.convex_hull(total_points)
        for i,big_convex_hull_point in enumerate(big_convex_hull_points):
            second = (i+1) % len(big_convex_hull_points)
            big_convex_hull_edges.append([int(big_convex_hull_point[0]),int(big_convex_hull_point[1]),int(big_convex_hull_points[second][0]),int(big_convex_hull_points[second][1])])
            print('cT',int(big_convex_hull_point[0]),int(big_convex_hull_point[1]),int(big_convex_hull_points[second][0]),int(big_convex_hull_points[second][1]),file=f)
        print('',file=f)
        # print("big_convex_hull_points:",big_convex_hull_points)
        for i,point in enumerate(big_convex_hull_points):
            second = (i+1) % len(big_convex_hull_points)
            if point in L_points and big_convex_hull_points[second] in R_points:                    #先找到有連接左右兩部分的邊
                intersec_two_edges.append([(int(point[0]),int(point[1])),(int(big_convex_hull_points[second][0]),int(big_convex_hull_points[second][1]))])
            elif point in R_points and big_convex_hull_points[second] in L_points:
                intersec_two_edges.append([(int(point[0]),int(point[1])),(int(big_convex_hull_points[second][0]),int(big_convex_hull_points[second][1]))])
        if (intersec_two_edges[0][0][1] +intersec_two_edges[0][1][1]) < (intersec_two_edges[1][0][1] +intersec_two_edges[1][1][1]):         #找一開始的邊
            top = intersec_two_edges[0]
            bottom = intersec_two_edges[1]
        else:
            top = intersec_two_edges[1]
            bottom = intersec_two_edges[0]
        # print("top:",top)                                                                           #找到最開始的線
        merge_order_point = top
        last_point = []
        used_order_point = []

        while merge_order_point != bottom:
        # for i in range(4):
            edge = Edge()
            edge.order_point = (merge_order_point[0],merge_order_point[1])
            edge.mid_point = self.calu_mid_point(merge_order_point)
            edge.length = self.calu_two_point_lengh(edge.order_point)
            edge.slope = self.calu_ver_slope(merge_order_point[0],merge_order_point[1])
            #print("oredr_point:",total_edge_list[0].order_point)
            merge_mid_line = self.mid_calu_line(edge.mid_point,edge.slope)
            if len(last_point) == 0:
                if merge_mid_line[0][1] > merge_mid_line[1][1]:
                    last_point = merge_mid_line[1]
                else:
                    last_point = merge_mid_line[0]
    
            min_order_point = []
            min_length = 999999
            min_cross_point = []
            for i,obj in enumerate(total_edge_list):
                if obj.order_point not in used_order_point and i < original_len:
                    #計算兩條線是否有相交
                    obj_mid_line = [(obj.mid_line[0],obj.mid_line[1]),(obj.mid_line[2],obj.mid_line[3])]
                    cross = self.merge_check_cross(obj_mid_line,merge_mid_line)
                    if cross != None and cross[1] >= last_point[1]: 
                        #算出與每一條的距離
                        length = self.calu_two_point_lengh((last_point,cross))
                        if length < min_length:
                            min_order_point = obj.order_point
                            min_cross_point = cross
                            min_length = length
            # print("last_point:",last_point," min_cross_point:",min_cross_point," order_point:",min_order_point)
            if len(min_cross_point) == 0:
                break 
            edge.mid_line = [int(last_point[0]),int(last_point[1]),int(min_cross_point[0]),int(min_cross_point[1])]
            edge.vector = [min_cross_point[0] - last_point[0], min_cross_point[1] - last_point[1]]
            # print("Append + 1 !!!!!")
            total_edge_list.append(edge)
            different = set(merge_order_point).symmetric_difference(set(min_order_point))
            merge_order_point = list(different)
            print("merge_order_point:",merge_order_point)
            last_point = min_cross_point
            used_order_point.append(min_order_point)
            
        #底部
        edge = Edge()
        edge.order_point = (bottom[0],bottom[1])
        edge.mid_point = self.calu_mid_point(edge.order_point)
        edge.slope = self.calu_ver_slope(edge.order_point[0],edge.order_point[1])
        edge.length = self.calu_two_point_lengh(edge.order_point)
        merge_mid_line = self.mid_calu_line(edge.mid_point, edge.slope)
        # print("merge_mid_line:",merge_mid_line)
        if merge_mid_line[0][1] < merge_mid_line[1][1]:
            edge.mid_line = [int(last_point[0]),int(last_point[1]),int(merge_mid_line[1][0]),int(merge_mid_line[1][1])]
        else:
            edge.mid_line = [int(last_point[0]),int(last_point[1]),int(merge_mid_line[0][0]),int(merge_mid_line[0][1])]
        edge.vector = [edge.mid_line[2] - last_point[0], edge.mid_line[3] - last_point[1]]
        total_edge_list.append(edge)

                # print(len(total_edge_list)-original_len,file=f)
        for num,txt_edge in enumerate(total_edge_list):
            if num >= original_len:
                print('h',txt_edge.mid_line[0],txt_edge.mid_line[1],txt_edge.mid_line[2],txt_edge.mid_line[3],file=f)

        print("cut!!!!")
        delete_indexs = []
        for i in range(len(edge_list1)):
            cross_flag = False
            for j in range(original_len,len(total_edge_list)):
                line = [(total_edge_list[i].mid_line[0],total_edge_list[i].mid_line[1]),(total_edge_list[i].mid_line[2],total_edge_list[i].mid_line[3])]
                hp_line = [(total_edge_list[j].mid_line[0],total_edge_list[j].mid_line[1]),(total_edge_list[j].mid_line[2],total_edge_list[j].mid_line[3])]
                cut_cross = self.cut_check_cross(line,hp_line)
                if cut_cross != None:
                    cross_flag = True
                    print("左邊")
                    print(total_edge_list[i].mid_line," ",cut_cross)
                    if (np.abs(total_edge_list[i].mid_line[0]-cut_cross[0])<=1 and np.abs(total_edge_list[i].mid_line[1]-cut_cross[1])<=1) or \
                    (np.abs(total_edge_list[i].mid_line[2]-cut_cross[0])<=1 and np.abs(total_edge_list[i].mid_line[3]-cut_cross[1])<=1):
                        continue
                    else:
                        print("在裡面")
                        if total_edge_list[i].mid_line[1] < total_edge_list[i].mid_line[3]:                     #比y(找出高跟低 越高越小值)
                            print("前面點較小")
                            if total_edge_list[i].mid_line[0] < total_edge_list[j].mid_line[0]:                 #比x
                                total_edge_list[i].mid_line[2] = cut_cross[0]
                                total_edge_list[i].mid_line[3] = cut_cross[1]
                            else:
                                total_edge_list[i].mid_line[0] = cut_cross[0]
                                total_edge_list[i].mid_line[1] = cut_cross[1]
                        
                        elif total_edge_list[i].mid_line[1] > total_edge_list[i].mid_line[3]:
                            print("後面點比較小")
                            if total_edge_list[i].mid_line[2] < total_edge_list[j].mid_line[0]:                 #比x
                                total_edge_list[i].mid_line[0] = cut_cross[0]
                                total_edge_list[i].mid_line[1] = cut_cross[1]
                            else:
                                total_edge_list[i].mid_line[2] = cut_cross[0]
                                total_edge_list[i].mid_line[3] = cut_cross[1]
                        else:                                                                                   #水平
                            if total_edge_list[i].mid_line[2] < total_edge_list[j].mid_line[0]:                 #比x
                                total_edge_list[i].mid_line[0] = cut_cross[0]
                                total_edge_list[i].mid_line[1] = cut_cross[1]
                            else:
                                total_edge_list[i].mid_line[2] = cut_cross[0]
                                total_edge_list[i].mid_line[3] = cut_cross[1]

            if cross_flag == False:
                if total_edge_list[i].mid_line[0] > total_edge_list[-1].mid_line[0]:
                    print("DELETE append",i)
                    delete_indexs.append(i)

        print("換右邊了")
        for i in range(len(edge_list1),original_len):                                                     #右邊
            cross_flag = False
            for j in range(original_len,len(total_edge_list)):
                line = [(total_edge_list[i].mid_line[0],total_edge_list[i].mid_line[1]),(total_edge_list[i].mid_line[2],total_edge_list[i].mid_line[3])]
                hp_line = [(total_edge_list[j].mid_line[0],total_edge_list[j].mid_line[1]),(total_edge_list[j].mid_line[2],total_edge_list[j].mid_line[3])]
                cut_cross = self.cut_check_cross(line,hp_line)
                if cut_cross != None:
                    cross_flag = True
                    print("right Cross!!!!")
                    print(total_edge_list[i].mid_line," ",cut_cross)
                    if (np.abs(total_edge_list[i].mid_line[0]-cut_cross[0])<=1 and np.abs(total_edge_list[i].mid_line[1]-cut_cross[1])<=1) or \
                    (np.abs(total_edge_list[i].mid_line[2]-cut_cross[0])<=1 and np.abs(total_edge_list[i].mid_line[3]-cut_cross[1])<=1):
                        continue
                    else:
                        print("在裡面")
                        if total_edge_list[i].mid_line[1] < total_edge_list[i].mid_line[3]:                             #比y
                            # print("前面點較小")
                            if total_edge_list[i].mid_line[0] < total_edge_list[j].mid_line[0]:
                                total_edge_list[i].mid_line[0] = cut_cross[0]
                                total_edge_list[i].mid_line[1] = cut_cross[1]
                            else:
                                total_edge_list[i].mid_line[2] = cut_cross[0]
                                total_edge_list[i].mid_line[3] = cut_cross[1]

                        elif total_edge_list[i].mid_line[1] > total_edge_list[i].mid_line[3]: 
                            # print("後面點較大")
                            if total_edge_list[i].mid_line[2] < total_edge_list[j].mid_line[0]:
                                total_edge_list[i].mid_line[2] = cut_cross[0]
                                total_edge_list[i].mid_line[3] = cut_cross[1]
                            else:
                                total_edge_list[i].mid_line[0] = cut_cross[0]
                                total_edge_list[i].mid_line[1] = cut_cross[1]
                        else:                                                                                           #水平
                            if total_edge_list[i].mid_line[2] < total_edge_list[j].mid_line[0]:
                                total_edge_list[i].mid_line[2] = cut_cross[0]
                                total_edge_list[i].mid_line[3] = cut_cross[1]
                            else:
                                total_edge_list[i].mid_line[0] = cut_cross[0]
                                total_edge_list[i].mid_line[1] = cut_cross[1]

            if cross_flag == False:
                if total_edge_list[i].mid_line[0] < total_edge_list[-1].mid_line[0]:
                    print("delete one!!!!!!")
                    delete_indexs.append(i)
        

        if len(delete_indexs) != 0: 
            for delete_index in reversed(delete_indexs):
                print("delete one!!!!!!")
                del total_edge_list[delete_index]

        print('',file=f)
        print('r',file=f)
        # print('',file=f)

        for point in total_points:
            print('p',point[0],point[1],file=f)
        # print('',file=f)

        for num,txt_edge in enumerate(total_edge_list):
            print('h',txt_edge.mid_line[0],txt_edge.mid_line[1],txt_edge.mid_line[2],txt_edge.mid_line[3],file=f)

        f.close()

        for edge in intersec_two_edges:
            big_convex_hull_edges.append([edge[0][0],edge[0][1],edge[1][0],edge[1][1]])

        return total_points,total_edge_list,big_convex_hull_points,big_convex_hull_edges

    def merge_cut_clockwise(self,v1,v2):
        # print("np.linalg(v1):",np.linalg(v1))
        theNorm = np.linalg.norm(v1)*np.linalg.norm(v2)
        rho = np.rad2deg(np.arcsin(np.cross(v1,v2)/theNorm))
        theta = np.rad2deg(np.arccos(np.dot(v1,v2)/theNorm))
        if rho < 0:
            return -theta
        else:
            return theta

    def point_distance_line(self,point,line_poin1,line_poin2):
        print("point:",point)
        a = line_poin2[1] - line_poin1[1]
        b = line_poin1[0] - line_poin2[0]
        c = (line_poin1[1] - line_poin2[1]) * line_poin1[0] +\
            (line_poin2[0] - line_poin1[0]) * line_poin1[1]
        print("A:",a,"B:",b,"C:",c)
        distance = np.abs(a*point[0][0]+b*point[0][1]+c) /(np.sqrt(a**2 + b**2))
        return distance

    def cut_check_cross(self,obj_mid_line,tmp_mid_line):
        obj_high_x = 0
        obj_low_x = 0
        obj_high_y = 0
        obj_low_y = 0
        tmp_high_x = 0
        tmp_low_x = 0
        tmp_high_y = 0
        tmp_low_y = 0
        cross_point = self.get_line_cross_point(obj_mid_line,tmp_mid_line)
        # print("cross point:",cross_point)
        # print("tmp_mid_line",tmp_mid_line)
        if cross_point != None:
            if obj_mid_line[0][0] < obj_mid_line[1][0]:
                obj_high_x = obj_mid_line[1][0]
                obj_low_x = obj_mid_line[0][0]
            else:
                obj_high_x = obj_mid_line[0][0]
                obj_low_x = obj_mid_line[1][0]
            if obj_mid_line[0][1] < obj_mid_line[1][1]:
                obj_high_y = obj_mid_line[1][1]
                obj_low_y = obj_mid_line[0][1]
            else:
                obj_high_y = obj_mid_line[0][1]
                obj_low_y = obj_mid_line[1][1]

            if tmp_mid_line[0][0] < tmp_mid_line[1][0]:
                tmp_high_x = tmp_mid_line[1][0]
                tmp_low_x = tmp_mid_line[0][0]
            else:
                tmp_high_x = tmp_mid_line[0][0]
                tmp_low_x = tmp_mid_line[1][0]
            if tmp_mid_line[0][1] < tmp_mid_line[1][1]:
                tmp_high_y = tmp_mid_line[1][1]
                tmp_low_y = tmp_mid_line[0][1]
            else:
                tmp_high_y = tmp_mid_line[0][1]
                tmp_low_y = tmp_mid_line[1][1]

            if obj_high_x < cross_point[0] or obj_low_x > cross_point[0]:
                return None
            if obj_high_y < cross_point[1] or obj_low_y > cross_point[1]:
                return None
            if obj_high_x < cross_point[0] or obj_low_x > cross_point[0]:
                return None
            if obj_high_y < cross_point[1] or obj_low_y > cross_point[1]:
                return None

            if tmp_high_x < cross_point[0] or tmp_low_x > cross_point[0]:
                return None
            if tmp_high_y < cross_point[1] or tmp_low_y > cross_point[1]:
                return None
            if tmp_high_x < cross_point[0] or tmp_low_x > cross_point[0]:
                return None
            if tmp_high_y < cross_point[1] or tmp_low_y > cross_point[1]:
                return None
            return cross_point
        else:
            return None

    def merge_check_cross(self,obj_mid_line,tmp_mid_line):
        obj_high_x = 0
        obj_low_x = 0
        obj_high_y = 0
        obj_low_y = 0
        cross_point = self.get_line_cross_point(obj_mid_line,tmp_mid_line)
        # print("cross point:",cross_point)
        # print("tmp_mid_line",tmp_mid_line)
        if cross_point != None:
            # print("Cross point:",cross_point)
            if obj_mid_line[0][0] < obj_mid_line[1][0]:
                obj_high_x = obj_mid_line[1][0]
                obj_low_x = obj_mid_line[0][0]
            else:
                obj_high_x = obj_mid_line[0][0]
                obj_low_x = obj_mid_line[1][0]
            if obj_mid_line[0][1] < obj_mid_line[1][1]:
                obj_high_y = obj_mid_line[1][1]
                obj_low_y = obj_mid_line[0][1]
            else:
                obj_high_y = obj_mid_line[0][1]
                obj_low_y = obj_mid_line[1][1]
            if obj_high_x < cross_point[0] or obj_low_x > cross_point[0]:
                return None
            if obj_high_y < cross_point[1] or obj_low_y > cross_point[1]:
                return None
            return cross_point
        else:
            return None

    def check_collinear(self,order_points):                             #確認是否三點共線
        before_slope = None
        collinear = False
        for order_point in order_points:                                        
            slope = self.calu_ver_slope(order_point[0],order_point[1])
            if slope == before_slope:
                collinear = True
            before_slope = slope
        return collinear

    def isosceles_right(self,points):
        modify_index = -1
        order_point = []
        for i,obj in enumerate(self.edge_list):
            print("vector:",obj.vector)
            #if obj.vector == [0,0] or obj.vector == [1,0] or obj.vector == [0,1] or obj.vector == [-1,0] or obj.vector == [0,-1]:
            if obj.vector == [0,0]:
                modify_index = i
                order_point = obj.order_point
                break
        for point in order_point:
            print("order point:",point)
            if point in points:
                points.remove(point)
        vector = [self.outer_center[0]-points[0][0]
                 ,self.outer_center[1]-points[0][1]]
        print("iso_right points:",points)
        return modify_index,vector
    
    def convex_hull_cross3(self,a, b, c):
        return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

    def convex_hull(self,points):
        points.sort(key=lambda x: (x[0],x[1]))
        stack = []
        num = len(points)
        for point in points:
            while len(stack) > 1 and self.convex_hull_cross3(stack[-1], stack[-2], point) > 0:
                stack.pop()
            stack.append(point)
        t = len(stack)
        for i in range(num-2, -1, -1):
            tmp_point = points[i]
            while len(stack) > t and self.convex_hull_cross3(stack[-1], stack[-2], tmp_point) > 0:
                stack.pop()
            stack.append(tmp_point)
        return stack

    def check_obtuse_angle(self):
        max_index = -1
        max_length = 0
        total = 0
        for i,obj in enumerate(self.edge_list):
            if obj.length**2 > max_length:
                max_length = obj.length**2
                max_index = i
            total += obj.length**2
        if total - max_length < max_length:
            return 1, max_index
        elif total - max_length == max_length:
            return 2,max_index
        else:
            return 0,max_index

    def calu_vector(self):                                          #微調整向量，因為向量可能在計算時有偏差
        for i,edge in enumerate(self.edge_list):
            if abs(edge.mid_point[0] - self.outer_center[0]) < 1:
                edge.mid_point[0] = self.outer_center[0]
            if abs(edge.mid_point[1] - self.outer_center[1]) < 1:
                edge.mid_point[1] = self.outer_center[1]
            edge.vector = [edge.mid_point[0] - self.outer_center[0]
                            ,edge.mid_point[1] - self.outer_center[1]]
            #print("vector:",edge.vector)

    def reset(self):
        self.edge_list = []
        self.points = []
        self.lines = []
        self.outer_center = []

    def calu_mid_point(self, order_point):
        mid_point = np.mean(order_point, axis=0)
        return mid_point

    def calu_two_point_lengh(self,order_point):
        x = order_point[0][0] - order_point[1][0]
        y = order_point[0][1] - order_point[1][1]
        return np.sqrt(x**2+y**2)

        

    def calu_step(self):
        print(0)
    
    def mid_line_formula_y(self,mid_point,slope,x):
        return (slope*(x - mid_point[0]) + mid_point[1])

    def mid_line_formula_x(self,mid_point,slope,y):
        if slope == 0:
            # return mid_point[0]
            return math.inf
        return ((y - mid_point[1])/slope + mid_point[0])

    def mid_calu_line(self,mid_point,slope):
        x = [-600, 1200]
        y = [-600, 1200]
        result = []
        for i in x:
            tmp_y = self.mid_line_formula_y(mid_point,slope,i)
            if tmp_y >= -600 and tmp_y <=1200:
                result.append((i,tmp_y))
                #print((i,tmp_y))
        for i in y:
            tmp_x = self.mid_line_formula_x(mid_point,slope,i)
            if tmp_x >=-600 and tmp_x <= 1200:
                result.append((tmp_x,i))
                #print((tmp_x,i))
        if len(result) != 2:
            result = list(set(result))
        return result


    def mid_line(self, mid_point, order_point):                             #將所有中垂線放入self.lines
        slope = self.calu_ver_slope(order_point[0],order_point[1])
        self.lines.append(self.mid_calu_line(mid_point,slope))
        return slope

    def calu_ver_slope(self, point1, point2):                               #算法線的斜率
        slope = 0
        up = point1[0] - point2[0]
        bottom = point1[1] - point2[1]
        if bottom == 0:
            slope = 99999
        else:
            slope = -(up/bottom)
        return slope


    def line_bound(self):                                                   #單一部分去做剪線(2、3個點)
        outer_x = self.outer_center[0]
        outer_y = self.outer_center[1]
        x_bound = -1
        y_bound = -1
        for i,obj in enumerate(self.edge_list):
            # print("outer x:",outer_x,"outer y:",outer_y)
            # print("vector x:",obj.vector[0],"vector y",obj.vector[1])
            vector_x = obj.vector[0]
            vector_y = obj.vector[1]
            # if obj.vector[0] > 0:
            #     x_bound = 600
            # else:
            #     x_bound = 0
            # if obj.vector[1] > 0:
            #     y_bound = 600
            # else:
            #     y_bound = 0
            # print("X_bound:",x_bound)
            # print("y_bound:",y_bound)
            if obj.vector[0] > 0:
                x_bound = 1200
            else:
                x_bound = -600
            if obj.vector[1] > 0:
                y_bound = 1200
            else:
                y_bound = -600
            if obj.vector[0] == 0:
                y = 99999
            else:
                y = (x_bound - outer_x) * (vector_y / vector_x) + outer_y
            if obj.vector[1] == 0:
                x = 99999
            else:
                x = (y_bound - outer_y) * (vector_x / vector_y) + outer_x
            # if int(y) <= 600 and int(y) >= 0:
            #     # print("Y BIGGER")
            #     self.lines[i] = [(x_bound,y), (outer_x,outer_y)]
            # elif int(x) <= 600 and int(x) >= 0:
            #     self.lines[i] = [(x,y_bound), (outer_x,outer_y)]
            if int(y) <= 1200 and int(y) >= -600:
                # print("Y BIGGER")
                self.lines[i] = [(x_bound,y), (outer_x,outer_y)]
            elif int(x) <= 1200 and int(x) >= -600:
                self.lines[i] = [(x,y_bound), (outer_x,outer_y)]


    def calc_abc_from_line_2d(self,x0, y0, x1, y1):
        a = y0-y1
        b = x1-x0
        c = x0*y1-x1*y0
        return a, b, c


    def get_line_cross_point(self, line1, line2):                                                   #看是否有相交，如有則是相交位置回傳
        a0, b0, c0 = self.calc_abc_from_line_2d(line1[0][0],line1[0][1],line1[1][0],line1[1][1])
        a1, b1, c1 = self.calc_abc_from_line_2d(line2[0][0],line2[0][1],line2[1][0],line2[1][1])
        D = a0*b1-a1*b0
        if D==0:
            return None
        x = (b0*c1-b1*c0)/D
        y = (a1*c0-a0*c1)/D
        # if x < 0 or y < 0:
        #     return None
        return [int(x),int(y)]


#=================================================================END=====================================================================