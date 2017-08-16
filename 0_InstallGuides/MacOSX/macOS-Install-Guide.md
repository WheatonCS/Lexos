# macOS Manual Installation Guide

## Overview:

1. [About *Lexos*](#about)
2. [Installing Python and Anaconda](#installing-anaconda)
3. [Installing Additional Packages](#installing-packages)
4. [Downloading and Extracting _Lexos_](#downloading-lexos)
5. [Starting and Launching _Lexos_](#starting-lexos)
6. [Quitting Lexos](#quitting-lexos)

### <a name='about-lexos'></a> About _Lexos_
_Lexos_ is an integrated workflow of tools to facilitate computational text analysis, presented in a web-based interface. Lexos is written primarily in Python 2.7.11 using the [*Flask*](http://flask.pocoo.org/) microframework, based on Werkzeug and Jinja 2. A heavy dose of Javascript and CSS is included on the front-end. We increasingly incorporate the wiz from [*D3.js*](http://d3js.org/) in our visualizations and the power in the [*scikit-learn*](http://scikit-learn.org/stable/) modules for text and statistical processing.

### <a name='installing-anaconda'></a>Installing Python and Anaconda
If you do not already have Python v2.7 installed on your computer, we recommend installing it through the free Anaconda distribution.[[1](#n1)] If you already have Python, Anaconda will run alongside your current installation. **Note: If you are installing Lexos v3.2 or above from the master branch of the Lexos repository, make sure to install Python 3.x instead. The rest of the installation procedure should be the same.**

1. Visit the Anaconda downloads page on the web: [https://continuum.io/downloads](https://continuum.io/downloads). Locate the **macOS symbol** on the screen (the apple); click on this **macOS** link to get to **Anaconda 4.4.0 For macOS Graphical Installer**. ![](installation-guide-images/installation-mac2.PNG)
2. Download the **Python 2.7 version Graphical Installer** by clicking on the green Download button.
3. Double-click the installer application icon (it will be called something like `Anaconda2-4.4.0-MacOSX-x86_64.pkg`) and follow the instructions on the screen.

When the process is complete, select **Close** to finish the installation of Anaconda.

You should now verify that we have installed it correctly. To do this, follow the instructions below:

1. Open a terminal window. If you are unfamiliar with how to access a terminal window, search for “terminal” in Spotlight. You should see a window appear with a command-line prompt, typically a `$`.
2. Type `python -V` (capital v) and hit the `Enter` key.

You should see a response that looks like: `Python 2.7.13 :: Anaconda 4.4.0 (64-bit)`. 
If you do not see `:: Anaconda 4.4.0` then your PATH variable was not updated during the Anaconda 
installation. We recommend that you uninstall Anaconda and try to install it again, following the 
instructions above. To uninstall Anaconda, type `rm -rf ~/anaconda2`, replacing `anaconda2` with the 
name of the Anaconda directory, if it is different. Hit the `Enter` key. 

### <a name='installing-packages'></a> Installing Additional Python Packages
You must now install three additional Python packages needed to run _Lexos_.
1. Begin my making sure that your package installer (pip) is up to date. In the terminal type `pip install -U pip` (capital u) and hit the `Enter` key. Your terminal window will display some information showing you the update process. Once that is completed, you can now use 'pip' (python package installer) in the next step.
2. In the terminal type the following three commands, hitting the `Enter` key after each one. The installation process for each may take some time.
```python
pip install gensim
pip install chardet
pip install natsort
```
When the last installation is finished, you are ready to download _Lexos_.

>Note: If any odd errors occur ensure your terminal is displaying something like `mac_name:~ your_user$` as your location, otherwise exit and open a new terminal.

### <a name='downloading-lexos'></a> Downloading and Extracting _Lexos_
To download _Lexos_, enter [https://github.com/WheatonCS/Lexos/archive/v3.1.1.zip](https://github.com/WheatonCS/Lexos/archive/v3.1.1.zip) in your browser's address bar. Alternatively, go to the _Lexos_ GitHub page: [https://github.com/WheatonCS/Lexos/releases](https://github.com/WheatonCS/Lexos/releases). Look under **Lexos v3.1.1**, click on the link that says `Source code (zip)` under **Downloads** and save the file.

Once the _Lexos_ zip archive has downloaded, go into your Downloads and right-click on the zip icon, then select **Open With > Archive Utility** (only do this if your mac didn't automatically unzip your file for you). Choose where you would like to install _Lexos_ and drag the folder there. If you wish, you may change the name of the extracted folder from `Lexos-3.1.1` to `Lexos`. In the instructions below, we will assume that you did this and that you extracted the `Lexos` folder to the Desktop.

### <a name='starting-lexos'></a> Starting and Launching _Lexos_
**Important: Close your current terminal window and open a new one.**

In most cases, the terminal window will open in your computer's user account directory. It will show your location by displaying something like `mac_name:~ your_user$`. If the command prompt says something else, you may need to navigate to this folder. For help with navigation using the command line, check out this article by _Macworld_ [http://www.macworld.com/article/2042378/master-the-command-line-navigating-files-and-folders.html](http://www.macworld.com/article/2042378/master-the-command-line-navigating-files-and-folders.html).

Now navigate to the `Lexos` folder by typing `cd Desktop/Lexos` and hit the `Enter` key. If you encounter an error, make sure that you are starting in your user account folder, that the Lexos folder is on the Desktop, and that it is called `Lexos`. The terminal should now display something like `mac_name:Lexos your_user$`.

Type `python lexos.py` and hit the `Enter` key. This will start _Lexos_. It may take a minute to see a response the first time you run the command because Python has to reconfigure some of the project files for your computer. But shortly after you should see the following:
```
Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
Restarting with stat
Debugger is active!
Debugger PIN: 236-087-009
```
**Important:** Keep the `python lexos.py` command running while you use _Lexos_. You may minimize the terminal window, **but do not close it**.

Once you see the message above, you are ready to launch _Lexos_. Go to a web browser and enter `localhost:5000` in the address bar. We recommend using either Firefox or Chrome (other browsers are not supported and may not work with _Lexos_). You will soon see the _Lexos_ upload page. For information about using _Lexos_, click the "Gear" icon at the top right of the screen.

**Note:** Because your computer is acting as both the web server and the user of _Lexos_, you may need to hit the **Reset** button in the top right corner of the **Upload** page to make sure files from any previous sessions are purged.

**Note:** We've noticed on that some versions of Mac OS X do not have the character encoding set to UTF-8, thus they got an error on this step. Here is a fix that has worked for us:

1. Open a new terminal.
2. Type `cd` and hit `Enter`.
3. Using an editor of your choice, edit the file `.bash_profile`. For instance, if using “open”, type `open .bash_profile`.
4. Add the following lines and then save the file (**Command+s**).
```
export LC_ALL=en_US.UTF-8
export LANG_=en_US.UTF-8
```
Return to the `Lexos` directory and restart _Lexos_ by entering the following commands.
```
cd
cd Desktop/Lexos
python lexos.py
```

### <a name='quitting-lexos'></a> Quitting _Lexos_
To quit _Lexos_ simply close your browser window and close the terminal window running `python lexos.py`.

_Last edited: August 16, 2017_

<a name='n1'></a>[1] [Anaconda](https://docs.continuum.io/anaconda/) is a free distribution of the Python programming language for large-scale data processing, predictive analytics, and scientific computing, that aims to simplify package management and deployment. As of August 2017, Anaconda includes 720+ of the most popular Python packages, including most of the packages needed for _Lexos_.