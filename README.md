![ToPy Logo](/images/topy_logo3d.png)

# ToPy
## Topology Optimization using Python
Exported from Google Code. Please see the wiki branch for now.

## Plans (not cast in stone, not necessarily in this order)
2. Create a wiki page for the installation, currently a PDF.
3. Show how to define a problem via Gmsh, or at least with the help of Gmsh. I'm not sure this is even going to be possible, and I need to get up to speed with Gmsh...
4. Create a simple Tkinter (not Qt lib, it's yet another set of dependencies) GUI to define problems instead of typing it out in a text editor. The idea is that you specify the type of problem and dimension (2D or 3D) and ToPy creates a Gmsh msh file for you. You can then easily view the node and element numbers (in Gmsh) which will make defining ToPy problems much easier. You then use the same Tkinter GUI to specify restraints and regions, regenerate the msh file and reload it in Gmsh. Once you're happy, ToPy creates a tpd file and solves.
5. Use Gmsh instead of Paraview to view results, can use Gmsh's timestep ability visualise how the domain changes (I think?).

	William Hunter

