# Back-end programming guide for Lexos


## <a name='overview'></a> Overview
* [Overview](#overview)
* [What is this?](#this)
* [Helpful tips](#tip)
* [general introduction of the backend](#intro)
* [Back-end structure and programming standards](#std)


## <a name='this'></a> What is this?
* This is the backend programming guide for Lexos programmers.
* You should read this before you start programming for the back-end in Lexos
* In this we will see more helpful tips and the standard for backend programming
* This guide assume you know basic web structure.
* This guide assume you know about python, if you find this hard to read, stop and go [here](http://www.codecademy.com/en/tracks/python)


## <a name='tip'></a> helpful tips
* read the ````constant.py```` and ````general_function.py```` in ````helpers```` folder before you do anything real, so that you don't reinvent the wheel.
* play with ````join```` and ````split```` function before you want to deal with strings

for example use
```python
str = ''.join[list]
```
in stead of
```python
str = ''
for element in list:
    str += element
```

use:
```python
rows = [','.join[row] for row in matrix]
csv = '\n'.join[rows]
```
to create a csv

* play with ````filter```` ````map```` function, ````*```` and in-line ````for```` loop before you want to deal with Lists

for example use:
```python
map(lambda element: element[:50], list)
```
instead of:
```python
for i in range(len(list)):
    list[i] = list[i][:50]
```

when you initialize the list, use ````*```` instead of a ````for```` loop:

use:
```python
emptyMatrix = [[]] * LenMatrix
```
instead of
```python
emptyMatrix = []
for _ in LenMatrix:
    emptyMatrix.append([])
```

* use ````try````, ````except```` instead of ````if```` when you are dealing with Dicts.

for example use:
```python
try:
    dict[i] += 1
except KeyError:
    dict[i] = 1
```
instead of:
```python
if i in dict:
    dict[i] += 1
else:
    dict[i] = 1
```

use:
```python
try:
    os.makedir(path)
except:
    pass
```
instead of:
```python
if os.path.isdir(path)
    pass
else:
    os.makedir(path)
```

this is both clearer and faster

* When you use ````except```` always specify the error type (````KeyError````, ````ValueError````, ect.) you want to except.

* when encounter Matrix, use ```np.array``` or ````dict```` instead of python List. (current program has python array all over the place, we need to fix that)

* read [this](https://wiki.python.org/moin/PythonSpeed/PerformanceTips) for more tips


## <a name='intro'></a> general introduction to the structure of backend
* Lexos backend is build with python and flask. flask lib in python enable us to interact with the web requests.

### crucial variable

* ```requset```: a variable that has web request information.

1. ````request.method````: return the method of the request, ````post```` or ````get```` in this case

2. ````request.form````: return a dict of the id of the request map to the value of the request

3. ````request.form.getlist````: returns a dict that contain id of the request map to the multiple values of the request (only if there is more than 1 values)

4. ````request.file````: return the a dict that contain id of the request map to the value of the request (only if the request value is a file)

* ````session````: a cookie that can be shared with the browser and the backend code:

1. this is used to cache users option and information.

2. this variable works pretty much like a dict

3. will not be renewed unless you call ````session_function.init````, so we use this to keep the users option on the GUI


## <a name='std'></a> Back-end structure and programming standards