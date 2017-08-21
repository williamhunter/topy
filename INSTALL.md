# Prerequisites

1. Start by installing Python 2.7.13 (32 or 64 bit), download from
the official Python site. If you're using Linux or Mac, you most
probably have Python installed already.
Unfortuamately ToPy requires Python 2.7 because of its dependence on
Pysparse, which is only available in binary format for Python 2.7.

2. **Windows 10:** Make sure Python is in your 'Path' Environment
Variable.
	1. If you don't know how to add it to 'Path', please search the web
	on how to do it.
	2. Check if Python works by typing it into a *cmd* shell.
	3. Check if `pip` works, also by typing it into a *cmd* shell. If it
	doesn't work, add Python27\Scripts to the Environment Variables,
	open a new *cmd* shell and check if it works.
	4. NOTE:- When using `pip`, run `cmd` as Administrator.
3. Download NumPy+MKL for Python 2.7 from Christoph Gohlke's website:
http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
and install with `pip` 
4. Download Pysparse, also from:
http://www.lfd.uci.edu/~gohlke/pythonlibs/#pysparse
and install with `pip`
5. Install matplotlib via `pip`
6. Install SymPy via `pip`
7. Install PyVTK via `pip`

8. **Linux**: Install equivalent packages via `pip` or by other means
(e.g., apt-get, yum, rpm,...)

9. **Mac**: I don't have access to a Mac, please adapt the above
instructions to suit.

Installing matplotlib and SymPy via other 'official' channels should
also work fine (in that ToPy should still work).

If everything installed correctly, you're ready to install ToPy.

# Installing ToPy
In a terminal ('cmd' on Windows), type:

	python setup.py install

or if you want to install locally, type:

	python setup.py install --user

You may require Administrator rights on Windows, depending on your setup.
	
## Creating the element stiffness matrices
The first time you run ToPy after a fresh install you'll see the
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
files shouldn't need to change.
---
William Hunter
Date: 2017-08-21


