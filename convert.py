#encoding = utf8
"""
Converter for gmesh meshs to Exodus II grids
@date 2015-08-03
@author me@diehlpk.de
@author ilyass.tabiai@gmail.com

 Usage: python convert.py -i mesh_file -o exodus_file -t type
"""
from vtk import vtkExodusIIWriter
from vtk import vtkUnstructuredGrid, VTK_TRIANGLE, VTK_QUAD, VTK_LINE, VTK_TETRA
from vtk import vtkIdList, vtkPoints
from vtk import vtkVersion
import re
import sys
import getopt


def setInput(meshX, writerExodusII):
    """
    Method compensates for python-vtk for backward incompatiblity
    Checks the vtk version and uses SetInput() for version 5
    or SetInputData() for version 6

    Args: mesh object, writerExodusII

    Returns:
        func: SetInput() for python-vtk version 5
                or SetInpurData() for python-vtk6
    """
    vtk_version = vtkVersion.GetVTKSourceVersion()
    vtk_version_split = re.findall(r"\b\d+\b", vtk_version)
    if int(vtk_version_split[0]) == 5:
        return writerExodusII.SetInput(meshX)
    else:
        return writerExodusII.SetInputData(meshX)


def allUnique(values):
    """
    Method checks if all entries in x are unique
        x (list): entries to be checked

    Returns:
        bool: Is unique

    """
    seen = set()
    return not any(i in seen or seen.add(i) for i in values)


def writeExodusIIGrid(path, points, cellNodes, case):
    """ 
    Methods writes the points and the cells in the Exodus II file format

    Args:
        path (string): The path where to write the Exodus II mesh
        points (list): The coordinates of the nodes of the grid
        cellNodes (list): The indices of the points to define the mesh
        case (int) The type of the vtk cells
                1 = VTK_LINE
                2 = VTK_TRIANGLE
                3 = VTK_QUAD
                4 = VTK_TETRA 	
    """
    mesh = vtkUnstructuredGrid()
    vtk_points = vtkPoints()
    for point in points:
        vtk_points.InsertNextPoint(
            float(point[0]), float(point[1]), float(point[2]))
    mesh.SetPoints(vtk_points)

    for cellNodes in cellNodes:
        pts = vtkIdList()
        num_local_nodes = len(cellNodes)
        pts.SetNumberOfIds(num_local_nodes)
        for k, node_index in enumerate(cellNodes):
            pts.InsertId(k, int(node_index) - 1)

        if case == '1':
            mesh.InsertNextCell(VTK_LINE, pts)
        if case == '2':
            mesh.InsertNextCell(VTK_TRIANGLE, pts)
        if case == '3':
            mesh.InsertNextCell(VTK_QUAD, pts)
        if case == '4':
            mesh.InsertNextCell(VTK_TETRA, pts)
    writer = vtkExodusIIWriter()
    writer.WriteAllTimeStepsOn()
    writer.SetFileName(path)
    setInput(mesh, writer)
    writer.Write()


def readMesh(path, cellType):
    """
    Methods reads a file in the mesh format and returns
    all nodes and cells inside this file

    Args:
        path (string:) The path to the mesh, including the file name

    Returns:
        points (list) The coordiantes of the nodes
        cells (list) The cells of the mesh
    """
    meshFile = open(path, 'r')
    nodes = 0
    cell = 0

    amount = -1
    amountCells = -1

    points = []
    cells = []

    for line in meshFile:

        if nodes == 2:
            line = re.sub("\n", "", line)
            splitted = line.split(' ')
            if len(splitted) == 4:
                # Extraction the coordiantes
                points.append(splitted[-3:])

        if nodes == 1:
            # Amount of coordiantes found
            nodes = 2
            amount = int(line)
        # Node are listed
        if re.sub("\n", "", line) == "$Nodes":
            nodes = 1
        # All nodes are read
        if re.sub("\n", "", line) == "$EndNodes":
            nodes = 3

        # Reading the cell information
        if cell == 2:
            line = re.sub("\n", "", line)
            splitted = line.split(' ')

            if len(splitted) > 2:
                # Case: 1 - 2-node line
                if splitted[1] == '1' and cellType == '1':
                    if allUnique(splitted[-2:]):
                        cells.append(splitted[-2:])
                # Case: 2 - 3-node triangle
                if splitted[1] == '2' and cellType == '2':
                    if allUnique(splitted[-3:]):
                        cells.append(splitted[-3:])

                # Case: 3 - 4-node quadrangle
                if splitted[1] == '3' and cellType == '3':
                    if allUnique(splitted[-4:]):
                        cells.append(splitted[-4:])
                # Case: 4 - 4-node tetrahedron
                if splitted[1] == '4' and cellType == '4':
                    if allUnique(splitted[-4:]):
                        cells.append(splitted[-4:])
        # Amount of cells found
        if cell == 1:
            cell = 2
            amountCells = int(line)
        # Cell information tag found
        if re.sub("\n", "", line) == "$Elements":
            cell = 1
        # Cell information closing tag found
        if re.sub("\n", "", line) == "$EndElements":
            cell = 3
    # ErrorHandling
    if amount == -1:
        print "Error: No nodes where found in the mesh file: " + str(path)
        sys.exit(1)
    if amountCells == -1:
        print "Error: No cells were found in the mesh file: " + str(path)
        sys.exit(1)
    if len(points) != amount:
        print "Error: Amount of readed nodes != amount of nodes:" + str(path)
        sys.exit(1)

    return points, cells


def main(argv):
    """
    Main	
    """
    types = ['1', '2', '3', '4']
    path = ''
    output = ''
    cellType = -1
    helpText = "convert.py -i <inputfile> -o <outputfile> -t <type> \n" \
        "1 = 2-node line \n 2 = 3-node triangle \n 3 = 4-node quadrangle"
    if len(sys.argv) != 7:
        print helpText
        sys.exit(1)

    try:
        opts, args = getopt.getopt(
            argv, "hi:o:t:", ["ifile=", "ofile=", "type="])
    except getopt.GetoptError:
        print helpText
        sys.exit(0)

    for opt, arg in opts:
        if opt == '-h':
            print helpText
            sys.exit(0)
        elif opt in ("-i", "--ifile"):
            path = arg
        elif opt in ("-o", "--ofile"):
            output = arg
        elif opt in ("-t", "--type"):
            cellType = arg
    if cellType not in types:
        print "Error: Only geometrical type 1,2,3 are supported see convert.py -h"
        sys.exit(1)
    points, cells = readMesh(path, cellType)
    writeExodusIIGrid(output, points, cells, cellType)

if __name__ == "__main__":
    main(sys.argv[1:])
