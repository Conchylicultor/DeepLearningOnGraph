"""
Reduce the mesh number of vertices and faces (compress the mesh)
Load and save in .off format
Use a modify version of Khaled Mamou program for the mesh reduction (BSD Licence)
https://github.com/kmammou/MeshDecimation

The modifications are just to allow the program to save in .off instead
of .obj (Warning: the starting index for the face are not the same)


Just indicate the parameters and target directories.

Use python 3 (but should be working with python 2)
"""

import os, sys

# Set directories
root = os.getcwd()
pathReductionTool = root + '/../Tools/MeshDecimation/src-build/MeshSimplification'
dirDataIn = root + '/../MeshsegBenchmark-1.0/data/off/'
dirDataOut = root + '/../MeshsegBenchmark-1.0/data/off_decimated/'

# Program parameters
maxDecimationError = 1.0 # Float
targetVertices = 1000 # Integer
targetFaces = 500


def main():

    # Global check
    if not os.path.exists(dirDataIn):
        raise IOError('Cannot find dirDataIn: ', dirDataIn)
    if not os.path.exists(dirDataOut):
        raise IOError('Cannot find dirDataOut: ', dirDataOut)
    
    # For each file
    filesList = os.listdir(dirDataIn)
    for filename in filesList:
        if filename.endswith('.off'): # Candidate
            print('Try reducing ', filename)
            fileIn = dirDataIn + filename
            fileOut = dirDataOut + filename
            cmd = "%s %s %d %d %f %s" % (pathReductionTool, fileIn, targetVertices, targetFaces, maxDecimationError, fileOut)
            print(cmd)
            os.system(cmd)


if __name__ == "__main__":
    main()
    