#! /usr/bin/python3
# -*- encoding: utf-8 -*-
import numpy as np
import pandas as pd
import math
from random import randint
from generate_train_data import apply_all


def readdata(filepath):
    """
    读取文件,返回轨迹数据,返回类型为pandas的Series,包含3000个numpy类型二维数组,每个为n*3大小:[[x,y,t],[x,y,t],...,[x,y,t]]
    """
    column_name = ['id', 'trace', 'target', 'label']
    df = pd.read_csv(filepath, sep=' ', header=None, names=column_name)
    traces = df.loc[:, 'trace']
    targets = df.loc[:, 'target']
    targets += ',0;'
    traces = traces + targets
    traces = traces.apply(lambda trace: [point.split(',') for point in trace.split(';')[:-1]])
    traces = traces.apply(lambda trace: np.array(trace, dtype='float'))
    # trace_with_target = traces + targets
    # df.insert(4, 'trace_with_target', trace_with_target)
    return traces, np.array(df.loc[:, 'label'], dtype='uint8')
#################################################################################


def readtestdata(filepath):
    """
    读取文件,返回轨迹数据,返回类型为pandas的Series,包含3000个numpy类型二维数组,每个为n*3大小:[[x,y,t],[x,y,t],...,[x,y,t]]
    """
    column_name = ['id', 'trace', 'target']
    df = pd.read_csv(filepath, sep=' ', header=None, names=column_name)
    traces = df.loc[:, 'trace']
    targets = df.loc[:, 'target']
    targets += ',0;'
    traces = traces + targets
    traces = traces.apply(lambda trace: [point.split(',') for point in trace.split(';')[:-1]])
    # print(traces)
    traces = traces.apply(lambda trace: np.array(trace, dtype='float'))
    # print(traces)
    return traces
#################################################################################


# 提取平均速度
def extract_avg_speed(trace: np.ndarray):


    """
    提取平均速度,参数为一个numpy二维数组,大小是n*3:[[x,y,t],[x,y,t],...,[x,y,t]]
    """
    trace = trace[:-1]
    path_length = 0
    tx = trace[0][0]
    ty = trace[0][1]
    for (x, y, t) in trace[1:]:
        path_length += math.sqrt((tx - x) ** 2 + (ty - y) ** 2)
        tx = x
        ty = y
    trace = trace.T
    avg_speed = (path_length / (trace[2].max() - trace[2].min()))
    return avg_speed


# 提取速度变化程度
def extract_speed_change_rate(trace: np.ndarray):
    trace = trace[:-1]
    trace = sorted(trace, key=lambda point: point[2])
    tx = trace[0][0]
    ty = trace[0][1]
    tt = trace[0][2]
    speeds = list()
    # for a in trace[1:]:
    #     print(a)
    for p in trace[1:]:
        x = p[0]
        y = p[1]
        t = p[2]
        if tt > t:
            print("error:error:error:error:error:error:error:error:error:error:er")
            break
        speeds.append(math.sqrt((tx - x) ** 2 + (ty - y) ** 2) / (0.5 if t == tt else t - tt))
        tx = x
        ty = y
        tt = t
    return np.var(np.array(speeds)) * len(trace)
#################################################################################


# 提取最大速度
def extract_max_speed(trace: np.ndarray):
    trace = trace[:-1]

    trace = sorted(trace, key=lambda point: point[2])
    tx = trace[0][0]
    ty = trace[0][1]
    tt = trace[0][2]
    max_speed = 0.000001
    for p in trace[1:]:
        x = p[0]
        y = p[1]
        t = p[2]
        if tt > t:
            print("error:error:error:error:error:error:error:error:error:error:er")
            break
        speed = (math.sqrt((tx - x) ** 2 + (ty - y) ** 2) / (0.5 if t == tt else t - tt))
        max_speed = speed if max_speed < speed else max_speed
        tx = x
        ty = y
        tt = t
    return max_speed
#################################################################################


# 提取最小速度
def extract_min_speed(trace: np.ndarray):
    trace = trace[:-1]
    trace = sorted(trace, key=lambda point: point[2])
    tx = trace[0][0]
    ty = trace[0][1]
    tt = trace[0][2]
    min_speed = 1000000000
    for p in trace[1:]:
        x = p[0]
        y = p[1]
        t = p[2]
        if tt > t:
            print("error:error:error:error:error:error:error:error:error:error:er")
            break
        speed = (math.sqrt((tx - x) ** 2 + (ty - y) ** 2) / (0.5 if t == tt else t - tt))
        if speed != 0.0:
            min_speed = speed if min_speed > speed else min_speed
        tx = x
        ty = y
        tt = t
    return min_speed
#################################################################################


# 提取时间轨迹是否凹陷  人工时间轨迹大部分凹陷，机器大部分凸起
# def extract_sunken(trace: np.ndarray):
#     trace = sorted(trace, key=lambda point: point[2])
#     ty = trace[0][1] = trace[0][0]
#     tt = trace[0][2]
#     min_speed = 1000000000
#     for p in trace[1:]:
#         x = p[0]
#         y = p[1]
#         t = p[2]
#         if tt > t:
#             print("error:error:error:error:error:error:error:error:error:error:er")
#             break
#         speed = (math.sqrt((tx - x) ** 2 + (ty - y) ** 2) / (0.5 if t == tt else t - tt))
#         if speed != 0.0:
#             min_speed = speed if min_speed > speed else min_speed
#         tx = x
#         ty = y
#         tt = t
#     return min_speed
#################################################################################


# 提取时间的震荡频率
# def extract_sunken(trace: np.ndarray):
#     trace = sorted(trace, key=lambda point: point[2])
#     tx = trace[0][0]
#     ty = trace[0][1]
#     tt = trace[0][2]
#     min_speed = 1000000000
#     for p in trace[1:]:
#         x = p[0]
#         y = p[1]
#         t = p[2]
#         if tt > t:
#             print("error:error:error:error:error:error:error:error:error:error:er")
#             break
#         speed = (math.sqrt((tx - x) ** 2 + (ty - y) ** 2) / (0.5 if t == tt else t - tt))
#         if speed != 0.0:
#             min_speed = speed if min_speed > speed else min_speed
#         tx = x
#         ty = y
#         tt = t
#     return min_speed

# 注意，本函数不用于训练，用于分类
def extract_if_traceback(trace: np.ndarray):
    """
    判断是否会重复轨迹，以此区分部分机器，参数为一个numpy二维数组,大小是n*3:[[x,y,t],[x,y,t],...,[x,y,t]]
    注意：机器在x轴上必定为递增的，不会递减
    若有返回 则判断为人  返回1
    否则需要继续判断人或机器，返回0
    """
    trace = trace[:-1]

    trace = trace.T
    cnt = 0
    if len(trace[0]) >= 2:
        for i in range(0, len(trace[0])-1):
            if trace[0][i] > trace[0][i + 1]:
                return 1

    else:
        return 1
    return cnt


# 注意，本函数不用于训练，用于分类
def extract_trace_count(trace: np.ndarray):
    """
    判断是否会重复轨迹，以此区分部分机器，参数为一个numpy二维数组,大小是n*3:[[x,y,t],[x,y,t],...,[x,y,t]]
    注意：机器在x轴上必定为递增的，不会递减
    若有返回 则判断为人  返回1
    否则需要继续判断人或机器，返回0
    """
    trace = trace[:-1]

    trace = trace.T
    cnt=0
    tmp=0
    if len(trace[0]) >= 2:
        for i in range(0, len(trace[0])-1):
            if trace[0][i] > trace[0][i + 1]:
                 tmp=tmp+1
            elif tmp!=0:
                cnt+=1
                tmp=0
    else:
        return 1/len(trace)
    if tmp != 0:
        cnt += 1
    return cnt/len(trace)
#################################################################################


def extract_area(trace: np.ndarray):
    """
    求时间分割的面积，参数为一个numpy二维数组,大小是n*3:[[x,y,t],[x,y,t],...,[x,y,t]]
    更改返回为float型，为0~1的百分比值，代表右下方面积比总面积
    若小于0.5，代表可能为人的可能性高
    否则大于0.5，代表凸型图，机器的可能性高
    但并不是明显特征，只是部分机器的比率更高
    """

    trace = trace[:-1]
    if len(trace) < 3:
        return 1
    trace = trace.T
    p = Point(0, 0)
    points = [p]
    if len(trace[0]) > 0:
        for i in range(0, len(trace[0])):
            p = Point(i+1, trace[2][i])
            points.append(p)
        p = Point(len(trace[2]), 0)
        points.append(p)
        area = GetAreaOfPolyGon(points)
        all_area = trace[2][len(trace[2]) - 1]*(len(trace[2]))
        return round(float(area/all_area), 4)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def GetAreaOfPolyGon(points):
    area = 0

    p1 = points[0]
    for i in range(1, len(points) - 1):
        p2 = points[i]
        p3 = points[i+1]

        # 计算向量
        vecp1p2 = Point(p2.x - p1.x, p2.y - p1.y)
        vecp2p3 = Point(p3.x - p2.x, p3.y - p2.y)

        # 判断顺时针还是逆时针，顺时针面积为正，逆时针面积为负
        vecMult = vecp1p2.x * vecp2p3.y - vecp1p2.y * vecp2p3.x  # 判断正负方向比较有意思
        sign = 0
        if vecMult > 0:
            sign = 1
        elif vecMult < 0:
            sign = -1

        triArea = GetAreaOfTriangle(p1, p2, p3) * sign
        area += triArea
    return round(abs(area), 5)


def GetAreaOfTriangle(p1, p2, p3):
    """
    计算三角形面积   海伦公式
    """
    p1p2 = GetLineLength(p1, p2)
    p2p3 = GetLineLength(p2, p3)
    p3p1 = GetLineLength(p3, p1)
    s = (p1p2 + p2p3 + p3p1) / 2
    area = s * (s - p1p2) * (s - p2p3) * (s - p3p1)  # 海伦公式
    if int(area) != 0:
        area = math.sqrt(area)
    return area


def GetLineLength(p1, p2):
    """
    计算边长
    """
    length = math.pow((p1.x - p2.x), 2) + math.pow((p1.y - p2.y), 2)  # pow  次方
    length = math.sqrt(length)
    return length
#################################################################################


# 增加提取新特征的方法
# 该函数只是针对一条轨迹数据进行特征提取
# def extract_feature(trace: np.ndarray):
#     # 处理过程
#     return feature
#
#
# 在main()添加以下形式的语句调用extract_feature方法处理所有轨迹数据获取3000个特征
# features = traces.apply(extract_feature)

def get_feature_list():
    """
    返回特征函数列表,每次有新的特征添加或减少都需要修改本函数的返回
    这样不需要在generate_train_data文件中每次引入
    另外新增加了一个features_[data].py文件，data当天日期，比如：6月23日 --> features_623.py
    新增加的文件对应的每次新的特征组合，现，每次有有更高分数出默认把低分数的文件移动到history文件夹中
    :return:
    """
    return [extract_avg_speed, extract_speed_change_rate, extract_max_speed, extract_min_speed,
            extract_if_traceback, extract_area]
    # return [extract_if_traceback]


def main():
    tt = int(input('1. train data; 2. test data: '))

    if tt == 1:
        traces, labels = readdata('data_train.txt')
        functions = get_feature_list()
        X = apply_all(functions, traces)
        X = np.nan_to_num(X)
        np.savetxt("train_feature630.txt", X, '%f')
    elif tt == 2:
        traces = readtestdata('data_test.txt')
        functions = get_feature_list()
        X = apply_all(functions, traces)
        X = np.nan_to_num(X)
        np.savetxt("test_feature630.txt", X, '%f')


if __name__ == '__main__':
    main()
