'''
Read the model identifier from the SBML for model matching.


@author: mkoenig
@date: 2015-02-09
'''

# Read the GlucoNet and HepatoCore model

gluconet = "data/GlucoNet.xml"
hepatocore = "data/HepatoCore.xml"

import libsbml
from libsbml import SBMLReader


# The objects have to be mapped between the two models
# 1. map compartments
# 2. map species
# 3. map reactions





if __name__ == "__main__":
    print '# GlucoNet'
    
    