#!/bin/bash

declare -r LexosCoreCommandFile=~/.lexos_core.command

echo "Python is warming up..."
cd ~/Lexos-master
echo $HOME/anaconda2/bin/python lexos.py > $LexosCoreCommandFile
chmod +x $LexosCoreCommandFile
open $LexosCoreCommandFile


sleep 3

# Detect user browser
open 'http://localhost:5000'

# clean up
rm -f $LexosCoreCommandFile
