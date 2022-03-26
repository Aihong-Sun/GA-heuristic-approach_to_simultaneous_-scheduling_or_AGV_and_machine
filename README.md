# GA-heuristic-approach_to_simultaneous_-scheduling_or_AGV_and_machine
## 1 Introduction(JSP+AGV)
 This problem is composed of two interrelated decision problems: the scheduling of machines, and the scheduling of
AGVs. Both problems are known to be NP-complete, resulting in a more complicated NP-complete problem when they are considered simultaneously. A
new hybrid Genetic-algorithm/heuristic coding scheme is developed for the studied problem. The developed coding scheme is combined with a set of genetic
algorithm (GA) operators selected from the literature of the applications of GAs to the scheduling problems. The algorithm is applied to a set of 82 test problems,
which was constructed by other researchers, and the comparison of the results indicates the superior performance of the developed coding.

## 2 Algorithm
### 2.1 Encode
The code length is the sum of the number of operations
### 2.2 Decode
Normal decoding +vehicle assignment algorithm(Its basic role is to find the AGV that is capable
of accomplishing the trip in the shortest time and to modify the value of (st) such
that the transportation time is considered.)

In addition, I made further improvements in decoding, in the original text, start time of operation 
### 2.3 crossover operator
  Unlike the original text, for simple reproduction, POX is used, which is why the reproduction effect is a little worse than the original text：
  - MAX(pre.completion_time,agv. last_trip_finish_time)+dht

  This program：
  - MAX(pre.completion_time,agv. last_trip_finish_time+transportation time between )+dht
### 2.4 Mutation operator
  also,we only use swap mutation
### 2.5 Elite Policy
  Elite Policy is used.
### 2.6 Parameter settings
  - pop_size=100
  - generations=100
  - crossover probability = 0.9
  - mutation probability = 0.1
  - elite number=10
  - run times = 5


## 3 Experience

### 3.1 Reappearance Effect

| Instance | literature | reappearance_result | gap	| Instance | literature | reappearance_result | gap	|
|    :----:  |   :----: |  :----: |   :----:  |   :----: |  :----: |   :----: |   :----: |
|  EX11	| 96  |	96  |	0 |	EX13  | 84 |	84  |	 0  |
|  EX21 |	102	| 100 |	+2	| EX23  | 86	| 86	|  0  |
|  EX31	| 99	| 106	| -7	| EX33	| 86	| 86  |	 0  |
|  EX41	| 112	| 117	| -5	| EX43	| 89	| 90	|  -1  |
|  EX51	| 87	| 87	| 0	| EX53	| 74  |	74  |	 0  |
|  EX61	| 118	| 121 |	-3	| EX63	| 104 |	103	|  +1  |
|  EX71	| 115	| 115 |	0	| EX73 |	86	| 85  |	 +1  |
|  EX81	| 161	| 161 |	0 |	EX83 |	153 |	153	|  0  | 
|  EX91	| 118	| 116 |	+2 | EX93	| 106	| 105	|  +1 |
|  EX101|	147	| 147 |	0	| EX103	| 141 |	140 |	  +1  |
|  EX12	| 82	| 82  |	0	| EX14 |	103 |	103 |	  0  |
|  EX22 |	76	| 76  |	0	| EX24 |	108 |	108 | 	0  |
|  EX32	| 85	| 85  |	0 |	EX34 |	111	| 112 |	  -1  |
|  EX42	| 88	| 87  |	+1  |	EX44 |	126	| 126 | 	0  |
|  EX52	| 69	| 69  |	0 |	EX54 |	96	| 97	|   -1 |
|  EX62	| 98	| 100  |	-2 |	EX64 |	120 |	121 |	 -1 |
|  EX72	| 79	| 80  |	-1 |	EX74 |	127 |	129 |	 -2  |
|  EX82	| 151 |	151 |	0 |	EX84 |	163	| 163	|  0  |
|  EX92	| 104 |	102 |	+2	| EX94 |	122 |	120	|  +2  |
|  EX102	|136 |	135 |	+1 |	EX104 |	159 |	159 | 	0 |

### 3.2 Convergence display
![image](https://user-images.githubusercontent.com/77766201/160228704-6f91c00a-e2db-4254-9b52-1886482d41e1.png)


### 3.2 Gantt graph display of partial instrances

#### 3.2.1 EX21
![image](https://user-images.githubusercontent.com/77766201/160227056-25811b13-4589-4365-8324-bdbaa266a30f.png)


