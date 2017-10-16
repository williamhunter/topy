# Dependencies
There always are... It shouldn't take more than a few minutes to download and install everything.

## All platforms
Install Python 2.7.13 (32 or 64 bit) - make sure your 'bitness' is correct
when downloading the other packages listed further below.
Download Python from the official Python site.
If you're using Linux or Mac, you most
probably have Python installed already.

If you want to know on what platform
you are, start Python and type:
```python
import platform
platform.architecture()
```

ToPy requires Python 2.7 because of its dependence on
Pysparse, which is only available in binary format for Python 2.7 on
Windows systems and is too much trouble/bother to compile from scratch
if you want to get up and running quickly. I've started to look into replacing
Pysparse with something else that's as quick -- it will take me a while because
I have a 'real' job.

The same is of course not true for Linux/Mac systems, so you may very well be
able to get ToPy to work with Python 3.x -- I've not tried.

## Windows
1. Make sure Python is in your 'Path' Environment Variables. *How?*
If you type 'python' in
a command prompt (cmd window) and you don't get an error, you're OK.  
	1. If you don't know how to add Python to 'Path', please search the web
on how to do it. Tip: Start a new cmd window after you've made changes to the
'Path' Environment Variable.
	2. Check if Python works by typing it into a cmd shell.
	3. Check if `pip` works, also by typing it into a cmd shell. If it
doesn't work, add Python27\Scripts to the Environment Variables,
open a new cmd shell and check if it works.
	4. Note:- When using `pip`, run `cmd` as Administrator.
	5. Installing with `pip` is easy:
	`pip install <package>`
2. Download NumPy+MKL for Python 2.7 from Christoph Gohlke's website:
http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
and install with `pip`
3. Download Pysparse, also from
http://www.lfd.uci.edu/~gohlke/pythonlibs/#pysparse
and install with `pip`
4. Install matplotlib via `pip`
5. Install SymPy via `pip`
6. Install PyVTK via `pip`

## Linux
Install equivalent packages as for Windows above via `pip` or by other means
(e.g., apt-get, yum, rpm,...). So, install he following:
1. NumPy+MKL
2. Pysparse
3. matplotlib
4. SymPy
5. PyVTK

## Mac
Install equivalent packages as for Linux above via `pip` or by other means.

Installing matplotlib and SymPy via other 'official' channels should
also work fine (in that ToPy should still work).

If everything installed correctly, you're ready to install ToPy.

# Installing ToPy
CD into the 'topy' directory (where 'setup.py' is located) and
in a terminal ('cmd' on Windows), type:

	python setup.py install

or if you want to install locally, type:

	python setup.py install --user

You may require Administrator rights on Windows, depending on your setup.

If there aren't any errors, then ToPy is installed. Congratulations!

# Getting started
See https://github.com/williamhunter/topy/wiki/Tutorials

# First run of ToPy
## Element stiffness matrices
The first time you run ToPy after a new install you'll see the
following in your terminal:

	It seems as though all or some of the element stiffness matrices
	do not exist. Creating them...
	This is usually only required once and may take a few minutes.
	SymPy is integrating: K for Q4bar...
	Created C:\Users\William\Programming\ToPy\topy\data\Q4bar.K (stiffness matrix).
	SymPy is integrating: K for Q4...
	Created C:\Users\William\Programming\ToPy\topy\data\Q4.K (stiffness matrix).
	SymPy is integrating: K for Q5B...
	Created C:\Users\William\Programming\ToPy\topy\data\Q5B.K (stiffness matrix).
	SymPy is integrating: K for Q4T...
	Created C:\Users\William\Programming\ToPy\topy\data\Q4T.K (stiffness matrix).
	SymPy is integrating: K for H8...
	Created C:\Users\William\Programming\ToPy\topy\data\H8.K (stiffness matrix).
	SymPy is integrating: K for H18B...
	Created C:\Users\William\Programming\ToPy\topy\data\H18B.K (stiffness matrix).
	SymPy is integrating: K for H8T...
	Created C:\Users\William\Programming\ToPy\topy\data\H8T.K (stiffness matrix).

You won't (shouldn't) see it again, even if ToPy is updated, since these
files shouldn't need to change. You can create the stiffness matrices without
solving a problem by simply running 'optimise.py' in the 'scripts' folder.

--

William Hunter
Date: 2017-08-21
