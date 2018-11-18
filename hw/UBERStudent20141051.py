#!/usr/bin/python3

import sys
import calendar

f = open(sys.argv[1], "rt")
w = open(sys.argv[2], "wt")

# f = open("uber_exp.txt", "rt")
# w = open("rslt.txt", "wt")

trip = dict()
vehicle = dict()

dayOfWeek = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

for line in f:
    r = line.split(',')
    d = r[1].split('/')
    day = calendar.weekday(int(d[2]), int(d[0]), int(d[1]))
    key = r[0] + "," + str(day)
    if key not in trip:
        vehicle[key] = int(r[2])
        trip[key] = int(r[3])
    else:
        vehicle[key] += int(r[2])
        trip[key] += int(r[3])

for key in sorted(trip.keys()):
    w.write(key[:7]+dayOfWeek[int(key[7:])]+" " + str(trip[key]) + "," + str(vehicle[key]) + "\n")

w.close()
f.close()
