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


def clone_and_fix_hepatocore():
    ''' 
        Clones the elements from the network and fixes the SBML
        * Compartment creation
        * Compartment mapping
        * Fix compartment part of ID 
    '''
    version = 1
    mid = 'HepatoCore2_v{}'.format(version)
    # read the original model
    doc_old = readSBML(hepatocore)
    m_old = doc_old.getModel()
    
    
    # Definition of compartments for the unified model
    comps = [
        {'id': 'extern', 'name':'extern'},
        {'id': 'pm',     'name':'plasma membrane'},
        {'id': 'cyto',   'name':'cytosol'},
        {'id': 'mm',     'name': 'mitochondrial membrane'},
        {'id': 'mito',   'name':'mitochondrial matrix'},
    ]
    # mapping of id parts to compartment ids
    comps_map = {
        'cytosol': 'cyto',
        'mitochondrial_matrix' : 'mito',
        'blood_circulation' : 'extern',
        'plasma_membrane' : 'pm',
    } 
             

    # Create new fixed model
    doc = SBMLDocument(3,1)
    m = SBMLDocument.createModel(doc, mid)
    m.setName(mid)
    
    # Create the compartments
    for cinfo in comps:
        c = m.createCompartment()
        c.setId(cinfo['id'])
        c.setName(cinfo['name'])
    
    # Create the species
    for s_old in m_old.getListOfSpecies():
        s = m.createSpecies()
        # get the compartment from id
        # replace the id
        # replace name
        s.setId(s_old.getId())
        
        
    
    writeSBMLToFile(doc, '{}.xml'.format(mid) );
    return m



if __name__ == "__main__":
    # Do all the replacements to the model
    m2 = clone_and_fix_hepatocore()
    exit() 
    
    print '# HepatoCore #'
    # check_sbml(hepatocore)
    doc = readSBML(hepatocore)
    m = doc.getModel()
    # compartment dictionary
    for c in Model.getListOfCompartments(m):
        print c.getId(), c.getName()
        
    # species dictionary
    for s in Model.getListOfSpecies(m):
        print s.getId(), s.getName(), s.getCompartment()
        
    # species dictionary
    for r in Model.getListOfReactions(m):
        print r.getId(), r.getName()
    
    print
    print '# GlucoNet #'
    doc = readSBML(gluconet)
    m2 = doc.getModel()
    # compartment dictionary
    for c in Model.getListOfCompartments(m2):
        print c.getId(), c.getName()
        
    print '#' * 80
   