#!/usr/bin/env python3

import sys
from itertools import permutations
from time import time
import os

def usage(status):
    print("Usage Error:")
    print("\t ./TravelingSaleman [$File/s]")
    sys.exit(status)


'''
First line of each case starts with a c followed by:
    a test case number
    an h for hamiltonian
2nd line  starts with a p
    followed by a u (undirected) or d (directed)
    followed by the number of variables
    followed by the number of edges
following lines are of two types
    starts with a v, followed by a list of the names of the vertices
    starts with an e, followed by the source vertex, followed by the target vertex (note for undirected graphs there is an edge going the other way)
'''


class hamiltonian:
    def __init__(self, hpath, case_no):
        self.is_hpath = hpath
        self.ncase = case_no

        self.verts = []
        self.edges = []

        self.nedges = 0
        self.nverts = 0

        self.undirected = False
        self.result = False
        self.time = 0
    
def file_read(file, hpaths):
    with open(file, 'r') as file:
        for line in file:

            #get rid of newline
            line = line.strip()

            #beginning of new graph
            if line.startswith("c"):
                #ex: c, 1, h
                c_num, is_path = line.split(",")[1:]
                if is_path == 'h':
                    hpaths.append(hamiltonian(True, int(c_num))) 
                else:
                    hpaths.append(hamiltonian(False, int(c_num)))
            
            elif line.startswith('p'):
                #ex: p, u, 1, 0
                undirected, nvars, nedges = line.split(",")[1:]

                if undirected == "u":
                    hpaths[-1].undirected = True
                else:
                    hpaths[-1].undirected = False

                hpaths[-1].nverts = int(nvars)
                hpaths[-1].nedges = int(nedges)
            
            #verticies
            elif line.startswith("v"):
                #ex: v, 0, 1, 2
                hpaths[-1].verts = line.split(",")[1:]

            #edges
            elif line.startswith("e"):
                #ex: e, 0, 1
                vert1, vert2 = line.split(",")[1:]
                if (hpaths[-1].undirected == True):
                    hpaths[-1].edges.append((vert1, vert2))
                    hpaths[-1].edges.append((vert2, vert1))
                else:
                    hpaths[-1].edges.append((vert1, vert2))
                    

def hpath_dump(hpath):
    print(f'Case: {hpath.ncase}')
    #print(f'verts: {hpath.verts}')
    #print(f'edges: {hpath.edges}')
    print(f'Number Verts: {hpath.nverts}')
    print(f'Result: {hpath.result}')
    print(f'Expected: {hpath.is_hpath}')
    print(f'Time: {hpath.time}')
    print()

def is_hpath(hpath):
    start = time()

    #edge case
    if hpath.nverts == 1:
        hpath.result = True
        hpath.time = time() - start
        return

    for path in permutations(hpath.verts):
        for i in range(hpath.nverts - 1):
            if (path[i], path[i+1]) not in (hpath.edges):
                break
            
            if i == hpath.nverts - 2:
                hpath.result = True
                hpath.time = time() - start
                return
    
    hpath.time = time() - start
    return

def write_file(hpath, file):
    data = f'{hpath.ncase},{hpath.nverts},{hpath.is_hpath},{hpath.time}\n'
    file.write(data)



def main(args=sys.argv[1:]):
    hpaths = []

    if not args:
        usage(1)

    file = args[0]
    if not os.path.isfile(file):
        print("File does not exist")
        usage(1)
    
    #read file and make edges and verts
    file_read(file, hpaths)
    
    #find ham path, and time
    with open("data.csv", "w") as file:
        file.write("Case_Number,Number_Nodes,H_Path?,Time\n")
        for hpath in hpaths:
            is_hpath(hpath)
            hpath_dump(hpath)
            
            #writing to csv
            write_file(hpath, file)

    #for hpath, write results to csv
    


if __name__ == "__main__":
    main()