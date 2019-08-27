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
from individual import Individual
from pystitia import contracts


@contracts(
	preconditions=(
		lambda args: isinstance(args.individual, Individual),
		lambda args: isinstance(args.chrom, int),
		lambda args: (0 <= args.chrom <= len(args.individual.chromosomes)-1) ^ (len(args.individual.chromosomes)*-1 <= args.chrom <= -1),
	),
	postconditions=(
		lambda args: __old__.args.individual == args.individual,
		lambda args: __old__.args.chrom == args.chrom,
		lambda args: __return__ is not args.individual,
		lambda args: __return__ != args.individual,
		lambda: __return__.chromosomes != __old__.args.individual.chromosomes,
		lambda args: all(e in args.chars for e in __return__.chromosomes[args.chrom]),
		lambda args: all(__old__.args.individual.chromosomes[i]==__return__.chromosomes[i] for i in range(len(args.individual.chromosomes)) if i!=args.chrom)
	)
)
def mutateSingleAllele(args): #p, chrom, chars):
	""" get the `chrom`th chromosome of the Individual p.
		Replace a random gene in this chromosome with a different allele from chars 
		Precondition: p[chrom] should be castable into a list
		Return a new individual. Do not destroy the input
	"""
	
	chromosome = args.individual[args.chrom][:]
	gene = randint(0, len(chromosome)-1)
	allele = choose([i for i in args.chars if i!= chromosome[gene]])
	chromosome[gene] = allele
	
	answer = Individual(args.individual.chromosomes[:])
	answer[args.chrom] = chromosome
	return answer


@contracts(
	preconditions=(
		lambda args: isinstance(args.p, Individual),
		lambda args: isinstance(args.chrom, int),
		lambda args: (0 <= args.chrom <= len(args.p.chromosomes)-1) ^ (len(args.p.chromosomes)*-1 <= args.chrom <= -1),
	),
	postconditions=(
		lambda args: __old__.args.p == args.p,
		lambda args: __old__.args.chrom == args.chrom,
		lambda: isinstance(__return__, Individual),
		lambda args: all(e in __return__.chromosomes[args.chrom] for e in args.p.chromosomes[args.chrom]),
		lambda args: all(e in args.p.chromosomes[args.chrom] for e in __return__.chromosomes[args.chrom]),
		lambda args: sum(i!=j for i,j in zip(__return__[args.chrom], args.p[args.chrom])) == 2,
	)
)
def swapmut(args): #p, chrom):
	""" Pick any two random cities and swap their positions in the tour 
		post[p, chrom]:
	"""

	answer = Individual(args.p.chromosomes[:])
	p = answer[args.chrom][:]
	i,j = sample(range(len(p)), 2)
	p[i], p[j] = p[j], p[i]
	answer[args.chrom] = p
	return answer


@contracts(
	preconditions=(
		lambda args: isinstance(args.p, Individual),
		lambda args: isinstance(args.chrom, int),
		lambda args: (0 <= args.chrom <= len(args.p.chromosomes)-1) ^ (len(args.p.chromosomes)*-1 <= args.chrom <= -1),
	),
	postconditions=(
		lambda args:__old__.args.p == args.p,
		lambda args: __old__.args.chrom == args.chrom,
		lambda: isinstance(__return__, Individual),
		lambda args: all(e in __return__.chromosomes[args.chrom] for e in args.p.chromosomes[args.chrom]),
		lambda args: all(e in args.p.chromosomes[args.chrom] for e in __return__.chromosomes[args.chrom]),
	)
)
def revmut(args): #p, chrom):
	""" Choose a random pair of points on the chromosome.
		Reverse the order of the genes between those two points on the chromosome 
	"""
	
	pp = args.p
	p = args.p[args.chrom]
	answer = []
	a,b = sample(range(len(p)), 2)
	if a>b: a,b = b,a
	answer.extend(p[:a])
	answer.extend(p[a:b+1][::-1])
	answer.extend(p[b+1:])
	indiv = Individual(pp.chromosomes[:])
	indiv[args.chrom] = answer
	return indiv


@contracts(
	preconditions=(
		lambda args: isinstance(args.p, Individual),
		lambda args: isinstance(args.chrom, int),
		lambda args: (0 <= args.chrom <= len(args.p.chromosomes) - 1) ^ (len(args.p.chromosomes) * -1 <= args.chrom <= -1),
	),
	postconditions=(
		lambda args: __old__.args.p == args.p,
		lambda args: __old__.args.chrom == args.chrom,
		lambda: isinstance(__return__, Individual),
		lambda args: __return__.chromosomes[args.chrom] != args.p.chromosomes[args.chrom],
		lambda args: all(e in __return__.chromosomes[args.chrom] for e in args.p.chromosomes[args.chrom]),
		lambda args: all(e in args.p.chromosomes[args.chrom] for e in __return__.chromosomes[args.chrom]),
		lambda args: len(__return__.chromsomes[args.chrom]) == len(args.p.chromosomes[args.chrom]),
	)
)
def shufflemut(args): #p, chrom):

	pp = args.p
	p = args.p[args.chrom][:]
	shuffle(p)
	answer = Individual(pp.chromosomes[:])
	answer[args.chrom] = p
	return answer
