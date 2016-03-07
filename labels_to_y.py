"""
DEPRECATED: Use seg_to_signal instead !!

Generate training signals and the segmentation files (used for 
visualisation) from the labels

Just indicate the input and output directory.

Use python 3 (but should be working with python 2)
"""

import os, sys
import numpy as np

# Set directories
root = os.getcwd()
dirLabelData = root + '/../MeshsegBenchmark-1.0/data/labels/'
dirOutSegmentation = root + '/../MeshsegBenchmark-1.0/data/seg/Benchmark2/'
dirOutSignal = root + '/../Data/Signals/'


class Category():
    """
    Contain informations of a mesh category (plane, human, ant,...)
    """
    def __init__(self):
        self.name = "" # Name of the categories
        self.min = 0
        self.max = 0 # Idx of the mesh
        self.labels = [] # List of the labels

def main():

    # Global check
    if not os.path.exists(dirLabelData):
        raise IOError('Cannot find dirLabelData: ', dirLabelData)
    if not os.path.exists(dirOutSegmentation):
        raise IOError('Cannot find dirOutSegmentation: ', dirOutSegmentation)
    if not os.path.exists(dirOutSignal):
        raise IOError('Cannot find dirOutSignal: ', dirOutSignal)
        
    # First, extract the labels idx for each category
    labelsFile = open(root + '/labelsIdx.txt', 'r')
    lines = labelsFile.readlines()
    labelsFile.close()
    
    categories = []
    i = 0 # Current category
    for line in lines:
        words = line.split()
        if len(words) == 3: # New category
            print('Category: ', words[0])
            newCategory = Category()
            newCategory.name = words[0]
            newCategory.min = int(words[1])
            newCategory.max = int(words[2])
            categories.append(newCategory) # Add a new categories
            i = i+1
        if len(words) == 1: # Label name
            print('Label: ', words[0])
            categories[i-1].labels.append(words[0])
        else:
            pass
    print(len(categories), ' categories detected.')
    
    # For each labels
    labelsFilesList = os.listdir(dirLabelData)
    for labelsFilename in labelsFilesList:
        idMesh = int(labelsFilename.split('_')[0]) # Little hack to get the id
        idCategory = -1
        for i, category in enumerate(categories):
            if idMesh <= category.max and idMesh >= category.min:
                idCategory = i
        assert idCategory != -1, 'Error: no corresponding category for the mesh %d' % idMesh
        
        # Extract
        labelList = readLabels(dirLabelData + labelsFilename, categories[idCategory])
        
        # Save result
        saveLabels(labelList, idMesh)


def readLabels(labelsFilename, category):
    """
    Extract the labels informations from the file

    Args:
        labelsFilename: path of the label file
    Returns:
        Array of the index of each vertex
    """
    
    # Open the file
    print('Open file ', labelsFilename)
    print('Category: ', category.name)
    labelsFile = open(labelsFilename, 'r')
    lines = labelsFile.readlines()
    labelsFile.close()
    
    # Extract rows
    labelIdx = -1
    #labelsArray = [[] for i in range(len(category.labels))]
    labelsArray = len(category.labels) * [[]]
    for line in lines:
        words = line.split()
        if len(words) == 1: # Label name
            labelIdx = category.labels.index(words[0])
        else:
            row = []
            for word in words:
                row.append(int(word))
            labelsArray[labelIdx] = row
            
    ## Sort the rows (same for everyone)
    ## TODO: Manually associate labels with name for each of the category (get category online,
    ## reacord the category on a text file and compare it to have the right id) !!!!!!!
    #points = zip(labelsNameArray, labelsArray)
    #sorted_points = sorted(points)
    #labelsNameArray = [point[0] for point in sorted_points]
    #labelsArray = [point[1] for point in sorted_points]
    
    #print('Extracted labels: ', labelsNameArray)
        
    # Merge the rows
    totalLen = 0
    for subList in labelsArray:
        for i in subList:
            if i > totalLen:
                totalLen = i
    print ('Nb total of element', totalLen)
    labelList = np.zeros(totalLen, dtype=np.uint8) # Prealocate
    # WARNING: Due to the dtype=np.uint8, there cannot be more than 255 label categories
    
    for i in range(len(labelsArray)):
        for j in range(len(labelsArray[i])):
            labelList[labelsArray[i][j] - 1] = i
    
    return labelList

def saveLabels(labelList, idMesh):
    """
    Generate the input files
    Multiples files can be generated (signals and seg files)

    Args:
        labelList: list of the labels
        idMesh: name of the mesh filename to save
    Returns:
        Array of the index of each vertex
    """
    # Options
    writeSegmentation = True
    writeSignal = True
    subsample = True
    
    if writeSegmentation:
        # Write the segmentations files (for visualisation)
        segFile = open(dirOutSegmentation + '%d.seg' % idMesh , "w")
        for label in labelList:
            segFile.write('%d\n' % label)
        segFile.close()
    
    if writeSignal:
        # Generate some signal files
        numberCategory = max(labelList) + 1 # Number of labels
        for i in range(numberCategory):
            print('Generate signal for label ', i)
            
            # Generate the signal (1 for current label, 0 otherwise)
            currentSignal = np.zeros(labelList.shape) # Copy the signal we will modify (no need for deepcopy here)
            currentSignal[labelList == i] = 1
            currentSignal[labelList != i] = 0
            
            # Check if at least 1 of the current label is present (ex: mesh with no arm), skip if otherwise
            skip = False
            if max(currentSignal) != 1:
                print('Warning: skip idx ', i, ' for the mesh ', idMesh, ' (Not existant)')
                skip = True
            
            # Record the signal
            if skip == False:
                # TODO: Subsample the signal to generate more training sample
                signalFile = open(dirOutSignal + '%d_%d.txt' % (idMesh, i) , "w")
                for signal in currentSignal:
                    signalFile.write('%d\n' % signal)
                signalFile.close()

if __name__ == "__main__":
    main()
    