class SalesAnalyzer:
    # Add a sale to the system. saleId is a number identifying a unique sale,
    # but info about the same sale might be added multiple times. If a sale is added multiple times,
    # its attributes should be the union of all attributes it was added with.
    # Attributes is a list of attributes (strings) that describe the product sold.
    # The total number of different attributes in a test will be at most 100.
    def addSale(self, saleId, attributes):
        pass
    
    # Return an estimation of the total number of (distinct) sales
    def totalSales(self):
        return 0
        
    # Return an estimation of the number of sales that has a given.
    def salesWithAttribute(self, attribute):
        return 0
    
    # Return an estimation of the number of sales with at least of one of the two attributes
    # attribute1 and attribute2.
    def salesWithAnyOfTwoAttributes(self, attribute1, attribute2):
        return 0
    
    # Return an estimation of the number of sales with both attribute1 and attribute2
    def salesWithBothAttributes(self, attribute1, attribute2):
        return 0
    
    # Returns an estimation of the number of sales with attribute but that does not have 
    # attribute exceptAttribute.
    def salesWithAttributeExcept(self, attribute, exceptAttribute):
        return 0
    
    # Returns an estimation of the number of sales with any of the attributes in the list attributes.
    # Should work for any non-empty list of attributes.
    def salesWithAnyOfAttributes(self, attributes):
        return 0