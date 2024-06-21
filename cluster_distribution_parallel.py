#This script runs as many processes simultaneously as there are probabilities p 
# For each: 
# creates a lattice and fills the lattice with occupation probability p, 
# finds and labels the clusters, 
# calculates the cluster sizes and saves them in a file sizes_data_<gridDimension>.txt

# These distributions can be plotted using cluster_dist_figure.py

import numpy as np
import time
import matplotlib.pyplot as plt
import multiprocessing
from percolation_class import Percolation

gridDIM = 1000

def clusters_prob(prob,sizes_list):

    gridXD=gridDIM
    gridYD=gridDIM

    perc = Percolation(gridXD, gridYD, prob)

    grid = perc.generate_grid()
    clusters, ids = perc.identify_clusters(grid)
    cluster_ids, sizes = perc.count_unique_elements(ids)

    sizes_list.append((prob, sizes))

if __name__ == "__main__":
    probs = [1 - 0.59274621, 1 - 0.57, 1 - 0.56, 1 - 0.55, 1 - 0.54]
    legend_labels = []

    # Use manager to create a shared list
    manager = multiprocessing.Manager()
    sizes_list = manager.list()


    # Create a pool of processes
    start = time.time()
    with multiprocessing.Pool(processes=len(probs)) as pool:
        pool.starmap(clusters_prob, [(probs[i], sizes_list) for i in range(len(probs))])
    end = time.time()

    # Save sizes to a file
    filename = f'sizes_{gridDIM}.txt'
    with open(filename, 'w') as f:
        for prob, sizes in sizes_list:
            f.write(f"Probability: {prob}, Sizes: {sizes}\n")

    print(f"Sizes saved to {filename}")

    print('start time: ', start)
    print('end time: ', end)
    print('elapsed time: ', end-start)



