'''
start date: 2021/9/14
from thesis:
    Arviv,,Kfir等.Collaborative reinforcement learning for a two-robot job transfer flow-shop scheduling problem[J].
    INTERNATIONAL JOURNAL OF PRODUCTION RESEARCH,2016,54(4):1196-1209.
'''

import random
import numpy as np
import copy

random.seed(64)

def trans_Matrix(trans,m):
    T=np.zeros((m,m))
    for i in range(len(T)):
        for j in range(len(T[i])):
            if i==j:
                T[i][j]=0
            elif i!=j and T[i][j]==0:
                T[i][j]=sum(trans[i:j])
                T[j][i]=T[i][j]
    return T

def Generate(n,m):
    AGV_speed= [[5,10], [3,5], [5,7]]
    Mch_speed=[[10,20],[25,45]]
    AGV1_speed=AGV_speed[0]
    Ms=Mch_speed[0]
    PT=[]
    MT=[]
    for i in range(n):
        PT_i=[random.randint(Ms[0],Ms[1]) for i in range(m)]
        MT_i=[_ for _ in range(m)]
        random.shuffle(MT_i)
        PT.append(PT_i)
        MT.append(copy.copy(MT_i))
    agv1_trans = [random.randint(AGV1_speed[0],AGV1_speed[1]) for i in range(1,m+1)]
    agv1_trans=trans_Matrix(agv1_trans,m+1)
    return PT ,agv1_trans,MT

n,m=5,5
PT,agv_trans,MT=Generate(n,m)
agv_num=2

for Mi in MT:
    Mi.insert(0,m)
    Mi.append(m)
for Pi in PT:
    Pi.insert(0,0)
    Pi.append(0)




