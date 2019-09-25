#!/usr/bin/python3

# I can't believe I have to do this, but this is for pre-processing a text file
# of IC package pad/pin names before I can hand it to Eagle's garbage ULP system.
# Did I mention ULP sucks?  No pointer operators... no * or &, and no decent string
# operators (e.g. strip() trim() etc)

import sys
import os

def fileExists(filename):
    fnames = os.listdir()
    if filename in fnames:
        return True
    else:
        return False

def readinput(infilename):
    inf = open(infilename, 'r')
    line = True
    pads = []
    names = []
    array = []
    while line:
        line = inf.readline()
        if line == "":
            line = False
            break
        #Hack!
        if line.startswith("Total"):        # This hack helps me get around the last line of the Xilinx file which says "Total number of pins: " etc.
            continue
        #EndHack!
        temp = line.split()
        if len(temp) > 1:
            pad, name = temp[0:2]
            if name in names:
                if name != "NC":            # We'll leave the 'NC' pins alone
                    name = name + "@" + pad
            pads.append(pad)
            names.append(name)
            temp[0] = pad
            temp[1] = name
            array.append(' '.join(temp))
        else:
            array.append(' '.join(line.split()))
    return array

def copyFiltered(infilename, outfilename, overwrite = False):
    if fileExists(outfilename):
        if not overwrite:
            print("Output file already exists.  Use -o to overwrite")
            return
    if not fileExists(infilename):
        print("File not found: {}".format(infilename))
        return

    array = readinput(infilename)

    outf = open(outfilename, 'w')
    for line in array:
        outf.write(line + "\n")
    outf.close()

    # line = True
    # while line:
        # line = inf.readline()
        # if line == "":
            # line = False
            # break
        # #Hack!
        # if line.startswith("Total"):        # This hack helps me get around the last line of the Xilinx file which says "Total number of pins: " etc.
            # continue
        # #EndHack!
        # outf.write(' '.join(line.split()) + "\n")
    # inf.close()
    # outf.close()
    return

def main():
    overwrite = False
    if len(sys.argv) > 2:
        infilename = sys.argv[1]
        outfilename = sys.argv[2]
        if len(sys.argv) > 3:
            if sys.argv[3] == '-o':
                overwrite = True
        print("Input file: {}\nOutput file: {}".format(infilename, outfilename))
        copyFiltered(infilename, outfilename, overwrite)
    else:
        print("Usage: PRE...py InFile.txt OutFile.txt [-o]")

if __name__ == "__main__":
    main()
