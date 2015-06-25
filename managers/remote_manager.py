from flask import request


def getTopWordOption():
    """
    get the top word option from the front end

    :return:
        testbyClass: option for proportional z test to see whether to use testgroup() or testall()
                        see analyze/topword.py testgroup() and testall() for more
        option: the wordf ilter to determine what word to send to the topword analysis
                    see analyze/topword.py testgroup() and testall() for more
        High: the Highest Proportion that sent to topword analysis
        Low: the Lowest Proportion that sent to topword analysis
    """
    if 'testInput' in request.form:  # when do KW this is not in request.form
        testbyClass = request.form['testInput'] == 'useclass'
    else:
        testbyClass = True

    outlierMethod = 'StdE' if request.form['outlierMethodType'] == 'stdErr' else 'IQR'

    # begin get option
    Low = 0.0  # init Low
    High = 1.0  # init High

    if outlierMethod == 'StdE':
        outlierRange = request.form["outlierTypeStd"]
    else:
        outlierRange = request.form["outlierTypeIQR"]

    if request.form['groupOptionType'] == 'all':
        option = 'CustomP'
    elif request.form['groupOptionType'] == 'bio':
        option = outlierRange + outlierMethod
    else:
        if request.form['useFreq'] == 'RC':
            option = 'CustomR'
            High = int(request.form['upperboundRC'])
            Low = int(request.form['lowerboundRC'])
        else:
            option = 'CustomP'
            High = float(request.form['upperboundPC'])
            Low = float(request.form['lowerboundPC'])

    return testbyClass, option, Low, High