#encoding = utf8
"""
"Converter for gmesh meshs to Exodus II grids
"@date 2015-08-03
"@author me@diehlpk.de
"@author 
"
"Usage: python convert.py -i mesh_file -o exodus_file
"""
from vtk import vtkExodusIIWriter
from vtk import vtkUnstructuredGrid, VTK_TRIANGLE, VTK_TETRA
from vtk import vtkIdList, vtkPoints
import re
import sys
import getopt

def writeExodusIIGrid(path, points, cellNodes):
    """ Methods writes the points and the cells in the Exodus II file format
    "@param path The path including the file name to write the Exodus II mesh
    "@param points The coordinates of the nodes of the grid
    "@param cellNodes The indices of the points to define the triangle of the
    "	mesh
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
            pts.InsertId(k, int(node_index)-1)
        mesh.InsertNextCell(VTK_TRIANGLE, pts)

    writer = vtkExodusIIWriter()
    writer.WriteAllTimeStepsOn()
    writer.SetFileName(path)
    writer.SetInputData(mesh)
    writer.Write()

def readMesh(path):
    """Methods reads a file in the mesh format and returns
    "  all nodes and cells inside this file
    "@param path The path to the mesh, including the file name
    "@return points The coordiantes of the nodes
    "@return cless The cells of the mesh
    """

    meshFile = open(path, 'r')
    nodes = 0
    cell = 0

    amount = -1
    amountCells = -1

    points = []
    cells = []
    i = -1
    j = -1

    for line in meshFile:

        # Reads lines between gmsh start-tag $Nodes and end-tag $EndNodes
        # The nodes variable is a flag
        if nodes == 2:
            line = re.sub("\n", "", line)
            splitted = line.split(' ')
            if len(splitted) == 4:
            # Storing each Node line in a list. Each list
            # elements contains 3 elements which are the node points.
                points.append(splitted[-3:])

        if nodes == 1:
            nodes = 2
            amount = int(line)
        # If the line is gmsh start-tag $Nodes, the flag-variable *nodes* is set to 2
        # This way the next loop will start recording node values
        if re.sub("\n", "", line) == "$Nodes":
            nodes = 1
        # If the line is gmsh end-tag $Nodes, set the flag-variable *nodes* to
        # 3
        if re.sub("\n", "", line) == "$EndNodes":
            nodes = 3

        # The pattern is similar to the previous part for nodes
        # A flag-variable *cell* is setup to determine if we are in the
        # $Elements block of the gmesh or not
        if cell == 2:
            line = re.sub("\n", "", line)
            splitted = line.split(' ')

            if len(splitted) > 2:
                cells.append(splitted[-3:])

        # If the line is the gmsh start-tag $Elements, the flag-variable *cell* is set to 2
        # This way the next loop will start recording node values
        # The first line of the $Elements block in gmsh contains the number of
        # cell elements
        if cell == 1:
            cell = 2
            amountCells = int(line)
        # If the line is gmsh start-tag $Elements, the flag-variable *cell* is set to 1
        # This way the next loop will start recording node values
        if re.sub("\n", "", line) == "$Elements":
            cell = 1
        # If the line is gmsh start-tag $Elements, the flag-variable *cell* is set to 3
        # This way the next loop will stop recording node values
        if re.sub("\n", "", line) == "$EndElements":
            cell = 3
    # ErrorHandling
    if amount == -1:
        print "Error: No nodes where found in the mesh file: " + str(path)
        sys.exit(1)
    if amountCells == -1:
        print "Error: No cells were found in the mesh file: " + str(path)
        sys.exit(1)
    if len(cells) != amountCells:
        print "Error: Amount of readed cells != amount of cells:" + str(path)
        sys.exit(1)
    if len(points) != amount:
        print "Error: Amount of readed nodes != amount of nodes:" + str(path)
        sys.exit(1)

    return points, cells


def main(argv):

    input = ''
    output = ''
    help = "convert.py -i <inputfile> -o <outputfile>"
    if(len(sys.argv) != 5):
    	print help
    	sys.exit(1)

    try:
        opts, args = getopt.getopt(
            argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
    	print help
        sys.exit(0)

    for opt, arg in opts:
        if opt == '-h':
            print help
            sys.exit(0)
        elif opt in ("-i", "--ifile"):
            input = arg
        elif opt in ("-o", "--ofile"):
            output = arg
    points, cells = readMesh(input)
    writeExodusIIGrid(output, points, cells)

if __name__ == "__main__":
    main(sys.argv[1:])
