import os
from logging import getLogger, INFO
import pandas as pd
import numpy as np
import pickle
import re

import re

#修改所有文件的后缀：

# log = getLogger()
file=r"C:/Users/Administrator/PycharmProjects/MADRL_for_-two_AGVs/Env/Instance/JSP_Transbot/Storer"
files=os.listdir(file)
Matrix = []
for f in files:
    if '.txt' in f:
        if 'Layout' in f:
            Matrix = []
            file_path = os.path.join(file, f)
            print(file_path)
            new_f=f.split('.')[0]
            with open(file_path, 'r') as data:
                List = data.readlines()
                for line in List:
                    pat = r'\d+'
                    result = re.findall(pat, line)
                    li=[int(ri) for ri in result]
                    Matrix.append(li)
            print(np.array(Matrix))
            with open(os.path.join(
                    r'C:\Users\Administrator\PycharmProjects\MADRL_for_-two_AGVs\Env\Instance\Bilge_Ulusoy\storer',
                    new_f + ".pkl"), "wb") as f1:
                pickle.dump(Matrix, f1, pickle.HIGHEST_PROTOCOL)

        elif 'yn' in f:
            J_num=0
            M_num=0
            file_path = os.path.join(file, f)
            print(file_path)
            new_f = f.split('.')[0]
            Matrix=[]
            with open(file_path, 'r') as data:
                List = data.readlines()
                for line in List:
                    pat = r'\d+'
                    result = re.findall(pat, line)
                    if len(result)==2:
                        J_num=int(result[0])
                        M_num=int(result[1])
                    else:
                        li = [int(ri) for ri in result]
                        Matrix.append(li)
            print(J_num,M_num,Matrix)
            print(np.array(Matrix))

            d=(  J_num ,M_num,Matrix )
            with open(os.path.join(r'C:\Users\Administrator\PycharmProjects\MADRL_for_-two_AGVs\Actor_Critic_for_JSP\Dataset\yn',  new_f + ".pkl"), "wb") as f1:
                pickle.dump(d, f1, pickle.HIGHEST_PROTOCOL)









