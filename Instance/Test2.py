import random
import numpy as np

random.seed(64)

def Generate(n,m,machine_speed,AGV_speed_pair):
    AGV_speed= [[5, 15], [15, 25], [25, 35]]
    Mch_speed=[[15,25],[25,45]]
    AGV1_speed,AGV2_speed=AGV_speed[AGV_speed_pair[0]],AGV_speed[AGV_speed_pair[1]]
    Ms=Mch_speed[machine_speed]
    PT=[]
    for i in range(n):
        PT_i=[random.randint(Ms[0],Ms[1]) for i in range(m)]
        PT.append(PT_i)
    agv_trans=[]
    agv1_trans = [random.randint(AGV1_speed[0],AGV1_speed[1]) for i in range(1,m)]
    agv2_trans=[random.randint(AGV2_speed[0],AGV2_speed[1]) for i in range(1,m)]
    agv_trans.extend([agv1_trans,agv2_trans])
    return PT ,agv_trans
n,m=5,5
agv_speed_pair=[0,0]
machine_speed=0
PT ,agv_trans=Generate(n,m,machine_speed,agv_speed_pair)
for i in range(2):
    agv_trans[i].append(0)