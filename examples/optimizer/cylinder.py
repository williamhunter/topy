"""

Example demonstrating optimization with multiple load cases. This enables the
ability to optimize the structure with respect to loads in different directions.

"""

from topy.optimizer import Optimizer
import numpy as np
# Initialize problem
opt = Optimizer('cylinder', 0.1, void_density = 0.001, max_iterations=50)
ex, ey, ez = 20, 20, 10
opt.set_problem_dimensions(ex, ey, ez)

# Create cylinder by removing material around
z0 = ez/2
x0, y0, r0 = ex/2+0.5,ey/2+.5,ex/2-1

x, y, z = opt.element_indices
mask = opt.elements[(x-x0)**2+(y-y0)**2>=r0**2]
opt.add_passive_elements(mask)


# Create hole in the middle:
r1 = r0/3
mask = opt.elements[(x-x0)**2+(y-y0)**2<=r1**2]
opt.add_passive_elements(mask)


# Fix points in center
bearing1 = opt.nodes[x0+r1+1,y0+1-1:y0+1+2,z0+1-1:z0+1+2]
bearing2 = opt.nodes[x0-r1+1,y0+1-1:y0+1+2,z0+1-1:z0+1+2]

opt.fix_nodes(bearing1, directions = ['x', 'y', 'z'])
opt.fix_nodes(bearing2, directions = ['x', 'y', 'z'])

de = 1
left = opt.nodes[x0-r0+de+1,y0+1,z0]
top = opt.nodes[x0+1,y0+r0-de+1,z0]
right = opt.nodes[x0+r0-de+1,y0+1,z0]
bottom = opt.nodes[x0+1,y0-r0+de+1,z0]

load_points = [left, right, top, bottom]


opt.load_nodes(load_points, 1, direction = 'x')


opt.add_load_case('y')
opt.load_nodes(load_points, 1, direction = 'y')

opt.add_load_case('z')
opt.load_nodes(load_points, 1, direction = 'z')

opt.run_optimization()