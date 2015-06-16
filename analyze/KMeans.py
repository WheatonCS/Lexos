# -*- coding: utf-8 -*-
import os
from os.path import join as pathjoin
from os import makedirs
import math

from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans as KMeans
import numpy as np
import matplotlib.pyplot as plt

import helpers.session_functions as session_functions
import helpers.constants as constants



# def save_object(obj, filename):
#     with open(filename, 'wb') as output:
#         pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def getKMeans(NumberOnlymatrix, matrix, k, max_iter, initMethod, n_init, tolerance, metric_dist, filenames):
    """
    Generate an array of centroid index based on the active files.

    Args:
        NumberOnlymatrix: a numpy matrix without file names and word
        matrix: a python matrix representing the counts of words in files
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
    
    color_list = plt.cm.Dark2(np.linspace(0, 1, k))

    colorList= color_list.tolist()

    for rgba in colorList:
        del rgba[-1]

    rgbTuples=[]

    for i in xrange (0,len(colorList)):
        rgbTuples.append(tuple(colorList[i]))

    #coordinates for each cluster
    reduced_data = PCA(n_components=2).fit_transform(matrix)

    #n_init statically set to 300 for now. Probably should be determined based on number of active files 
    kmeans = KMeans(init= initMethod, n_clusters=k, n_init=n_init, tol= tolerance, max_iter=max_iter)
    kmeansIndex = kmeans.fit_predict(reduced_data)
    bestIndex = kmeansIndex.tolist()

    coloredPoints=[]

    for i in xrange(0,len(bestIndex)):
        coloredPoints.append(rgbTuples[bestIndex[i]])

    xs, ys = reduced_data[:, 0], reduced_data[:, 1]

    for x, y, name, color in zip(xs, ys, filenames, coloredPoints):
        plt.scatter(x, y, c=color, s=40)
        plt.text(x, y, name, color=color)
    
    
    xUpperBound= max(xs) + 30
    xLowerBound= min(xs) - 30

    yUpperBound= max(ys) + 30
    yLowerBound= min(ys) - 30

    plt.ylim((yLowerBound,yUpperBound))
    plt.xlim((xLowerBound,xUpperBound))

    xTicksMax= (math.ceil((math.ceil(xUpperBound))/10))*10
    xTicksMin= (math.floor((math.floor(xLowerBound))/10))*10

    yTicksMax= (math.ceil((math.ceil(yUpperBound))/10))*10
    yTicksMin= (math.floor((math.floor(yLowerBound))/10))*10

    plt.xticks(np.arange(xTicksMin, xTicksMax, 30.0))
    plt.yticks(np.arange(yTicksMin, yTicksMax, 30.0))

    folderPath = pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER)
    if (not os.path.isdir(folderPath)):
        makedirs(folderPath)

    plt.savefig(pathjoin(folderPath, constants.KMEANS_GRAPH_FILENAME))

    plt.close()
    # trap bad silhouette score input
    if k<= 2:
        siltteScore = "N/A [Not avaiable for K " + inequality + " 2]"

    elif (k > (matrix.shape[0]-1)):
        siltteScore = 'N/A [Not avaiable if (K value) > (number of active files -1)]'

    else:
        kmeans.fit(NumberOnlymatrix)
        labels = kmeans.labels_  # for silhouette score
        siltteScore = getSiloutteOnKMeans(labels, matrix, metric_dist)


    colorChart=''

    for i in xrange(0,len(colorList)):
        for j in xrange (0,3):
            colorList[i][j]= int(colorList[i][j]*255)
        
        temp=tuple(colorList[i])
        temp2="rgb" + str(temp)+"#"
        colorChart+=temp2

    return bestIndex, siltteScore, colorChart # integer ndarray with shape (n_samples,) -- label[i] is the code or index of the centroid the i'th observation is closest to

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