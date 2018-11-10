#import matplotlib.pyplot as plt
#import matplotlib.colors as clr
import numpy as np
from numpy import linalg as LA
#import numpy.linalg.norm as norm
import os
import sys

def label(p):
    return dict[p]

''' Calculate the euclidean distance between two points. '''
def euclidean_distance(p, q):
    dist = ((p[0]-q[0])**2 + (p[1]-q[1])**2)**0.5
    return dist

def range_query(db, dist_func, q, eps):
    neighbours = set()

    #q = np.asarray(q)
    for p in db:
        # TODO: Implement support for multiple distance metrics
        dist = euclidean_distance(p, q)
        if dist <= eps:
            neighbours |= {p}

    return neighbours


'''
Pseudocode source: https://en.wikipedia.org/wiki/DBSCAN
'''
def descan_method(db, dist_func, eps, min_pts):
    c = 0

    for p in db:

        if db[p] != None:
            continue

        neighbours = range_query(db, dist_func, p, eps)

        if len(neighbours) < min_pts:
            db[p] = 0 # Noise
            continue

        c = c + 1
        print("C = ", c)

        db[p] = c

        s = neighbours - {p}

        new_neighbours = set()

        for q in s:
            if db[q] == 0:
                db[q] = c
            if db[q] != None:
                continue
            db[q] = c
            neighbours = range_query(db, dist_func, q, eps)
            if len(neighbours) >= min_pts:
                new_neighbours |= neighbours
        s |= new_neighbours
    return db

''' load_file '''
def load_file(filename):

    srcfolder = os.path.dirname(os.path.abspath(__file__))
    datafolder = os.path.join(srcfolder, "Data")
    filepath = os.path.join(datafolder, filename)

    # Load the .dat file into an object.
    datfile = np.loadtxt(filename, dtype=str, skiprows=0, usecols=(0,1), delimiter=';')

    return datfile


''' Extract information from the file where each line in the file is following
the format: x;y; '''
def make_db(file):
    db = dict()

    # Extract first row and extract n and d.
    firstline = file[0,:]
    n = firstline[0].astype(int)
    d = firstline[1].astype(int)

    # Extract x and ycolumn.
    file = file[1:len(file)]

    db = {tuple([float(e) for e in p]): None for p in file}
    #db = {tuple(p): None for p in file}
    #print(db)
    return n, d, db

#scatter("./Data/cluster_100_2_2.dat")


''' Read three command line arguments: filename, eps and minPts.'''
filename = str(sys.argv[1])
eps = float(sys.argv[2])
min_pts = float(sys.argv[3])

file = load_file(filename)


# Make the from the file
n, d, db = make_db(file)

db = descan_method(db, 'euclidean', eps, min_pts)

for k in db:
    print(db[k])