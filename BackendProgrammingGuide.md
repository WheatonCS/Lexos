# Back-end Programming Guide for Lexos


## <a name='overview'></a> Overview
* [Overview](#overview)
* [What is This?](#this)
* [Helpful Tips](#tip)
* [A General Introduction to Some Important Things](#intro)
* [Back-end Program Structure and Programming Standards](#std)

---


## <a name='this'></a> What is This?
* This is the back-end programming guide for Lexos programmers.
* It would be helpful to read it before programming the back-end of Lexos, including tips and standards.
* This guide assumes you know basic web structure and python (if you find this hard to read, stop and go [here](http://www.codecademy.com/en/tracks/python))

---


## <a name='tip'></a> Helpful Tips
#### 1. Read the `constant.py` and `general_function.py` in `helpers` folder before you do anything real, so that you don't reinvent the wheel.
#### 2. Play with `join` and `split` function before you want to deal with strings

For example use:
```python
str = ''.join[list]
```
Instead of:
```python
str = ''
for element in list:
    str += element
```
To create a csv:
```python
rows = [','.join[row] for row in matrix]
csv = '\n'.join[rows]
```

#### 3. Play with `filter` `map` function, `*` and in-line `for` loop before you want to deal with Lists

  For example use:
  ```python
  map(lambda element: element[:50], list)
  ```
  Instead of:
  ```python
  for i in range(len(list)):
      list[i] = list[i][:50]
  ```

When you initialize the list, use `*` rather than a `for` loop:

  For example use:
  ```python
  emptyMatrix = [[]] * LenMatrix
  ```
  Instead of:
  ```python
  emptyMatrix = []
  for _ in LenMatrix:
      emptyMatrix.append([])
  ```

#### 4. Use `try`, `except` rather than `if` when you are dealing with Dicts.

  For example use:
  ```python
  try:
      dict[i] += 1
  except KeyError:
      dict[i] = 1
  ```
  Instead of:
  ```python
  if i in dict:
      dict[i] += 1
  else:
      dict[i] = 1
  ```

  Use:
  ```python
  try:
      os.makedir(path)
  except:
      pass
  ```
  Instead of:
  ```python
  if os.path.isdir(path)
      pass
  else:
      os.makedir(path)
  ```

  These are both clearer and faster

#### 5. Using `except` to do complicated jobs, always specifies the error type (`KeyError`, `ValueError`, ect.) that you want to except.

#### 6. When encounter Matrix, use `np.array` or `dict` instead of python List.

(Current program has python array all over the place, we need to fix that)
  
  Use:
  ```python
  for element in npArray.flat():
      print element
  ```
  Instead of:
  ```python
  for row in pythonList:
      for element in row:
          print element
  ```

  Read [this tutorial](http://wiki.scipy.org/Tentative_NumPy_Tutorial) for more info

#### 7. Use `lambda` to create temp function

  Use:
  ```python
  sortedList = sorted(ListofTuples, key=lambda tup: tup[n])
  ```
  Instead of:
  ```python
  def sortby(somelist, n):
      nlist = [(x[n], x) for x in somelist]
      nlist.sort()
      return [val for (key, val) in nlist]
  ```

#### 8. Read [this](https://wiki.python.org/moin/PythonSpeed/PerformanceTips) for more tips

---


## <a name='intro'></a> A General Introduction to Some Important Things
* Lexos back-end is build with python and `Flask`. `Flask` lib in python enables us to interact with the web requests.

### Crucial Variable

* `request`: a variable that has web request information
    * `request.method`: return methods of the request, `post` or `get` in this case
    * `request.form`: return a Dict containing the id of the request map to the value of the request
    * `request.form.getlist`: return a Dict containing the id of the request map to the multiple values of the request (only if there is more than 1 value)
    * `request.file`: return a Dict containing the id of the request map to the value of the request (only if the request value is a file)

* `session`: a cookie that can be shared with the browser and the back-end code
    * This is used to cache users options and information, also send the default information (which is in `constant.py`) to the front-end
    * This variable works like a Dict
    * It will not be renewed unless you call `session_function.init`, so we use it to keep users' options on the GUI
    * This variable can be accessed both in the front-end and the back-end, so we sometimes use it to send information to the front-end.

### File Structure

* All the files are stored in `/tmp/Lexos/`. In order to simplify the file monitoring process, you might want to clear this folder frequently.
* Inside `/tmp/Lexos/`, there are workspace files (`.lexos` file) and the `session folder` (the folder with a random string as its name)
* Workspace file is generated whenever people click `download workspace`
* Inside the `session folder`, there are at most 3 files:
    * `filemanager.p`: the file that containing pickeled [FileManager](#filemanager) in this way we can save and load (with `utility.loadFileManager` and `utility.saveFileManager`)
    FileManager when every user send a request
    * `filecontents/`: the folder containing all the user uploaded file
    * `analysis_results/`: the folder containing all the result that user need to [download](#download) (For example, the CSV, Rolling Window graph and etc.)

### The Magic
* This section introduce how the front end and backend interact

* <a name='intro'></a> Download
    1. Create a file that the user want to download in a path, and save the path in a variable, for example `SavePath`
    2. Return `SavePath` to `lexos.py`
    3. Use `return send_file(SavePath, attachment_filename=filename, as_attachment=True)` to send file to the user
    4. See the `topword`, `tokenizer` or `rollingwindow` function in `lexos.py` for detail

* Render template
    1. First in the backend produce the result, for example I have 2 variable I want to send to the front end `labels` and `results`
    2. Send to the front-end by `return render_template(front-end.html, labels=labels, result=result)`
    3. Then in `front-end.html` there will be [jinja](http://jinja.pocoo.org/docs/dev/templates/) code that can call `labels` and `result`
    4. The jinja will finish the html and send the page to the user.

* Session
    1. As we talked before, session is the variable that can be accessed both on the front-end and back-end
    2. Session can be called in front end as a jinja variable.
    3. Session are ONLY used to cache user's option, do not cache any other thing in it.

---


## <a name='std'></a> Back-end Program Structure and Programming Standards

* Notice Lexos project is not completely following this guide for now.


### description of trivial stuff for the back-end (optional reading):

* `templates/`: the folder contain all the html file

* `static/`: the folder contain all the javascript, image, CSS that are needed in the GUI

* `TestSuite/`: the folder contain all the testing file we use on Lexos.

* `0_InstallGuide/`: the folder with all the install guide. (this is for user, including pdf and docx version)

* `gitignore`: the file specifies intentionally untracked files to ignore

* `LICENSE`: just a [MIT license](http://opensource.org/licenses/MIT)

* `BackendProgrammingGuide.md`: this file. (^_^)

### description of the files that are useful and the file structure

#### 1. `/lexos.py`

* Description: the file that is used to connect the file with the front end

* Calling map:

```
lexos.py -> managers/utility.py (used to save and load file manager, and use to get to push to the front-end)
         -> managers/file_manager.py (mainly used to get labels)
         -> managers/session_manager.py (used to load default, and cache options)
         -> helpers/* (these files can be accessed through out the whole project)
```

* Programming workflow:
    1. load filemanager
    2. load variable (usually loading labels. If there is other variable need to be load, write a function to load them)
    3. split request
        * 'GET' request
            1. apply default setting to the `session`
            2. get result(optional, usually we don't need to get result in 'GET' request)
            3. render_template
        * 'POST' request (sometime we need to use `if` `else` to handle 'POST', because we need to render different template, example see `topword()`)
            1. get result
            2. turn result into display form (generally handle something like generate preview of the result) or save the result in a file (for download) (optional)
            3. savefilemanager (optional)
            4. cache session
            5. render_template or send_file

* programming workflow example:

use `topword()` as example: with prop-z test for class and download file
```python
# load filemanager
fileManager = managers.utility.loadFileManager()

# load variable (usually loading labels. If there is other variable need to be load, write a function to load them)
labels = fileManager.getActiveLabels()

# split request ('GET')
if request.method == 'GET':

    # apply default setting to the `session`
    if 'topwordoption' not in session:
        session['topwordoption'] = constants.DEFAULT_TOPWORD_OPTIONS
    if 'analyoption' not in session:
        session['analyoption'] = constants.DEFAULT_ANALIZE_OPTIONS

    # get result(optional, usually we don't need to get result in 'GET' request)
    ClassdivisionMap = fileManager.getClassDivisionMap()[1:]

    # error handlation
    if ClassdivisionMap != [] and len(ClassdivisionMap[0]) == 1:
        session['topwordoption']['testMethodType'] = 'pz'
        session['topwordoption']['testInput'] = 'useAll'

    # render_template
    return render_template('topword.html', labels=labels, classmap=ClassdivisionMap, topwordsgenerated='class_div')

# split request ('POST')
if request.method == "POST":

    # get result
    result = utility.GenerateZTestTopWord(fileManager)  # get the topword test result

    # turn result into display form (generally handle something like generate preview of the result) or save the result in a file (for download) (optional)
    path = utility.getTopWordCSV(result, 'pzClass')

    # not saving filemanager

    # cache session
    session_functions.cacheAnalysisOption()
    session_functions.cacheTopwordOptions()

    # render_template or send_file
    return send_file(path, attachment_filename=constants.TOPWORD_CSV_FILE_NAME, as_attachment=True)
```

* special comment:
    * in `lexos.py` there should not be any complicated statement, general rule of thumb is that there should be no nested loop or if.
    because this file is used to just send information to the front end. if you need to use a complicated statement, add a function somewhere else.

#### 2.`managers/utility.py`

* Description: there are 3 type of function in this file:
    * the function load request from remote, and turn them into the option that processor can understand
        * for example `getTopWordOption()`
    * the function that is used to combine all the information together to give a result that can send to the front end
        * for example `GenerateZTestTopWord(filemanager)`
    * other functions: (those does not have a good place in this project)
        * `saveFileManager()`, `loadFileManager()`

* Calling map:

```
utility.py -> file_manager.py (used to get file informations. be cautious if you want to change lexos_file information)
           -> session_manager.py (used to get the session_folder only)
           -> processor/* (used to do calculation)
           -> helpers/* (these files can be accessed through out the whole project)
```

* Programming workflow:
    * get remote option function
        1. none
    * other function
        1. none
    * the function that is used to combine all the information together to give a result that can send to the front end
        0. not none! (surprise!)
        1. get remote option: either call the corresponding get remote option function or write it inside this function
        2. load the local content from `file_manager.py`
        3. convert the data into the data structure that processor can understand (optional)
        4. send the data to the processor and get result
        5. combine other information together with the data structure (optional, for example file names, labels and so on)

* programming workflow example

this code is from `GenerateZTestTopWord(filemanager)` test for class branch
```python

# get remote option: either call the corresponding get remote option function or write it inside this function (call get remote function)
testbyClass, option, Low, High = getTopWordOption()


# load the local content from `file_manager.py`
ngramSize, useWordTokens, useFreq, useTfidf, normOption, greyWord, showDeleted, onlyCharGramsWithinWords, MFW, culling = filemanager.getMatrixOptions()

countMatrix = filemanager.getMatrix(useWordTokens=useWordTokens, useTfidf=False, normOption=normOption,
                                    onlyCharGramsWithinWords=onlyCharGramsWithinWords, ngramSize=ngramSize,
                                    useFreq=False, greyWord=greyWord, showGreyWord=showDeleted, MFW=MFW,
                                    cull=culling)


# convert the data into the data structure that processor can understand (optional)
WordLists = matrixtodict(countMatrix)


# send the data to the processor and get result
analysisResult = testall(WordLists, option=option, Low=Low, High=High)


# combine other information together with the data structure (optional) stick the temp label in front of the data
humanResult = [[countMatrix[i + 1][0], analysisResult[i]] for i in range(len(analysisResult))]


# return
return humanResult
```

* special comment:
    * in this file we should only handle data structure transformation, not calculation (calculation is handled in `/processors/*`)
    * if a function don't need to get `request` and don't need to call `fileManager`, this function does not belong in this file.
    * if a function are doing intense math and calculation, this function does not be in this file. (calculation is handled in `/processors/*`)





