import mmh3
import math

class HyperLogLog:

	# Phase 0
	def __init__(self):
		self.p = 5
		self.m = 2**self.p
		self.M = [0] * self.m
		self.a16 = 0.673
		self.a32 = 0.697
		self.a64 = 0.709
		self.am = 0.7213 / (1 + 1.079/self.m) # For m >= 128


	def trailingZeros(self, x):
		xBin = bin(x)
		xBin = str(xBin)
		return len(xBin) - len(xBin.rstrip('0'))

	# Add the element to the set represented by this HyperLogLog.
	def add(self, element):
		# Calculate the hash value of the element.
		x = mmh3.hash(element, signed=False)

		# Calculate the index by bit shifting the value p times.
		idx = x >> (x.bit_length() - self.p)
		if idx < self.m/2:
			print("idx = " + str(idx))

		# Calculate w by creating a string of ones that has the same length as
		# length(x) - p. Then by performing a bitwise and, we get the first
		# length(x) - p bits of x.
		bitStringOnes = (1 << (x.bit_length() - self.p)) - 1 # l-p + 1
		w = x & bitStringOnes

		# Update the value in M.
		self.M[idx] = max(self.M[idx], self.trailingZeros(w))


	def rawEstimate(self):
		# Determine alpha value to useself.
		if self.p == 4:
			alpha = self.a16
		elif self.p == 5:
			alpha = self.a32
		elif self.p == 6:
			alpha = self.a64
		else:
			alpha = self.am

		print("M is")
		print(self.M)
		print()
		return alpha * self.m**2 * (sum([2**(-m) for m in self.M]))**(-1)

	def getV(self):
		counter = 0
		for x in self.M:
			if x == 0:
				counter += 1

		return counter

	def linearCounting(self, m, V):
		return m * math.log(m/V)

	# Should return an estimate of the current number of (distinct) elements in the set.
	def count(self):
		E = self.rawEstimate()
		print("E = " + str(E))

		if E <= 5/2 * self.m:
			V = self.getV()
			if V != 0:
				Eprime = self.linearCounting(self.m, V)
			else:
				Eprime = E
		elif E <= 1/32 * 2**32:
			Eprime = E
		else:
			Eprime = -2**32 * math.log(1 - E / 2**32)
		return Eprime

	# Should return a new hyperloglog that corresponds to the union(merge)
	# of self and other.
	def __add__(self, other):
		# Assuming that self.M and other.M has the same length.
		hllUnion = [max(self.M[x], other.M[x]) for x in range(len(self.M))]

		hll = HyperLogLog()
		hll.M = hllUnion

		return hll
