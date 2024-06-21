import numpy as np
import matplotlib.pyplot as plt

from percolation_class import Percolation

grid_xD = 150
grid_yD = 150
probs = [0.9, 0.45, 0.42, 1-0.59274621,0.35, 0.1]
fig, axes = plt.subplots(3, 2, figsize=(6, 9))

for k,prob in enumerate(probs):
    perc = Percolation(grid_xD,grid_yD,prob)

    grid = perc.generate_grid()

    clusters,ids=perc.identify_clusters(grid)
    # print("number of clusters = ", len(clusters))
    # print(ids)

    cluster_ids, sizes = perc.count_unique_elements(ids)

    cluster_ids_without_zero = []
    sizes_without_zero = []

    # print('cluster ids = ', cluster_ids)
    # print('cluster sizes = ', sizes)

    for idx, id in enumerate(cluster_ids):
        if id != 0:
            cluster_ids_without_zero.append(id)
            sizes_without_zero.append(sizes[idx])

    # Find the index of the maximum cluster size
    max_cluster_size = max(sizes_without_zero)
    max_cluster_index = sizes_without_zero.index(max_cluster_size)
    max_cluster_id = cluster_ids_without_zero[max_cluster_index]

    # print('max cluster size = ', max_cluster_size)
    # print('id of largest cluster = ', max_cluster_id)

    largest_cluster_pos = cluster_ids_without_zero.index(max_cluster_id)
    # print('position of largest cluster in cluster list = ', largest_cluster_pos)
    # print('largest cluster size = ', len(clusters[largest_cluster_pos]))
    largest_cluster_coords = clusters[largest_cluster_pos]

    # Color specified coordinates red
    for cy, cx in largest_cluster_coords:
        grid[cy, cx] = 2  # Assigning 2 to mark these coordinates for red

    ax = axes[k // 2, k % 2]
    ax.matshow(grid[1:-1, 1:-1], cmap=plt.cm.gray_r)
    num_sig_figs = 8
    formatted_prob = f"{1 - prob:.{num_sig_figs}g}" 
    ax.set_title(f"p = {formatted_prob}")
    #ax.set_title(f"p = {1-prob}")
    ax.axis('off')

plt.tight_layout()
plt.show()

