import copy
import random
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

#注：此处的Machine和AGV分别表示Machine类列表和AGV类列表
def Gantt(Machines,agvs=None,file=None):
    plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 如果要显示中文字体,则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus'] = False  # 显示负号
    M = ['red', 'blue', 'yellow', 'orange', 'green', 'palegoldenrod', 'purple', 'pink', 'Thistle', 'Magenta',
         'SlateBlue', 'RoyalBlue', 'Cyan', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
         'navajowhite','navy', 'sandybrown', 'moccasin']
    Job_text=['J'+str(i+1) for i in range(100)]
    Machine_text=['M'+str(i+1) for i in range(50)]
    t = 0
    k=0
    if agvs!=None:
        for k in range(len(agvs)):
            for m in range(len(agvs[k].using_time)):
                if agvs[k].using_time[m][1] - agvs[k].using_time[m][0] != 0:
                    if agvs[k]._on[m]!=None:
                        plt.barh(k, width= agvs[k].using_time[m][1]- agvs[k].using_time[m][0],
                                        height=0.6,
                                        left=agvs[k].using_time[m][0],
                                        color=M[agvs[k]._on[m]],
                                        edgecolor='black')
                    else:
                        plt.barh(k, width=agvs[k].using_time[m][1] - agvs[k].using_time[m][0],
                                 height=0.6,
                                 left=agvs[k].using_time[m][0],
                                 color='white',
                                 edgecolor='black')
                    # plt.text(x=agvs[k].using_time[m][0]+(agvs[k].using_time[m][1] - agvs[k].using_time[m][0])/2-2,
                    #          y=k-0.05,
                    #          # s=Machine_text[agvs[k].trace[m]]+'-'+Machine_text[agvs[k].trace[m+1]],
                    #          fontsize=5)
                if  agvs[k].using_time[m][1]>t:
                    t=agvs[k].using_time[m][1]

    for i in range(len(Machines)):
        for j in range(len(Machines[i].using_time)):
            if Machines[i].using_time[j][1] - Machines[i].using_time[j][0] != 0:
                plt.barh(i+k+1, width=Machines[i].using_time[j][1] - Machines[i].using_time[j][0],
                         height=0.8, left=Machines[i].using_time[j][0],
                         color=M[Machines[i]._on[j]],
                         edgecolor='black')
                plt.text(x=Machines[i].using_time[j][0]+(Machines[i].using_time[j][1] - Machines[i].using_time[j][0])/2 - 0.1,
                         y=i+k+1,
                         s=Job_text[Machines[i]._on[j]],
                         fontsize=12)
            if Machines[i].using_time[j][1]>t:
                t=Machines[i].using_time[j][1]
    if agvs!=None:
        list=['AGV1','AGV2','AGV3']
        list1=['M'+str(_+1) for _ in range(len(Machines))]
        list.extend(list1)
        plt.xlim(0,t)
        plt.hlines(k + 0.4,xmin=0,xmax=t, color="black")  # 横线
        # plt.yticks(np.arange(i + k + 3), list,size=13,)
        plt.title('Scheduling Gantt chart')
        plt.ylabel('Machines')
        plt.xlabel('Time(s)')
    if file!=None:
        with open(file,'wb') as fb:
            plt.savefig(fb,dpi=600, bbox_inches='tight')
    plt.show()


class Machine:
    def __init__(self,idx):
        self.idx=idx
        self.using_time=[]
        self._on=[]
        self.end=0

    def update(self,s,pt,_on):
        e=s+pt
        self.using_time.append([s,e])
        self._on.append(_on)
        self.end=e

class Job:
    def __init__(self,idx,PT,MT,L_U):
        self.idx=idx
        self.PT=PT
        self.MT=MT
        self.cur_site=L_U
        self.L_U=L_U
        self.end=0
        self.cur_op=0

    def get_info(self):
        return self.end,self.cur_site,self.PT[self.cur_op],self.MT[self.cur_op]

    def update(self,e):
        self.end=e
        self.cur_op+=1
        self.cur_site=self.MT[self.cur_op-1]

class AGV:
    def __init__(self,idx,L_U):
        self.idx=idx
        self.cur_site=L_U
        self.using_time=[]
        self._on=[]
        self._to=[]
        self.end=0

    def ST(self,s,t1,t2):
        start=max(s,self.end+t1)
        return start-t1,start+t2

    def update(self,s,trans1,trans2,J_site,J_m,_on=None):
        self.using_time.append([s,s+trans1])
        self.using_time.append([s + trans1, s+trans1 + trans2])
        self._on.append(None)
        self._on.append(_on)
        self._to.extend([J_site,J_m])
        self.end=s+trans1+trans2
        self.cur_site=J_m


class RJSP:
    def __init__(self,n,m,agv_num,PT,MT,TT,L_U):
        self.n,self.m,self.agv_num=n,m,agv_num
        self.PT=PT
        self.MT=MT
        self.TT=TT
        self.L_U=L_U
        self.Jobs=[]
        self.C_max=0

    def reset(self):
        self.Jobs = []
        for i in range(self.n):
            Ji = Job(i, self.PT[i], self.MT[i], self.L_U)
            self.Jobs.append(Ji)
        self.Machines = []
        for j in range(self.m+1):
            Mi = Machine(j)
            self.Machines.append(Mi)
        self.AGVs = []
        for k in range(self.agv_num):
            agv = AGV(k, self.L_U)
            self.AGVs.append(agv)

    def VAA_decode(self,Ji):
        Ji=self.Jobs[Ji]
        J_end,J_site,op_t,op_m=Ji.get_info()
        J_m=self.Machines[op_m]
        best_agv=None
        min_tf=99999
        best_s,best_e,t1,t2=None,None,None,None
        for agv in self.AGVs:
            trans1=self.TT[agv.cur_site][J_site]
            trans2=self.TT[J_site][op_m]
            start,end=agv.ST(J_end,trans1,trans2)
            if end<min_tf:
                best_s,best_e,t1,t2 = start,end,trans1,trans2
                best_agv=agv
                min_tf=best_e
        best_agv.update(best_s,t1,t2,J_site,op_m,Ji.idx)
        start=max(best_e,J_m.end)
        J_m.update(start,op_t,Ji.idx)
        Jend=start+op_t
        Ji.update(Jend)
        if Jend>self.C_max:
            self.C_max=Jend

class GA:
    def __init__(self,n,m,agv_num,PT,MT,agv_trans,pop_size=100,gene_size=100,pc=0.9,pm=0.1,N_elite=10):
        self.N_elite=N_elite
        self.rjsp=RJSP(n,m,agv_num,PT,MT,agv_trans,m)
        self.Pop_size=pop_size
        self.gene_size=gene_size
        self.pc=pc
        self.pm=pm
        op_num=[len(Pi) for Pi in self.rjsp.PT]
        self.Chromo_list=[]
        for i in range(len(op_num)):
            self.Chromo_list.extend([i for _ in range(op_num[i])])

    def initial_population(self):
        self.Pop=[]
        for i in range(self.Pop_size):
            random.shuffle(self.Chromo_list)
            self.Pop.append(copy.copy(self.Chromo_list))

    #POX:precedence preserving order-based crossover
    def POX(self,CHS1, CHS2):
        Job_list = [i for i in range(self.rjsp.n)]
        random.shuffle(Job_list)
        r = random.randint(3, self.rjsp.n - 2)
        Set1 = Job_list[0:r]
        new_CHS1 = list(np.zeros(len(self.Chromo_list), dtype=int))
        new_CHS2 = list(np.zeros(len(self.Chromo_list), dtype=int))
        for k, v in enumerate(CHS1):
            if v in Set1:
                new_CHS1[k] = v + 1
        for i in CHS2:
            if i not in Set1:
                Site = new_CHS1.index(0)
                new_CHS1[Site] = i + 1

        for k, v in enumerate(CHS2):
            if v not in Set1:
                new_CHS2[k] = v + 1
        for i in CHS2:
            if i in Set1:
                Site = new_CHS2.index(0)
                new_CHS2[Site] = i + 1

        new_CHS1 = np.array([j - 1 for j in new_CHS1])
        new_CHS2 = np.array([j - 1 for j in new_CHS2])
        return CHS1, CHS2


    #交换变异
    def swap_mutation(self,p1):
        D = len(p1)
        c1 = p1.copy()
        r = np.random.uniform(size=D)
        for idx1, val in enumerate(p1):
            if r[idx1] <= self.pm:
                idx2 = np.random.choice(np.delete(np.arange(D), idx1))
                c1[idx1], c1[idx2] = c1[idx2], c1[idx1]
        return c1

    def Elite(self):
        Fit=dict(enumerate(self.Fit))
        Fit=list(sorted(Fit.items(),key=lambda x:x[1]))
        idx=[]
        for i in range(self.N_elite):
            idx.append(Fit[i][0])
        return idx

    # 选择
    def Select(self):
        idx1=self.Elite()
        Fit = []
        for i in range(len(self.Fit)):
            fit = 1 / self.Fit[i]
            Fit.append(fit)
        Fit = np.array(Fit)
        idx = np.random.choice(np.arange(len(self.Fit)), size=len(self.Fit)-self.N_elite, replace=True,
                               p=(Fit) / (Fit.sum()))
        Pop=[]
        idx=list(idx)
        idx.extend(idx1)
        for i in idx:
            Pop.append(self.Pop[i])
        self.Pop=Pop

    def decode(self,Ci):
        self.rjsp = RJSP(n, m, agv_num, PT, MT, agv_trans, m)
        self.rjsp.reset()
        for i in Ci:
            self.rjsp.VAA_decode(i)
        return self.rjsp.C_max

    def fitness(self):
        self.Fit=[]
        for Pi in self.Pop:
            self.Fit.append(self.decode(Pi))

    def crossover_operator(self):
        random.shuffle(self.Pop)
        Pop1,Pop2=self.Pop[:int(self.Pop_size/2)],self.Pop[int(self.Pop_size/2):]
        for i in range(len(Pop1)):
            if random.random()<self.pc:
                p1,p2=self.POX(Pop1[i],Pop2[i])
                Pop1[i],Pop2[i]=p1,p2
        self.Pop=Pop1+Pop2

    def mutation_operator(self):
        for i in range(len(self.Pop)):
            if random.random()<self.pm:
                p=self.swap_mutation(self.Pop[i])
                self.Pop[i]=p


    def main(self):
        import matplotlib.pyplot as plt

        Fit_best=[]
        self.initial_population()
        self.fitness()
        Best_Fit=min(self.Fit)
        for i in range(self.gene_size):
            self.Select()
            self.crossover_operator()
            self.mutation_operator()
            self.fitness()
            Min_Fit=min(self.Fit)
            # print("迭代次数：",i,'----->>>最小完工时间',Best_Fit,'----->>>平均完工时间',sum(self.Fit)/len(self.Fit))
            # Gantt(self.rjsp.Machines, self.rjsp.AGVs)
            if Min_Fit<Best_Fit:
                Best_Fit=Min_Fit
        # Gantt(self.rjsp.Machines, self.rjsp.AGVs)
            Fit_best.append(Best_Fit)
        x=[_ for _ in range(self.gene_size)]
        plt.plot(x,Fit_best)
        plt.show()
        plt.xlabel("step")
        plt.ylabel("makespan")
        return Best_Fit
        # print(self.Pop)

if __name__=="__main__":
    from Instance.Text_extract import data
    import time

    # Instance set C2 contains problem with t/p>0.25
    #Instance set C1 contains problem with t/p>0.25
    C=["C2",'C1']
    K = ["11", '21', '31', '41', '51', '61', '71', '81', '91', '101', "12", '22', '32', '42', '52', '62', '72', '82',
         '92', '102',
         "13", '23', '33', '43', '53', '63', '73', '83', '93', '103', "14", '24', '34', '44', '54', '64', '74', '84',
         '94', '104']
    for Ci in C:
        for Ki in K:
            print('-------------------------')
            f=r'C:\Users\Administrator\PycharmProjects\MADRL_for_-two_AGVs\Env\Instance\Bilge_Ulusoy'+'/'+Ci+'/'+'E'+Ki+'.pkl'
            n, m, PT, agv_trans, MT, agv_num=data(f)
            for i in range(10):
                t1=time.time()
                ga=GA(n,m,agv_num,PT,MT,agv_trans)
                best=ga.main()
                t2=time.time()

                print('runs:',i+1,'times','Instance：',Ci+'/E'+Ki,'best makespan：',best,'using time:',t2-t1)
            print()



















