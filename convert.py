#encoding = utf8

from vtk import vtkExodusIIWriter
from vtk import vtkUnstructuredGrid, VTK_TRIANGLE, VTK_TETRA
from vtk import  vtkIdList, vtkPoints 
import re

mes = "./untitled.msh"

def writeExodusIIGrid(path,points,cellNodes):
	mesh = vtkUnstructuredGrid()  
	vtk_points = vtkPoints() 
	for point in points: 
    		vtk_points.InsertNextPoint(point[0], point[1], point[2]) 
	mesh.SetPoints( vtk_points )
	
	for cellNodes in cellsNodes: 
    		pts = vtkIdList() 
    		num_local_nodes = len(cellNodes) 
    		pts.SetNumberOfIds(num_local_nodes) 
    	for k, node_index in enumerate(cellNodes): 
        	pts.InsertId(k, node_index) 
    		mesh.InsertNextCell(VTK_TRIANGLE, pts) 

	writer = vtkExodusIIWriter() 
	writer.WriteAllTimeStepsOn() 
	writer.SetFileName(path) 
	writer.SetInputData(mesh) 
	writer.Write() 

def readMesh(path):

	meshFile = open(path,'r')
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
				points.append([splitted[1],splitted[2],splitted[3]])

		if nodes == 1:
			nodes = 2
			amount = int(line)		
		if re.sub("\n", "", line) == "$Nodes":
			nodes = 1
		if re.sub("\n", "", line) == "$EndNodes":
                        nodes = 3

		if cell == 2:
                        line = re.sub("\n", "", line)
                        splitted = line.split(' ')
                        if len(splitted) == 7:
				cells.append([splitted[4],splitted[5],splitted[6]])
			if len(splitted) == 8:
				cells.append([splitted[5],splitted[6],splitted[7]])
		if cell == 1:
			cell = 2
			amountCells = int(line)		
		if re.sub("\n", "", line) == "$Elements":
			cell = 1
		if re.sub("\n", "", line) == "$EndElements":
                        cell = 3
				

	print len(cells), amountCells 
	print len(points) , amount
readMesh(mes)
