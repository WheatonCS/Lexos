# -*- coding: utf-8 -*-
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans as KMeans

def getKMeans(NumberOnlymatrix, matrix, k, max_iter, initMethod, n_init, tolerance, DocTermSparseMatrix, metric_dist):
    """
    Generate an array of centroid index based on the active files.

    Args:
        NumberOnlymatrix: a matrix without file names and word
        matrix: a matrix representing the counts of words in files
        k: int, k-value
        max_iter: int, maximum number of iterations
        initMethod: str, method of initialization: 'k++' or 'random'
        n_init: int, number of iterations with different centroids
        tolerance: float, relative tolerance, inertia to declare convergence 
        DocTermSparseMatrix: sparse matrix of the word counts
        metric_dist: str, method of the distance metrics


    Returns:
        kmeansIndex: a numpy array of the cluster index for each sample 
        siltteScore: float, silhouette score
    """

    """Parameters for KMeans (SKlearn)"""
    # n_clusters: int, optional, default: 8
    #             namely, K;  number of clusters to form OR number of centroids to generate
    # max_iter :  int
    #             Maximum number of iterations of the k-means algorithm for a single run
    # n_init :    int, optional, default: 10
    #             Number of time the k-means algorithm will be run with different centroid seeds
    # init :      'k-means++', 'random' or an ndarray
    #             method for initialization; 
    #            'k-means++': selects initial cluster centers for k-mean clustering in a smart way to speed up convergence
    # precompute_distances : boolean
    # tol :       float, optional default: 1e-4
    #             Relative tolerance w.r.t. inertia to declare convergence
    # n_jobs :    int
    #             The number of jobs to use for the computation
    #             -1 : all CPUs are used
    #             1 : no parallel computing code is used at all; useful for debugging
    #             For n_jobs below -1, (n_cpus + 1 + n_jobs) are used. 
    #             -2 : all CPUs but one are used.

    

    inequality = '≤'.decode('utf-8')
    # trap bad silhouette score input

    #Convert from sparse matrix
    data= DocTermSparseMatrix.toarray()


    #coordinates for each cluster
    reduced_data = PCA(n_components=2).fit_transform(data)

    coordList=reduced_data.tolist()


    #Run fit_predict 100 times and find the most common combo to account for variation

    combosDict= {}

    for i in xrange(0,300):
        kmeans = KMeans(init= initMethod, n_clusters=k, n_init=n_init)
        kmeansIndex = kmeans.fit_predict(reduced_data)
        item= kmeansIndex.tolist()
        combo= ' '.join(str(x) for x in item)
        if combo in combosDict:
            combosDict[combo]+=1
        else:
            combosDict[combo]=1

    values=list(combosDict.values())
    keys=list(combosDict.keys())
    bestKey=keys[values.index(max(values))]
    stringIndex= bestKey.split()

    bestIndex=[]
    for x in stringIndex:
        bestIndex.append(int(x))



    if k<= 2:
        siltteScore = "N/A [Not avaiable for K " + inequality + " 2]"

    elif (k > (matrix.shape[0]-1)):
        siltteScore = 'N/A [Not avaiable if (K value) > (number of active files -1)]'

    else:
        kmeans.fit(NumberOnlymatrix)
        labels = kmeans.labels_  # for silhouette score
        siltteScore = getSiloutteOnKMeans(labels, matrix, metric_dist)

    return bestIndex, siltteScore # integer ndarray with shape (n_samples,) -- label[i] is the code or index of the centroid the i'th observation is closest to

def getSiloutteOnKMeans(labels, matrix, metric_dist):
    """
    Generate the silhouette score based on the KMeans algorithm.

    Args:
        labels: a list, class label of different files
        matrix: a matrix representing the counts of words in files
        metric_dist: str, method of the distance metrics

    Returns:
        siltteScore: float, silhouette score
    """

    siltteScore = metrics.silhouette_score(matrix, labels, metric=metric_dist)
    siltteScore = round(siltteScore,4)
    return siltteScore