"""

Example demonstrating optimization with multiple load cases. This enables the
ability to optimize the structure with respect to loads in different directions.

"""

from topy.optimizer import Optimizer

# Initialize problem
opt = Optimizer('multi_load', 0.10, load_case = 'vertical')
opt.set_problem_dimensions(10, 10, 20)

# Define fixed nodes (entire z = 0 plane)
left_face = opt.nodes[:,:,0]
opt.fix_nodes(left_face, directions = ['x', 'y', 'z']) # Fixed in all directions

# Apply a load in -y direction at a single node in the center of the z = 20 plane
right_center = opt.nodes[(opt.num_nodes[0])/2,(opt.num_nodes[1])/2,-1]
opt.load_nodes([right_center], -1, direction = 'y')

""" Create a second load case to also optimize for horizontal loads. Note that
this is very different than applying loads in both directions to the same load
case, try to comment out the line below and observe the difference in the
output """
opt.add_load_case('horizontal')

# Apply a load in -x direction
opt.load_nodes([right_center], -1, direction = 'x')

opt.run_optimization()