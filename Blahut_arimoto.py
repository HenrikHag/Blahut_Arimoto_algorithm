# Algorithm to approximate the channel capacity given a stationary transition probability distribution.
import numpy as np
# import random as rand

n = 2
m = 2
number_of_iterations = 1000
Trans_prob_distr = np.array([[0.4, 0.6], [0.6, 0.4]])


# Iterates one step for Q given the last p
def iterate_Q(previous_p):
    result = np.array([[0. for i in range(m)],[0. for i in range(n)]])
    for i in range(n):
        for j in range(m):
            result[i,j] = previous_p[i]*Trans_prob_distr[i,j]/sum([previous_p[k]*Trans_prob_distr[k,j] for k in range(n)])
    return result

# Iterates one step for p given the last Q
def iterate_p(previous_Q):
    result = np.array([1. for i in range(n)])
    for i in range(m):
        result
    return result

# Computes the capacity given the last Q and p from the algorithm
def Compute_C(last_Q, last_p):
    return 0

def main(Trans_prob_distr):
    # "Random" initialization
    p = np.array([0.4, 0.6])    # n vector
    # initialization
    Q = np.array([[0. for i in range(m)],[0. for i in range(n)]])   # m x n matrix
    for i in range(number_of_iterations):
        Q = iterate_Q(p)    # Find new Q_ij from previous p_i
        p = iterate_p(Q)    # Find new p_i from previous Q_ij
    C = Compute_C(Q,p)
    print(C)
    return 0

if __name__ == "__main__":
    main(Trans_prob_distr)