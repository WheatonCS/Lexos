# ----------- USING SCIPY ------------
# from numpy import array
# import numpy as numpy
# from scipy.cluster.vq import vq, kmeans, kmeans2, whiten

# def getKMeans(matrix,k,iterateNumber):
#     """Parameters for KMeans"""
#     # whiten: Normalize a group of observations on a per feature basis
#     #         Each feature is divided by its standard deviation across all observations to give it unit variance

#     # matrix = zip(*matrix)


#     matrix = whiten(matrix)
#     codebook, distortion = kmeans(obs=matrix, k_or_guess=k, iter=iterateNumber, thresh=1e-05)
#     code, dist = vq(obs=matrix, code_book=codebook)
#     print code
#     return code

# -------- USING SKLEARN -----------
from sklearn import cluster

def getKMeans(matrix,k,iterateNumber, DocTermSparseMatrix):
    """Parameters for KMeans"""
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
    # n_jobs :    int
    #             The number of jobs to use for the computation
    #             -1 : all CPUs are used
    #             1 : no parallel computing code is used at all; useful for debugging
    #             For n_jobs below -1, (n_cpus + 1 + n_jobs) are used. 
    #             -2 : all CPUs but one are used.

    k_means = cluster.KMeans(n_clusters=k, max_iter=300, n_init=iterateNumber, init='k-means++', precompute_distances=True, n_jobs=1)
    k_means.fit(matrix)
    labels = k_means.labels_  # for silhouette score
    # k_means.cluster_centers_  if needed
    centerIndex = k_means.fit_predict(DocTermSparseMatrix)   # Index of the closest center each sample belongs to
    return centerIndex  # integer ndarray with shape (n_samples,) -- label[i] is the code or index of the centroid the i'th observation is closest to