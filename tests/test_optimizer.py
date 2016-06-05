'''
Created on 06/03/2015

@author: Gregers
'''

from topy.optimizer import Optimizer
import unittest
import numpy as np
import topy
        

allowed_missing = ['FXTR_NODE_X', 'FXTR_NODE_Y', 'FXTR_NODE_Z',
                   'LOAD_NODE_X', 'LOAD_NODE_Y', 'LOAD_NODE_Z',
                   'LOAD_VALU_X', 'LOAD_VALU_Y', 'LOAD_VALU_Z',
                   'LOAD_VAL_OUT', 'LOAD_DOF_OUT']

class Test(unittest.TestCase):




#==============================================================================
#     def setUp(self):
#         self.airLogger = AirLogger()
#         self.airServer = AirServer(self.airLogger)
#         self.airClient = AirClient(client)
# 
#     def tearDown(self):
#         self.airClient.disconnect()
#         self.airServer.stop(reactor_stop =  False)
#         pass
#==============================================================================


    def test_init(self):                
        self.opt = Optimizer('test', 0.15, Optimizer.prob_types.comp)
        self.opt.set_problem_dimensions(20, 20, 40)
        self.opt.fix_nodes(np.arange(441), directions=['x', 'y', 'z'])
        self.opt.load_nodes([17860], 1, direction = 'x')
        
    def load_topy(self, filename):
        t = topy.Topology()
        t.load_tpd_file(filename)
        return t
        
    def test_compare(self):
        self.test_init()
        t = self.load_topy('test_optimizer.tpd')
        assert np.all(self.opt.topy_dict['FIX_DOF'] == t.topydict['FIX_DOF'])
        assert list(self.opt.loaded_dof) == list(t.topydict['LOAD_DOF'])
        assert list(self.opt.loads) == list(t.topydict['LOAD_VAL'])
        
        assert set(t.topydict.keys()) - set(self.opt.topy_dict.keys()) - set(allowed_missing) == set([])
        
        for key in self.opt.topy_dict.keys():
            if type(t.topydict[key]) == np.ndarray:
                assert np.all(self.opt.topy_dict[key] == t.topydict[key])
            else:
                print key, type(self.opt.topy_dict[key]), type(t.topydict[key])
                assert self.opt.topy_dict[key] == t.topydict[key], (self.opt.topy_dict[key], t.topydict[key])
        
        #print self.opt.topy_dict['ELEM_K'], t.topydict['ELEM_K']
        #assert self.opt.topy_dict['ELEM_K'] == t.topydict['ELEM_K']
        #print set(t.topydict.keys()) - set(self.opt.topy_dict.keys()) - set(allowed_missing)
        #print t.topydict['PASV_ELEM']
        
        

    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()