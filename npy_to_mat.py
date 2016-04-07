"""
Convert the .npy into .mat (for plotting into matlab)

Just indicate the input and output directory.

Use python 3 (but should be working with python 2)
"""

import os, sys
import numpy as np
import scipy.io as sio
import utils

# Set directories
root = os.getcwd()
#dirDataIn = root + '/../Data/Meshs/'
dirDataIn = root + '/../Data/Test_mesh_01/samples/'
dirDataOut = root + '/../Data/Test_mesh_01/samples_mat/'
savedVariableName = 'y'


def main():

    # Global check
    assert(os.path.exists(dirDataIn))
    assert(os.path.exists(dirDataOut))
    
    # For each file
    filesList = os.listdir(dirDataIn)
    for filename in filesList:
        print('Try converting ', filename)
        name = filename.split('.')[0] # Little hack to get the filename
        if filename.endswith('.npy'): # Candidate
            matrix = np.load(dirDataIn + filename, fix_imports = True)
        elif filename.endswith('.txt'): # Candidate
            matrix = utils.loadLabelList(dirDataIn + filename)
        else:
            print('Wrong format, skiped')
            continue
        sio.savemat(dirDataOut + name + '.mat', {savedVariableName:matrix})

if __name__ == "__main__":
    main()
    