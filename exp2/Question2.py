import random
import numpy as np

def logistic_map(mu, x, n):
    """
    计算Logistic混沌映射的值
    :param mu: 映射函数的参数
    :param x: 初始值
    :param n: 迭代数
    :return: 迭代n次后的值
    """
    for i in range(n):
        x = mu * x * (1 - x)
    return x

def logistic_pemutation(n, mu):
    """
    构造长度为n的置乱
    :param n 置乱的长度
    :param mu: 映射函数的参数
    :return: 置乱后的序列
    """
    # 生成初始序列
    seq = [logistic_map(mu, 0.5, i) for i in range(1, n+1)]
    # 排序并生成置乱序列
    scramble_seq = [seq.index(x) for x in sorted(seq)]
    return scramble_seq

# 计算序列的熵
def entropy(seq1,seq2):
    seq=np.abs(np.array(seq1) - np.array(seq2))
    hist, _ = np.histogram(seq, bins=len(seq))
    p = hist / len(seq)
    return -np.sum(p * np.log2(p + 1e-12))

# 计算序列的相关系数
def correlation_coefficient(seq1, seq2):
    return np.corrcoef(seq1, seq2)[0, 1]

# 计算序列的位置差异度
def move_distance(seq1, seq2):
    return np.sum(np.abs(np.array(seq1) - np.array(seq2)))/len(seq1)

# 计算序列的欧拉距离
def euclidean_distance(seq1, seq2):
    return np.sqrt(np.sum((np.array(seq1) - np.array(seq2))**2))/len(seq1)

# 计算序列的逆序对数
def count_inversions(seq1, seq2):
    inv_count = 0
    for i in range(n):
        for j in range(i+1, n):
            if seq1[i] < seq1[j] and seq2.index(seq[i]) > seq2.index(seq[j]):
                inv_count += 1
    return inv_count

# 计算评估指标

# 序列长度
num=[100,1000,10000]
# 参数mu
mu=[3.6,3.7,3.8]
# 置乱算法
method=['random','logistic']

for n in num:
    for mode in method:
        permuted_seq = [i for i in range(0,n)]
        # random.shuffle方法
        if mode == 'random':
            random.shuffle(permuted_seq)
            seq = [i for i in range(0,n)]
            print("\nMode:{}|Number:{}".format(mode,n))
            print("Entropy:", entropy(seq,permuted_seq))
            print("Correlation coefficient:", correlation_coefficient(seq, permuted_seq))
            print("Move distance:", move_distance(seq, permuted_seq))
            if n < 10000:
                print("Euclidean_distance:", euclidean_distance(seq, permuted_seq))
                inv_count= count_inversions(seq, permuted_seq)
                print("count_inversions:",inv_count)
                print("Normalized Inversion Count:", inv_count / (len(seq) * (len(seq) - 1) / 2))
        # logistic方法
        if mode == 'logistic':
            for m in mu:
                permuted_seq=logistic_pemutation(n,m)
                seq = [i for i in range(0,n)]
                print("\nMode:{}|Number:{}|Mu:{}".format(mode,n,m))
                print("Entropy:", entropy(seq,permuted_seq))
                print("Correlation coefficient:", correlation_coefficient(seq, permuted_seq))
                print("Move distance:", move_distance(seq, permuted_seq))
                if n < 10000:
                    print("Euclidean_distance:", euclidean_distance(seq, permuted_seq))
                    inv_count= count_inversions(seq, permuted_seq)
                    print("count_inversions:",inv_count)
                    print("Normalized Inversion Count:", inv_count / (len(seq) * (len(seq) - 1) / 2))
        