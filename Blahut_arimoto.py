import numpy as np
import math

######################################################
### Change system and simulation configuration:
######################################################

# Define the transition probability distribution
# trans_prob_distr = np.array([[0.6, 0.4], [0.4, 0.6]])   # 2 dimensional array
# trans_prob_distr = np.array([[1., 0.], [0.3, 0.7]])   # 2 dimensional array
trans_prob_distr = np.array(
    [
        [0.192924, 0.089701, 0.021833, 0.152806, 0.011611, 0.086720, 0.165786, 0.015761, 0.109188, 0.015682, 0.025470, 0.073875, 0.035944, 0.002699],
        [0.014871, 0.216260, 0.005303, 0.119562, 0.118172, 0.133585, 0.157966, 0.055477, 0.053210, 0.011355, 0.062284, 0.031863, 0.013020, 0.007072],
        [0.112542, 0.160423, 0.236331, 0.165273, 0.004366, 0.013188, 0.002696, 0.033401, 0.005471, 0.068635, 0.047322, 0.036100, 0.049478, 0.064774],
        [0.015249, 0.090436, 0.031359, 0.210700, 0.074665, 0.018877, 0.040756, 0.017114, 0.109960, 0.024227, 0.171975, 0.112956, 0.050542, 0.031184],
        [0.027588, 0.047386, 0.108748, 0.053770, 0.197346, 0.011192, 0.087548, 0.013377, 0.081362, 0.006143, 0.116144, 0.139228, 0.083607, 0.026561],
        [0.028725, 0.021479, 0.187318, 0.012265, 0.045138, 0.275349, 0.000883, 0.005216, 0.004482, 0.086729, 0.058492, 0.107850, 0.044141, 0.121933],
        [0.031631, 0.049566, 0.058419, 0.181859, 0.114117, 0.020115, 0.203303, 0.102987, 0.100286, 0.043775, 0.009645, 0.062433, 0.013086, 0.008778],
    ]
)

# Increase to increase accuracy
number_of_iterations = 1000



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

# Iterates one step for Q given the last p
def iterate_Q(previous_p):
    result = np.array([[0. for columns in range(n)] for rows in range(m)])
    for j in range(m):      # For each column
        divisor = sum([previous_p[k]*trans_prob_distr[k,j] for k in range(n)])
        if divisor == 0.:
            print("Divisor is 0 error in iterate_Q")
            exit()
        for i in range(n):  # For each row
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