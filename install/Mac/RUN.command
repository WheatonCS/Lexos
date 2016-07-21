#!/bin/bash
echo "Python is warming up..."
cd ~/Lexos-master
$HOME/anaconda2/bin/python lexos.py &

sleep 3

# Detect user browser
open 'http://localhost:5000'
