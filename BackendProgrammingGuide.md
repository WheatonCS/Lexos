# Back-end programming guide for Lexos


## Overview
* Overview
* What is this?
* Helpful tips
* general introduction of the backend
* Back-end structure and programming standards


## What is this?
* This is the backend programming guide for Lexos programmers.
* You should read this before you start programming for the back-end in Lexos
* In this we will see more helpful tips and the standard for backend programming
* This guide assume you know basic web structure.
* This guide assume you know about python, if you find this hard to read, stop and go [here](http://www.codecademy.com/en/tracks/python)


## helpful tips
* read the ````constant.py```` and ````general_function.py```` in ````helpers```` folder before you do anything real, so that you don't rebuilding the wheel
* play with ````join```` and ````split```` function before you want to deal with strings
* play with ````filter```` ````map```` function and in-line ````for```` loop before you want to deal with Lists
* use ````try````, ````except```` instead of ````if```` when you are dealing with Dicts.

for example use:
```
try:
    dict[i] += 1
except KeyError:
    dict[i] = 1
```
instead of:
```
if i in dict:
    dict[i] += 1
else:
    dict[i] = 1
```
this is more clear and fast

*


## general introduction to the structure of backend
* Lexos backend is build with python and flask. flask lib in python enable us to interact with the web requests.

### crucial variable

```requset```: a variable that has web request information.
1. ````request.method````: return the method of the request, ````post```` or ````get```` in this case
2. ````request.form````: return a dict of the id of the request map to the value of the request
3.
