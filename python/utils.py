# ============================================================================
# Utility functions
# Alfonso Cortes - Inria AIO
# 
# ============================================================================

import numpy as np

def read_data(file_name):
    file = open(file_name,'r')
    str_data = file.readlines()
    M = len(str_data)
    N = int(len((str_data[0]).split())/2 + 1) #len(vector_names)
    data = np.zeros((N,M))
    for j in range(0,M):
        str_line = str_data[j]
        str_values = str_line.split()
        data[0][j] = float(str_values[0])
        for i in range(1,N):
            data[i][j] = float(str_values[i*2-1])
    file.close()
    return data

def net(n):
    return " net" + str(n)