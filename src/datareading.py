import os
import pandas as pd
import numpy as np


def Stochastic_read(path,Model_len,Realizations_numbers):

    a=os.listdir(path)
    x=pd.read_table(path+a[100],header=None,encoding='gb2312',sep='\s+')
                    
    for i in range(len(x.iloc[0,:])-1):
        locals()["C"+str(i)]=np.empty([Model_len,Realizations_numbers])

    for i in range(Realizations_numbers):
        x = pd.read_table(path+a[i],header=None,encoding='gb2312',sep='\s+')
        for j in range(len(x.iloc[0,:])-1):

            locals()["C"+str(j)][:,i]=x.iloc[:,j+1]

        print('Progress= %.2f' % (i/Realizations_numbers*100)+'%', end='\r')
    print('Progress= %.2f' % 100+'%', end='\r')

    data=[]
            
    for i in range(len(x.iloc[0,:])-1):
        data.append(locals()["C"+str(i)])
                
    return list(data)
    
def Deterministic_read(path):

    data = pd.read_table(path,header=None,encoding='gb2312',sep='\s+')

    return data