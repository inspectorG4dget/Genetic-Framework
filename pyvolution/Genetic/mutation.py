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

from random import randint, choice as choose, sample, shuffle
from Genetic.individual import Individual

def mutateSingleAllele(p, chrom, chars):
	""" get the `chrom`th chromosome of the Individual p.
		Replace a random gene in this chromosome with a different allele from chars 
		Precondition: p[chrom] should be castable into a list
		Return a new individual. Do not destroy the input
		
		pre:
			isinstance(p, Individual)
			isinstance(chrom, int)
			forall(p.chromosomes[chrom], lambda e: e in chars)
			(0 <= chrom <= len(p.chromosomes)-1) ^ (len(p.chromosomes)*-1 <= chrom <= -1)
			
		post[p, chrom]:
			__old__.p == p
			__old__.chrom == chrom
			__return__ is not p
			__return__ != p
			__return__.chromosomes != __old__.p.chromosomes
			forall(__return__.chromosomes[chrom], lambda e: e in chars)
			forall([i for i in range(len(p.chromosomes)) if i!=chrom], lambda c: __old__.p.chromosomes[i]==__return__.chromosomes[i])
		
	"""
	
	chromosome = p[chrom][:]
	gene = randint(0, len(chromosome)-1)
	allele = choose([i for i in chars if i!= chromosome[gene]])
	chromosome = chromosome[:gene] + [allele] + chromosome[gene+1:]
	
	answer = Individual(p.chromosomes[:])
	answer[chrom] = chromosome
	return answer

def swapmut(p, chrom):
	""" Pick any two random cities and swap their positions in the tour 
		
		pre:
			isinstance(p, Individual)
			isinstance(chrom, int)
			(0 <= chrom <= len(p.chromosomes)-1) ^ (len(p.chromosomes)*-1 <= chrom <= -1)
		
		post[p, chrom]:
			__old__.p == p
			__old__.chrom == chrom
			isinstance(__return__, Individual)
			forall(p.chromosomes[chrom], lambda e: e in __return__.chromosomes[chrom])
			forall(__return__.chromosomes[chrom], lambda e: e in p.chromosomes[chrom])
			sum(i!=j for i,j in zip(__return__[chrom], p[chrom])) == 2
		"""
	answer = Individual(p.chromosomes[:])
	p = answer[chrom][:]
	i,j = sample(range(len(p)), 2)
	p[i], p[j] = p[j], p[i]
	answer[chrom] = p
	return answer

def revmut(p, chrom):
	""" Choose a random pair of points on the chromosome.
		Reverse the order of the genes between those two points on the chromosome 
		
		pre:
			isinstance(p, Individual)
			isinstance(chrom, int)
			(0 <= chrom <= len(p.chromosomes)-1) ^ (len(p.chromosomes)*-1 <= chrom <= -1)
		
		post[p, chrom]:
			__old__.p == p
			__old__.chrom == chrom
			isinstance(__return__, Individual)
			forall(p.chromosomes[chrom], lambda e: e in __return__.chromosomes[chrom])
			forall(__return__.chromosomes[chrom], lambda e: e in p.chromosomes[chrom])
	"""
	
	pp=p
	p = p[chrom]
	answer = []
	a,b = sample(range(len(p)), 2)
	if a>b: a,b = b,a
	answer.extend(p[:a])
	answer.extend(p[a:b+1][::-1])
	answer.extend(p[b+1:])
	indiv = Individual(pp.chromosomes[:])
	indiv[chrom] = answer
	return indiv

def shufflemut(p, chrom):
	"""
		pre:
			isinstance(p, Individual)
			isinstance(chrom, int)
			(0 <= chrom <= len(p.chromosomes)-1) ^ (len(p.chromosomes)*-1 <= chrom <= -1)
		
		post[p, chrom]:
			__old__.p == p
			__old__.chrom == chrom
			isinstance(__return__, Individual)
			__return__.chromosomes[chrom] != p.chromosomes[chrom]
			forall(p.chromosomes[chrom], lambda e: e in __return__.chromosomes[chrom])
			forall(__return__.chromosomes[chrom], lambda e: e in p.chromosomes[chrom])
			len(__return__.chromsomes[chrom]) == len(p.chromosomes[chrom])
	"""
	
	pp = p
	p = p[chrom][:]
	shuffle(p)
	answer = Individual(pp.chromosomes[:])
	answer[chrom] = p
	return answer
