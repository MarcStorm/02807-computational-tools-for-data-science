# To use this tester, you should run: python3 SalesAnalyzerTester.py SASample1.txt

import SalesAnalyzer
import sys

analyzer = SalesAnalyzer.SalesAnalyzer()

# Go through the data file line by line
with open(sys.argv[1], "r") as file:
    for line in file:
        cleanLine = line.replace("\n", "")
        parts = cleanLine.split(" ")
        cmd = parts[0]

        if cmd == "AS": # Add sale line
            analyzer.addSale(int(parts[1]), parts[2:])
        elif cmd == "TS": # totalSales line
            estimate = analyzer.totalSales()
            print("TotalSales:", estimate, "Real count:", parts[1])
        elif cmd == "SWA": # salesWithAttribute total sales line
            estimate = analyzer.salesWithAttribute(parts[1])
            print("SalesWithAttribute:", estimate, "Real count:", parts[2])
        elif cmd == "SWAOTA": # salesWithAnyOfTwoAttributes total sales line
            estimate = analyzer.salesWithAnyOfTwoAttributes(parts[1], parts[2])
            print("SalesWithAnyOfTwoAttributes:", estimate, "Real count:", parts[3])
        elif cmd == "SWBA": # salesWithBothAttributes total sales line
            estimate = analyzer.salesWithBothAttributes(parts[1], parts[2])
            print("SalesWithBothAttributes:", estimate, "Real count:", parts[3])
        elif cmd == "SWAE": # salesWithAttributeExcept total sales line
            estimate = analyzer.salesWithAttributeExcept(parts[1], parts[2])
            print("SalesWithAttributeExcept:", estimate, "Real count:", parts[3])
        elif cmd == "SWAOA": # salesWithAnyOfAttributes total sales line
            estimate = analyzer.salesWithAnyOfAttributes(parts[1:-1])
            print("SalesWithAnyOfAttributes:", estimate, "Real count:", parts[-1])