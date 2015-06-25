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
  sortedList = sorted(ListofTuples, key=lambda tup: tup[1])
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
    * `filemanager.p`: the file that containing pickeled [FileManager](#filemanager) in this way we can save and load (with `session_function.loadFileManager` and `session_function.saveFileManager`)
    FileManager when every user send a request
    * `filecontents/`: the folder containing all the user uploaded file
    * `analysis_results/`: the folder containing all the result that user need to [download](#download) (For example, the CSV, Rolling Window graph and etc.)

### The Magic
* This section introduce how the front end and backend interact

* <a name='intro'></a> Download
    1. Create that a user want to download in a path, and save the path in a variable, for example `SavePath`
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
