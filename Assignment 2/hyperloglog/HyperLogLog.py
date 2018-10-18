class HyperLogLog:		
	# Add the element to the set represented by this HyperLogLog.
	def add(self, element):
		pass
	
	# Should return an estimate of the current number of (distinct) elements in the set.
	def count(self):
		return 0
	
	# Should return a new hyperloglog that corresponds to the union(merge)
	# of self and other.
	def __add__(self, other):
		return None