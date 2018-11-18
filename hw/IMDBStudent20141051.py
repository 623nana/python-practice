#!/usr/bin/python3

import sys

f = open(sys.argv[1], "rt")
w = open(sys.argv[2], "wt")

# f = open("movies_exp.txt", "rt")
# w = open("rslt.txt", "wt")

movie = dict()

for line in f:
    r = line.split('::')
    genre = r[2].strip().split('|')
    for g in genre:
        if g not in movie:
            movie[g] = 1
        else:
            movie[g] += 1

for key in movie.keys():
    text = key + " " + str(movie[key]) + "\n"
    w.write(text)
w.close()
f.close()
