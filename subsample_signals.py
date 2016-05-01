"""
Subsample the signals files to demultipliate the number of
training samples.
This is the script which generate the dataset training and
testing samples (before convertion)

Warning: Be careful to the natural orders of the files (the labels
must be on the same order than the file lists). Same for the conversion
to lua (orders must correspond too)
Warning: In the current version, all categories must be present (there
cannot be a model without an arm for instance). No skipped allowed

Just indicate the input and output directory.

Use python 3 (but should be working with python 2)
"""

import os, sys
import random
import numpy as np
import scipy.io as sio
import utils

# Set directories
root = os.getcwd()
dirInSignals = root + '/../Data/Test_mesh_01/signals/'
dirOutSamples = root + '/../Data/Test_mesh_01/samples/'
dirOutSamplesTr = dirOutSamples + 'tr/'
dirOutSamplesTe = dirOutSamples + 'te/'

ratioSubsampling = 80 # 0 > no subsampling, 100 > full subsampling


def main():
    
    # Global check
    assert(os.path.exists(dirInSignals))
    assert(os.path.exists(dirOutSamples))
    assert(os.path.exists(dirOutSamplesTr))
    assert(os.path.exists(dirOutSamplesTe))
    
    # Training and testing labels
    labelsListTr = []
    labelsListTe = []
    
    # For each mesh
    signalsFilesList = utils.sortFiles(os.listdir(dirInSignals)) # Warning: Natural order important
    categoryId = 0 # TODO: Should be extracted from the filename
    for signalFilename in signalsFilesList: # One file correspond to one category (class)
        # Load signal
        print('Subsample ', signalFilename)
        idSignal = signalFilename.split('.')[0] # Little hack to get the id
        completeSignal = utils.loadLabelList(dirInSignals + signalFilename)
        
        # Training subsampling
        # Randomly remove signals from categories
        # For each signal, we generate multples samples
        print('Training...')
        for i in range(500): # TODO: Tune this variable (dynamically depend of the signal ?)
            decimatedSignal = np.copy(completeSignal)
            for j in range(len(completeSignal)): # Iterate over
                if completeSignal[j] == 1: # Candidate for subsampling
                    if random.randrange(100) < ratioSubsampling: # x% chance of removal
                        decimatedSignal[j] = 0 # Subsample
            utils.saveLabelList(decimatedSignal, dirOutSamplesTr + idSignal + '_' + str(i) + '.txt') # Save (Warning: the natural order must correspond to the label list order)
            sio.savemat(dirOutSamplesTr + idSignal + '_' + str(i) + '.mat', {'y':decimatedSignal})
            labelsListTr.append(categoryId) # Add the category of the label (Warning: No categories skippables !!!)
            
        # Testing subsampling
        # Only one vertex active, the rest of zeroes
        print('Testing...')
        for j in range(len(completeSignal)): # Iterate over the signal
            if completeSignal[j] == 1: # Candidate for subsampling
                decimatedSignal = np.zeros(completeSignal.shape) # Only zeroes
                decimatedSignal[j] = 1 # Except for the current signal
                utils.saveLabelList(decimatedSignal, dirOutSamplesTe + idSignal + '_' + str(j) + '.txt')
                sio.savemat(dirOutSamplesTe + idSignal + '_' + str(j) + '.mat', {'y':decimatedSignal})
                labelsListTe.append(categoryId) # Add the category of the label (Warning: No categories skippables !!!)
        
        categoryId += 1 # Next categories

    # Save labels
    utils.saveLabelList(labelsListTr, dirOutSamples + 'trlabels.txt')
    utils.saveLabelList(labelsListTe, dirOutSamples + 'telabels.txt')
    sio.savemat(dirOutSamples + 'trlabels.mat', {'labels':np.array(labelsListTr)})
    sio.savemat(dirOutSamples + 'telabels.mat', {'labels':np.array(labelsListTe)})


if __name__ == "__main__":
    main()
    