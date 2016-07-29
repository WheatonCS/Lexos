#!/bin/bash
echo "Python is warming up..."
cd ~/Lexos-master

osascript -e 'tell application "Terminal" to do script "$HOME/anaconda2/bin/python ~/Lexos-master/lexos.py"'
sleep 6

# Detect user browser
open 'http://localhost:5000'
