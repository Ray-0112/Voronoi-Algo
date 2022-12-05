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
