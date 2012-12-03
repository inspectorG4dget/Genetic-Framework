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

def crossOnes(p1, p2):
	""" Length preserving one-point crossover of chromosome at index chrom
		Tuple containing two new children is returned
		
		pre:
			isinstance(p1, list)
			isinstance(p2, list)
		
		post[p1, p2]:
			p1 == __old__.p1
			p2 == __old__.p2
			
			isinstance(__return__, tuple)	# returns a tuple
			len(__return__) == 2
			forall(__return__, lambda e: isinstance(e, list))	# return-tuple is made of lists
			forall(__return__, lambda child: child in p1 or child in p2)
			forall(__return__, lambda L: id(L) not in [id(p1), id(p2)])	# elements in the return-tuple do not have the same memory addresses as the inputs
			
		"""
	
	crosspoint = randint(0, len(p1)-1)
	child1 = p2[:crosspoint]+p1[crosspoint:]
	child2 = p1[:crosspoint]+p2[crosspoint:]
	
	return child1, child2

def injectionco(p1, p2):
	"""
		pre:
			isinstance(p1, list)
			isinstance(p2, list)
			len(p1) == len(p2)
			sorted(p1) == range(len(p1))
			sorted(p2) == range(len(p2))
		
		post[p1, p2]:
			p1 == __old__.p1
			p2 == __old__.p2
		post:
			isinstance(__return__, list)
			len(__return__) == len(p1)
			id(__return__) not in [id(p1), id(p2)]
			forall(__return__, lambda city: city in p1 and city in p2)
			len(set(__return__)) == len(__return__)
		"""

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
	
	return answer

def twoChildCrossover(p1,p2, crossfuncs, crossparams):
	"""
		Crossover all the chromosomes in the two individuals.
		The crossover function for each pair of  corresponding chromosomes is the the corresponding element in crossfuncs, 
		called with the corresponding tuple in crossparams.
		
		Note that it is assumed that each crossover function in crossfuncs returns two child chromosomes
	
		pre:
			isinstance(p1, Individual)
			isinstance(p2, Individual)
			len(p1) == len(p2)
			len(p1) == len(crossfuncs)
			len(crossfuncs) == len(crossparams)
			forall(crossparams, lambda params: isinstance(params, tuple))
		
		post:
			__old__.p1 is p1
			__old__.p2 is p2
			__old__.p1 == p1
			__old__.p2 == p2
			
			len(__return__) == 2
			forall(_return__, lambda p: isinstance(p, Individual))
			forall(__return__, lambda p: len(p)==len(p1))
			forall(__return__, lambda p: all(len(c)==len(p1[i]) for i,c in enumerate(p.chromosomes)))
			forall(__return__, lambda p: all(len(c)==len(p2[i]) for i,c in enumerate(p.chromosomes)))
	"""
	
	c1, c2 = Individual([]), Individual([])
	for i, (crossfunc, crossparams) in enumerate(zip(crossfuncs, crossparams)):
		chrom1, chrom2 = crossfunc(p1[i], p2[i], *crossparams)
		c1.append(chrom1)
		c2.append(chrom2)
	
	return c1, c2

def oneChildCrossover(p1, p2, crossfuncs, crossparams):
	"""
		Crossover all the chromosomes in the two individuals.
		The crossover function for each pair of  corresponding chromosomes is the the corresponding element in crossfuncs, 
		called with the corresponding tuple in crossparams.
		
		Note that it is assumed that each crossover function in crossfuncs returns one child chromosome
		
		pre:
			isinstance(p1, Individual)
			isinstance(p2, Individual)
			len(p1) == len(p2)
			len(p1) == len(crossfuncs)
			len(crossfuncs) == len(crossparams)
		
		post:
			__old__.p1 is p1
			__old__.p2 is p2
			__old__.p1 == p1
			__old__.p2 == p2
			
			len(__return__) == 1
			isinstance(__return__, Individual)
			len(__return__)==len(p1)
			all(len(c)==len(p1[i]) for i,c in enumerate(__return__.chromosomes))
			all(len(c)==len(p1[i]) for i,c in enumerate(__return__.chromosomes))
	"""
	answer = Individual([])
	for i, (crossfunc, crossparams) in enumerate(zip(crossfuncs, crossparams)):
		answer.append(crossfunc(p1[i], p2[i], *crossparams))
	
	return answer
