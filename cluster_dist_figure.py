import numpy as np
import time
import matplotlib.pyplot as plt
from percolation_class import Percolation
import re

data=[]

gridDIM=1000

f = open(f"sizes_{gridDIM}.txt", "r")
for line in f:
    try:
        # Example line: "Probability: 0.40725379, Sizes: [10, 15, 20, ...]"
        # Use regex to extract probability and sizes
        match = re.match(r"Probability: (\d+\.\d+), Sizes: \[(.*)\]", line.strip())
        if match:
            prob = float(match.group(1))
            sizes_str = match.group(2)
            sizes = list(map(int, sizes_str.split(', ')))  # Split by ', ' to handle spaces
            data.append((prob, sizes))
        else:
            raise ValueError("Line does not match expected format")
    except Exception as e:
        print(f"Error parsing line '{line.strip()}': {e}")
    
        data.append((prob, sizes))

BinNum = 50
num_sig_figs = 8
legend_labels=[]
for prob, sizes in data:
    #print(f"Probability: {prob}, Sizes: {sizes}")
    perc = Percolation(None,None,None)
    midpts, Freq = perc.lnbin(sizes, BinNum)
    plt.loglog(midpts, Freq, marker='.', linestyle='', markersize=5)
    #plt.scatter(cluster_size,cluster_freq, marker='o',color='b')
    # plt.loglog(cluster_size, cluster_freq, marker='o', linestyle='', color='b', markersize=8)

    formatted_prob = f"{1 - prob:.{num_sig_figs}g}"
    legend_labels.append(f"p = {formatted_prob}")

plt.legend(legend_labels, loc='upper right')
plt.show()
    

    
    