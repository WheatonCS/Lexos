#!/bin/sh

echo Installer Version 1.1 — Mac 64-bit
    
# Additional Package Requirements
    declare -r requirementsPath=~/Lexos-master/requirement.txt

# Lexos-URL
    declare -r lexosURL=https://github.com/WheatonCS/Lexos/archive/master.zip
    
# Anaconda-URL: Mac 64-bit
    declare -r pythAddress=https://repo.continuum.io/archive/Anaconda2-4.0.0-MacOSX-x86_64.sh

# Temp Anaconda Download Path
    declare -r pythDownPath=/tmp/Anaconda2-4.0.0-MacOSX-x86_64.sh

#----------------------------------------------------------------------------------------------

# Identify Computer
    echo Trying to identify your computer...   
    declare bitCount=0
    bitCount=$(getconf LONG_BIT)

    if [ $bitCount != 0 ]; then
        echo Success--This computer is $bitCount bits
    else
        echo failure... bit count undefined
    fi
    
# Verify URL Constants
    echo Verifying Anaconda URL...
    curl -s --head $pythAddress | head -n 1 | grep "HTTP/1.[01] [23].." > /dev/null
    # on success (page exists), $? will be 0; on failure (page does not exist or
    # is unreachable), $? will be 1
    if [ $? == 1 ]; then
        echo failed to reach $pythAddress 
    else
        echo Success — Anaconda URL contacted
    fi

    echo Verifying Lexos URL…
    curl -s --head $lexosURL | head -n 1 | grep "HTTP/1.[01] [23].." > /dev/null
    # on success (page exists), $? will be 0; on failure (page does not exist or
    # is unreachable), $? will be 1
    if [ $? == 1 ]; then
        echo failed to reach $lexosURL
    else
        echo Success — Lexos URL contacted
    fi

# File Transfer
    echo Beginning download...
    curl -k $pythAddress --output $pythDownPath

# Begin Installation process
    bash $pythDownPath -b
    
# Lexos-master download and unpack
    curl -Lk $lexosURL --output /tmp/master.zip
    unzip /tmp/master.zip -d ~/
    
# Install additional packages (Mac and Linux)
    ~/anaconda2/bin/pip install -r $requirementsPath
    
# Exit message
    echo Lexos installer has completed successfully.
    echo You may now exit this window and use the "RUN.command" to launch Lexos
    echo (if the site does not load immediately refresh the web page)


$SHELL
