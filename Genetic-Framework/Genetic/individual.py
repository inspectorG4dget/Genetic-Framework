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

class Individual:
	ID = count()
	def __init__(self, chromosomes):
		""" Given a bunch of chromosomes, this individual is a wrapper around them. It holds all chromosomes in place.
		
		pre:
			isinstance(chromosomes, list)
		post[chromosomes]:
			__old__.chromosomes == chromosomes
		post:
			hasattr(self, 'chromosomes')
			self.chromosomes == chromosomes
		"""
		self.chromosomes = chromosomes[:]	# managed as a list as order is used to identify chromosomal functions (i.e. chromosome i encodes functionality f)
		self.id = self.ID.next()
	
	def __eq__(self, other):
		"""
			pre:
				isinstance(other, Individual)
			post[self, other]:
				len(self.chromosomes) == len(__old__.self.chromosomes)
				forall(range(len(self.chromosomes)), lambda i: self.chromosomes[i] == __old__.self.chromosomes[i])
				len(other.chromosomes) == len(__old__.other.chromosomes)
				forall(range(len(other.chromosomes)), lambda i: other.chromosomes[i] == __old__.other.chromosomes[i])
		"""
		return self.chromosomes == other.chromosomes
	
	def __hash__(self):
		"""
			post[self]:
				__old__.self == self
		"""
		return hash(tuple(tuple(chromosome) for chromosome in self.chromosomes))
	
	def __len__(self, chrom=None):
		"""
			post[self]:
				__old__.self == self
		"""
		if not chrom:
			return len(self.chromosomes)
		else:
			return len(self.chromosomes[chrom])
	
	def __getitem__(self, i):
		"""
			post[self]:
				__old__.self == self
		"""
		return self.chromosomes[i]
	
	def __setitem__(self, index, obj):
		"""
			pre:
				(0 <= index <= len(self.chromosomes)) ^ (len(self.chromosomes)*-1 >= index >= -1)
			post[self]:
				self.chromosomes[index] == obj
		"""
		self.chromosomes[index] = obj
	
	def __contains__(self, chromosome):
		"""
			post[self, chromosome]:
				__old__.self == self
				__old__.chromosome == chromosome
		"""
		return chromosome in self.chromosomes
	
	def __repr__(self):
		"""
			post[self]:
				__old__.self == self
		"""
		return "Individual([%s])" %', '.join(str(c) for c in self.chromosomes)
	
	def __str__(self):
		"""
			post[self]:
				__old__.self == self
		"""
		return str(self.id)
	
	def append(self, chrom):
		"""
			post[self.chromosomes]:
				len(__old__.self.chromosomes)+1 == len(self.chromosomes)
				self.chromosomes[-1] == chrom
		"""
		self.chromosomes.append(chrom)
	
	def count(self, sub, chrom):
		"""
			post[self.chromosomes]:
				__old__.self.chromosomes == self.chromosomes
		"""
		
		return self.chromosomes[chrom].count(sub)
