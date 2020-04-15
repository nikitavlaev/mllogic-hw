#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pycosat
import numpy as np
import sys

path = 'inputs/input' + sys.argv[1] + '.txt'
data = np.loadtxt(path, dtype='int')
print(data)
if data.shape[0] != data.shape[1]:
    print("Not square-shaped table")
    exit(1)
if data.shape[0] != 9:
    print("Table should be 9x9")
    exit(2)


# In[2]:


def encode_cell(row,col,num):
    return 100 * num + 10 * row + col 


# In[5]:


def show_res(res):
    ans = np.zeros((9,9), dtype = 'int')
    for i in range(1, 10):
        for j in range(1, 10):
            for num in range(1, 10):
                if encode_cell(i,j,num) in res:
                    ans[i-1,j-1] = num
    return ans                


# In[13]:


cnf = []
ids = range(1, 10)
#add "each cell contains at least one number and at most one number"
for i in ids:
    for j in ids:
        cnf.append([encode_cell(i,j,num) for num in range(1,10)]) #at least one
        res = []
        for ii in range(1,10):
            for jj in range(ii + 1,10):
                cnf.append([-encode_cell(i,j,ii), -encode_cell(i,j,jj)]) #not two different at the same time
                
#do not touch cells given
for i in ids:
    for j in ids:
        if data[i-1,j-1] != 0:
            cnf.append([encode_cell(i,j,data[i-1,j-1].item())]) 
#add "each row and col and 3x3 contains every number"
for i in ids:
    i33 = (i - 1) // 3 
    j33 = (i - 1) % 3
    for j1 in ids:
        for j2 in range(j1 + 1,10):
            for num in range(1,10):
                cnf.append([-encode_cell(i,j1,num), -encode_cell(i,j2,num)])
                cnf.append([-encode_cell(j1,i,num), -encode_cell(j2,i,num)])
                cnf.append([-encode_cell(i33 * 3 + (j1 - 1) // 3 + 1, j33 * 3 + (j1 - 1) % 3 + 1,num),
                            -encode_cell(i33 * 3 + (j2 - 1) // 3 + 1, j33 * 3 + (j2 - 1) % 3 + 1,num)])
                
    
res = pycosat.solve(cnf)
if res == "UNSAT" or res == "UNKNOWN":
    print(res)
else:    
    print(show_res(res))

