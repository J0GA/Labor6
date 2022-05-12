import networkx as nx
import numpy as np
#import pylab as plt
import matplotlib.pyplot as plt
import scipy.sparse as sp
import math
import timeit

# Импорт данных из файла .json и распаковка данных
n=6
D = [[] for i in range(n)] # "объявляет" матрицу(двумерный массив)
with open('m.txt') as file:
    for i in range(n):
        D[i] = [int(t) for t in file.readline().split()] # читает всю строку, делит по пробелам, и сохраняет как массив интов записывая в строку матрицы

Matrix = np.array(D)
def get_matrix_triad(coo_matrix):
	if not sp.isspmatrix_coo(coo_matrix):
		coo_matrix = sp.coo_matrix(coo_matrix)
	temp = np.vstack((coo_matrix.row, coo_matrix.col, coo_matrix.data)).transpose()
	return temp.tolist()
edags = get_matrix_triad(Matrix)
print(edags)
G = nx.Graph()
H = nx.path_graph(Matrix.shape[0])
G.add_nodes_from(H)
G.add_weighted_edges_from(edags)
nx.draw(G, with_labels=True)
plt.savefig('graph.png')
plt.close()

start_time = timeit.default_timer()
def get_link_v(v, D):
    for i, weight in enumerate(D[v]):
        if weight > 0:
            yield i

def arg_min(T, S):
    amin = -1
    m = math.inf  # максимальное значение
    for i, t in enumerate(T):
        if t < m and i not in S:
            m = t
            amin = i
    return amin
n=6
D = [[] for i in range(n)] # "объявляет" матрицу(двумерный массив)
with open('m.txt') as file:
    for i in range(n):
        D[i] = [int(t) for t in file.readline().split()] # читает всю строку, делит по пробелам, и сохраняет как массив интов записывая в строку матрицы
N = len(D)  # число вершин в графе
T = [math.inf]*N   # последняя строка таблицы
v = 0       # стартовая вершина (нумерация с нуля)
S = {v}     # просмотренные вершины
T[v] = 0    # нулевой вес для стартовой вершины
while v != -1:          # цикл, пока не просмотрим все вершины
    for j in get_link_v(v, D):   # перебираем все связанные вершины с вершиной v
        if j not in S:           # если вершина еще не просмотрена
            w = T[v] + D[v][j]
            if w < T[j]:
                T[j] = w
    v = arg_min(T, S)            # выбираем следующий узел с наименьшим весом
    if v >= 0:                    # выбрана очередная вершина
        S.add(v)                 # добавляем новую вершину в рассмотрение
print(T)
print(f"Программа выполнила работу за {str(timeit.default_timer()-start_time)} сек.")