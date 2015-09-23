# Introduction

What is ToPy? The short version: Topology optimisation (or optimization, if you prefer) using Python.

ToPy is written in Python and used to solve one of three types of topology optimisation problems. You type a simple text input file (TPD file) and define one of the following three problems:
  1. minimum compliance,
  1. heat conduction or
  1. mechanism design (synthesis).

ToPy solves the problem to obtain a 2D (or 3D, depending on the input file) solid-void (black and white) solution. The result is
  1. an optimally stiff structure for minimum compliance problems,
  1. an optimal distribution of two materials for heat conduction problems and
  1. an optimal distribution of material for efficient mobility.

The 2D results are PNG files and the 3D results are VTK files.

Some examples are shown here: [ToPy Examples](https://github.com/williamhunter/ToPy/edit/wiki/ToPyExamples.md)

There is a tutorial to solve a 2D compliance problem here [ToPy 2D Tutorial](https://github.com/williamhunter/ToPy/edit/wiki/ToPy2DTutorial.md).

## Limitations
  * ToPy only works with regular square (for 2D)  and cubic (for 3D) meshes
  * No GUI for defining problems (but maybe in the future)
  * No CAD interface (although you can save the 3D files as STL files via Paraview)
  * ...

## Background
The development was done on Linux (32-bit), but ToPy works on Windows (32 and 64-bit¹) and OS X (Lion 10.7.4 64-bit)¹ too.

ToPy was part of my Master's thesis at the University of Stellenbosch, South Africa.

¹ <sub>Thanks to Nikos Kaminakis for letting me know.</sub>

# Status
Currently, the only way to get ToPy is to wait until I upload all the code, the Google Code repo is history.

# Examples
See ToPyExamples for two examples of the input (problem definition) files and their output after it was solved with ToPy.
[ToPy Examples](https://github.com/williamhunter/ToPy/edit/wiki/ToPyExamples.md)

