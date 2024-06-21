#adapted from https://github.com/ussserrr/percolation-python

import numpy as np

import matplotlib.pyplot as plt

from functions import count_unique_elements

def generate_grid(probability_of_zero):
    grid = np.zeros((grid_y_dimension + 2, grid_x_dimension + 2))
    for cell in np.nditer(grid[1:-1, 1:-1], op_flags=['readwrite']):
        cell[...] = 0 if np.random.random() < probability_of_zero else 1
    return grid

def generate_grid_with_color(probability_of_zero, coords_to_color):
    grid = np.zeros((grid_y_dimension + 2, grid_x_dimension + 2))
    for cell in np.nditer(grid[1:-1, 1:-1], op_flags=['readwrite']):
        cell[...] = 0 if np.random.random() < probability_of_zero else 1
    
    # Color specified coordinates red
    for y, x in coords_to_color:
        grid[y, x] = 2  # Assigning 2 to mark these coordinates for red
    
    return grid


grid_x_dimension = 150
grid_y_dimension = 150
probability_of_zero = [0.9, 0.45, 0.42, 0.41,0.35, 0.1]
colors=['b','g','r']

legend_labels = []

#num_plots = len(probability_of_zero)
fig, axes = plt.subplots(3, 2, figsize=(6, 9))
#fig1, ax1 = plt.subplots(1, 1, figsize=(5, 5))

for ind, prob in enumerate(probability_of_zero):

    grid = generate_grid(prob)

    num_of_ones = np.count_nonzero(grid)

    ids = np.arange(num_of_ones)
    coords = [list(x) for x in np.argwhere(grid>0)]

    while True:
        cw = []

        for i in np.arange(num_of_ones):
            y,x = coords[i]

            if grid[y-1][x]==1 and grid[y][x-1]==0:
                ids[i] = ids[coords.index([y-1,x])]
            elif grid[y][x-1]==1 and grid[y-1][x]==0:
                ids[i] = ids[coords.index([y,x-1])]
            elif grid[y-1][x]==1 and grid[y][x-1]==1:
                first_neighbor_id = ids[coords.index([y-1,x])]
                second_neighbor_id = ids[coords.index([y,x-1])]
                ids[i] = np.min([first_neighbor_id, second_neighbor_id])
                if first_neighbor_id!=second_neighbor_id:
                    cw.append([first_neighbor_id,second_neighbor_id])

        if cw==[]:
            break
        else:
            for id1,id2 in cw:
                wrong_id = np.max([id1,id2])
                correct_id = np.min([id1,id2])
                ids[ids==wrong_id] = correct_id

    cluster_ids,sizes=count_unique_elements(ids)

    #find the cluster_id corresponding to the largest size cluster
    max_size=np.max(sizes)
    max_size_index = np.argmax(sizes)
    max_size_cluster_id = cluster_ids[max_size_index]
    print('max cluster size = ', max_size)
    print('max cluster size idx = ', max_size_index)

    clusters_coordinates = []
    for idx in np.unique(ids):
        clusters_coordinates.append([
            coords[k]
            for k in range(len(ids))
            if ids[k]==idx
            ])
        
    print('coords = ', len(clusters_coordinates[max_size_index]))
    coords_to_color = clusters_coordinates[max_size_index]
        
    # Color specified coordinates red
    for cy, cx in coords_to_color:
        grid[cy, cx] = 2  # Assigning 2 to mark these coordinates for red
        
    #grid = generate_grid_with_color(prob,coords_to_color)
    #ax = axes[ind]

    ax = axes[ind // 2, ind % 2]
    ax.matshow(grid[1:-1, 1:-1], cmap=plt.cm.gray_r)
    ax.axis('off')


    upwards = False
    lefttoright = False
    for cluster in clusters_coordinates:
        cluster = np.array(cluster).T
        if (1 in cluster[0]) and (grid_y_dimension in cluster[0]):
            upwards = True
            #coords_to_color=cluster
        if (1 in cluster[1]) and (grid_x_dimension in cluster[1]):
            lefttoright = True
            #coords_to_color=cluster

    if upwards and not lefttoright:
        ax.set_title(f"There is an upwards percolation, p = {prob}")
    elif not upwards and lefttoright:
        ax.set_title(f"There is a percolation from left to right, p = {prob}")
    elif upwards and lefttoright:
        ax.set_title(f"There are both types of percolation, p = {prob}")
    else:
        ax.set_title(f"There is no percolation, p = {prob}")



    # from functions import lnbin
    # BinNum = 50
    # midpts, Freq = lnbin(sizes, BinNum)
    # #print(midpts)
    # #print(Freq)
    # ax1.loglog(midpts, Freq, marker='.', linestyle='', color=colors[ind], markersize=8)
    # # Prepare legend labels based on percolation types
    # if upwards and not lefttoright:
    #     legend_labels.append("Upwards percolation")
    # elif not upwards and lefttoright:
    #     legend_labels.append("Left to right percolation")
    # elif upwards and lefttoright:
    #     legend_labels.append("Both types of percolation")
    # else:
    #     legend_labels.append("No percolation")

# # Add legend to ax1
# ax1.legend(legend_labels, loc='upper right')

# # Set labels and title for ax1
# ax1.set_xlabel('Cluster Size')
# ax1.set_ylabel('Frequency')
# ax1.set_title('Log-Log Plot of Cluster Frequency')


plt.tight_layout()
plt.show()

