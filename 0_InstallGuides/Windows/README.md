# Windows Manual Installation Guide

## Overview:

1. About *Lexos* (#about)
2. Installing Python and Anaconda (#installing-anaconda)
3. Installing Additional Packages (#installing-packages)
4. Downloading and Extracting _Lexos_ (#downloading-lexos)
5. Starting and Launching _Lexos_ (#starting-lexos)
6. Quitting Lexos (#quitting-lexos)

### <a name='about'></a> About _Lexos_
_Lexos_ is an integrated workflow of tools to facilitate computational text analysis, presented in a web-based interface. Lexos is written primarily in Python 2.7.11 using the [*Flask*](http://flask.pocoo.org/) microframework, based on Werkzeug and Jinja 2. A heavy dose of Javascript and CSS is included on the front-end. We increasingly incorporate the wiz from [*D3.js*](http://d3js.org/) in our visualizations and the power in the [*scikit-learn*](http://scikit-learn.org/stable/) modules for text and statistical processing.

### <a name='installing-anaconda'></a>Installing Python and Anaconda
If you do not already have Python v2.7 installed on your computer, we recommend installing it through the free Anaconda distribution.[1] If you already have Python, Anaconda will run alongside your current installation.

1. Visit the Anaconda downloads page on the web: [(http://continuum.io/downloads](http://continuum.io/downloads). Locate the **Jump to:** on the screen; click on the **Windows** link.
2. Download the **Python 2.7 Windows 64-bit Graphical Installer** by clicking on the blue button. If you have a very old computer, you may have to use the Windows 32-bit version, in which case, you should click the smaller link below. If you are unsure whether you computer is running a 32-bit or a 64-bit version of Windows, follow the instructions at [https://support.microsoft.com/en-us/kb/827218](https://support.microsoft.com/en-us/kb/827218).
3. Double-click the installer application icon (it will be called something like `Anaconda2-4.1.1-Windows-x86_64.exe`) and follow the instructions on the screen.
> *Note: The installation location is not important; however, make sure that you leave the option to `Update the PATH variable` checked. This will ensure that Windows knows that you want to use the Anaconda distribution of Python when you launch _Lexos_. This is especially important if you already have a different version of Python installed.*
4. When the process is complete, select **Finish** to finish the installation of Anaconda.

You should now verify that we have installed it correctly. To this follow the instructions below:
1. Open a Windows Command Prompt. If you are unfamiliar with how to access the Command Prompt, hit [WindowsKey] + [R] to bring up the Run box and type `cmd.exe` into the text field. Then hit `Enter`. A blck Command Prompt window should appear.
2. Type `python -V` followed by `Enter`

You should see a response that looks like: `Python 2.7.12 :: Anaconda 4.1.1 (64-bit)`. If you do not see `:: Anaconda 4.1.1` then you did not update your PATH variable during the Anaconda installation. We recommend that you uninstall Anaconda and try to install it again, following the instructions above. To uninstall Anaconda, go to your computer's Control Panel, choose `Add or Remove Programs` or `Uninstall a program` and then select `Python 2.7 (Anaconda)`.

### <a name='installing-packages'></a> Installing Additional Python Packages
You must now install the three additional packages needed to run _Lexos_.
1. Begin my making sure that your package installer (pip) is up to date. Type `pip install -U pip` followed by `Enter`. Your command Prompt window will display some information showing you the update process. Once that is completed, you can now use 'pip' (python package installer) in the next step.
2. Type the following three commands, each followed by `Enter`. The installation process for each may take some time.
```python
pip install gensim
pip install chardet
pip install natsort
```
When the last installation is finished, you are ready to download _Lexos_.

### <a name='downloading-lexos'></a> Downloading and Extracting _Lexos_
To download _Lexos_, enter [https://github.com/WheatonCS/Lexos/archive/master.zip](https://github.com/WheatonCS/Lexos/archive/master.zip) in your browser's address bar. Alternatively, go to the _Lexos_ GitHub page: [https://github.com/WheatonCS/Lexos](https://github.com/WheatonCS/Lexos). Click the green **Clone or download** button on the right side of the screen; then click the **Download Zip** button. 

Once the _Lexos_ zip archive has downloaded, right-click on the icon and select **Extract All...**. Choose where you would like to install _Lexos_. If you wish, you may change the name of the extracted folder from `Lexos-master` to `Lexos`. In the instructions below, we will assume that you did this and that you extracted the `Lexos` folder to the Desktop.

### <a name='starting-lexos'></a> Starting and Launching _Lexos_
Return to the Command Prompt window or open a new one by typing `[WindowsKey] + [R]` to bring up the Run box, and then type `cmd.exe`. In most cases, the Command Prompt window will open in your computer's user account directory. It will show your location by displaying something like `C:\Users\YOUR_NAME`. If the command prompt says something else, you may need to navigate to this folder. For help with navigation in the Windows Command Prompt, check out this article by Wikihow: [http://www.wikihow.com/Change-Directories-in-Command-Prompt](http://www.wikihow.com/Change-Directories-in-Command-Prompt)).

Now navigate to the `Lexos` folder by typing `cd Desktop\Lexos` followed by `Enter`. If you encounter an error, make sure that you are starting in your user account folder, that the Lexos folder is on the Desktop, and that it is called `Lexos`. The Command Prompt should now display `C:\Users\YOUR_NAME\Desktop\Lexos`.

Type `python lexos.py` followed by `Enter`. This will start _Lexos_. It may take a minute to see a response the first time you run the command because Python has to reconfigure some of the project files for your computer. But shortly after you should see the following:
```
Restarting with stat
Debugger is active!
Debugger pin code: 236-087-009
Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
**Important:** Keep the `python lexos.py` command running while you use _Lexos_. You may minimize the Command Prompt window, but do not close it.

Once you see the message above, you are ready to launch _Lexos_. Go to a web browser and enter [`localhost:5000`](localhost:5000) in the address bar. We recommend using either Firefox or Chrome (other browsers are not supported and may not work with _Lexos_). You will soon see the _Lexos_ upload page. For information about using _Lexos_, click the "Gear" icon at the top right of the screen.

**Note:** Because your computer is acting as both the web server and the user of _Lexos_, you may need to hit the **Reset** button in the top right corner of the **Upload** page to make sure files from any previous sessions are purged.

### <a name='quitting-lexos'></a> Quitting _Lexos_
To quit _Lexos_ simply close your browser window and close the Command Prompt window running `python lexos.py`.

*Last edited: August 20, 2016*

[1] [Anaconda](https://docs.continuum.io/anaconda/) is a free distribution of the Python programming language for large-scale data processing, predictive analytics, and scientific computing, that aims to simplify package management and deployment. As of June 2016, Anaconda includes 820+ of the most popular Python packages, including most of the packages needed for *Lexos*.