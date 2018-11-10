import numpy as np
import os
import sys

'''
euclidean_distance will calculate the euclidean distance between two points.
'''
def euclidean_distance(p, q):
    dist = ((p[0]-q[0])**2 + (p[1]-q[1])**2)**0.5
    return dist

'''
range_query will find all points within a range of eps of q.
'''
def range_query(db, q, eps):
    neighbours = set()

    for p in db:
        dist = euclidean_distance(p, q)
        if dist <= eps:
            neighbours |= {p}

    return neighbours

'''
descan will create clusters based on the DBSCAN algorithm.
Pseudocode source: https://en.wikipedia.org/wiki/DBSCAN
'''
def descan(db, eps, min_pts):
    c = 0

    for p in db:

        # The point has already assigned to a cluster or marked as noise.
        if db[p] is not None:
            continue

        # Find neighbours of the point.
        neighbours = range_query(db, p, eps)

        # If it doesn't have the minimum amount of neighbours, mark the point
        # as a noise point.
        if len(neighbours) < min_pts:
            db[p] = 0 # Noise
            continue

        c += 1
        db[p] = c

        # Create the seed set.
        s = neighbours.remove(p)

        while len(neighbours) > 0:

            q = neighbours.pop()

            if db[q] == 0:
                db[q] = c
            if db[q] is not None:
                continue

            db[q] = c

            q_neighbours = range_query(db, q, eps)

            if len(q_neighbours) >= min_pts:
                neighbours |= q_neighbours

    return db


''' load_file '''
def load_file(filename):

    srcfolder = os.path.dirname(os.path.abspath(__file__))
    datafolder = os.path.join(srcfolder, 'Data')
    filepath = os.path.join(datafolder, filename)

    # Load the .dat file into an object.
    datfile = np.loadtxt(filename, dtype=str, skiprows=0, usecols=(0,1), delimiter=';')

    return datfile


'''
Extract information from the file where each line in the file is following
the format: x;y;
'''
def make_db(file):
    db = dict()

    # Extract first row and extract n and d.
    firstline = file[0,:]
    n = firstline[0].astype(int)
    d = firstline[1].astype(int)

    # Extract x and ycolumn.
    file = file[1:len(file)]

    db = {tuple([float(e) for e in p]): None for p in file}

    return n, d, db

'''
Read three command line arguments: filename, eps and minPts.
'''
filename = str(sys.argv[1])
eps = float(sys.argv[2])
min_pts = float(sys.argv[3])

file = load_file(filename)


# Make the from the file
n, d, db = make_db(file)

db = descan(db, eps, min_pts)

for k in db:
    print(db[k])
