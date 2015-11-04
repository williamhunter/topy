import numpy as np
import elements
#from parser import _e2sdofmapinit
from topy.parser import _e2sdofmapinit


from pysparse import spmatrix
import topology
from time import time
from visualisation import create_3d_geom

class ProblemTypes:
    comp = 'comp'
    mech = 'mech'
    heat = 'heat'
    
class ElementStiffnessMatrices2D:
    Q4 = 'Q4'
    Q5B = 'Q5B'
    Q4a5B = 'Q4a5B'
    Q4T = 'Q4T'
    
class ElementStiffnessMatrices3D:
    H8 = 'H8'
    H18B = 'H18B'
    H8T = 'H8T'
    



class Optimizer:
    """ Basic class for setting up and running optimization directly from
    python without tpd files. The purpose of this class is:
        Be able to define problems directly in python for more advanced
            definition of loaded and fixed nodes, for example on curved surfaces.
        Make the problems easily scalable by defining physical dimensions
            instead of the number of elements.
    
    Currently this is designed to optimize 3D
    mechanical problems and might not be usable for other problem types """
    
    def __init__(self, name, vol_frac, problem_type = ProblemTypes.comp,
                 filter_radius = 1.5, dof_pn = 3, max_iterations = 100,
                 penalty_factor = 1, eta = 0.5,
                 elem_k = ElementStiffnessMatrices3D.H8, void_density = 0.01):
        """ Initializes Topology Optimizer
        
        Parameters
        ----------
        
        name : str
            The name of the specific optimization. Output files will have this
            name.
        vol_frac : float
            The final volume fraction
        problem_type :
            Type of problem - select from Optimizer.prob_types
        filter_radius : float
            The radius used for filtering
        dof_pn : int
            Number of degrees of freedom per node
        max_iterations : int
            Maximum number of iterations to perform
        penalty_factor : float
            Start value of penalty factor
        eta : float or str
            Eta
        elem_k:
            Element stiffness matrix, choose from Optimizer.k_2d or k_3d
        void_density: float
            Minimum density where element is disabled
        
        """
        
        self.dof = dof_pn
        self.fixed_dof = []
        self.loaded_dof = []
        self.loads = []   
        
        self.max_iterations = max_iterations
        
        self.topy_dict = {'PROB_TYPE': problem_type,
                          'PROB_NAME': name,
                          'VOL_FRAC': vol_frac,
                          'FILT_RAD': filter_radius,
                          'DOF_PN': dof_pn,
                          'NUM_ITER': max_iterations,
                          'P_FAC': penalty_factor,
                          'ETA': eta,
                          'ELEM_TYPE': elem_k,
                          'ELEM_K': getattr(elements, elem_k),
                          'FIX_DOF': self.fixed_dof,
                          'LOAD_DOF': self.loaded_dof,
                          'LOAD_VAL': self.loads,
                          'PASV_ELEM': np.array([]),
                          'ACTV_ELEM': np.array([]),
                          'P_HOLD'     : 15,  # num of iters to hold p constant from start
                          'P_INCR'     : 0.2,  # increment by this amount
                          'P_CON'      : 1,  # increment every 'P_CON' iters
                          'P_MAX'      : 3,  # max value of 'P_CON'     
                          'Q_FAC'      : 1,
                          'Q_HOLD'     : 15,  # num of iters to hold q constant from start
                          'Q_INCR'     : 0.05,  # increment by this amount
                          'Q_CON'      : 1,  # increment every 'Q_CON' iters
                          'Q_MAX'      : 5}  # max value of 'Q_CON'}
        

        
        
    def set_problem_dimensions(self, x_size, y_size, z_size, epul = 1):
        """ Defines the problem size. The sizes can either be defined as a
        a number of elements, or alternatively in physical dimensions, in which
        case epul is used to set the number of elements per unit length. The
        latter makes it easy to change the number of elements
        
        Note: Currently the code does not check the inputs, make sure the sizes
        are all an integer multiple of 1/epul.
        
        Parameters
        ----------
        x_size : int
            Size of the problem in x-direction
        y_size : int
            Size of the problem in y-direction
        z_size : int
            Size of the problem in z-direction
        epul: float
            Elements per unit length
        """
        num_elements = np.array([x_size, y_size, z_size])*epul
        self.elements = num_elements[0]*num_elements[1]*num_elements[2]
        num_nodes = num_elements + 1
        
        self.topy_dict['NUM_ELEM_X'] = num_elements[0]
        self.topy_dict['NUM_ELEM_Y'] = num_elements[1]    
        self.topy_dict['NUM_ELEM_Z'] = num_elements[2]   
        
        self.topy_dict['E2SDOFMAPI'] = _e2sdofmapinit(num_elements[0],
                                                      num_elements[1],
                                                      self.dof)
        
        self.nodes = np.arange(num_nodes[0]*num_nodes[1]*num_nodes[2])
        Ksize = len(self.nodes)*self.dof
        print "Ksize", Ksize
        self.topy_dict['K'] = spmatrix.ll_mat_sym(Ksize, Ksize) #  Global stiffness matrix   
    
    
        
        
    def fix_nodes(self, nodes, directions):
        """ Fixes nodes in the specified direction
        
        Parameters
        ----------
        
        nodes : list
            List of node numbers (as in self.nodes) to fix
        directions : str or list of str
            Which direction to fix, 'x', 'y' or 'z'
        
        """
        nodes = list(nodes)
        
#        if type(directions) != list:
#            assert type(directions) == str
#            directions = [directions]
#        for direction in directions:
#            key = self.fxtr_names[direction]
#            if key in self.topy_dict:
#                self.topy_dict[key].extend(nodes)
#            else:
#                self.topy_dict[key] = nodes
    
        for direction in directions:
            for node in nodes:
                self.fixed_dof.append(node*self.dof+self.directions[direction]) 
            
    def load_nodes(self, nodes, loads, direction):
        """ Loads nodes in the specified direction
        
        Parameters
        ----------
        
        nodes : list
            List of node numbers (as in self.nodes) to fix
        loads : list or float
            Load, can either be a list of loads for individual loads or a float,
            in which case all nodes are applied a load of load/len(nodes)
        direction : str
            Which direction to fix, 'x', 'y' or 'z'
        
        """

#        keys = self.load_names[direction]
        nodes = list(nodes)
        if type(loads) == float or type(loads) == int:
            loads = [float(loads)/len(nodes)]*len(nodes)
        assert len(nodes) == len(loads)
#        if keys[0] in self.topy_dict:
#            self.topy_dict[keys[0]].extend(nodes)
#            self.topy_dict[keys[1]].extend(loads)
#        else:
#            self.topy_dict[keys[0]] = nodes
#            self.topy_dict[keys[1]] = loads
        
        for node, load in zip(nodes, loads):
            self.loaded_dof.append(node*self.dof+self.directions[direction])
            self.loads.append(load)
            
        
    def run_optimization(self):
        
        # Set up ToPy:
        t1 = topology.Topology()
        t1.topydict = self.topy_dict
        t1.set_top_params()

        etas_avg = []

        # Optimising function:
        def optimise():
            t1.fea()
            t1.sens_analysis()
            
            #t2.fea()
            #t2.sens_analysis()
            #t1.df += t2.df
            
            t1.filter_sens_sigmund()
            #t2.df = t1.df
            t1.update_desvars_oc()
            
            #t2.desvars = t1.desvars
            # Below this line we print and create images:
            create_3d_geom(t1.desvars, prefix=t1.probname, \
            iternum=t1.itercount, time='none')
            print '%4i  | %3.6e | %3.3f | %3.4e | %3.3f | %3.3f |  %1.3f  |  %3.3f '\
            % (t1.itercount, t1.objfval, t1.desvars.sum()/(self.elements), \
            t1.change, t1.p, t1.q, t1.eta.mean(), t1.svtfrac)
            # Build a list of average etas:
            etas_avg.append(t1.eta.mean())

        # Start optimisation runs, create rest of design domains:
        print '%5s | %11s | %5s | %10s | %5s | %5s | %7s | %5s ' % ('Iter', \
        'Obj. func.  ', 'Vol. ', 'Change    ', 'P_FAC', 'Q_FAC', 'Ave ETA', 'S-V frac.')
        print '-' * 79
        ti = time()

        n = 0
        while t1.change > t1.void and n < self.max_iterations:
            optimise()
    
        te = time()
    
        # Print solid-void ratio info:
        print '\nSolid plus void to total elements fraction = %3.5f' % (t1.svtfrac)
        # Print iteration info:
        print t1.itercount, 'iterations took %3.3f minutes (%3.3f min/iter. \
        or %3.3f sec/iter.)'\
        %((te - ti) / 60, (te - ti) / 60 / t1.itercount, (te - ti) / t1.itercount)
        print 'Average of all ETA\'s = %3.3f (average of all a\'s = %3.3f)' \
        % (np.array(etas_avg).mean(), 1/np.array(etas_avg).mean() - 1)


    
    
    
    prob_types = ProblemTypes
    k_2d = ElementStiffnessMatrices2D
    k_3d = ElementStiffnessMatrices3D
    directions = {'x': 0, 'y': 1, 'z': 2}
    #fxtr_names = {'x': 'FXTR_NODE_X', 'y': 'FXTR_NODE_Y', 'z': 'FXTR_NODE_Z' }
    #load_names = {'x': ['LOAD_NODE_X', 'LOAD_VALU_X'],
    #              'y': ['LOAD_NODE_Y', 'LOAD_VALU_Y'],
    #              'z': ['LOAD_NODE_Z', 'LOAD_VALU_Z']}
    
    
    
    
if __name__ == '__main__':
    opt = Optimizer('test', 0.15, Optimizer.prob_types.comp)
    opt.set_problem_dimensions(20, 20, 40)
    opt.fix_nodes(np.arange(441), directions=['x', 'y', 'z'])
    opt.load_nodes([17860], 1, direction = 'x')
    opt.run_optimization()