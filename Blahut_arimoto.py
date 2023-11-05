import numpy as np
import math

######################################################
### Change system and simulation configuration:
######################################################

# Define the transition probability distribution
# trans_prob_distr = np.array([[0.6, 0.4], [0.4, 0.6]])   # 2 dimensional array
trans_prob_distr = np.array([[1., 0.], [0.3, 0.7]])   # 2 dimensional array

# Increase to increase accuracy
number_of_iterations = 1000



######################################################
### Variables and functions:
######################################################

# Dimensions of problem defined from trans_prob_distr
n = len(trans_prob_distr[0])    # Rows
m = len(trans_prob_distr[1])    # Columns

# Initialization of the p vector of 1D and n length
rng = np.random.default_rng()
p = rng.random(n)   # n vector
sum_p = sum(p)
for i in range(n):
    p[i] /= sum_p

# Iterates one step for Q given the last p
def iterate_Q(previous_p):
    result = np.array([[0. for columns in range(n)] for rows in range(m)])
    for j in range(n):      # For each column
        divisor = sum([previous_p[k]*trans_prob_distr[k,j] for k in range(n)])
        if divisor == 0.:
            print("Divisor is 0 error in iterate_Q")
            exit()
        for i in range(m):  # For each row
            result[j,i] = previous_p[i]*trans_prob_distr[i,j]/divisor
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
            if trans_prob_distr[i,j] > 0:
                result += last_p[i]*trans_prob_distr[i,j]*math.log2(last_Q[j,i]/last_p[i])
    return result

def main(p):
    for i in range(number_of_iterations):
        Q = iterate_Q(p)    # Find new Q_ij from previous p_i
        # print(f"p[{i}]: {np.reshape(p,2)}") # TEST
        p = iterate_p(Q)    # Find new p_i from previous Q_ij
        # print(f"Q[{i}]: {np.reshape(Q,4)}") # TEST
    C = compute_C(Q,p)
    print(C)
    return 0

if __name__ == "__main__":
    main(p)
    # print(1.+(0.6*math.log2(0.6)+0.4*math.log2(0.4))) # Formula for a symmetric DMC