#!/bin/bash  
declare location=$(pwd)        
echo Getting ready to uninstall
if cd /home/$USER; then
    rm -rf ~/anaconda2
    rm -rf ~/Lexos-master
fi

cd
if [ -e ~/Downloads/Anaconda2-4.0.0-Linux-x86_64.sh ]; then
    rm -rf ~/Downloads/Anaconda2-4.0.0-Linux-x86_64.sh
fi
cd $location
echo uninstall completed successfully
$SHELL
