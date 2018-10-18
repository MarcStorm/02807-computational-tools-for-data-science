class HyperLogLog:

	# Phase 0
	def __init__(self):
        p = 9
		m = 2^p
		M = [0] * m
		a16 = 0.673
		a32 = 0.697
		a64 = 0.709
		am = 0.7213/(1 + 1.079/m) # For m >= 128

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
