#!/usr/bin/env python
# coding: utf-8

# In[26]:


#values: 0,1,2,3...
import numpy as np

data = np.loadtxt('input.txt', dtype = np.int32)
print(data)
dim = data.shape[0]


# In[27]:


#check for commutativity

def check_for_com(data):
    return np.allclose(data, data.T, rtol=1e-05, atol=1e-08)


# In[28]:


#check for neutral

def check_array(arr):
    for i, x in np.ndenumerate(arr):
        if i != x:
            return False
    return True

def get_neutral(data):
    neutr_mask_rows = np.apply_along_axis(check_array, axis=1, arr=data)
    neutral_rows = next((i for i, x in enumerate(neutr_mask_rows) if x), None)
    neutral = neutral_rows if check_array(data[:, neutral_rows]) else None
    return neutral
    


# In[29]:


#check for reversibility

def check_for_rev(neutral, data):
    dim = data.shape[0]
    covrd_xs = list(range(dim))
    covrd_ys = list(range(dim))
    for (i,j), x in np.ndenumerate(data):
        if x == neutral:
            try:
                covrd_xs.remove(i)
                covrd_ys.remove(j)
            except ValueError:
                continue
    return len(covrd_xs) + len(covrd_ys) == 0


# In[30]:


#check for associativity

def check_for_assoc(data):
    is_assoc = True
    for (i,j), x in np.ndenumerate(data):
        for k in range(dim):
            is_assoc = is_assoc and data[x,k] == data[i,data[j,k]]
    return is_assoc
    


# In[31]:


is_assoc = check_for_assoc(data)

if is_assoc:
    is_com = check_for_com(data)
    neutral = get_neutral(data)
    if neutral is not None:
        is_rev = check_for_rev(neutral, data)
        if is_rev:
            if is_com:
                print("Abel group")
            else:
                print("group")
        else:
            if is_com:
                print("commutative monoid")
            else:
                print("monoid")
    else:
        print("semigroup")
else:
    print("magma")

