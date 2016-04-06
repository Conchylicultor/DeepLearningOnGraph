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
#dirData = root + '/../Data/Meshs/'
dirData = root + '/../Data/Test_mesh_01/'


def main():

    # Global check
    if not os.path.exists(dirData):
        raise IOError('Cannot find dirData: ', dirData)
    
    # For each file
    filesList = os.listdir(dirData)
    for filename in filesList:
        if filename.endswith('.npy'): # Candidate
            npyToMat(filename)
        if filename.endswith('.txt'): # Candidate
            txtToMat(filename)

def npyToMat(filename):
    print('Try converting ', filename)
    name = filename.split('.')[0] # Little hack to get the filename
    matrix = np.load(dirData + filename, fix_imports = True)
    sio.savemat(dirData + name + '.mat', {'V':matrix})

def txtToMat(filename):
    print('Try converting ', filename)
    name = filename.split('.')[0] # Little hack to get the filename
    matrix = utils.loadLabelList(dirData + filename)
    sio.savemat(dirData + name + '.mat', {'y':matrix})

if __name__ == "__main__":
    main()
    