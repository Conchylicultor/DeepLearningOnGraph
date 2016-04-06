"""
Some utilities functions used in multiple scripts

Use python 3 (but should be working with python 2)
"""

import os, sys
import numpy as np

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
        A point cloud (list of coordinates)
    """
    
    Xin = np.zeros((len(meshFaces), 3))
    
    for i, face in enumerate(meshFaces):
        # Compute the centroid of the triangle
        
        A = np.array(meshVertices[face[0]])
        B = np.array(meshVertices[face[1]])
        C = np.array(meshVertices[face[2]]) # Triangle coordinates
        
        center = (A + B + C)/3
        Xin[i,:] = center
    
    return Xin

def sortFiles(filesList, startFrom=None):
    """
    Generate an ordered list of files to compute

    Args:
        filesList: The file list to sort (will be modified)
        startFrom: To start from a particular file (avoid recomputing the beginning each times)
    Returns:
        The sorted list
    """
    
    filesList.sort() # Alphabetical order
    startIndex = 0
    if startFrom != None:
        startIndex = filesList.index(startFrom) # Raise an exception if not found
    return filesList[startIndex:]

def loadLabelList(filename):
    """
    Load the labels informations from the segmentation file

    Args:
        filename: path of the label file
    Returns:
        Array of the label of each node
    """
    assert filename.endswith('.seg') or filename.endswith('.txt'), 'Wrong file format'
    
    labelList = []
    
    labelsFile = open(filename, 'r')
    lines = labelsFile.readlines()
    labelsFile.close()
    
    # Extract rows
    for line in lines:
        labelList.append(int(line))
    
    return np.asarray(labelList)
    
def saveLabelList(labelList, filename):
    """
    Save the labels informations on a seg file (or signal file)

    Args:
        labelsFilename: Array of the label of each node
        filename: path of the label file
    """
    assert filename.endswith('.seg') or filename.endswith('.txt'), 'Wrong file format'
    
    segFile = open(filename, "w")
    for label in labelList:
        segFile.write('%d\n' % label)
    segFile.close()
