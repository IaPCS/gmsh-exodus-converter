# gmsh-exodus-converter
Converts a mesh written with gmsh to the exodus II format, which is used in common simulations tools, like [Peridigm](https://peridigm.sandia.gov/)

Usage:

`python convert.py -i input.msh -o output.g -t element_type`

element_type is an integer (see **Supported gmsh element types** section)

## Requirements

- VTK Toolkit >= 5.8 (with python bindings)

## Supported gmsh element types

The `input.msh` file must be generated with Gmsh. Currently, only the following elements are supported:

2D

- 2 = 3-node triangle 
- 3 = 4-node quadrangle

3D

- 4 = 4-node tetrahedron

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

For detailed information, check [this section of gmsh documentation](http://geuz.org/gmsh/doc/texinfo/gmsh.html#MSH-ASCII-file-format)

`$Elements` _[The start-tag **$Elements** anounces that the elements are going to be listed]_

`729` _[Number of elements]_

`1 15 2 0 1 1` _[Element number] [Elmnt type] [Elmnt physical entity tag] [Elmnt Geometry point] [Vertex tag]_
```
2 15 2 0 2 2
3 15 2 0 3 3
4 15 2 0 4 4
5 15 2 0 5 5
...
```
`$EndElements` _[The end-tag **$EndElements** anounces that the Elements list is over]_

###### Element types

- 1  = 2-node line
- 2  = 3-node line
- 3  = 4-node quadrangle
- 4  = 4-node tetrahedron
- 15 = 1-node point

## Example

2D

Mesh generated with gmesh | Exodus geometry visualized with paraview
:------------------------:|:----------------------------------------:
![Mesh](./doc/example_mesh_1.png?raw=true "Mesh generated with gmesh")|![Exodus](./doc/example_exodus_1.png?raw=true "Mesh generated with gmesh")

3D

Mesh generated with gmesh | Exodus geometry visualized with paraview
:------------------------:|:----------------------------------------:
![Mesh](./doc/3D_Cube_gmsh.png?raw=true "Mesh generated with gmesh")|![Exodus](./doc/3D_Cube_exodusII.png?raw=true "Mesh generated with gmesh")
