# Algorithm to approximate the channel capacity given a stationary transition probability distribution.
import numpy as np
import math
# import random as rand

# Define the transition probability distribution
trans_prob_distr = np.array([[0.6, 0.4], [0.4, 0.6]])   # 2 dimensional array
n = len(trans_prob_distr[0])    # Rows
m = len(trans_prob_distr[1])    # Columns

# Testing for the example, TO BE REMOVED LATER
if (n!=2 or m!=2):
    print("Error, n is",n,"and m is",m)

number_of_iterations = 1000
# Initialization of the p vector of 1D and n length
rng = np.random.default_rng()
p = rng.random(n)   # n vector
sum_p = sum(p)
for i in range(n):
    p[i] /= sum_p
# print(p)




# Iterates one step for Q given the last p
def iterate_Q(previous_p):
    result = np.array([[0. for columns in range(n)] for rows in range(m)])
    for j in range(n):      # For each column
        divisor = sum([previous_p[k]*trans_prob_distr[k,j] for k in range(n)])
        for i in range(m):  # For each row
            result[i,j] = previous_p[i]*trans_prob_distr[i,j]/divisor
    return result

# Iterates one step for p given the last Q
def iterate_p(previous_Q):
    result = np.array([1. for i in range(n)])
    for i in range(n):
        for j in range(m):
            result[i] *= previous_Q[j,i]**trans_prob_distr[i,j]
    normalization = sum(result)
    for i in range(n):
        result[i] /= normalization
    return result

# Computes the capacity given the last Q and p from the algorithm
def compute_C(last_Q, last_p):
    result = 0
    for i in range(n):      # Row
        for j in range(m):  # Column
            result += last_p[i]*trans_prob_distr[i,j]*math.log2(last_Q[j,i]/last_p[i])
    return result

def main(p):
    for i in range(number_of_iterations):
        Q = iterate_Q(p)    # Find new Q_ij from previous p_i
        p = iterate_p(Q)    # Find new p_i from previous Q_ij
    C = compute_C(Q,p)
    print(C)
    return 0

if __name__ == "__main__":
    main(p)