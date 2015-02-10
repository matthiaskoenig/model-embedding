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
    version = 2
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

def hepatocore_gluconet_mapping(m):
    '''
    Performs the unification of the models
    i.e. mapping of 
    '''
    # reorder substrates and products
    reorder = ["TPI", "PGK", "PGM", "PK", "LDH", "LACT", "CS"]
    # compartments
    c_map = {
             "extern" : "extern",
             "cyto" : "cyto",
             "mito" : "mito",
             }
    # species
    s_map = {
             "atp" : "ID_13648_cyto",
             "adp" : "ID_13653_cyto",
             "amp" : "ID_13667_cyto",
             "utp" : "ID_14675_cyto",
             "udp" : "ID_14335_cyto",
             "gtp" : "ID_13710_cyto",
             "gdp" : "ID_13815_cyto",
             "nad" : "ID_13620_cyto",
             "nadh" : "ID_13623_cyto",
             "phos" : "ID_13652_cyto",
             "pp" : "ID_13666_cyto",
             "co2" : "ID_13640_cyto",
             "h20" : "ID_13633_cyto",
             "h" : "ID_13622_cyto",
             "glc1p" : "ID_14180_cyto",
             "udpglc" : "ID_15273_cyto",
             "glyglc" : "ID_15924_cyto",
             "glc" : "ID_14148_cyto",
             "glc6p" : "ID_14102_cyto",
             "fru6p" : "ID_14103_cyto",
             "fru16bp" : "ID_13904_cyto",
             "fru26bp" : "ID_14479_cyto",
             "grap" : "ID_13727_cyto",
             "dhap" : "ID_13973_cyto",
             "bpg13" : "ID_14497_cyto",
             "pg3" : "ID_14468_cyto",
             "pg2" : "ID_14467_cyto",
             "pep" : "ID_14341_cyto",
             "pyr" : "ID_13917_cyto",
             "oaa" : "ID_14191_cyto",
             "lac" : "ID_15668_cyto",
             "glc_ext" : "ID_14148_extern",
             "lac_ext" : "ID_15668_extern",
             "co2_mito" : "ID_13640_mito",
             "phos_mito" : "ID_13652_mito",
             "oaa_mito" : "ID_14191_mito",
             "pep_mito" : "ID_14341_mito",
             "acoa_mito" : "ID_13675_mito",
             "pyr_mito" : "ID_13917_mito",
             "cit_mito" : "ID_14112_mito",
             "atp_mito" : "ID_13648_mito",
             "adp_mito" : "ID_13653_mito",
             "gtp_mito" : "ID_13710_mito",
             "coa_mito" : "ID_13910_mito",
             "nadh_mito" : "ID_13623_mito",
             "nad_mito" : "ID_13620_mito",
             "h20_mito" : "ID_13633_mito",
             "h_mito" : "ID_13622_mito",
             }
            # reactions
            r_map = {}
GLUT2" : "ID_19899_pm
GK" : "ID_17645_cyto
G6PASE" : "ID_17695_cyto
GPI" : "ID_17609_cyto
G16PI" : "ID_20371_cyto
UPGASE" : "ID_18627_cyto
PPASE" : "ID_18123_cyto
GS" : "ID_19252_cyto
GP" : "ID_19256_cyto
NDKGTP" : "ID_18783_cyto
NDKUTP" : "ID_18741_cyto
AK" : "ID_18668_cyto
PFK2" : "ID_20390_cyto
FBP2" : "ID_20364_cyto
PFK1" : "ID_18688_cyto
FBP1" : "ID_18113_cyto
ALD" : "ID_17905_cyto
TPI" : "ID_18806_cyto
GAPDH" : "ID_18374_cyto
PGK" : "ID_17950_cyto
PGM" : "ID_17925_cyto
EN" : "ID_18349_cyto
PK" : "ID_19054_cyto
PEPCK" : "ID_17808_cyto
PEPCKM" : "ID_17808_mito
PC" : "ID_18157_mito
LDH" : "ID_19002_cyto
LACT" : "ID_20156_pm
PYRTM" : "ID_19868_mm
PEPTM" : "ID_20065_mm
PDH" : "ID_19260_mito
CS" : "ID_17711_mito
NDKGTPM" : "ID_18783_mito
    
    


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
   
