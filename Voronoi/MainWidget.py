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
        

