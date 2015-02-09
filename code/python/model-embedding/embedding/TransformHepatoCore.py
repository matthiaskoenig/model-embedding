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
sbml_dir = "../data"
gluconet = "{}/GlucoNet.xml".format(sbml_dir)
hepatocore = "{}/HepatoCore.xml".format(sbml_dir)
#######################################################################
# Definition of compartments 
comps_dict = [
        {'id': 'extern', 'name':'extern'},
        {'id': 'pm', 'name':'plasma membrane'},
        {'id': 'cyto', 'name':'cytosol'},
        {'id': 'mm', 'name': 'mitochondrial membrane'},
        {'id': 'mim', 'name': 'mitochondrial inner membrane'},
        {'id': 'mito', 'name':'mitochondrial matrix'},
]

# mapping of hepatocore id parts to compartment ids
comps_map = {
        'blood_circulation' : 'extern',
        'plasma_membrane' : 'pm',
        'cytosol': 'cyto',
        'mitochondrial_membrane' : 'mm',
        'mitochondrial_inner_membrane' : 'mim',
        'mitochondrial_matrix' : 'mito',
} 

import time
from libsbml import *

def get_cid_from_string(s):
    # return first entry in the comps map
    for cid in comps_map.iterkeys():
        if cid in s:
            return cid
    else:
        print 'Not found compartment in: {}'.format(cid)
    return None

def replace_cid_in_string(s):
    for cid, cid_new in comps_map.iteritems():
        s = s.replace(cid, cid_new)
    return s

def remove_cid_from_name(s):
    for cid in comps_map.iterkeys():
        s = s.replace('_{}'.format(cid), '')
    return s


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
    
    # Create new HepatoCore model with implemented fixes
    doc = SBMLDocument(3,1)
    m = SBMLDocument.createModel(doc, mid)
    m.setName(mid)
    
    # Create the compartments
    for cinfo in comps_dict:
        c = m.createCompartment()
        c.setId(cinfo['id'])
        c.setName(cinfo['name'])
    
    # Create the species
    for s_old in m_old.getListOfSpecies():
        s = m.createSpecies()
        # get the compartment from id
        # replace the id
        # replace name
        sid = s_old.getId()
        cid = get_cid_from_string(sid)
        # now replace
        sid = replace_cid_in_string(sid)
        cid = replace_cid_in_string(cid)
        s.setId(sid)
        s.setCompartment(cid)
        name = s_old.getName()
        if name:
            name = remove_cid_from_name(name)
            s.setName(name)
     
    # Create the reactions
    for r_old in m_old.getListOfReactions():
        r = m.createReaction()
        
        rid = r_old.getId()
        print '#', rid, '#'
        cid = get_cid_from_string(rid)
        # now replace
        rid = replace_cid_in_string(rid)
        cid = replace_cid_in_string(cid)
        r.setId(rid)
        r.setCompartment(cid)
        name = r_old.getName()
        if name:
            name = remove_cid_from_name(name)
            r.setName(name)   
        
        # substrates
        print 'reactants:'
        for s_old in r_old.getListOfReactants():
            print s_old.getSpecies(), s_old.getStoichiometry()
            s = r.createReactant()
            s.setSpecies(replace_cid_in_string(s_old.getSpecies()))
            s.setStoichiometry(s_old.getStoichiometry())
        
        # products
        print 'products:'
        for s_old in r_old.getListOfProducts():
            print s_old.getSpecies(), s_old.getStoichiometry()
            s = r.createProduct()
            s.setSpecies(replace_cid_in_string(s_old.getSpecies()))
            s.setStoichiometry(s_old.getStoichiometry())
        
    writeSBMLToFile(doc, '{}/{}.xml'.format(sbml_dir, mid) );
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
   
