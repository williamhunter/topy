"""

Example demonstrating basic use of the Optimizer class.

Note that by defining fixed and loaded nodes by reference to the node array
the number of elements can easily be changed for increased resolution

"""

from topy.optimizer import Optimizer

# Initialize problem
opt = Optimizer('basic', 0.15)
opt.set_problem_dimensions(10, 10, 20)

# Define fixed nodes (entire z = 0 plane)
left_face = opt.nodes[:,:,0]
opt.fix_nodes(left_face, directions = ['x', 'y', 'z']) # Fixed in all directions

# Apply a load in -y direction at a single node in the center of the z = 20 plane
right_center = opt.nodes[(opt.num_nodes[0])/2,(opt.num_nodes[1])/2,-1]
opt.load_nodes([right_center], -1, direction = 'y')

opt.run_optimization()