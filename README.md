# ToPy
<div align="center">
	<img src="./imgsrc/ToPy_logo.png">
</div>

ToPy is a lightweight topology optimization framework for Python that can solve
compliance (stiffness), mechanism synthesis and heat conduction problems in 2D and 3D.
Please refer to the [ToPy Wiki](https://github.com/williamhunter/topy/wiki) for further information.

ToPy was originally hosted on Google Code.

## Installation
Once you've downloaded the depenencies (see the [INSTALL](https://github.com/williamhunter/topy/blob/master/INSTALL.md))
file all you need to do is the following:

```bash
$ git clone https://github.com/williamhunter/topy.git
$ cd topy/topy
$ python setup.py install
```

Alternatively, you can download the latest stable release, but it usually lags
a little behind the Master branch (as can be expected).

## Getting started
The main class of **ToPy** is 'Topology'. It defines the main constraints,
grid and parameters of optimization -- but you don't really have to bother
yourself with this if you just want to get some results.

### There are two ways of defining a problem
1. **TPD file**: You define the problem with keywords
(see [Help](https://github.com/williamhunter/topy/wiki/Help)) in a simple text file and solve via the command line
2. **Config dictionary**: This is similar to the TPD file approach, however,
you define the problem directly in a Python file; it's very useful if you want to
experiment and don't want to keep making changes to a text file.
You can later save the Config to a text file (a TPD file).

### TPD (**T**oPy **P**roblem **D**efinition) file
There is a minimal set of parameters, which is required for successful definition of a ToPy problem:
```
PROB_TYPE  : comp
PROB_NAME  : mbb_beam_minimal
ETA        : 0.5
DOF_PN     : 2
VOL_FRAC   : 0.5
FILT_RAD   : 1.5
P_FAC      : 3
ELEM_K     : Q4
NUM_ELEM_X : 60
NUM_ELEM_Y : 20
NUM_ELEM_Z : 0
NUM_ITER   : 10
FXTR_NODE_X: 1|21
FXTR_NODE_Y: 1281
LOAD_NODE_Y: 1
LOAD_VALU_Y: -1
```
You can read more about successful problem definition [here](https://github.com/williamhunter/topy/tree/master/templates).

When the `.tpd` file is defined, then the rest is simple:

```python
from topy import Topology

topology = Topology()
topology.load_tpd_file('file.tpd')
```

### Config dictionary
First you have to define a config dictionary (note the similarity with a TPD
file, especially the keywords):

```Python
config = {
     'DOF_PN': 2,
     'ELEM_K': 'Q4',
     'ETA': '0.5',
     'FILT_RAD': 1.5,
     'FXTR_NODE_X': range(1, 22),
     'FXTR_NODE_Y': 1281,
     'LOAD_NODE_Y': 1,
     'LOAD_VALU_Y': -1,
     'NUM_ELEM_X': 60,
     'NUM_ELEM_Y': 20,
     'NUM_ELEM_Z': 0,
     'NUM_ITER': 94,
     'PROB_NAME': 'beam_2d_reci',
     'PROB_TYPE': 'comp',
     'P_FAC': 3.0,
     'VOL_FRAC': 0.5
}
```
The requirements are the same as for `.tpd` file.

```Python
topology = Topology(config=config)
```
### Optimization (solving the problem)

You can use the one-line solution:

```bash
$ python topy/scripts/optimise.py <filename>.tpd
```

Or you can use a Python script:

```Python
import topy

config = {...}
t = topy.Topology(config)
t.set_top_params()
topy.optimise(t)
```

### Visualization (seeing the result)
Module `topy.visualization` allows one to save the output as a `.png` image for 2D problems or as a `.vtk` file for 3D. You can animate the obtained images with
the [convert](https://www.imagemagick.org/script/convert.php) tool.

```bash
convert -delay 35 *.png anim.gif
```

<div align="left">
	<img src="./imgsrc/beam_2d_reci_gsf.gif" width=40%>
	<img src="./imgsrc/inverter_2d_eta03.gif" width=30%>
	<img src="./imgsrc/t-piece_2d_Q4_eta04_gsf.gif" width=20%>
</div>

## Tutorials
[Tutorials](https://github.com/williamhunter/topy/wiki/Tutorials)

## Examples
[Examples](https://github.com/williamhunter/topy/wiki/Examples)

## How to cite ToPy
If you've used ToPy in your research work, please consider to cite:
```
@misc{Hunter2007william,
  author = {Hunter, William and others},
  title = {ToPy - Topology optimization with Python},
  year = {2017},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/williamhunter/topy}},
  }
```
