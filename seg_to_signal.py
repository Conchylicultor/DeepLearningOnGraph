"""
Generate training signals and the segmentation files (used for 
visualisation) from the labels

Just indicate the input and output directory.

Use python 3 (but should be working with python 2)
"""

import os, sys
import numpy as np
import utils

# Set directories
root = os.getcwd()
dirInSegmentation = root + '/../MeshsegBenchmark-1.0/data/seg/Bench_decimated/'
dirOutSignal = root + '/../Data/Signals_decimated/'


def main():

    # Global check
    assert(os.path.exists(dirInSegmentation))
    assert(os.path.exists(dirOutSignal))
    
    # For each mesh
    labelsFilesList = utils.sortFiles(os.listdir(dirInSegmentation))
    for labelsFilename in labelsFilesList:
        print('Generate signal for ', labelsFilename)
        idMesh = labelsFilename.split('.')[0] # Little hack to get the id
        
        # Eventually create the subfolder where to put the signal
        dirOutCurrentSignal = dirOutSignal + idMesh + '/'
        if not os.path.exists(dirOutCurrentSignal):
            os.makedirs(dirOutCurrentSignal)
        
        # Extract
        labelList = utils.loadLabelList(dirInSegmentation + labelsFilename)
        
        # Generate some signal files
        generateSignal(labelList, idMesh)


def generateSignal(labelList, idMesh):
    """
    Generate the input files
    Multiples files can be generated (signals and seg files)
    
    Warning: The subfolder name has to be consistent with the one describe in 
    the main function

    Args:
        labelList: list of the labels
        idMesh: name of the mesh filename to save
    Returns:
        Array of the index of each vertex
    """
    
    # Generate some signal files
    numberCategory = max(labelList) + 1 # Number of labels
    for i in range(numberCategory):
        # Check if at least 1 of the current label is present (ex: mesh with no arm), skip if otherwise
        if i in labelList:
            print('Generate signal for label ', i)
            
            # Generate the signal (1 for current label, 0 otherwise)
            currentSignal = np.zeros((len(labelList), 1)) # Copy the signal we will modify (no need for deepcopy here)
            currentSignal[labelList == i] = 1
            currentSignal[labelList != i] = 0
            
            # Record the signal (On the subfolder)
            # We do not subsample the signal here (to generate more training sample) but we do it when loading the training sample
            utils.saveLabelList(currentSignal, dirOutSignal + '%s/%s_%d.txt' % (idMesh, idMesh, i))
        else:
            print ('Warning: skip idx ', i, ' for the mesh ', idMesh, ' (Not existant)')
        

if __name__ == "__main__":
    main()
    