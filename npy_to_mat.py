"""
Convert the .npy into .mat (for plotting into matlab)

Just indicate the input and output directory.

Use python 3 (but should be working with python 2)
"""

import os, sys
import numpy as np
import scipy.io as sio

# Set directories
root = os.getcwd()
dirData = root + '/../Data/Meshs/'


def main():

    # Global check
    if not os.path.exists(dirData):
        raise IOError('Cannot find dirData: ', dirData)
    
    # For each file
    filesList = os.listdir(dirData)
    for filename in filesList:
        if filename.endswith('.npy'): # Candidate
            print('Try converting ', filename)
            name = filename.split('.')[0] # Little hack to get the filename
            matrix = np.load(dirData + filename, fix_imports = True)
            sio.savemat(dirData + name + '.mat', {'M':matrix})


if __name__ == "__main__":
    main()
    