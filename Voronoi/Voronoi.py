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

