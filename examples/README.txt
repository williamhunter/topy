Various ToPy examples

Go to the 'scripts' directory and find 'optimise.py' file. This Python script
reads and loads the TPD (ToPy Problem Definition) file. You can (obviously)
change 'optimise.py' to suit your needs.

The 'mbb_beam' directory is probably the best place to start experimenting.

Note to Windows users:
----------------------
You have to copy the 'optimise.py' type files to each example directory. Under
Linux (and I suspect OS X too) you can make use of symbolic links - I don't know
if there's a similar mechanism in Windows to accomplish this.


===========================
=== To run the programs ===
===========================
In a terminal/console, type:
   python optimise.py <filename>.tpd
in the relevant example directory.


=======================
=== Animation notes ===
=======================
All 3D animations were created with the help of ParaView 3 and the programs
mentioned below. In ParaView, save the animation as a sequence of PNG's, or
directly as an AVI, however, the latter format produces larger files.

1) GIF's:
---------
Create with: ImageMagick's convert.
View with: Any decent web browser.
Command (example): convert -delay 35 *.png anim.gif

2) MNG's:
---------
Create with: ImageMagick's convert.
View with: ImageMagick's display or ShowImg or any other MNG viewer.
Command (example): convert -delay 35 *.png anim.mng

3) MPEG's:
----------
Create with: mkmpeg4 Python script under Linux
(see http://www.gfdl.noaa.gov/products/vis/animation/index.html)
View with: MPlayer, Noatun, VLC Player, MS Windows Media Player, etc.
Command (example): mkmpeg4 -v -f 2 -o anim.mpeg 'ls still*.png'
