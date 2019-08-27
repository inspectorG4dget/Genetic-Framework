'''
Copyright 2012 Ashwin Panchapakesan

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

from itertools import count
from pystitia import contracts


class Individual:
	ID = count()

	@contracts(
		preconditions=(
			lambda chromosomes: isinstance(chromosomes, list),
		),
		postconditions=(
			lambda self: hasattr(self, 'chromosomes'),
		)
	)
	def __init__(self, chromosomes):
		"""
		Given a bunch of chromosomes, this individual is a wrapper around them. It holds all chromosomes in place.
		"""
		self.chromosomes = chromosomes[:]	# managed as a list as order is used to identify chromosomal functions (i.e. chromosome i encodes functionality f)
		self.id = next(self.ID)


	@contracts(
		preconditions=(
			lambda other: isinstance(other, Individual),
		),
		postconditions=(
			lambda self: len(self.chromosomes)==len(__old__.self.chromosomes),
			lambda self: all(self.chromosomes[i] == __old__.self.chromosomes[i] for i in range(len(self.chromosomes))),
			lambda other: len(other.chromosomes)==len(__old__.other.chromosomes),
			lambda other: all(other.chromosomes[i] == __old__.other.chromosomes[i] for i in range(len(other.chromosomes))),
		)
	)
	def __eq__(self, other):
		return self.chromosomes == other.chromosomes


	@contracts(
		postconditions=(
			lambda self: __old__.self == self,
		)
	)
	def __hash__(self):
		return hash(tuple(tuple(chromosome) for chromosome in self.chromosomes))


	@contracts(
		preconditions=(
			lambda self, chrom: (chrom is None) or ((chrom<len(self.chromosomes)) ^ (-1 >= chrom >= -len(self.chromosomes))),
		),
		postconditions=(
			lambda self: __old__.self == self,
		)
	)
	def __len__(self, chrom=None):
		if chrom is None:
			return len(self.chromosomes)
		else:
			return len(self.chromosomes[chrom])

	def __iter__(self): return self.chromosomes.__iter__()

	@contracts(
		preconditions=(
			lambda self,i: (0<=i<len(self.chromosomes)) ^ (-1 >= i >= -len(self.chromosomes)),
		),
		postconditions=(
			lambda self: __old__.self == self,
		)
	)
	def __getitem__(self, i):
		return self.chromosomes[i]


	@contracts(
		preconditions=(
			lambda self, index: (0 <= index < len(self.chromosomes)) ^ (len(self.chromosomes)*-1 >= index >= -1),
		),
		postconditions=(
			lambda self, index, obj: self.chromosomes[index] == obj,
		)
	)
	def __setitem__(self, index, obj):
		self.chromosomes[index] = obj


	@contracts(
		postconditions=(
			lambda self: __old__.self == self,
			lambda chromosome: __old__.chromosome == chromosome,
		)
	)
	def __contains__(self, chromosome):
		return chromosome in self.chromosomes


	@contracts(
		postconditions=(
			lambda self: __old__.self == self,
		)
	)
	def __repr__(self):
		return "Individual([{}])".format(', '.join(str(c) for c in self.chromosomes))


	@contracts(
		postconditions=(
			lambda self: __old__.self == self,
		)
	)
	def __str__(self):
		return str(self.id)

	@contracts(
		postconditions=(
			lambda self:len(__old__.self.chromosomes)+1 == len(self.chromosomes),
			lambda self, chrom: self.chromosomes[-1] == chrom),
	)
	def append(self, chrom):
		self.chromosomes.append(chrom)


	@contracts(
		postconditions=(
			lambda self: __old__.self.chromosomes == self.chromosomes,
		)
	)
	def count(self, sub, chrom):
		return self.chromosomes[chrom].count(sub)
