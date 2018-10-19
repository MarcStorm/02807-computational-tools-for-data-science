from HyperLogLog import HyperLogLog

class SalesAnalyzer:

    def __init__(self):
        self.hll = HyperLogLog()
        self.attrDict = dict()

    # Add a sale to the system. saleId is a number identifying a unique sale,
    # but info about the same sale might be added multiple times. If a sale is added multiple times,
    # its attributes should be the union of all attributes it was added with.
    # Attributes is a list of attributes (strings) that describe the product sold.
    # The total number of different attributes in a test will be at most 100.
    def addSale(self, saleId, attributes):

        # Add saleId
        self.hll.add(str(saleId))

        # Add attributes
        for attr in attributes:
            if attr not in self.attrDict:
                self.attrDict[attr] = HyperLogLog()

            self.attrDict[attr].add(str(saleId))

    # Return an estimation of the total number of (distinct) sales
    def totalSales(self):
        return self.hll.count()

    # Return an estimation of the number of sales that has a given.
    def salesWithAttribute(self, attribute):
        if attribute in self.attrDict:
            return self.attrDict[attribute].count()
        else:
            return 0

    # Return an estimation of the number of sales with at least of one of the two attributes
    # attribute1 and attribute2.
    def salesWithAnyOfTwoAttributes(self, attribute1, attribute2):
        return self.salesWithAnyOfAttributes([attribute1, attribute2])

    # Return an estimation of the number of sales with both attribute1 and attribute2
    def salesWithBothAttributes(self, attribute1, attribute2):
        hll1 = self.attrDict[attribute1]
        hll2 = self.attrDict[attribute2]
        return hll1.inter(hll2).count()

    # Returns an estimation of the number of sales with attribute but that does not have
    # attribute exceptAttribute.
    def salesWithAttributeExcept(self, attribute, exceptAttribute):
        hll1 = self.attrDict[attribute]
        hll2 = self.attrDict[exceptAttribute]
        hllMerged = hll1 + hll2

        return hllMerged.count() - hll2.count()

    # Returns an estimation of the number of sales with any of the attributes in the list attributes.
    # Should work for any non-empty list of attributes.
    def salesWithAnyOfAttributes(self, attributes):
        hlls = [self.attrDict[attr] for attr in attributes]

        hllMerged = HyperLogLog()
        for hll in hlls:
            hllMerged += hll

        return hllMerged.count()
