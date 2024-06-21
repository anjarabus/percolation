import numpy as np

def count_unique_elements(arr):
    # Initialize an empty dictionary to store counts
    element_count = {}
    
    # Count occurrences of each element in the array
    for element in arr:
        if element in element_count:
            element_count[element] += 1
        else:
            element_count[element] = 1
    
    # Output the number of unique elements and their counts
    num_unique_elements = len(element_count)
    print(f"Number of clusters: {num_unique_elements}")
    
    #print("Size of each cluster:")
    counts=[]
    elements=[]
    for element, count in element_count.items():
        counts.append(count)
        elements.append(element)
        #print(f"{element}: {count}")
    return elements,counts

def lnbin(x, BinNum):
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




