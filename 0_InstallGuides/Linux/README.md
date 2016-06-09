**Linux Install Guide** (last performed when using Ubuntu v14.x)

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
> **a) Visit the website:** [**http://continuum.io/downloads**](http://continuum.io/downloads)

> **b)** On the website, locate *Choose Your Installer* on the screen; click on the *Linux* link.

### **c) Download the Anaconda installer** (Linux 64-bit Python v2.7).

> **d)** After locating the install script (e.g., in Downloads/ ), **run the (bash) shell installer**
>
> **bash Anaconda-4.0.0-Linux-x86_64.sh**
>
> *(note: a newer version of Anaconda may have a new version number; check your exact filename).*

**2. Install additional packages**

> Now that Anaconda has been installed, we can verify that we have installed it correctly. Then we will install the two additional packages we need to run Lexos.
>
> **a. Open a new terminal** (this is important to ensure that your $PATH includes Anaconda).
>
> **b. Verify that Anaconda is installed** by typing in the terminal the following command:
>
> **python -V**
>
> *You should see a response that looks like : *
>
> *Python 2.7.11 :: Anaconda 4.0.0 (64-bit) If you do not see “:: Anaconda 4.0.0” then you did not open a new termnal (see (a) above) or you did not update your PATH variable during the Anaconda installation (back on Step #1) and thus, you should return to Step #1 and reinstall Anaconda correctly. *
>
> **c. Make sure that your package installer (pip) is up to date: **
>
> **pip install -U pip**
>
> **d. Install three additional needed packages**
>
> **pip install gensim**
>
> **pip install chardet**
>
> **pip install natsort**

**3. Download and extract *Lexos***

> **a.** Go to the *Lexos* github page: [**https://github.com/WheatonCS/Lexos**](https://github.com/WheatonCS/Lexos)
>
> **b.** At the bottom of the right-side navigation bar you will see a button to “**Download ZIP**”.
>
> Click this button to download a zipped file which contains the file folder which holds all the necessary source code for *Lexos*. **Extract** the contents of the .ZIP file **to your Desktop**. *If you want you can change the name of the containing folder from Lexos-master to just Lexos, but be sure to use the new name you used when in the command line on the subsequent steps.*

**4. Start *Lexos***

> **a.** Open a new terminal window
>
> **b.** <span id="__DdeLink__74_2053500975" class="anchor"></span>On the command line, use the cd command to navigate inside the Lexos-master folder.
>
> **cd Desktop/Lexos-master**
>
> **c. Start *Lexos *** -- On the command line enter:
>
> **python lexos.py **
>
> *It may take a minute the first time you run the command because Python has to reconfigure some of the project files for your computer, but shortly after you should see the following:*
>
> * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
>
> * Restarting with stat
>
> *Note: You must keep the “python lexos.py” command running while you use Lexos. You may minimize the terminal window, but do not close the terminal window.*
>
> **d. Using *Lexos* with your browser**
>
> To interact with the program you need to open your favorite web browser (Firefox or Chrome) and in the URL-address bar enter:
>
> **localhost:5000**
>
> *Because your computer is acting as both the web server and the user of Lexos, you may need to hit the *Reset* button in the top right corner of the Upload page to make sure files from any previous sessions are purged. *
>
> *To quit Lexos simply close the command prompt window (where you entered *
>
> *python lexos.py **). ***
>
> *Last edited: June 2, 2016*

[1] **Anaconda** is a free distribution of the Python programming language for large-scale data processing, predictive analytics, and scientific computing, that aims to simplify package management and deployment. As of June 2016, Anaconda includes 820+ of the most popular Python packages, including most of the packages needed for *Lexos*.
