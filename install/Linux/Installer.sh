#!/bin/bash          
echo Welcome to easy installer! This is a work in progress!
echo As of version 1.0 the installer works with 32 and 64 bit linux

# Text Editor
    declare -r textEditor=gedit

#Lexos-URL
    declare -r lexosURL=https://github.com/WheatonCS/Lexos/archive/master.zip

# Linux
    #64 bit
    declare -r pythAddress64=https://repo.continuum.io/archive/Anaconda2-4.0.0-Linux-x86_64.sh
    declare -r pythDownPath64=/tmp/Anaconda2-4.0.0-Linux-x86_64.sh
    
    #32 bit
    declare -r pythAddress32=https://repo.continuum.io/archive/Anaconda2-4.0.0-Linux-x86.sh
    declare -r pythDownPath32=/tmp/Anaconda2-4.0.0-Linux-x86.sh
    
# Mac
    #64 bit
    #declare -r pyth64Address=https://repo.continuum.io/archive/Anaconda2-4.0.0-MacOSX-x86_64.sh

#----------------------------------------------------------------------------------------------

# Identify Computer
    #Mac command for identifying 64 bit
    #64bool=$(sysctl hw |grep 64bit)
    echo Trying to identify your computer...   
    declare bitCount=0
    bitCount=$(getconf LONG_BIT)

    if [ $bitCount != 0 ]; then
        echo Success--This computer is $bitCount bits
    else
        echo failure... bit count undefined
    fi
    
    # choose URL depending on 32 or 64 bit systems 
    if [ $bitCount == 64 ]; then
        declare -r pythAddress=$pythAddress64
        declare -r pythDownPath=$pythDownPath64
	echo $pythDownPath
    elif [ $bitCount == 32 ]; then
        declare -r pythAddress=$pythAddress32
        declare -r pythDownPath=$pythDownPath32
    fi

# Verify URL Constants
    echo Verifying URL...
    curl -s --head $pythAddress | head -n 1 | grep "HTTP/1.[01] [23].." > /dev/null
    # on success (page exists), $? will be 0; on failure (page does not exist or
    # is unreachable), $? will be 1
    if [ $? == 1 ]; then
        echo failed to reach $pythAddress 
    else
        echo Success--URL contacted
    fi

# File Transfer
    echo Beginning download...
    # Works on linux and mac
    curl -k $pythAddress --output $pythDownPath

    #Works on linux and mac, uses mac url for 64 bit
    
# Pop-Up Instruction window
    #> /tmp/Instructions.txt #create new file
    #echo "Install Instructions:" >> ./tmp/Instructions.txt
    #echo "  1) " >> ./tmp/Instructions.txt
    #$textEditor Instructions.txt

# Begin Installation process
    #Linux execute command
    bash $pythDownPath -b

    #Mac execute command
    #bash /home/lexos/Desktop/TESTING/Anaconda2-4.0.0-MacOSX-x86_64.sh

# Install additional packages (Mac and Linux)
    ~/anaconda2/bin/pip install -U pip
    ~/anaconda2/bin/pip install gensim
    ~/anaconda2/bin/pip install chardet
    ~/anaconda2/bin/pip install natsort
    
    #exec ./home/$USER/Desktop/aux.sh

# Install Git && Clone Repository
    #Mac
    #brew install hub

    #Linux
    wget $lexosURL -O /tmp/master.zip
    unzip /tmp/master.zip -d ~/
    #sudo apt-get install git-all
    #curl -k $lexosURL --output ~/
    #cd; git clone https://github.com/WheatonCS/Lexos.git
    #cd Lexos/

$SHELL
