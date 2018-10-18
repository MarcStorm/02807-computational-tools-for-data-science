import numpy as np
from collections import Counter
from urllib import parse
import datetime
import bisect

class LogAnalyzer:

    def __init__(self):
        logFileContent = None
        cachedAverageObjectSize = None
        cachedMostFrequentIp = None
        datetimesSorted = []
        statusCodeMap = dict()
        resourcesMap = dict()
        resourceCountMap = dict()

    def convertToDatetime(self):

        result = []

        # Extract time ranges from the log file.
        timeRangesArray = self.logFileContent[:,3]
        timeZonesArray = self.logFileContent[:,4]

        for i in range(0, len(timeRangesArray)):

            # Get the time range and time zone from respective arrays and strip
            # first and last character respectively as it is a square bracket.
            timeRange = timeRangesArray[i][1:]
            timeZone = timeZonesArray[i][:-1]

            # Join the two variables
            dateTimeRange = " ".join([timeRange, timeZone])

            # Construct datetime object
            dt = datetime.datetime.strptime(dateTimeRange, "%d/%b/%Y:%H:%M:%S %z")

            result.append(dt)

        result.sort()

        return result

    def countAllStatusCodes(self):

        result = dict()

        # Extract status codes from the log file.
        statusCodeArray = self.logFileContent[:,8]

        for i in range(0, len(statusCodeArray)):
            statusCodeRequest = int(statusCodeArray[i])

            if statusCodeRequest in result:
                result[statusCodeRequest] = result[statusCodeRequest] + 1
            else:
                result[statusCodeRequest] = 1

        return result

    def countResources(self):

        result = dict()

        # Get all the resources.
        allResources = self.resources()

        for r in allResources:
            if r in result:
                result[r] = result[r] + 1
            else:
                result[r] = 1

        return result

    def makeResourceStructure(self):

        # Get all the resources.
        allResources = self.resources()

        result = dict()

        for resource in allResources:

            m = parse.parse_qs(parse.urlsplit(resource).query)

            for (n, v) in m.items():

                # If the name doesn't exists in the map, add it.
                if n not in result:
                    result[n] = dict()

                for value in v:
                    if value not in result[n]:
                        result[n][value] = set()

                    result[n][value].add(resource)

        return result


    # Each index in the array will correspond to a list of the following info:
    # host ident authuser date request status bytes
    #logFileContent = []

    # This should parse the log file named filename, store relevant data in the object,
    # and finally return the number of (non-empty) log lines in the file.
    # See https://en.wikipedia.org/wiki/Common_Log_Format for the format.
    def parse(self, filename):

        # Reset global variables
        self.cachedAverageObjectSize = None
        self.cachedMostFrequentIp = None

        # Open file and read all lines.
        with open(filename) as f:
            fileContent = f.readlines()

        # Make sure whitespace characters at the end of each line is removed.
        fileContent = [l.strip() for l in fileContent]

        # Split every line read from file by space.
        self.logFileContent = np.array([l.split(' ') for l in fileContent])

        # Convert to datetime
        self.datetimesSorted = self.convertToDatetime()

        self.statusCodeMap = self.countAllStatusCodes()

        self.resourcesMap = self.makeResourceStructure()

        self.resourceCountMap = self.countResources()

        return len(self.logFileContent)

    # The average of object sizes of all requests
    def averageObjectSize(self):

        if self.cachedAverageObjectSize is None:
            sum = 0
            bytesArray = self.logFileContent[:,9]

            for i in range(0, len(bytesArray)):
                bytes = int(bytesArray[i])
                sum += bytes

            average = sum/len(bytesArray)
            self.cachedAverageObjectSize = average
            return average
        else:
            return self.cachedAverageObjectSize

    # The most frequent ip address among the log lines.
    # (if multiple exists, just retun any of them)
    def mostFrequentIp(self):

        if self.cachedMostFrequentIp is None:

            # Extract IPs from the log file.
            ipsArray = self.logFileContent[:,0]

            # Count occurrences of each IP.
            countedIp = Counter(ipsArray)

            # Return the most frequent IP. If two is most frequent one is returned.
            result = max(ipsArray, key = countedIp.get)
            self.cachedMostFrequentIp = result
            return result
        else:
            return self.cachedMostFrequentIp

    # Should return a list of all resources requested in sorted order
    def resources(self):

        # Load resources from log file into new variable.
        resourcesArray = self.logFileContent[:,6]

        # Convert ndarray to list
        resourcesList = resourcesArray.tolist()

        # Sort the list
        resourcesList.sort()

        return resourcesList

    # Should return a list of all distinct resources requested in sorted order
    def distinctResources(self):

        # Get all the resources.
        allResources = self.resources()

        # Convert to set to get rid of duplicate values
        distinctResourcesSet = set(allResources)

        # Convert back to list and sort.
        distinctResourcesList = list(distinctResourcesSet)
        distinctResourcesList.sort()

        return distinctResourcesList

    # Should return the number of requests that gave the given HTTP status code.
    def numberOfStatusCode(self, statuscode):
        if statuscode in self.statusCodeMap:
            return self.statusCodeMap[statuscode]
        else:
            return 0


    # Should return the number of requests made in the given time range (inclusive start/end).
    # start and end will begiven as datetime objects (described on https://docs.python.org/2/library/datetime.html)
    def countRequestsInTimeRange(self, start, end):

        leftIdx = bisect.bisect_left(self.datetimesSorted, start)
        rightIdx = bisect.bisect_right(self.datetimesSorted, end)

        return rightIdx - leftIdx

    # This function should return a list of resources that fulfill a given criteria in sorted order.
    # To solve this, you must parse the query string part of the resources in the log file.
    # For example the resource /showcars?year=2010&color=red has two query string parameters,
    # one with the name year and value 2010 and one with name color and value red.
    # See more details on https://en.wikipedia.org/wiki/Query_string.
    # Given a name and value of such a query string parameter, return the list of all
    # resources that match (again in sorted order after resource name).
    def resourcesWithQueryParam(self, name, value):

        uniqueResources = list(self.resourcesMap.get(name, {}).get(value, []))

        result = []

        for r in uniqueResources:
            multiplier = self.resourceCountMap[r]
            temp = [r] * multiplier
            result.extend(temp)

        result.sort()

        return result

    # This is like the previous exercise, except you are now given a list of criterias
    # instead of a single criteria. This function should return a list of all the resources
    # that match _all_ the criterias in the list (again in sorted order after resource name).
    # The criterias are given as a list of tuples where the first element in the tuple is the
    # name and the second the value. For instance queryParams could be
    # [("year", "2010"), ("color", "red")].
    def resourcesWithAllQueryParams(self, queryParams):

        allSets = []

        for (n, v) in queryParams:
            s = self.resourcesMap.get(n, {}).get(v, set())

            allSets.append(s)

        tempList = list(set.intersection(*allSets))
        tempList.sort()

        result = []

        for r in tempList:
            multiplier = self.resourceCountMap[r]
            temp = [r] * multiplier
            result.extend(temp)

        return result

def containsParameters(resource, name, value):

    t = parse.urlsplit(resource)

    a = parse.parse_qs(t.query).get(name, [])

    if a is None:
        return False
    else:
        return value in a
