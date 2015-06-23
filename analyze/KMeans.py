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

def centroid(xs,ys):
    
    centroidX=sum(xs)/len(xs)
    centroidY=sum(ys)/len(ys)
    centroid=[centroidX,centroidY]
    return centroid

def translatePointsToPositive(xs, ys, transX, transY):

    coordList=[]
    for i in xrange(0,len(xs)):
        xs[i]+=transX
        ys[i]+=transY
        coordList.append([xs[i],ys[i]])

    return coordList

def translateCoordsToPositive(xs, ys, transX, transY):

    for i in xrange(0,len(xs)):
        xs[i]+=transX
        ys[i]+=transY
        

    return xs,ys

def translateCentroidsToPositive(coords, transX, transY):

    coordList=[]
    for i in xrange(0,len(coords)):
        coords[i][0]+=transX
        coords[i][1]+=transY
        coordList.append([coords[i][0],coords[i][1]])

    return coordList

def textAttrsDictionary(title, x, y):
    
    attrDict= {"x":x,"y":y,"title":title}
    return attrDict

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

def getKMeansPCA(NumberOnlymatrix, matrix, k, max_iter, initMethod, n_init, tolerance, metric_dist, filenames):
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
        bestIndex: an array of the cluster index for each sample 
        siltteScore: float, silhouette score
        colorChart: string, list delimited by # of colors to use   
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
    
    #get color gradient
    color_list = plt.cm.Dark2(np.linspace(0, 1, k))

    #make color gradient a list
    colorList= color_list.tolist()

    #remove the a value from the rgba lists
    for rgba in colorList:
        del rgba[-1]

    rgbTuples=[]

    #convert to tuples and put in a list
    for i in xrange (0,len(colorList)):
        rgbTuples.append(tuple(colorList[i]))

    #coordinates for each cluster
    reduced_data = PCA(n_components=2).fit_transform(matrix)

    #n_init statically set to 300 for now. Probably should be determined based on number of active files 
    kmeans = KMeans(init= initMethod, n_clusters=k, n_init=n_init, tol= tolerance, max_iter=max_iter)
    kmeansIndex = kmeans.fit_predict(reduced_data)
    bestIndex = kmeansIndex.tolist()

    coloredPoints=[]

    #make list of color for each point
    for i in xrange(0,len(bestIndex)):
        coloredPoints.append(rgbTuples[bestIndex[i]])

    #split x and y coordinates
    xs, ys = reduced_data[:, 0], reduced_data[:, 1]

    #plot and label points
    for x, y, name, color in zip(xs, ys, filenames, coloredPoints):
        plt.scatter(x, y, c=color, s=40)
        plt.text(x, y, name, color=color)
    
    
    xUpperBound= max(xs) + 30 #set upper bound a little higher than the max
    xLowerBound= min(xs) - 30 #set lower bound a little lower than the min

    yUpperBound= max(ys) + 30
    yLowerBound= min(ys) - 30

    plt.ylim((yLowerBound,yUpperBound))
    plt.xlim((xLowerBound,xUpperBound))

    xTicksMax= (math.ceil((math.ceil(xUpperBound))/10))*10     #Set max tick mark to the next 10 above max (42 -> 50)
    xTicksMin= (math.floor((math.floor(xLowerBound))/10))*10   #Set min tick mark to the next 10 below max (-42 -> -50)

    yTicksMax= (math.ceil((math.ceil(yUpperBound))/10))*10
    yTicksMin= (math.floor((math.floor(yLowerBound))/10))*10

    xTickAmount= (xTicksMax-xTicksMin)/10 #Make it so there are always 10 ticks on x an y axis
    yTickAmount= (yTicksMax-yTicksMin)/10

    plt.xticks(np.arange(xTicksMin, xTicksMax, xTickAmount))
    plt.yticks(np.arange(yTicksMin, yTicksMax, yTickAmount))

    #folder for results
    folderPath = pathjoin(session_functions.session_folder(), constants.RESULTS_FOLDER)
    if (not os.path.isdir(folderPath)):
        makedirs(folderPath)

    #save the plot
    plt.savefig(pathjoin(folderPath, constants.KMEANS_GRAPH_FILENAME))

    #close the plot so next one doesn't plot over the last one
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

    #make a string of rgb tuples to send to the javascript separated by # cause jinja hates lists of strings
    colorChart=''

    for i in xrange(0,len(colorList)):
        for j in xrange (0,3):
            colorList[i][j]= int(colorList[i][j]*255) #Browser needs rgb tuples with int values 0-255 we have rgb tuples of floats 0-1
        
        temp=tuple(colorList[i])
        temp2="rgb" + str(temp)+"#"
        colorChart+=temp2

    return bestIndex, siltteScore, colorChart # integer ndarray with shape (n_samples,) -- label[i] is the code or index of the centroid the i'th observation is closest to

def getKMeansVoronoi(NumberOnlymatrix, matrix, k, max_iter, initMethod, n_init, tolerance, metric_dist, filenames):
    """
    Generate an array of centroid index based on the active files, list of points for the centroids, and a list 
    of points for the chunks.

    Args:
        NumberOnlymatrix: a numpy matrix without file names and word
        matrix: a python matrix representing the counts of words in files
        k: int, k-value
        max_iter: int, maximum number of iterations
        initMethod: str, method of initialization: 'k++' or 'random'
        n_init: int, number of iterations with different centroids
        tolerance: float, relative tolerance, inertia to declare convergence 
        metric_dist: str, method of the distance metrics
        filenames: list of active files


    Returns:
        bestIndex: an array of the cluster index for each sample 
        siltteScore: float, silhouette score
        colorChart: string of rgb tuples  
        finalPointsList: list of xy coords for each chunk 
        finalCentroidsList: list of xy coords for each centroid 
        textData: dicitonary of labels, xcoord, and ycoord 
        maxVal: the maximum x or y value used to set bounds in javascript
    """

    #xy coordinates for each chunk
    reduced_data = PCA(n_components=2).fit_transform(matrix)

    #n_init statically set to 300 for now. Probably should be determined based on number of active files 
    kmeans = KMeans(init= initMethod, n_clusters=k, n_init=n_init, tol= tolerance, max_iter=max_iter)
    kmeansIndex = kmeans.fit_predict(reduced_data)
    bestIndex = kmeansIndex.tolist()
    fullCoordList=reduced_data.tolist()

    #make an array centroidGroups whose elements are the coords that belong to each centroid 
    i= 1
    seen=[bestIndex[0]]
    centroidGroups= [[] for _ in range(k)] #make a list of k lists, one for each cluster
    centroidGroups[bestIndex[0]].append((fullCoordList[0])) #Group the centroids based on their cluster number

    while i < len(bestIndex):
        if bestIndex[i] in seen:
            centroidGroups[bestIndex[i]].append(fullCoordList[i])
            i+=1
        else:
            seen.append(bestIndex[i])
            centroidGroups[bestIndex[i]].append(fullCoordList[i])
            i+=1

    #Separate the x an y coordinates to calculate the centroid
    xsList=[]
    ysList=[]
    for i in xrange(0,len(centroidGroups)):
        tempXcoordList=[]
        tempYcoordList=[]
        for j in xrange(0,len(centroidGroups[i])):
            tempXcoord=centroidGroups[i][j][0]
            tempXcoordList.append(tempXcoord)
            tempYcoord=centroidGroups[i][j][1]
            tempYcoordList.append(tempYcoord)
        xsList.append(tempXcoordList)
        ysList.append(tempYcoordList)

    #calculate the coordinates for the centroid
    centroidCoords=[] 
    for i in xrange(0,len(xsList)):
        if len(xsList[i])==1:
            temp1=xsList[i][0] #each element in xslist is a list, but we need an int
            temp2=ysList[i][0] #each element in yslist is a list, but we need an int
            centroidCoords.append([temp1,temp2])
        else:
            centroidCoord=centroid(xsList[i],ysList[i])
            centroidCoords.append(centroidCoord)
    
    
    xs, ys = reduced_data[:, 0], reduced_data[:, 1]


    origXs=xs.tolist()
    origYs=ys.tolist()

    #Looks the same as above but necessary because neither can be manipulated more than once  
    xs=xs.tolist()
    ys=ys.tolist()

    #Translate every coordinate to positive as svg starts at top left with coordinate (0,0)
    transX=abs(min(xs))+100
    transY=abs(min(ys))+100

    transXs, transYs= translateCoordsToPositive(origXs,origYs,transX,transY)

    #Find the max coordinate to help determine the width (D3)
    maxX=max(transXs)
    maxY=max(transYs)

    maxList=[maxX,maxY]

    maxVal=max(maxList)

    #If maxY is the max it should be 4/3 the maxX
    if (abs(maxVal- maxY) < .00001) and (maxVal < ((4/3)* maxX)):
        maxVal=(4/3)*maxX  

    #Create a dictionary of filename,xCoord, yCoord to apply labels (D3)
    textData=[]
    for i in xrange(0,len(origXs)):
        temp= textAttrsDictionary(filenames[i],transXs[i],transYs[i])
        textData.append(temp)

    #Make a color gradient wtih k colors
    color_list = plt.cm.Dark2(np.linspace(0, 1, k))
    colorList= color_list.tolist()

    #Convert rgba to rgb (all a's are 1 and as such are unnecessary)
    for rgba in colorList:
        del rgba[-1]

    #Make the values tuples
    rgbTuples=[]
    for i in xrange (0,len(colorList)):
        rgbTuples.append(tuple(colorList[i]))

    #Order the colors based on cluster number so colors in Voronoi correspond to colors in table
    seen2=[]
    seen2.append(bestIndex[0]) 

    noRepeats=[]
    noRepeats.append(bestIndex[0])
    for i in xrange(1,len(bestIndex)):
        if bestIndex[i] not in seen2:
            seen2.append(bestIndex[i])
            noRepeats.append(bestIndex[i])

    orderedColorList=[None]*k

    for i in xrange(0,len(noRepeats)):
        orderedColorList[noRepeats[i]]=colorList[i]

    #make a string of rgb tuples to send to the javascript separated by # cause jinja hates lists of strings
    colorChart=''

    for i in xrange(0,len(orderedColorList)):
        for j in xrange (0,3):
            orderedColorList[i][j]= int(orderedColorList[i][j]*255) #Browser needs rgb tuples with int values 0-255 we have rgb tuples of floats 0-1
        
        temp=tuple(orderedColorList[i])
        temp2="rgb" + str(temp)+"#"
        colorChart+=temp2

    finalPointsList=translatePointsToPositive(xs,ys,transX,transY)
   
    finalCentroidsList=translateCentroidsToPositive(centroidCoords,transX,transY)
   
    #Starts with a dummy point set off the screen to get rid of yellow mouse tracking action (D3)
    finalCentroidsList.insert(0,[-500,-500])

    inequality = '≤'.decode('utf-8')
    if k<= 2:
        siltteScore = "N/A [Not avaiable for K " + inequality + " 2]"

    elif (k > (matrix.shape[0]-1)):
        siltteScore = 'N/A [Not avaiable if (K value) > (number of active files -1)]'

    else:
        kmeans.fit(NumberOnlymatrix)
        labels = kmeans.labels_  # for silhouette score
        siltteScore = getSiloutteOnKMeans(labels, matrix, metric_dist)


    return bestIndex, siltteScore, colorChart, finalPointsList, finalCentroidsList, textData, maxVal
