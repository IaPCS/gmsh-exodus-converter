#encoding = utf8

from vtk import vtkExodusIIWriter
from vtk import vtkUnstructuredGrid, VTK_TRIANGLE, VTK_TETRA
from vtk import  vtkIdList, vtkPoints 
import re

mes = "./test_files/specimen_typeI_nogroups.msh"

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

	#To start counting at zeor, initial value must be -1
	amount = -1
	amountCells = -1

	points = []
	cells = []	
	i = -1
	j = -1

	print "meshFile:", meshFile

	for line in meshFile:
		
		#Reads lines between gmsh start-tag $Nodes and end-tag $EndNodes
		#The nodes variable is a flag
		if nodes == 2:
                        line = re.sub("\n", "", line)
                        splitted = line.split(' ')
			#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
			#I do not understand why the following line is necessary, is it just a verification?
			#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
			### We just need the last 3 splitted elements so I used the command *splitted[j][-3:]* to extract the 3 last elements 
                        if len(splitted) == 4:
				#Storing each Node line in a list. Each list elements contains 3 elements which are the node points.
				points.append(splitted[-3:])
				
				#The following lines are for debugging purposes
				#i = i + 1
				#print "Original:", line
				#print "Read/Stored by script:", points[i]
				#print "Using -3", splitted[-3:]
				#print
		
		if nodes == 1:
			nodes = 2
			amount = int(line)
		#If the line is gmsh start-tag $Nodes, the flag-variable *nodes* is set to 2
		#This way the next loop will start recording node values	
		if re.sub("\n", "", line) == "$Nodes":
			nodes = 1
		#If the line is gmsh end-tag $Nodes, set the flag-variable *nodes* to 3
		if re.sub("\n", "", line) == "$EndNodes":
                        nodes = 3

		#The pattern is similar to the previous part for nodes
		#A flag-variable *cell* is setup to determine if we are in the $Elements block of the gmesh or not
		if cell == 2:
                        line = re.sub("\n", "", line)
                        splitted = line.split(' ')
			
			#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
			# The structure of $Elements in gmsh is given by the following:
			#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
			# $Elements
			# number-of-elements
			# elm-number elm-type number-of-tags < tag > ... node-number-list
			# $EndElements
			#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
			### We just need the *node-number-list* so I used the command *cells[j][-3:]* to extract the last elements instead of separating 
			### the 2 cases *len(splitted) == 7* or *len(splitted) == 8*
                        if len(splitted) == 7:
				cells.append(splitted[-3:])

				#The following lines are for debugging pruposes
				#j = j + 1
				#print "Original:", line
				#print "Read/Store by script:", cells[j]
				#print "Using -3", splitted[-3:]
				#print 

			### XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
			### XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
			# I think that with *splitted[-3:]* we do not need to separate *len(splitted) == 7* or *len(splitted) == 8*
			if len(splitted) == 8:
				cells.append(splitted[-3:])

				#The following lines are for debugging pruposes
				j = j + 1
				#print "Original:", line
				#print "Read/Store by script:", cells[j]
				#print "Using -3", splitted[-3:]
				#print 

		#If the line is the gmsh start-tag $Elements, the flag-variable *cell* is set to 2
		#This way the next loop will start recording node values
		#The first line of the $Elements block in gmsh contains the number of cell elements
		if cell == 1:
			cell = 2
			amountCells = int(line)
		#If the line is gmsh start-tag $Elements, the flag-variable *cell* is set to 1
		#This way the next loop will start recording node values
		if re.sub("\n", "", line) == "$Elements":
			cell = 1
		#If the line is gmsh start-tag $Elements, the flag-variable *cell* is set to 3
		#This way the next loop will stop recording node values
		if re.sub("\n", "", line) == "$EndElements":
                        cell = 3
				

	print "Number of cells/elements:", len(cells), "Amount of cells/elements:", amountCells 
	print "Number of nodes:", len(points) , "Amount of nodes:", amount
readMesh(mes)
