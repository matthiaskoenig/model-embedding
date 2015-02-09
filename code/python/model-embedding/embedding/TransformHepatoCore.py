'''
Reads the HepatoCore model and applies the transformation to the model so that 
valid SBML which can be used for FBA simulations and model matching.

* create proper compartments
* assign species and reactions to compartments
* fix naming of ids
* validate the SBML model

The objects have to be mapped between the two models
    1. map compartments
    2. map species
    3. map reactions

The database with the id specifications is needed, i.e. HepatoCore has
to be up and running.
hepatocore id <-> 


@author: mkoenig
@date: 2015-02-09
'''
#######################################################################
gluconet = "../data/GlucoNet.xml"
hepatocore = "../data/HepatoCore.xml"
#######################################################################

import sys
import time
import os
import os.path
from libsbml import *
 
def check_sbml(filename): 
    current = time.clock();
    doc = readSBML(filename); 
    errors = doc.getNumErrors();
    
    print;
    print(" filename: " + filename);
    print(" file size: " + str(os.stat(filename).st_size));
    print(" read time (ms): " + str(time.clock() - current));
    print(" validation error(s): " + str(errors));
    print;
    doc.printErrors();
    return errors;




if __name__ == "__main__":
    print '# HepatoCore #'
    # check_sbml(hepatocore)
    doc = readSBML(hepatocore)
    m = doc.getModel()
    # compartment dictionary
    for c in Model.getListOfCompartments(m):
        print c.getId(), c.getName()
        
    # species dictionary
    for s in Model.getListOfSpecies(m):
        print s.getId(), s.getName(), s.getCompartment(), s.getBoundaryCondition()
        
    # species dictionary
    for r in Model.getListOfReactions(m):
        print r.getId(), r.getName(), r.getCompartment(), r.getBoundaryCondition()
    
        
    
    
    
    
    
    
    # print compartments
    print m.getId()
    print m.getName()