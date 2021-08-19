# Getting started with Python

## Guide to install Python related software for the course.

If you find mistakes/typos or links that do no longer function, please contact: 

Jochen Köhler (jochen.kohler@ntnu.no)

### Install Python ?

First, make sure that you have python installed at all. You can verify your version by opening the terminal on your computer:

+ MacOS: open spotlight with the shortcut Cmd + spacebar, and type-in: *terminal*. Then, hit enter to open the terminal.
+ Windows: One of the following two options: 
    - Windows+R, then type-in *cmd* and press enter.
    - Start >> Program Files >> Accessories >> Command Prompt

Once you have a terminal window opened, type the following command (note that the dollar symbol indicates beginning of command, but should not be typed in the command window):
```
$ python -V
```

In my case the output looks like this
```
Python 3.8.10
```

If you need to install Python on your computer, here are some guides:
+ [NTNU guide](https://innsida.ntnu.no/wiki/-/wiki/English/Installing+Python#section-Installing+Python-Install+the+latest+version+of+Python) (for Windows, MacOS, and LINUX)
+ [For MacOS](https://opensource.com/article/19/5/python-3-default-mac) (in case you find it better/easier than the NTNU guide)

### Install Anaconda
Now install Anaconda.  The procedure depends on your operating system:

#### MacOS

Make sure you are working on a zsh terminal, i.e. if is says "-zsh" in the header of your terminal window, you are ok. 

If it says "-bash" instead, type the following command:
```
$ chsh -s /bin/zsh
```
Then restart your terminal. It should now say -- ~ -- -zsh on top. 

Now install Anaconda.  Try the instructions on the [Anaconda page](https://docs.anaconda.com/anaconda/install/mac-os/#macos-graphical-install). I recommend to install it via the Terminal - just follow the instructions. 
After you have installed it, run this command in the Terminal: 
```
$ conda init zsh
```

#### Windows: 
Follow the instructions on this [link](https://docs.anaconda.com/anaconda/install/windows/).



### Conda Environments

It is a good idea that we work on a course specific conda environment. A conda environment is a directory that contains a specific collection of conda packages that we will use in the course. So we can be sure to have the required packages and dependencies when we are in the environment. And the course specific installation will not "disturb" when you are outside the environment. 

Create a conda environment called tktpy: 
```
$ conda create --name tktpy
```

Once the process is finished, check that it has been successfully created:
```
$ conda info --envs
```

It should show at least an environment called base (with a * next to it) and another called tktpy. The * means that the current environment is base. We need to activate the environment we want to work at. For that, type the following:
```
$ conda activate tktpy
```
Now you are in the course specific environment and we can install excactely the same softwareversions and dependencies.

Let's agree that we work with python 3.9.0, so install via conda:
```
$ conda install python=3.9.0
```
And we install spyder version 5.0.5:
```
$ conda install -y spyder=5.0.5
```
Next, you need to install the course requirements. These are the python packages that we will use during the course. They are stored in a file called 'tktreq.txt'. To download the file, type:
```
$ curl -OL https://raw.githubusercontent.com/jochenkohler/TKT4196_material/master/tktreq.txt
```

To install them, type the following command:
```
$ pip install -r tktreq.txt 
```

### Jupyter

Jupyter notebooks are created for pedagogic purpose. You can use Jupyter Notebooks or Jupyter-lab to view/edit notebooks. To use widgets (interactive boxes) follow these instructions:
To install jupyter-lab (assuming that conda is installed): 
```
$ conda install -y jupyter jupyterlab nodejs
```

Then, install the required widget extensions with the following commands:
```
$ pip install ipywidgets
$ jupyter nbextension enable --py widgetsnbextension
$ jupyter labextension install @jupyter-widgets/jupyterlab-manager
```
