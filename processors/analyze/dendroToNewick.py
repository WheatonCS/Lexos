# Tells Flask to load this function when someone is at '/hierarchy'
@app.route("/cluster", methods=["GET", "POST"])
def cluster():
    fileManager = managers.utility.loadFileManager()
    leq = '≤'

    if request.method == "GET":
        # "GET" request occurs when the page is first loaded.
        if 'analyoption' not in session:
            session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS
        if 'hierarchyoption' not in session:
            session['hierarchyoption'] = constants.DEFAULT_HIERARCHICAL_OPTIONS
        labels = fileManager.get_active_labels()
        thresholdOps = {}
        return render_template(
            'cluster.html',
            labels=labels,
            thresholdOps=thresholdOps)

    if 'getdendro' in request.form:
        labelDict = fileManager.get_active_labels()
        labels = []
        for ind, label in list(labelDict.items()):
            labels.append(label)
        # Apply re-tokenisation and filters to DTM
        # countMatrix = fileManager.getMatrix(ARGUMENTS OMITTED)

        # Get options from request.form
        orientation = str(request.form['orientation'])
        title = request.form['title']
        pruning = request.form['pruning']
        pruning = int(request.form['pruning']) if pruning else 0
        linkage = str(request.form['linkage'])
        metric = str(request.form['metric'])

        # Get active files
        allContents = []  # list of strings-of-text for each segment
        tempLabels = []  # list of labels for each segment
        for lFile in list(fileManager.files.values()):
            if lFile.active:
                contentElement = lFile.load_contents()
                allContents.append(contentElement)

                if request.form["file_" + str(lFile.id)] == lFile.label:
                    tempLabels.append(lFile.label)
                else:
                    newLabel = request.form["file_" + str(lFile.id)]
                    tempLabels.append(newLabel)

        # More options
        ngramSize = int(request.form['tokenSize'])
        useWordTokens = request.form['tokenType'] == 'word'
        try:
            useFreq = request.form['normalizeType'] == 'freq'

            # if use TF/IDF
            useTfidf = request.form['normalizeType'] == 'tfidf'
            normOption = "N/A"  # only applicable when using "TF/IDF", set default value to N/A
            if useTfidf:
                if request.form['norm'] == 'l1':
                    normOption = 'l1'
                elif request.form['norm'] == 'l2':
                    normOption = 'l2'
                else:
                    normOption = None
        except BaseException:
            useFreq = useTfidf = False
            normOption = None

        onlyCharGramsWithinWords = False
        if not useWordTokens:  # if using character-grams
            # this option is disabled on the GUI, because countVectorizer count
            # front and end markers as ' ' if this is true
            onlyCharGramsWithinWords = 'inWordsOnly' in request.form

        greyWord = 'greyword' in request.form
        MostFrequenWord = 'mfwcheckbox' in request.form
        Culling = 'cullcheckbox' in request.form

        showDeletedWord = False
        if 'greyword' or 'mfwcheckbox' or 'cullcheckbox' in request.form:
            if 'onlygreyword' in request.form:
                showDeletedWord = True

        if useWordTokens:
            tokenType = 'word'
        else:
            tokenType = 'char'
            if onlyCharGramsWithinWords:
                tokenType = 'char_wb'

        from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
        vectorizer = CountVectorizer(
            input='content',
            encoding='utf-8',
            min_df=1,
            analyzer=tokenType,
            token_pattern=r'(?u)\b[\w\']+\b',
            ngram_range=(
                ngramSize,
                ngramSize),
            stop_words=[],
            dtype=float,
            max_df=1.0)

        # make a (sparse) Document-Term-Matrix (DTM) to hold all counts
        DocTermSparseMatrix = vectorizer.fit_transform(allContents)
        dtm = DocTermSparseMatrix.toarray()

        from sklearn.metrics.pairwise import euclidean_distances
        from scipy.cluster.hierarchy import ward

        import matplotlib.pyplot as plt
        from scipy.cluster.hierarchy import average, weighted, ward, single, complete, dendrogram
        from scipy.cluster import hierarchy
        from scipy.spatial.distance import pdist

        if orientation == "left":
            orientation = "right"
        if orientation == "top":
            LEAF_ROTATION_DEGREE = 90
        else:
            LEAF_ROTATION_DEGREE = 0

        if linkage == "ward":
            dist = euclidean_distances(dtm)
            np.round(dist, 1)
            linkage_matrix = ward(dist)
            dendrogram(
                linkage_matrix,
                orientation=orientation,
                leaf_rotation=LEAF_ROTATION_DEGREE,
                labels=labels)
            Z = linkage_matrix
        else:
            Y = pdist(dtm, metric)
            Z = hierarchy.linkage(Y, method=linkage)
            dendrogram(
                Z,
                orientation=orientation,
                leaf_rotation=LEAF_ROTATION_DEGREE,
                labels=labels)

        plt.tight_layout()  # fixes margins

        # Conversion to Newick/ETE
        # Stuff we need
        from scipy.cluster.hierarchy import average, linkage, to_tree
        #from hcluster import linkage, to_tree
        from ete2 import Tree, TreeStyle, NodeStyle

        # Change it to a distance matrix
        T = to_tree(Z)

        # ete2 section
        root = Tree()
        root.dist = 0
        root.name = "root"
        item2node = {T: root}

        to_visit = [T]
        while to_visit:
            node = to_visit.pop()
            cl_dist = node.dist / 2.0
            for ch_node in [node.left, node.right]:
                if ch_node:
                    ch = Tree()
                    ch.dist = cl_dist
                    ch.name = str(ch_node.id)
                    item2node[node].add_child(ch)
                    item2node[ch_node] = ch
                    to_visit.append(ch_node)

        # This is the ETE tree structure
        tree = root
        ts = TreeStyle()
        ts.show_leaf_name = True
        ts.show_branch_length = True
        ts.show_scale = False
        ts.scale = None
        if orientation == "top":
            ts.rotation = 90
            ts.branch_vertical_margin = 10  # 10 pixels between adjacent branches

        # Draws nodes as small red spheres of diameter equal to 10 pixels
        nstyle = NodeStyle()
        nstyle["size"] = 0

        # Replace the node labels
        for leaf in tree:
            k = leaf.name
            k = int(k)
            leaf.name = labels[k]

        # Apply node styles to nodes
        for n in tree.traverse():
            n.set_style(nstyle)

        # Convert the ETE tree to Newick
        newick = tree.write()
        f = open(
            'C:\\Users\\Scott\\Documents\\GitHub\\d3-dendro\\newickStr.txt',
            'w')
        f.write(newick)
        f.close()

        # Save the image as .png...
        from os import path, makedirs

        # Using ETE
        folder = pathjoin(
            session_manager.session_folder(),
            constants.RESULTS_FOLDER)
        if (not os.path.isdir(folder)):
            makedirs(folder)

        # saves dendrogram as a .png with pyplot
        plt.savefig(path.join(folder, constants.DENDROGRAM_PNG_FILENAME))
        plt.close()
        # if orientation == "top":
        #     plt.figure(figsize=(20,80))
        # else:
        #     plt.figure(figsize=(80,20))

        pdfPageNumber, score, inconsistentMax, maxclustMax, distanceMax, distanceMin, monocritMax, monocritMin, threshold = utility.generateDendrogram(
            fileManager)
        session['dengenerated'] = True
        labels = fileManager.get_active_labels()

        inconsistentOp = "0 " + leq + " t " + leq + " " + str(inconsistentMax)
        maxclustOp = "2 " + leq + " t " + leq + " " + str(maxclustMax)
        distanceOp = str(distanceMin) + " " + leq + " t " + \
            leq + " " + str(distanceMax)
        monocritOp = str(monocritMin) + " " + leq + " t " + \
            leq + " " + str(monocritMax)

        thresholdOps = {
            "inconsistent": inconsistentOp,
            "maxclust": maxclustOp,
            "distance": distanceOp,
            "monocrit": monocritOp}

        managers.utility.saveFileManager(fileManager)
        session_manager.cacheAnalysisOption()
        session_manager.cacheHierarchyOption()
        import random
        ver = random.random() * 100
        return render_template(
            'cluster.html',
            labels=labels,
            pdfPageNumber=pdfPageNumber,
            score=score,
            inconsistentMax=inconsistentMax,
            maxclustMax=maxclustMax,
            distanceMax=distanceMax,
            distanceMin=distanceMin,
            monocritMax=monocritMax,
            monocritMin=monocritMin,
            threshold=threshold,
            thresholdOps=thresholdOps,
            ver=ver)


# Tells Flask to load this function when someone is at '/hierarchy'
@app.route("/cluster/output", methods=["GET", "POST"])
def clusterOutput():
    imagePath = pathjoin(
        session_manager.session_folder(),
        constants.RESULTS_FOLDER,
        constants.DENDROGRAM_PNG_FILENAME)
    return send_file(imagePath)
