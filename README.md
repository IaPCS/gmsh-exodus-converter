# gmsh-exodus-converter
Converts a mesh written with gmsh to the exodus II format to use it with Peridigm

Usage:

python convert.py -i input.msh -o output.g t <type>

## Requirements

- VTK Toolkit >= 5.8 (with python bindings)

## Supported gmsh element types

2D

- 2 3-node triangle 
- 3 4-node quadrangle

## gmsh format
Description of the gmsh format and how it works. An example can be found [here](https://github.com/diehlpk/gmsh-exodus-converter/blob/master/test_files/specimen_typeI_nogroups.msh).
The _[brackets]_ contain comments expanations about each line. More complex files can be found, refer to the [gmsh documentation](http://www.geuz.org/gmsh/doc/texinfo/gmsh.html#MSH-ASCII-file-format) in that case.

###### Mesh format
```
$MeshFormat
2.2 0 8
$EndMeshFormat
```

###### Nodes

`$Nodes` _[The start-tag **$Nodes** anounces that the nodes are going to be listed]_

`148` _[Number of nodes]_

`1 2.5 9.5 49.6423745119` _[Node number] [Element node point 1] [Elmnt node pt2] [Elmnt node #pt3]_
```
2 2.5 6.5 28.5
3 -2.5 9.5 49.6423745119
4 -2.5 6.5 28.5
...
```
`$EndNodes` _[The end-tag **$EndNodes** anounces that the node list is over]_

###### Elements

`$Elements` _[The start-tag **$Elements** anounces that the elements are going to be listed]_

`729` _[Number of elements]_

`1 15 2 0 1 1` _[Element number] [Elmnt type] [Elmnt tag] [Elmnt point 1] [Elmnt pt 2] [Elmnt pt 3]_
```
2 15 2 0 2 2
3 15 2 0 3 3
4 15 2 0 4 4
5 15 2 0 5 5
...
```
`$EndElements` _[The end-tag **$EndElements** anounces that the Elements list is over]_

## Example

Mesh generated with gmesh | Exodus geometry visualized with paraview
:------------------------:|:----------------------------------------:
![Mesh](./doc/example_mesh_1.png?raw=true "Mesh generated with gmesh")|![Exodus](./doc/example_exodus_1.png?raw=true "Mesh generated with gmesh")
