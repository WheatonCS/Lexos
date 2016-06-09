#!/bin/bash  
echo "Python is warming up..."
export PATH="/home/testacct/anaconda2/bin:$PATH"
cd /home/$USER/Lexos-master
python lexos.py
$SHELL
