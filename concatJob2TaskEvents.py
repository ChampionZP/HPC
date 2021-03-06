'''
----------------------------------------------------------------------------------------
This file concates job_events datasets and task_events datasets by keyword 
JobId，then writes them out to disk.

job_events: JE
task_events: TE

1. Extract data of NameID and LogNameID in job_events datasets to task_events datasets
2. Resort task_events data by dictionary order: {JobId, TaskIdInThisJob, TimeStamp}

Author: Ping Zhang
-----------------------------------------------------------------------------------------
'''

print(__doc__)

import pandas as pd
import numpy as np
import time
from multiprocessing import Pool 
import os 

# For MapUserStr2ID function
'''
userNameStr = pd.read_csv('userNameStr',header=None)
userID = np.arange(1,len(userNameStr)+1)

replaceValue_user = {} 

for user, ID1 in zip(userNameStr[0].tolist(), userID):
    replaceValue_user[user] = ID1

TE_fieldNames = ['TimeStamp', 'MissInfo', 'JobId', 'TaskIdInThisJob',
                 'MachineId', 'EventType', 'UserId', 
                 'SchedulClass', 'Priority', 'ReqCPUCores', 
                 'ReqRAM', 'ReqDisk', 'DiffMachineCons']

'''

def sortByDict(DATASET):
     


def extractNameID(JE,TE):
    #check join function


























def MapUserStr2ID(TE, FILE):
    try:
        TE = TE.replace({6:replaceValue_user})
    except:
        print('failed to map user name to userID!')

    TE.to_csv('../task_events/%s'%(FILE),\
        header=TE_fieldNames, index=None)

# For DropMissLines function
TE_fieldNames = ['TimeStamp', 'JobId', 'TaskIdInThisJob',
                 'MachineId', 'EventType', 'UserId', 
                 'SchedulClass', 'Priority', 'ReqCPUCores', 
                 'ReqRAM', 'ReqDisk', 'DiffMachineCons']

def DropMissLines(TE, FILE):

    # 1. extract recodes with 'MissInfo' field empty
    TE.loc[:,(1)].fillna(1000,inplace=True)
    TE = TE[TE[1] == 1000]
    try:
        TE = TE.drop([1],axis=1)
    except:
        print("failed to delete 'MissInfo' field!")
    
    # 2. eliminate recodes(line) with 'NaN' in any field
    try:
        TE.dropna(axis=0, how='any', inplace=True)
    except:
        print('failed to eliminate lines with NaN!')

    TE.to_csv('../task_events/%s'%(FILE),\
        header=TE_fieldNames, index=None)
   
def handle(filePath, FILE):
    print('preprocessing ... %s' %(FILE))
    TE = pd.read_csv(filePath,header=None,low_memory=False)
    DropMissLines(TE, FILE)


if __name__ == '__main__':
    
    t1 = time.time() 

    p = Pool()
    for root, _, fileList in os.walk('../task_events/'):
        for FILE in fileList:
            filePath = os.path.join(root, FILE) 
            p.apply_async(handle, args=(filePath, FILE, ))
    p.close()
    p.join()

    t2 = time.time()

    print('time cost is %f'%(t2-t1))
    


# For multithreading processing, replaced with multiprocess processing,
# which is faster

'''
class MyThread(Thread):
    def __init__(self, filePath, FILE):
        Thread.__init__(self)
        self.filePath = filePath
        self.FILE = FILE 

    def run(self):
        handle(self.filePath, self.FILE)

'''

'''
if __name__ == '__main__':

    threads = []
    
    t1 = time.time()

    for root, _, fileList in os.walk('../task_events_test/'):
        for FILE in fileList:
            filePath = os.path.join(root, FILE) 
            thread = MyThread(filePath, FILE)
            threads.append(thread)
            thread.start()
        for t in threads:
            t.join()
    
    t2 = time.time()

    print('time cost is %f'%(t2-t1))

'''

