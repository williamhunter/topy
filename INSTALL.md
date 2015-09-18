# Prerequisites

1. Start by installig Python 2.7 (32-bit works fine), download from the official site.
2. Windows only: Make sure Python is in your Path Environment Variable.
	1. If you don't know how to add it, please search the web.
	2. Check if Python works by typing it into a *cmd* shell.
	3. Check if 'pip' works, also by typing it into a *cmd* shell. If it doesn't work, add Python27\Scripts to the Environement Variables too.
	4. When using 'pip', run 'cmd' as Administrator.
5. Install NumPy+MKL for Python 2.7 from here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
5. Install PySparse, also from http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
6. Install PyVTK, also from http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
7. Install matplotlib via `pip`
8. Install SymPy via `pip`

If everything installed correctly, you're set.

# Installing ToPy
In a shell ('cmd' window on Windows), type:

	python setup.py install