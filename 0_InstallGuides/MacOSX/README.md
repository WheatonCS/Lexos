**Mac OSX Install Guide**

**Overview:**

0. About *Lexos*

1. Install Python and Anaconda

2. Install additional packages

3. Download and extract *Lexos*

4. Start *Lexos*

**0. About *Lexos***

> *Lexos* is an integrated workflow of tools to facilitate the computational analyses of texts, presented in a web-based interface. Lexos is written primarily in Python 2.7.11 using the [*Flask*](http://flask.pocoo.org/) microframework, based on Werkzeug and Jinja 2. A heavy dose of Javascript and CSS is included on the front-end. We increasingly incorporate the wiz from [*D3.js*](http://d3js.org/) in our visualizations and the power in the [*scikit-learn*](http://scikit-learn.org/stable/) modules for text and statistical processing.

**1. Install Python**

> Install a free distribution of Python v2.7 called Anaconda[1].
>
> **a) Visit the website:** [**http://continuum.io/downloads**]()

### b) On the website, locate *Choose Your Installer* on the screen; click on the *OS X* link.

> **c) Download the Anaconda installer** (Python v2.7 Graphical Installer).
>
> **d) Double-click on the installer application** icon (.pkg file) and follow the instructions.
>
> **e)** Finally, select **Continue** to finish the install of Anaconda.

2. **Install additional packages**

> Now that Anaconda has been installed, we can verify that we have installed it correctly. Then we will install the two additional packages we need to run Lexos.
>
> **a. Open a terminal window.** *(If you are unfamiliar with how to access a terminal window, search for “terminal” in Spotlight. You should see a window appear with a command-line prompt, typically a “$” prompt).*
>
> **b. Verify that Anaconda is installed** by typing in the terminal the following command:
>
> **python -V**
>
> *You should see a response that looks like : *
>
> ***Python 2.7.11 :: Anaconda 4.1.0 (64-bit) If you do not see “:: Anaconda 4.1.0” then you did not update your PATH variable during the Anaconda installation (back on Step #1) and thus, you should return to Step #1 and reinstall Anaconda correctly. ***
>
> **c. Make sure that your package installer (pip) is up to date: **
>
> **pip install -U pip**
>
> *Your terminal should display some information showing you the update process. If you don’t have pip, do the following: sudo easy_install pip (requires your password)*
>
> **d. Install four additional needed packages**
>
> **pip install gensim**
>
> **pip install chardet**
>
> **pip install natsort**
>
> **pip install ete2**

**3. Download and extract *Lexos***

> **a.** Go to the *Lexos* github page: [**https://github.com/WheatonCS/Lexos**]()
>
> **b.** At the bottom of the right-side navigation bar you will see a button to “**Download ZIP**”.
>
> Click this button to download a zipped file which contains the file folder which holds all the necessary source code for *Lexos*. **Extract** the contents of the .ZIP file **to your Desktop**. *If you want you can change the name of the containing folder from Lexos-master to just Lexos, but be sure to use the new name you used when in the command line on the subsequent steps.*

4. **Start *Lexos***

> **a.** Close your current window and **open a new terminal window**. **IMPORTANT!**
>
> **b.** <span id="__DdeLink__74_2053500975" class="anchor"></span>On the command line, use the cd command to navigate inside the Lexos-master folder[2].
>
> **cd Desktop/Lexos-master**
>
> **c. Start *Lexos ***-- On the command line enter:
>
> <span id="__DdeLink__555_381611071" class="anchor"></span>**python lexos.py **
>
> *It may take a minute the first time you run the command because Python has to reconfigure some of the project files for your computer, but shortly after you should see the following:*
>
> * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
>
> * Restarting with stat
>
> *Note: You must keep the “python lexos.py” command running while you use Lexos. You may minimize the terminal window, but do not close the terminal window.*
>
> *Note: We've noticed on that some version of Mac OS X do not have the character encoding set to UTF-8, thus they got an error on this step. Here is a fix that has worked for us:*
>
> (i) **cd**
>
> (ii) *using an editor of your choice, e.g., perhaps “open”:* **open .bash_profile**
>
> (iii) *add these two lines and save (command-s) the file*
>
> **export LC_ALL=en_US.UTF-8**

**export LANG=en_US.UTF-8**

> (iv) *return to the Lexos directory by entering these two commands, then restart* Lexos
>
> **cd**
>
> <span id="__UnoMark__556_381611071" class="anchor"></span>**cd Desktop/Lexos-master**
>
> **python lexos.py **
>
> **d. Using *Lexos* with your browser**
>
> To interact with the program you need to open your favorite web browser (Firefox or Chrome) and in the URL-address bar enter:
>
> **localhost:5000**
>
> *Because your computer is acting as both the web server and the user of Lexos, you may need to hit the *Reset* button in the top right corner of the Upload page to make sure files from any previous sessions are purged. *
>
> *To quit Lexos simply close the terminal window (where you entered *
>
> *python lexos.py **). ***

*Last edited: July 22, 2016*

[1] **Anaconda** is a free distribution of the Python programming language for large-scale data processing, predictive analytics, and scientific computing, that aims to simplify package management and deployment. As of June 2016, Anaconda includes 820+ of the most popular Python packages, including most of the packages needed for *Lexos*.

[2] (If you need additional information on file navigation, check out this article by macworld <http://www.macworld.com/article/2042378/master-the-command-line-navigating-files-and-folders.htm> )
