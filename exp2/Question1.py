import itertools
import math
import random
import matplotlib.pyplot as plt
from sympy import primerange, sqrt, log, Rational

def find_order(permutation):
    n = len(permutation)
    visited = [False] * n
    order = 1

    for i in range(n):
        if not visited[i]:
            cycle_length = 0
            current = i
            while not visited[current]:
                visited[current] = True
                current = permutation[current]
                cycle_length += 1
            order = (order * cycle_length) // math.gcd(order, cycle_length)

    return order

# n值较小的情况计算T与p(K)
def samll_n_plot_p_k_curve(N,T=10000):
    orders = [0] * (T + 1)
    total_permutations = 0
    # 遍历循环
    for p in itertools.permutations(range(N)):
        order = find_order(p)
        orders[order] += 1
        total_permutations += 1
    # 计算最大阶T
    for i in range(T,0,-1):
        if(orders[i]!=0):
            T=i
            break
    # 统计频率
    cumulative_probabilities = [0] * (T + 1)
    for i in range(1, T + 1):
        cumulative_probabilities[i] = cumulative_probabilities[i - 1] + orders[i] / total_permutations
    # 绘制p(K)
    print(f'Maximum order T for N = {N}: {T}')
    plt.plot(range(T + 1), cumulative_probabilities)
    plt.xlabel('K')
    plt.ylabel('p(K)')
    plt.title(f'p(K) curve for N = {N}; T = {T}')
    plt.show()

# Landau's function g(n)
def f(N): # compute terms a(0)..a(N)
    V = [1 for j in range(N+1)]
    if N < 4:
        C = 2
    else:
        C = Rational(166, 125)
    for i in primerange(C*sqrt(N*log(N))):
        for j in range(N, i-1, -1):
            hi = V[j]
            pp = i
            while pp <= j:
                hi = max(V[j-pp]*pp, hi)
                pp *= i
            V[j] = hi
    return V
# Philip Turecek, Mar 31 2023

# 产生随机置乱
def generate_permutation(n):
    permutation = list(range(n))
    random.shuffle(permutation)
    return permutation

# n值较大的情况计算T与p(K)
def large_n_plot_p_k_curve(N,T):
    # 统计基数
    radix=1000
    freq=1000
    cumulative_probabilities = [0] * (freq + 1)
    i=0
    for K in range(0,T,T//freq):
        count=0
        for j in range(radix):
            p=generate_permutation(N)
            order = find_order(p)
            if order < K:
                count+=1
        cumulative_probabilities[i]=count/radix
        i+=1
        
    # 绘制p(K)
    print(f'Maximum order T for N = {N}: {T}')
    plt.plot(range(0,T,T//freq), cumulative_probabilities)
    plt.xlabel('K')
    plt.ylabel('p(K)')
    plt.title(f'p(K) curve for N = {N}; T = {T}')
    plt.show()


N = 200
# samll_n_plot_p_k_curve(N)
T=f(200)[N]
if N >= 50:
    large_n_plot_p_k_curve(N,T)
