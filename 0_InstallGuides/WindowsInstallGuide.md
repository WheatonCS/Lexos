# Windows Install Guide

## Overview:
1. Install Python and Anaconda
2. Install additional packages
3. Download and extract Lexos
4. Navigate to the correct directory and run Lexos

## 1. Install Python and Anaconda
To run Lexos locally on your own personal computer you will first need to install Python, the programming language Lexos is written in, as well as a few additional libraries which cover the more advanced visual and computational functionality.  So first off we need to install a distribution of Python called Anaconda which can be located here:
* [http://continuum.io/downloads](http://continuum.io/downloads)

Download the correct version of Python 2.7 for your machine and then launch the installer exe when it is complete.  Follow the install guide, the install location is not important; however, make sure that you leave the option to 'Update the PATH variable' checked so that later on when you type 
	“python nameOfFile.py” into the terminal, it knows that you specifically want to use the Anaconda distribution, this prevents any confusion if you already have a different version of Python installed.  Finally, hit continue and install Anaconda.

## 2.  Install additional packages
Now Anaconda has been installed we can verify that we installed it correctly and then install the two additional packages we need to run Lexos. Open your command prompt.  (If you are unfamiliar with how to access the command prompt hit [WindowsKey] + [R] to bring up the Run box and type “cmd.exe” into the text field and hit enter)  First we want to verify that Anaconda is installed so type 
“python -V” into the command line and hit enter.  You should see a response that looks like this: “Python 2.7.10 :: Anaconda 2.2.0 (64-bit)”  if you do not see :: Anaconda 2.2.0 then you did not update your PATH variable and so you should reinstall Anaconda correctly.  If you did, then you are ok to begin installing the addition required packages.  First though, you'll need to make sure that your package installer command is up to date so type “pip install -U pip” and hit enter.  Your terminal should display some information showing you the update process, once that is completed you can now use 'pip' the python package installer.  So type “pip install gensim” to install the first package and then “pip install chardet” to install the second one.  Now you are almost ready to run Lexos on your personal computer.

## 3. Download and extract Lexos

Go to the Lexos [GitHub page](https://github.com/WheatonCS/Lexos) and at the bottom of the right-side navigation bar you will see a button to “Download ZIP”. Click this button to download a zipped file which contains the filefolder which holds all the necessary source code for Lexos.  Extract the contents of the .ZIP file to your Desktop, if you want you can change the name of the containing folder from Lexos-master to just Lexos, but be sure to use the name you choose when in the command line.

## 4. Navigate to the correct directory and run Lexos
Now you have everything ready.  Python has been sucessfully installed, all of the required packages are ready, and you have the code for Lexos downloaded and uncompressed and ready to be run.  So open a new command prompt and use the CD command to navigate inside the Lexos-master folder.  If it is on your desktop you should be able to type “cd Desktop\Lexos-master”.  (If you need additional information on file navigation, check out this article by wikihow http://www.wikihow.com/Change-Directories-in-Command-Prompt)  After you have arrived at the Lexos folder, you are ready to run the program by typing “python lexos.py” and hitting enter.  It may take a minute the first time you run the command because python has to reconfigure some of the project files for your computer, but shortly after you should see a message in the command prompt that says:
	Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
	Restarting with stat

Lexos in now running on your computer! But where is it?  To interact with the program you will need to open your favorite web browser and in the address bar type “localhost:5000” and hit enter (or click [here](http://localhost:5000).  Because your computer is acting as both the server and the user of Lexos, you may need to hit the Reset button in the top right corner of the Upload/home page to make sure files from previous sessions do not get confused.  

To quit Lexos simply close the command prompt window that it is running in.  And to update simply re-download the Lexos zipped file from github and use it to replace the files on your desktop. 

Thank you for using Lexos.
