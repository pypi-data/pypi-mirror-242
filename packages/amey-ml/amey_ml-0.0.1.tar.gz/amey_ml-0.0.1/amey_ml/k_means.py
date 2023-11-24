import numpy as np

def output(data_file, K, initialization):
    """
    Perform the K-means clustering algorithm on a dataset.

    Args:
        data_file (str): The file path for the input data, expected to be in a text format where
                         each line represents a single data point.
        K (int): The number of clusters to form.
        initialization (str): The method for initializing the centroids.
                              "random" - select K random points from the data as the initial centroids.
                              "round_robin" - select K points using a round-robin approach from the data.
    
    The function will reshape 1D data into a 2D array for compatibility with the algorithm.
    The main loop of the function continues until the cluster assignments stop changing, indicating convergence.
    
    After convergence, the function prints each data point along with its cluster assignment and writes
    this information to an output file. The output file is named by appending the number of clusters (K)
    to the base name of the input file, separated by an underscore, and retaining the original file extension.
    
    Returns:
        None: This function does not return any value. It writes the clustering results to an output file
              and also prints them to the console.
    """

    # Load the data
    output_file=data_file.split('.')[0]+'_'+str(K)+'.txt'
    data = np.loadtxt(data_file)
    
    # Check if the data is 1D or 2D
    if data.ndim == 1:
        data = data.reshape(-1, 1)
    
    # Initialization
    if initialization == "random":
        centroids = data[np.random.choice(range(data.shape[0]), K, replace=False)]
    elif initialization == "round_robin":
        centroids = np.array([data[i % len(data)] for i in range(K)])
    
    # Initial assignments
    assignments = np.zeros(data.shape[0], dtype=int)
    for i, point in enumerate(data):
        if initialization == "round_robin":
            assignments[i] = i % K + 1
        elif initialization == "random":
            assignments[i] = np.argmin(np.linalg.norm(point - centroids, axis=1)) + 1
    
    # Main k-means loop
    while True:
        # Create new centroids
        new_centroids = np.array([data[assignments == i+1].mean(axis=0) for i in range(K)])
        
        # Assign points to the nearest centroid
        new_assignments = np.array([np.argmin(np.linalg.norm(point - new_centroids, axis=1)) + 1 for point in data])
        
        # Check for convergence
        if np.array_equal(assignments, new_assignments):
            break
        else:
            centroids = new_centroids
            assignments = new_assignments
    
    with open(output_file, 'w') as output_file:
        for i, point in enumerate(data):
            cluster_id = assignments[i]
            if point.shape[0] == 1:  # 1D case
                print('%10.4f --> cluster %d' % (point[0], cluster_id))
                output_file.write('%10.4f --> cluster %d\n' % (point[0], cluster_id))
            else:  # 2D case
                print('(%10.4f, %10.4f) --> cluster %d' % (point[0], point[1], cluster_id))
                output_file.write('(%10.4f, %10.4f) --> cluster %d\n' % (point[0], point[1], cluster_id))
