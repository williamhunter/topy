# Prerequisites

1. Start by installing Python 2.7 (32-bit works fine), download from the official site. If you're uing Linux, you most probably have it already.
2. **Windows only:** Make sure Python is in your Path Environment Variable.
	1. If you don't know how to add it, please search the web.
	1. Check if Python works by typing it into a *cmd* shell.
	1. Check if 'pip' works, also by typing it into a *cmd* shell. If it doesn't work, add Python27\Scripts to the Environment Variables too.
	1. When using 'pip', run 'cmd' as Administrator.
	1. Install NumPy+MKL for Python 2.7 from here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
	1. Install PySparse, also from http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
	1. Install PyVTK, also from http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
1. **Linux**: Install above packages via `pip` or by other means (e.g., apt-get, yum, rpm, etc).
7. Install matplotlib via `pip`
8. Install SymPy via `pip`

Installing matplotlib and SymPy via other 'official' channels should also work fine (in that ToPy should still work).

If everything installed correctly, you're set.

# Installing ToPy
In a shell ('cmd' window on Windows), type:

	python setup.py install

or if you want to install locally, type:

	python setup.py install --user