import numpy as np
import math
from Example_trans_prob_distr import *

PLOT_CAPACITY_OVER_TIME = True
if PLOT_CAPACITY_OVER_TIME:
    import matplotlib.pyplot as plt
    PLOT_SCALE_LOG = False



######################################################
### Change system and simulation configuration:
######################################################

# Choose the number of iterations the algorithm will run
# Increase to increase accuracy
number_of_iterations = 1000

# Define the transition probability distribution
# Choose from example_A to example_E from Example_arrays.py
trans_prob_distr = example_A



######################################################
### Variables and functions:
######################################################

# Dimensions of problem defined from trans_prob_distr
n = len(trans_prob_distr)       # Rows
m = len(trans_prob_distr[0])    # Columns

# Initialization of the p vector of 1D and n length
rng = np.random.default_rng()
p = rng.random(n)   # n vector
sum_p = sum(p)
for i in range(n):
    p[i] /= sum_p

def iterate_Q(previous_p):
    """
    Iterates one step for `Q` given the last `p`
    previous_p: The `p` from the previous iteration or the initial `p`

    Return new iteration of `Q`, a (m x n) 2D numpy array
    """
    result = np.array([[0. for columns in range(n)] for rows in range(m)])
    for j in range(m):      # For each row
        divisor = sum([previous_p[k]*trans_prob_distr[k,j] for k in range(n)])
        if divisor == 0.:
            print("Divisor is 0 error in iterate_Q")
            exit()
        for i in range(n):  # For each column
            result[j,i] = previous_p[i]*trans_prob_distr[i,j]/divisor
    return result

def iterate_p(previous_Q):
    """
    Iterates one step for `p` given the last `Q`
    previous_Q: The `Q` from the previous iteration
    
    Return new iteration of `p`, a (n) 1D numpy array
    """
    result = np.array([1. for i in range(n)])
    for i in range(n):
        for j in range(m):
            result[i] *= previous_Q[j,i]**trans_prob_distr[i,j]
    normalization = sum(result)
    for i in range(n):
        result[i] /= normalization
    return result

def compute_C(last_Q, last_p):
    """
    Computes the capacity given the last `Q` and `p` from the Blahut-Arimoto algorithm.
    """
    result = 0
    for i in range(n):      # Row
        for j in range(m):  # Column
            if trans_prob_distr[i,j] > 0. and last_p[i] > 0.:
                result += last_p[i]*trans_prob_distr[i,j]*math.log2(last_Q[j,i]/last_p[i])
    return result

def main(p):
    if PLOT_CAPACITY_OVER_TIME:
        capacity_over_time = []
    # Q = np.array([])
    for i in range(number_of_iterations):
        Q = iterate_Q(p)    # Find new Q_ij from previous p_i
        # print(f"p[{i}]: {np.reshape(p,2)}") # TEST
        p = iterate_p(Q)    # Find new p_i from previous Q_ij
        # print(f"Q[{i}]: {np.reshape(Q,4)}") # TEST
        if PLOT_CAPACITY_OVER_TIME:
            capacity_over_time.append(compute_C(Q,p))
    C = compute_C(Q,p)
    if PLOT_CAPACITY_OVER_TIME:
        plt.figure()
        plt.plot([x for x in range(len(capacity_over_time))], capacity_over_time)
        if PLOT_SCALE_LOG:
            plt.yscale('log')
        plt.savefig("fig/capacity_over_time.png")
    print(C)
    return 0

if __name__ == "__main__":
    main(p)
    print(1.+(0.6*math.log2(0.6)+0.4*math.log2(0.4))) # Formula for a symmetric DMC