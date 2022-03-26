import pickle
import numpy as np


def data(f):
    with open(f, "rb") as fb:
        d = pickle.load(fb)
    n,m,agv_num=len(d[3]),d[1],d[2]
    PT ,agv_trans,MT=d[3],d[5],d[4]
    MT1=[]
    for mi in MT:
        mt1=[]
        for k in mi:
            mt1.append(k-1)
        MT1.append(mt1)
    MT=MT1

    # MT1=[]
    # for mi in MT:
    #     mt1=[m]
    #     for k in mi:
    #         mt1.append(k-1)
    #     if mt1[-1]!=m:
    #         mt1.append(m)
    #     MT1.append(mt1)
    # MT=MT1
    # for pi in PT:
    #     pi.insert(0,0)
    #     if pi[-1]!=0:
    #         pi.append(0)
    # print()
    # print(PT)
    # print(MT)
    # print(agv_trans)
    return n,m,PT,agv_trans,MT,agv_num


f2=r'C:\Users\Administrator\PycharmProjects\MADRL_for_-two_AGVs\Env\Instance\Bilge_Ulusoy\storer\swv1.pkl'

def data_for_storer(f):

    with open(f, "rb") as fa:
        d= pickle.load(fa)
        # print(d)
    n, m, M= d[0],d[1], d[2]
    if m==10:
        with open(r'C:\Users\Administrator\PycharmProjects\MADRL_for_-two_AGVs\Env\Instance\Bilge_Ulusoy\storer\Layout_10m.pkl', "rb") as fb:
            agv_trans = pickle.load(fb)
    if m==15:
        with open(
                r'C:\Users\Administrator\PycharmProjects\MADRL_for_-two_AGVs\Env\Instance\Bilge_Ulusoy\storer\Layout_15m.pkl',
                "rb") as fb:
            agv_trans = pickle.load(fb)
    PT=[]
    MT=[]
    for i in range(len(M)):
        L=[m]
        L1=[0]
        for j in range(0,len(M[i]),2):
            L.append(M[i][j])
            L1.append(M[i][j+1])
        L.append(m)
        L1.append(0)
        MT.append(L)
        PT.append(L1)
    return n,m,PT,agv_trans,MT

n,m,PT,agv_trans,MT=data_for_storer(f2)
