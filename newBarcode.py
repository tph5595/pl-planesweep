import numpy as np 
from numba import njit, prange
import time
import sys

import pl_sweep.pl_planesweep as pl_planesweep

birth = 1.0
death = 0.0

# @njit(parallel=True)
# @njit()
def setup(bd_pairs, eventList):
    for i in prange(0, bd_pairs.shape[0]):
        eventList[i*2][0] = bd_pairs[i][0]
        eventList[i*2][1] = bd_pairs[i][1]
        eventList[i*2][2] = birth
        eventList[i*2][3] = i
        eventList[i*2+1][0] = bd_pairs[i][1]
        eventList[i*2+1][1] = bd_pairs[i][0]
        eventList[i*2+1][2] = death
        eventList[i*2+1][3] = i
    return eventList

# @njit()
def handle_birth(event, stackSize, k, filteredSet, top_k, stack, filteredSize):
    if stackSize < k:
        stackSize = stackSize + 1
        # print('{}'.format(filteredSet))
        filteredSet[filteredSize][0] = event[0]
        filteredSet[filteredSize][1] = event[1]
        filteredSize = filteredSize +1
        top_k[int(event[3])] = 1
    else:
        stack = np.append(stack, int(event[3]))
    return stack, filteredSize, stackSize, top_k

# @njit()
def handle_death(event, stackSize, k, filteredSet, top_k, bd_pairs, stack,\
        filteredSize):
    # print("top_k: {}".format(top_k))
    if top_k[int(event[3])] == 1:
        # print("pair was in top_k")
        if stack.shape[0] == 0:
            stackSize = stackSize - 1
        else:
            # print("adding")
            new_e_i = int(stack[0])
            stack = np.delete(stack, 0)
            # print("pair in death{}".format(bd_pairs[new_e_i][0]))
            filteredSet[filteredSize][0] = bd_pairs[new_e_i][1]
            filteredSet[filteredSize][1] = bd_pairs[new_e_i][0]
            # filteredSet.append(bd_pairs[new_e_i])
            filteredSize = filteredSize + 1
            top_k[new_e_i] = 1
    else:
        # Remove from stack
        # print("{}".format(stack))
        # print("{}".format(event))
        # print("{}".format(top_k))
        # print("val: {}".format(event[3]))
        # print("remove, ", len(stack), "\t", np.searchsorted(stack, event[3]))
        stack = np.delete(stack, np.where(stack == event[3]))

    return stack, filteredSize, stackSize, top_k

# @njit()
def no_jit_sort(eventList):
    return eventList[np.argsort(eventList[:, 0])]

# force compilation in nopython mode
# @njit()
def filter(bd_pairs, k):
    # Assume pairs come in sorted by birth
    # sort and setup
    eventList = np.zeros((bd_pairs.shape[0] * 2, 4), dtype='float64')
    eventList = setup(bd_pairs, eventList)
    # print("eventList: {}".format(eventList))
    eventList = no_jit_sort(eventList)
    # print("eventList: {}".format(eventList))

    stackSize = 0
    filteredSet = np.zeros((bd_pairs.shape[0], 2), dtype='float64')
    # print('{}'.format(filteredSet))

    filteredSize = int(0)
    stack = np.array([], dtype='int64')
    top_k = np.zeros((bd_pairs.shape[0] * 2), dtype='float64')
    for i in range(0, eventList.shape[0]):
        # print("type: {}".format(eventList[i][2]))
        if eventList[i][2] == birth:
            # print("birth")
            stack, filteredSize, stackSize, top_k = handle_birth(eventList[i], stackSize, k, filteredSet, top_k, stack,
                    filteredSize)
        else:
            # print("death")
            stack, filteredSize, stackSize, top_k = handle_death(eventList[i], stackSize, k, filteredSet, top_k,\
                    bd_pairs, stack, filteredSize)

    # print('filteredSize: {}'.format(filteredSize))
    return filteredSet[:filteredSize]

def main():
    
    for i in range(100000):
        bd_pairs = np.array([[0, 6], [1, 3], [2, 7]], dtype='float64')
        k = 1
        ret = filter(bd_pairs, k)
        # print('{}'.format(ret))
        
def getPairs(fn):
    lines = None
    result = []
    with open(fn) as f:
       lines = f.readlines()
    for l in lines:
        lis = l.split(" ")
        if len(lis) != 2:
            print("bad line: {}".format(l))
            exit(1)
        result.append(tuple(lis))
    return result

if len(sys.argv) != 3:
    print("Incorrect number of arguments.")
    print(len(sys.argv))
    exit(1)

fn = sys.argv[1]
iterations = int(sys.argv[2])
bd_pairs = np.array(getPairs(fn))
k = 2

print("Starting test...")

start = time.time()
for _ in range(iterations):
    bd_pairs_filtered =  filter(bd_pairs, k)
    # bd_pairs_filtered = bd_pairs
    pl_obj = pl_planesweep.PersistenceLandscape(bd_pairs_filtered, k)
    pl_obj.generate_landscapes()
end = time.time()
print(end -start)
# if __name__ == "__main__":
#     main()
