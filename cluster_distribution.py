#This script runs a for loop over probabilities p
# For each p:  
# creates a lattice and fills it with occupation probability p, 
# finds and labels the clusters, 
# calculates the cluster sizes and plots the distribution of cluster sizes

import numpy as np
import time
import matplotlib.pyplot as plt
from percolation_class import Percolation

gridXD = 2000
gridYD = 2000
# probs=[1-0.1,1-0.55,1-0.58,1-0.59274621,1-0.65,1-0.9]
# colors=['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:grey']
#probs=[1-0.59274621,1-0.57,1-0.55]
probs=[1 - 0.59274621, 1 - 0.57, 1 - 0.56, 1 - 0.55, 1 - 0.54]
colors=['tab:blue','tab:green','tab:red','tab:orange', 'tab:purple']
legend_labels=[]
start=time.time()
for k,prob in enumerate(probs):
    perc = Percolation(gridXD, gridYD, prob)

    grid = perc.generate_grid()
    clusters,ids=perc.identify_clusters(grid)
    cluster_ids, sizes = perc.count_unique_elements(ids)

    # print(sizes[1:])

    BinNum = 100
    midpts, Freq = perc.lnbin(sizes, BinNum)
    # print(midpts)
    # print(Freq)
    plt.loglog(midpts, Freq, marker='.', linestyle='', color=colors[k], markersize=8)
    num_sig_figs=8
    formatted_prob = f"{1 - prob:.{num_sig_figs}g}" 
    legend_labels.append(f"p = {formatted_prob}")

    # cluster_size,cluster_freq = count_unique_elements(sizes)
    # print(cluster_size)
    # print(cluster_freq)

    # #plt.scatter(cluster_size,cluster_freq, marker='o',color='b')
    # plt.loglog(cluster_size, cluster_freq, marker='o', linestyle='', color='b', markersize=8)
end = time.time()
print('start time: ', start)
print('end time: ', end)
print('elapsed time: ', end-start)
plt.legend(legend_labels, loc='upper right')
plt.show()


