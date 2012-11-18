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

from Genetic.individual import Individual

from random import randint, sample

def crossOnes(p1, p2, chrom):
	""" Length preserving one-point crossover of chromosome at index chrom
		Tuple containing two new children is returned
		
		pre:
			isinstance(p1, Individual)
			isinstance(p2, Individual)
			isinstance(chrom, int)
		
		post[p1, p2, chrom]:
			isinstance(__return__, tuple)	# returns a tuple
			len(__return__) == 2
			forall(__return__, lambda e: isinstance(e, Individual))	# return-tuple is made of Individuals
			forall(__return__[0].chromosomes, lambda c: isinstance(c, list))
			forall(__return__[1].chromosomes, lambda c: isinstance(c, list))
			forall(__return__[0][chrom], lambda L: forall(L, lambda elem: elem in p1[chrom] or elem in p2[chrom]))
			forall(__return__[1][chrom], lambda L: forall(L, lambda elem: elem in p1[chrom] or elem in p2[chrom]))
			forall(__return__, lambda L: id(L) not in [id(p1), id(p2)])	# elements in the return-tuple do not have the same memory addresses as the inputs
			p1 == __old__.p1
			p2 == __old__.p2
			
		"""
	
	c1, c2 = p1[chrom], p2[chrom]
	crosspoint = randint(0, len(c1)-1)
	child1 = c2[:crosspoint]+c1[crosspoint:]
	child2 = c1[:crosspoint]+c2[crosspoint:]
	
	answer1 = Individual(p1.chromosomes[:])
	answer1[chrom] = child1
	
	answer2 = Individual(p2.chromosomes[:])
	answer2[chrom] = child2
	
	return answer1, answer2

def injectionco(p1, p2, chrom):
	"""
		pre:
			isinstance(p1, Individual)
			isinstance(p2, Individual)
			isinstance(chrom, int)
			forall(p1, lambda elem: any(isinstance(elem, i.__class__) for i in p2))
			forall(p2, lambda elem: any(isinstance(elem, i.__class__) for i in p1))
			len(p1) == len(p2)
		
		post[p1, p2]:
			p1 == __old__.p1
			p2 == __old__.p2
		post:
			isinstance(__return__, p1.__class__)	# returns an individual
			len(__return__) == len(p1)
			id(__return__) not in [id(p1), id(p2)]
			forall(__return__.chromosomes[0], lambda elem: __return__.count(elem, 0) == 1)
		"""

	pp1, _pp2 = p1, p2
	p1, p2 = p1[chrom], p2[chrom]
	answer = [None for _ in xrange(len(p1))]
	a,b = sample(range(len(p1)), 2)
	if a > b: a,b = b,a
	ab = p1[a:b]
	answer[a:b] = ab
	remainder = [city for city in p2 if city not in ab]
	for i in xrange(a):
		answer[i] = remainder.pop(0)
	for i in xrange(b, len(answer)):
		answer[i] = remainder.pop(0)
	
	indiv = Individual(pp1.chromosomes[:])
	indiv[chrom] = answer
	return indiv
