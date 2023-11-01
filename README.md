# Blahut Arimoto algorithm

An implementation in Python3 of the standard convex optimization technique by Arimoto and Blahut.  
The script is intended to approximate the channel capacity `C` for a discrete memoryless channel (DMC) given a stationary transition probability distribution `trans_prob_distr` as a two dimensional array, `n x m` matrix.  

---
# Description of algorithm
Given a fixed transition probability distribution $\omega_{ij}$ for the DMC, first initialize a vector $p^{0}=(p_1,p_2,...)$, where $p_i \ge 0$ and $\sum_np_i=1$, and where $0\le i\le n$ and $0\le j\le m$.  
Then do for iterations $t=(1,2,...)$:  
1) Evolve Q:  
$Q_{ji}^{t} = \frac{p_i^{t-1}\omega_{ij}}{\sum_{k=1}^np_k^{t-1}\omega_{kj}}$
2) Evolve p:  
$p_i^{t} = \frac{\prod_{j=1}^m(Q_{ji}^t)^{\omega_{ij}}}{\sum_{k=1}^n\prod_{j=1}^m(Q_{jk}^t){\omega_{kj}}}$   

As long as the criteria for convergence are satisfied, the channel capacity can be approximated to arbitrary accuracy by the equation:  
$\lim_{t\rightarrow\infty}\sum_{i=1}^n\sum_{j=1}^m p_i^t\omega_{ij}\log_2\Big (\frac{Q_{ji}^t}{p_i^t}\Big )$

---
# To run:
Change the transition probability distribution and increase `number_of_iterations` to achieve satisfactory accuracy.  