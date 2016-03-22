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
* This guide assumes you know basic web structure and Python (if you find this hard to read, stop and go [here](http://www.codecademy.com/en/tracks/python))

---


## <a name='tip'></a> Helpful Tips
#### 1. Read the `constant.py` and `general_function.py` in the `helpers` folder before you do anything real, so that you don't reinvent the wheel.
#### 2. Play with the `join` and `split` functions before you deal with strings. Small changes
in the use of these functions can make a significant difference in runtime efficiency.

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
To create a comma-separated-value (csv) file:
```python
rows = [','.join[row] for row in matrix]
csv = '\n'.join[rows]
```

#### 3. Play with the `filter` `map` function, the `*` operator, and in-line `for` loops before you deal with Lists

  For example use:
```python
list = map(lambda element: element[:50], list)
```
  Instead of:
```python
for i in range(len(list)):
  list[i] = list[i][:50]
```

When you initialize the list, use `*` rather than a `for` loop:

This is not used that often

For example use:
```python
empty_list = [0] * Len_list
```
Instead of:
```python
emptyMatrix = []
for _ in LenMatrix:
  emptyMatrix.append(0)
```

#### 4. Use `try`, `except` rather than `if` when you are dealing with Python dictionaries.

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


#### 5. Using `except` to do complicated jobs; as a general rule, specify the error type (`KeyError`, `ValueError`, etc.) explicitly when using except.

#### 6. When working with matrices, use `np.array` or `dict` instead of a Python list.

(Note to self: our current code uses Python arrays in a number of places; we need to fix that)
  
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

  Read [this tutorial](http://wiki.scipy.org/Tentative_NumPy_Tutorial) for more info.

#### 7. Use `lambda` to create a temporary function

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
sortedList = sortby(ListofTuples, n)
```

#### 8. Read [this](https://wiki.python.org/moin/PythonSpeed/PerformanceTips) for more tips.

---


## <a name='intro'></a> A General Introduction to Some Important Things
* The Lexos back-end is built with Python and `Flask`, a microframework. The `Flask` library in Python enables us to interact with web requests.

### Two Crucial Variables

* `request`: a variable that has web request information
    * `request.method`: return methods of the request, `post` or `get` in this case
    * `request.form`: return a Dict containing the id of the request map to the value of the request
    * `request.form.getlist`: return a Dict containing the id of the request map to the multiple values of the request (only if there is more than 1 value)
    * `request.file`: return a Dict containing the id of the request map to the value of the request (only if the request value is a file)

* `session`: a cookie that can be shared with the browser and the back-end code
    * This is used to cache users options and information, also sends the default information (which is in `constant.py`) to the front-end
    * This variable works like a Dict
    * It will not be renewed unless you call `session_function.init()`; we use it to keep users' options on the Graphical User's Interface (GUI)
    * This variable can be accessed both in the front-end and the back-end, so we sometimes use it to send information to the front-end.

### File Structure

* Any files upload and/or created during a session are presently stored in `/tmp/Lexos/`. In order to simplify the file monitoring process, you might want to clear this folder frequently
* Inside `/tmp/Lexos/`, there are workspace files (`.lexos` file) and the `session folder` (the folder with a random string as its name since each session is stored in its own folder)
* A Workspace file is generated whenever a user clicks `Download Workspace` (presently at the top of the GUI).
* Inside the `session folder`, there are at most 3 files:
    * `filemanager.py`: the file that contains the [FileManager](#filemanager) as 
pickeled information of the files in the current session, including files that have cut into segments. 
In this way we can save and load (with `utility.loadFileManager` and `utility.saveFileManager`)
    * `filecontents/`: the folder containing all the user's uploaded files
    * `analysis_results/`: the folder containing all the results that a user needed to [download](#download) (for example, a .csv document-term matrix, a Rolling Window graph, etc.)

### The Front-end to Back-end Magic
* This section introduces how the front-end and back-end interact.

* <a name='intro'></a> Download
    1. Create a file that the user wants to download in a path, and save the path in a variable, for example `SavePath`
    2. Return `SavePath` to `lexos.py`
    3. Use `return send_file(SavePath, attachment_filename=filename, as_attachment=True)` to send a file to the user
    4. See the `topword`, `tokenizer` and/or `rollingwindow` functions in `lexos.py` for detail

* Render template
    1. First in the back-end produce the requested result; for example, assume I have 2 variables I want to send to the front-end: `labels` and `results`
    2. Send to the front-end by `return render_template(front-end.html, labels=labels, result=result)`
    3. Then in `front-end.html` there will be [Jinja](http://jinja.pocoo.org/docs/dev/templates/) code that can make use of `labels` and `result`
    4. The Jinja will complete (fill-in) the html and send the page to the user.

* Session
    1. As we noted before, session is the variable that can be accessed both on the front-end and back-end
    2. Session can be called in the front-end as a Jinja variable.
    3. Session is ONLY used to cache a user's option(s); do not cache anything else in it.

---


## <a name='std'></a> The Back-end Program Structure and Programming Standards

* Note: the Lexos project is not completely following this guide at this time.


### A description of trivial stuff for the back-end (optional reading):

* `templates/`: the folder contain all the html files

* `static/`: the folder contain all the javascript, images, and CSS that are needed in the GUI

* `TestSuite/`: the folder containing a set of (benchmark) tests we use on Lexos.

* `0_InstallGuide/`: the folder containing installation directions if you are installing Lexos locally (rather than using the web-based app). 

* `gitignore`: the file specifies intentionally untracked files to ignore

* `LICENSE`: a [MIT license](http://opensource.org/licenses/MIT)

* `BackendProgrammingGuide.md`: this file. (^_^)

### A description of the files that are used when working with Lexos software, as well as the file structure encountered

#### 1. `/lexos.py`

* Description: the file that is used to connect the file with the front end

* Calling map:

```
lexos.py -> managers/utility.py (used to save and load the filemanager and push info to the front-end)
         -> managers/file_manager.py (mainly used to get labels)
         -> managers/session_manager.py (used to load the default and cached options)
         -> helpers/* (these files can be accessed throughout the entire project)
```

* Programming workflow:
    1. load filemanager
    2. load variable (usually loading labels. If there are other variables to load, write a function to load them)
    3. split request
        * 'GET' request
            1. apply the default setting to the `session`
            2. get result(optional, usually we don't need to get the result in a 'GET' request)
            3. render_template
        * 'POST' request (sometimes we need to use `if` `else` to handle 'POST', because we need to render different templates, for example see `topword()`)
            1. get the calculation result
            2. turn result into display form (generally handles something like generating a preview of the result) or save the result in a file (for download) (optional)
            3. savefilemanager (only when the file manager is changed)
            4. cache session
            5. render_template or send_file

* programming workflow example:

The following uses the Analysis tool `topword()` as an example: Download the file branch of prop-z test for class branch
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
    session_manager.cacheAnalysisOption()
    session_manager.cacheTopwordOptions()

    # render_template or send_file
    return send_file(path, attachment_filename=constants.TOPWORD_CSV_FILE_NAME, as_attachment=True)
```

* special comment:
    * in `lexos.py` we recommend you avoid including complicated statements; a general rule of thumb is that there should be no nested `loop` or `if` statements because this file is used to just send information to the front-end. If you need to use a complicated statement, add a function somewhere else.

#### 2.`managers/utility.py`

* Description: there are 3 type of functions in this file:
    * the function loads a request remotely, and turns them into the option that the processor can understand
        * for example `getTopWordOption()`
    * the function that is used to combine all the information together to give a result that can be sent to the front-end
        * for example `GenerateZTestTopWord(filemanager)`
    * other functions: 
        * `saveFileManager()`, `loadFileManager()`

* Calling map:

```
utility.py -> file_manager.py (used to get file information. Be cautious when changing lexos_file information)
           -> session_manager.py (used to get the session_folder only)
           -> processor/* (used to do calculations)
           -> helpers/* (these files can be accessed throughout the entire project)
```

* Programming workflow:
    * get remote option function
        1. none
    * other function
        1. none
    * the function that is used to combine all the information together to give a result that can send to the front-end
        0. not none! (surprise!)
        1. get remote option: either call the corresponding get remote option function or write it inside this function
        2. load the local content from `file_manager.py`
        3. convert the data into the data structure that the processor can understand (optional)
        4. send the data to the processor and get result(s)
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


# combine other information together with the data structure (optional)
# stick the temp label in front of the data
humanResult = [[countMatrix[i + 1][0], analysisResult[i]] for i in range(len(analysisResult))]


# return
return humanResult
```

* special comment:
    * in this file we should only handle data structure transformation, not calculations (calculation is handled in `/processors/*`)
    * if a function doesn't need to get `request` and doesn't need to call `fileManager`, this function does not belong in this file.
    * if a function is doing intense math and calculation, this function does not belong in this file. (calculation is handled in `/processors/*`)

#### 3. `session_manager.py`

* Description: the file that is used to edit, save, load, and initiate a session.

* Calling map:

```
session_manager.py -> helpers/* (these files can be accessed throughout the whole project)
```

* programming workflow:
    * cache functions:
        * cache functions have 4 types of options that we need to cache:
            * box (check box)
            * input (radio button and input box)
            * list (multiple requests with the same name, for example, in the word cloud select document section all requests have the name: `'segmentlist'`)
            * files (this is complicated; for now, we only cache filenames, see `cacheMultiCloudOptions()` for more information)
    * other functions
        * these functions are (pretty) stable; do not add or change them unless absolutely necessary
    * load default function:
        * let the session load the default options on a page when you first go into that page
        * Note: THIS DOES NOT EXISTS IN THE PROJECT YET

* programming workflow example
    * for example you need to cache the option for `lalala`, because we just decide to name our new feature `lalala`, and everyone loved this name :)

`helpers/constant.py`:

```python
# these are the names of the requests that you want to cache:
LALALAINPUT = ('input1', 'input2')
LALALALIST = ('list1',)  # make sure you have the ending ',' when you only have one element
LALALAFILE = ('file1', 'file2')
LALALABOX = ('box1', 'box2', 'box3', 'box4', 'box5', 'box6', 'god!-we-really-have-lot-of-boxes')

# those are the default options that will show on the page; you should add the defualt even if you are not caching it
# input and file are mapped to a string
# boxes map to a boolean value to indicate whether that is checked
# lists map to a list
DEFAULT_LALALA_OPTION = {'input1': 'the-default-of-input1', 'input2': 'the-default-of-input2',
'box1': True, 'box2': True, 'box3': True, 'box4': True, 'box5': False, 'box6': False, 'god!-we-really-have-lot-of-boxes': False
,'list1': [], 'file1': '', 'file2': '',
'this-is-the-option-that-I-do-not-want-to-cache': 'lalalahahaha', 'this-is-another-option-that-I-do-not-want-to-cache': False}
```

`managers/session_manager.py`:

```python
# caching the input
for input in constants.MULTICLOUDINPUTS:
        session['lalalaoptions'][input] = (
            request.form[input] if input in request.form else constants.DEFUALT_LALALA_OPTION[input])

# caching the list
for list in constants.CLOUDLIST:
        session['lalalaoption'][list] = request.form.getlist(list)

# caching check boxs
for box in constants.RWBOXES:
    session['lalalaoptions'][box] = (box in request.form)

# caching the filename
for file in constants.MULTICLOUDFILES:
    filePointer = (request.files[file] if file in request.files else constants.DEFUALT_LALALA_OPTION[file])
    topicstring = str(filePointer)
    topicstring = re.search(r"'(.*?)'", topicstring)
    filename = topicstring.group(1)
    if filename != '':
        session['lalalaoptions'][file] = filename
```

`template/lalala.html`:
```html
<!-- inputs radio button -->
<label>input1 option1<input type="radio" name="input1" value="option1" {{ 'checked' if session['lalalaoptions']['input1'] == 'option1' }}/></label>

<!-- inputs input box -->
<input type="number" name="input2" id="max_iter" min="1" step="1" value="{{ session['lalalaoptions']['input2'] }}" />

<!-- check box -->
<label> box1 <input type="checkbox" name="box1" {{ 'checked' if  session['lalalaoptions']["box1"] }}/> </label>

<!-- list -->
{% for fileID, label in labels.items() %}
    <label>{{label}}
        <input type="checkbox" name="list1" class="lalalalist" {{ 'checked' if fileID|unicode in session['lalalaoptions']['list1']}} id="{{fileID}}_selector" value="{{fileID}}">
    </label>
{%- endfor %}

<!-- file (name) -->
<input type="file" id="lalalafile1" name="file1"/>
<div class="lalalafileclass" id="lalalafileid" name="">{{ session['lalalaoptions']['file1']}}</div>
```

* special comment
    * do not add any strings or numbers in the caching function; put all of them in constant.py (as shown above)
    * for caching functions, you don't usually get all 4 type of options, just write what you need.


#### 4. `file_manager.py` and `lexos_file.py`

* description
    * `file_manager.py` deal with the local file accessing and editing
    * `lexos_file.py` is a class that represents a file inside the Lexos program. It has class label, active or not, and other properties

* calling map
```
file_manager.py -> lexos_file.py
                -> session_managers.py (for session_folder only)
                -> helpers/*

lexos_file.py -> session_managers.py (for session_folder only)
              -> helpers/*
```

* special comment
    * these two files are functioning in a (relatively) stable fashion and these two classes can handle any thing we need on the file side.
    * do not edit these two files unless you have to.
    * do not access the method and property of `LexosFile` outside of `file_manager.py`
    * the processor should not be accessed in `lexos_file.py` (for now, cut and scrub)


#### 5. `helpers/constant.py`

* special comment
    * all the filenames and directories should be constant
    * all the numbers should be in constant
    * all the caching and default options in the session should be in constant (see `mananagers/session_manger.py` for more info)

#### 6. `processors/*`

* special comment
    * this includes some of the more intense Python and "math land"
    * comment the code as you are write 
    * PLEASE do not write ugly code here, think before you begin; re-read when you finish.

