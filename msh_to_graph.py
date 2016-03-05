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

# Set directories
root = os.getcwd()
dirMeshData = root + '/../MeshsegBenchmark-1.0/data/off/'
dirOut = root + '/../Data/Meshs/npy/'

def main():

    # Global check
    if not os.path.exists(dirMeshData):
        raise IOError('Cannot find dirMeshData: ', dirMeshData)
    if not os.path.exists(dirOut):
        raise IOError('Cannot find dirOut: ', dirOut)
        
    # For each mesh
    meshFilesList = os.listdir(dirMeshData)
    meshFilesList.sort() # Alphabetical order
    for meshFilename in meshFilesList:
        # Generate the graph data
        idMesh = meshFilename.split('.')[0]
        print('Extract mesh ', idMesh)
        meshFilename = dirMeshData + '%s.off' % idMesh
        meshVertices, meshFaces = extractMesh(meshFilename)
        print('Compute point cloud...')
        pointCloud = meshToPointCloud(meshVertices, meshFaces)
        print('Create graph...')
        graph = pygsp.graphs.NNGraph(pointCloud, NNtype='radius', center=True, rescale=True, epsilon=0.2)
        #graph = pygsp.graphs.NNGraph(pointCloud) > Use KNN, much faster
        print('Generate laplacian...')
        graph.create_laplacian('normalized')
        
        # Save result
        print('Saving...')
        baseSaveName = dirOut + idMesh
        np.save(baseSaveName + '_cloud.npy', pointCloud, fix_imports=True)
        np.save(baseSaveName + '_graph.npy', graph.W, fix_imports=True)
        np.save(baseSaveName + '_laplacian.npy', graph.L, fix_imports=True) # fix_imports set to allow retrocompatibility with python 2
        
        # Plot
        #pygsp.plotting.plot_pointcloud(pointCloud)
        #input("Press Enter to continue...")
        #graph.plot()
        #input("Press Enter to continue...")

def extractMesh(meshFilename):
    """
    Extract the mesh informations from the file

    Args:
        meshFilename: path of the mesh file (.off format only !!)
    Returns:
        vertices: Array of the x,y,z position of each mesh points
        faces: Array of the vertex indexes of each triangle
    """
    
    # Open the file
    print('Open file ', meshFilename)
    meshFile = open(meshFilename, 'r')
    lines = meshFile.readlines()
    meshFile.close()

    # Initialisation and global information
    meshCount = lines[1].split()
    vertexCount = int(meshCount[0])
    faceCount = int(meshCount[1])
    edgeCount = int(meshCount[2])
    print('Mesh: ', vertexCount, ' vertices, ', faceCount, ' faces, ', edgeCount, ' edges')
    
    vertices = []
    faces = []
    
    # For each line of the file
    for line in lines[2:]: # Skip the first two lines (OFF and number of vertices)
        words = line.split()
    
        if len(words) == 3: # Read points
            # Save each point coordinates in an array
            vertices.append([float(words[0]), float(words[1]), float(words[2])])
        elif len(words) == 4: # Read triangles >> vertex
            faces.append([int(words[1]), int(words[2]), int(words[3])])
        
    if len(vertices) != vertexCount:
        print('Error: Number of vertices does not matches')
    if len(faces) != faceCount:
        print('Error: Number of faces does not matches')
        
    return vertices, faces
    
def meshToPointCloud(meshVertices, meshFaces):
    """
    Compute the point clouds informations from the mesh informations

    Args:
        vertices: Array of the x,y,z position of each mesh points
        faces: Array of the vertex indexes of each triangle
    Returns:
        A weighted graph
    """
    
    Xin = np.zeros((len(meshFaces), 3))
    
    for i, face in enumerate(meshFaces):
        # Compute the circumcenter of the triangle
        
        A = np.array(meshVertices[face[0]])
        B = np.array(meshVertices[face[1]])
        C = np.array(meshVertices[face[2]]) # Triangle coordinates
        
        AC = C - A
        AB = B - A
        ABxAC = np.cross(AB, AC)
        
        n = np.cross(ABxAC, AB) * np.linalg.norm(AC)**2  +  np.cross(AC, ABxAC) * np.linalg.norm(AB)**2
        d = 2.0 * np.linalg.norm(ABxAC)**2
        
        center = A + n/d
        
        Xin[i,:] = center
    
    return Xin

if __name__ == "__main__":
    main()
    