#!/usr/bin/python3
import decimal
import itertools

def expand(R, base=10):
	m = 1
	while True:
		for v in [ v*m for v in R[:-1] ]:
			if (v % 1 == 0):
				yield int(v)
			else:
				yield v
		m *= base
def stride(R, s):
	yield from itertools.islice(expand(R), None, len(R)*s, s)
def dotdot(R, begin, end):
	for v in expand(R):
		if (begin <= v < end):
			yield v
		elif (end <= v):
			yield end
			break
class Range(list):
	"""
	>>> R5/2
	[10, 25, 63, 160, 400, 1000]

	>>> 0.01*(R5/2)
	[0.1, 0.25, 0.63, 1.6, 4.0, 10.0]

	>>> R5
	[10, 16, 25, 40, 63, 100]

	>>> 0.01*(Rpp5)
	[0.1, 0.15, 0.25, 0.4, 0.6, 1.0]
	"""
	def __mul__(self, other):
		return Range(v*other for v in self)
	def __rmul__(self, other):
		return self*other
	def __truediv__(self, other):
		return Range(stride(self, other))
	def __call__(self, begin, end):
		return Range(dotdot(self, begin, end))
	def floorceil(self, n, b=1):
		if (b == n): return (b, b)
		for e in expand(self):
			if (e == n): return (e, e)
			elif (b < n < e): return (b, e)
			b = e
	def round(self, n, tie='up'):
		"""
		>>> R5.round(20)
		16

		>>> (R40/3).round(21)
		20
		"""
		f, c = self.floorceil(n)
		if f == c: return f
		if (n-f) == (c-n):
			return c if tie=='up' else f
		return f if (n-f) < (c-n) else c
#
R5 = Range(int(x) for x in '10 16 25 40 63 100'.split())
R10 = Range(decimal.Decimal(x) if '.' in x else int(x) for x in '10 12.5 16 20 25 31.5 40 50 63 80 100'.split())
R20 = Range(decimal.Decimal(x) if '.' in x else int(x) for x in '10 11.2 12.5 14 16 18 20 22.4 25 28 31.5 35.5 40 45 50 56 63 71 80 90 100'.split())
R40 = Range(decimal.Decimal(x) if '.' in x else int(x) for x in '10 10.6 11.2 11.8 12.5 13.2 14 15 16 17 18 19 20 21.2 22.4 23.6 25 26.5 28 30 31.5 33.5 35.5 37.5 40 42.5 45 47.5 50 53 56 60 63 67 71 75 80 85 90 95 100'.split())

Rp10 = Range(decimal.Decimal(x) if '.' in x else int(x) for x in '10 12.5 16 20 25 32 40 50 63 80 100'.split() )
Rp20 = Range(decimal.Decimal(x) if '.' in x else int(x) for x in '10 11 12.5 14 16 18 20 22 25 28 32 36 40 45 50 56 63 71 80 90 100'.split() )
Rp40 = Range(decimal.Decimal(x) if '.' in x else int(x) for x in '10 10.5 11 12 12.5 13 14 15 16 17 18 19 20 21 22 24 25 26 28 30 32 34 36 38 40 42 45 48 50 53 56 60 63 67 71 75 80 85 90 95 100'.split() )

Rpp5 = Range(int(x) for x in '10 15 25 40 60 100'.split() )
Rpp10 = Range(int(x) for x in '10 12 15 20 25 30 40 50 60 80 100'.split() )
Rpp20 = Range(int(x) for x in '10 11 12 14 16 18 20 22 25 28 30 35 40 45 50 50 55 60 70 80 90 100'.split())

#
if __name__ == '__main__':
	import doctest
	doctest.testmod()
