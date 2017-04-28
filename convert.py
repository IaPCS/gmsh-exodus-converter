#encoding = utf8
"""
Converter for gmesh meshs to Exodus II grids
@date 2015-08-03
@author me@diehlpk.de
@author ilyass.tabiai@gmail.com

 Usage: python convert.py -i mesh_file -o exodus_file -t type
"""
import gmshexodusconverter.mesh as mesh 
import sys
import getopt

def main(argv):
    """
    Main
    """
    path = ''
    output = ''
    helpText = "convert.py -i <inputfile> -o <outputfile>\n"
    if len(sys.argv) != 5:
        print helpText
        sys.exit(1)

    try:
        opts, args = getopt.getopt(
            argv, "hi:o:", ["ifile=", "ofile="])
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

    mesher = mesh.GmshExodusConverter()
    points, cells, cellTypes = mesher.readMesh(path)
    mesher.writeExodusIIGrid(output, points, cells, cellTypes)

if __name__ == "__main__":
    main(sys.argv[1:])
