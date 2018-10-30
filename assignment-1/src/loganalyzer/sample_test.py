import datetime

from LogAnalyzer import LogAnalyzer

analyzer = LogAnalyzer()
lines = analyzer.parse("webserver1.log")

print("Parsed " + str(lines) + " lines from the log file")

#print("The average object size is: " + str(analyzer.averageObjectSize()))

#print("The most frequent ip is: " + str(analyzer.mostFrequentIp()))

#print("The resources visted are:\n" + "\n".join(analyzer.resources()))

#print("The distinct resources visted are:\n" + "\n".join(analyzer.distinctResources()))

#print(str(analyzer.numberOfStatusCode(200)) + " successfully loaded got the requested resource")

#print(str(analyzer.numberOfStatusCode(404)) + " got resource not found")

#start = datetime.datetime(2018, 9, 3, 10, 15, 0, 0, datetime.timezone(datetime.timedelta(hours=0)))
#end = datetime.datetime(2018, 9, 3, 10, 20, 0, 0, datetime.timezone(datetime.timedelta(hours=0)))
#print(str(analyzer.countRequestsInTimeRange(start, end)) + " requests during the timeframe")

#print("Resources with color=red:\n" + "\n".join(analyzer.resourcesWithQueryParam("color", "red")))

#print("Resources with year=2005:\n" + "\n".join(analyzer.resourcesWithQueryParam("year", "2005")))

print("Resources with year=2010 and color=orange:\n" + "\n".join(analyzer.resourcesWithAllQueryParams([("year", "2010"), ("color", "orange")])))
