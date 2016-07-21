#!/bin/sh

echo Updater Version 1.0 — Mac 64-bit

# Lexos-URL
    declare -r lexosURL=https://github.com/WheatonCS/Lexos/archive/master.zip
    
# Lexos-master download and unpack
    curl -Lk $lexosURL --output /tmp/master.zip
    unzip -o /tmp/master.zip -d ~/


$SHELL
