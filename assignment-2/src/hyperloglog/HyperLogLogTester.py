# To use this tester, you should run: python3 HyperLogLogTester.py HHLSample1.txt

import HyperLogLog
import sys

# Prepare 5 HyperLogLogs
hlls = [HyperLogLog.HyperLogLog() for _ in range(5)]

# Go through the data file line by line
with open(sys.argv[1], "r") as file:
    for line in file:
        cleanLine = line.replace("\n", "")
        (cmd, set, value) = cleanLine.split(" ")[:3]

        # See if this was an add, count, or merge command
        if cmd == "A":
            hlls[int(set)].add(value)
        elif cmd == "C":
            estimate = hlls[int(set)].count()
            print("Estimate:", estimate, "Real count:", value)
        elif cmd == "M":
            (cmd, m1, m2, m3) = cleanLine.split(" ")
            hlls[int(m3)] = hlls[int(m1)] + hlls[int(m2)]