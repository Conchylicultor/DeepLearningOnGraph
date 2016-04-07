"""
Subsample the signals files to demultipliate the number of
training samples.

Just indicate the input and output directory.

Use python 3 (but should be working with python 2)
"""

import os, sys
import random
import numpy as np
import utils

# Set directories
root = os.getcwd()
dirInSignals = root + '/../Data/Test_mesh_01/signals/'
dirOutSamples = root + '/../Data/Test_mesh_01/samples/'


def main():
    # Global check
    assert(os.path.exists(dirInSignals))
    assert(os.path.exists(dirOutSamples))
    
    # For each mesh
    signalsFilesList = utils.sortFiles(os.listdir(dirInSignals))
    for signalFilename in signalsFilesList:
        # Load signal
        print('Subsample ', signalFilename)
        idSignal = signalFilename.split('.')[0] # Little hack to get the id
        completeSignal = utils.loadLabelList(dirInSignals + signalFilename)
        
        # For each signal, we generate multples samples
        for i in range(500): # TODO: Tune this variable (dynamically depend of the signal ?)
            decimatedSignal = np.copy(completeSignal)
            for j in range(len(completeSignal)): # Iterate over
                if completeSignal[j] == 1: # Candidate for subsampling
                    if random.randrange(2) == 0: # 50% chance of removal
                        decimatedSignal[j] = 0 # Subsample
            utils.saveLabelList(decimatedSignal, dirOutSamples + idSignal + '_' + str(i) + '.txt') # Save


if __name__ == "__main__":
    main()
    