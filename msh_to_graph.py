"""
Generate dataset from mesh meshFilesList

Just indicate the input and output folder by modifying dirMeshData and dirOut.
The mesh have to be from ".off" format
The laplacian generated is normalized

Use python 3 (but should be working with python 2)
"""

import os, sys
import pygsp
import numpy as np
import utils

# Set directories
root = os.getcwd()
dirMeshData = root + '/../MeshsegBenchmark-1.0/data/off_decimated/'
dirOut = root + '/../Data/Meshes_decimated/'
dirOutPlot = root + '/../Data/Plot/'

startFromMesh = '325.off' # Avoid recomputing from scratch (1.off to restart from begining)

def main():

    # Global check
    if not os.path.exists(dirMeshData):
        raise IOError('Cannot find dirMeshData: ', dirMeshData)
    if not os.path.exists(dirOut):
        raise IOError('Cannot find dirOut: ', dirOut)
        
    # For each mesh
    meshFilesList = utils.sortFiles(os.listdir(dirMeshData), startFromMesh)
    for meshFilename in meshFilesList:
        # Generate the graph data
        idMesh = meshFilename.split('.')[0]
        print('Extract mesh ', idMesh)
        meshFilename = dirMeshData + '%s.off' % idMesh
        meshVertices, meshFaces = utils.extractMesh(meshFilename)
        print('Compute point cloud...')
        pointCloud = utils.meshToPointCloud(meshVertices, meshFaces)
        print('Create graph...')
        #graph = pygsp.graphs.NNGraph(pointCloud, NNtype='radius', center=True, rescale=True, epsilon=0.2)
        graph = pygsp.graphs.NNGraph(pointCloud)# > Use KNN, much faster
        print('Generate laplacian...')
        graph.create_laplacian('normalized')
        
        # Save result
        print('Saving...')
        baseSaveName = dirOut + idMesh
        np.save(baseSaveName + '_cloud.npy', pointCloud, fix_imports=True)
        np.save(baseSaveName + '_graph.npy', graph.W, fix_imports=True)
        np.save(baseSaveName + '_laplacian.npy', graph.L, fix_imports=True) # fix_imports set to allow retrocompatibility with python 2
        
        # Save plot
        print('Plotting ', graph.N, ' nodes, ', graph.Ne, ' edges')
        plotSavedName = dirOutPlot + idMesh + '_'
        graph.plot (default_qtg=False, savefig=True, plot_name=plotSavedName + 'graph')
        #input("Press Enter to continue...")

if __name__ == "__main__":
    main()
    