import mmh3
import math

class HyperLogLog:

	# Phase 0
	def __init__(self, p = 10):
		assert 4 <= p && p <= 16
		self.p = p
		self.m = 2**self.p
		self.M = [0] * self.m
		self.a16 = 0.673
		self.a32 = 0.697
		self.a64 = 0.709
		self.am = 0.7213 / (1 + 1.079/self.m) # For m >= 128
		self.alpha = self.setAlpha()

	def setAlpha(self):
		# Determine alpha value to useself.
		if self.p == 4:
			return self.a16
		elif self.p == 5:
			return self.a32
		elif self.p == 6:
			return self.a64
		else:
			return self.am

	def rho(self, x):
		xBin = bin(x)
		xBin = str(xBin)
		return 1 + (len(xBin) - len(xBin.rstrip('0')))
		#return 1 + 32 - self.p - x.bit_length() # Leading zeros.

	# Add the element to the set represented by this HyperLogLog.
	def add(self, element):
		# Calculate the hash value of the element.
		x = mmh3.hash(element, signed=False)

		# Calculate the index by bit shifting the value 32 - p times.
		idx = x >> (32 - self.p)

		# Calculate w by creating a string of ones that has the same length as
		# length(x) - p. Then by performing a bitwise and, we get the first
		# length(x) - p bits of x.
		bitStringOnes = (1 << (32 - self.p)) - 1
		w = x & bitStringOnes

		# Update the value in M.
		self.M[idx] = max(self.M[idx], self.rho(w))


	def rawEstimate(self):
		return self.alpha * self.m**2 * (sum([2**(-m) for m in self.M]))**(-1)

	def getV(self):
		counter = 0
		for x in self.M:
			if x == 0:
				counter += 1

		return counter

	def linearCounting(self, m, V):
		return m * math.log2(m/V)

	# Should return an estimate of the current number of (distinct) elements in the set.
	def count(self):
		E = self.rawEstimate()

		if E <= 5/2 * self.m:
			V = self.getV()
			if V != 0:
				Eprime = self.linearCounting(self.m, V)
			else:
				Eprime = E
		elif E <= 1/32 * 2**32:
			Eprime = E
		else:
			Eprime = -2**32 * math.log2(1 - E / 2**32)
		return Eprime

	# Should return a new hyperloglog that corresponds to the union(merge)
	# of self and other.
	def __add__(self, other):
		hll = HyperLogLog()
		# Assuming that self.M and other.M has the same length.
		hll.M = [max(self.M[x], other.M[x]) for x in range(len(self.M))]

		return hll

	def inter(self, other):
		hll = HyperLogLog()
		# Assuming that self.M and other.M has the same length.
		hll.M = [min(self.M[x], other.M[x]) for x in range(len(self.M))]

		return hll
