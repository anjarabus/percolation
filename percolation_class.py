import numpy as np

class Percolation: 
    
    def __init__(self, gridXD, gridYD, prob):
        self.grid_y_dimension = gridXD
        self.grid_x_dimension = gridYD
        self.probability_of_zero = prob

    def generate_grid(self):
        grid = np.zeros((self.grid_y_dimension + 2, self.grid_x_dimension + 2), dtype=int)
        for y in range(1, self.grid_y_dimension + 1):
            for x in range(1, self.grid_x_dimension + 1):
                if np.random.random() < self.probability_of_zero:
                    grid[y, x] = 0
                else:
                    grid[y, x] = 1
        return grid

    def identify_clusters(self,grid):
        grid_shape = grid.shape
        ids = np.zeros_like(grid, dtype=int)
        current_id = 1
        
        for y in range(grid_shape[0]):
            for x in range(grid_shape[1]):
                if grid[y, x] == 1:
                    # Check neighbors
                    neighbors = []
                    if y > 0 and grid[y-1, x] == 1:
                        neighbors.append(ids[y-1, x])
                    if x > 0 and grid[y, x-1] == 1:
                        neighbors.append(ids[y, x-1])
                    
                    if len(neighbors) == 0:
                        ids[y, x] = current_id
                        current_id += 1
                    else:
                        min_neighbor_id = min(neighbors)
                        ids[y, x] = min_neighbor_id
                        for neighbor_id in neighbors:
                            if neighbor_id != min_neighbor_id:
                                ids[ids == neighbor_id] = min_neighbor_id
        
        #cluster_ids, sizes = count_unique_elements(ids)
        
        clusters = []
        for cluster_id in np.unique(ids):
            if cluster_id != 0:  # Skip background (0)
                cluster_coords = np.argwhere(ids == cluster_id)
                clusters.append(cluster_coords)
        
        return clusters, ids

    def count_unique_elements(self,arr):
        element_count = {}
        
        for element in arr.flatten():
            if element in element_count:
                element_count[element] += 1
            else:
                element_count[element] = 1
        
        element_ids = list(element_count.keys())
        element_counts = list(element_count.values())
        
        return element_ids, element_counts
    
    def lnbin(self,x, BinNum):
        x = np.sort(x)
        i = 0
        while x[i] <= 0:
            i += 1
        
        percentage_binned = (len(x) - i) / len(x) * 100
        print(f"Percentage of input vec binned: {percentage_binned:.2f}%")
        
        FPT = x[i:]  # Filtered positive values
        LFPT = np.log(FPT)
        max1 = np.log(np.ceil(np.max(FPT)))
        min1 = np.log(np.floor(np.min(FPT)))
        
        LFreq = np.zeros(BinNum)
        LTime = np.zeros(BinNum)
        Lends = np.zeros((BinNum, 2))
        step = (max1 - min1) / BinNum
        
        # Log Binning Data
        for i in range(len(FPT)):
            for k in range(1, BinNum + 1):
                if (k - 1) * step + min1 <= LFPT[i] < k * step + min1:
                    LFreq[k - 1] += 1
                LTime[k - 1] = k * step - (0.5 * step) + min1
                Lends[k - 1, 0] = (k - 1) * step + min1
                Lends[k - 1, 1] = k * step + min1
        
        ends = np.exp(Lends)
        widths = ends[:, 1] - ends[:, 0]
        Freq = LFreq / widths / len(x)
        #eFreq = 1 / np.sqrt(LFreq) * Freq
        midpts = np.exp(LTime)
        
        return midpts, Freq#, eFreq




