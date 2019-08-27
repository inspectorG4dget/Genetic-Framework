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

from itertools import izip
from Genetic.individual import Individual #@UnusedImport # import only for contract checking

def score(p, scorefuncs, scorefuncparams, SCORES):
	"""
		pre:
			isinstance(p, Individual)
			isinstance(scorefuncs, list)
			forall(scorefuncs, lambda f: hasattr(f, '__call__'))
			isinstance(scorefuncparams, list)
			forall(scorefuncparams, lambda p: isinstance(p, tuple))
			isinstance(SCORES, dict)
		
		post[p, SCORES, scorefuncs, scorefuncparams]:
			p == __old__.p
			p in SCORES
			scorefuncs == __old__.scorefuncs
			scorefuncparams == __old__.scorefuncparams
			(p in __old__.SCORES and len(__old__.SCORES) == len(SCORES)) ^ (p not in __old__.SCORES and len(__old__.SCORES)+1 == len(SCORES))
	"""

	if p not in SCORES:
		SCORES[p] = sum(scorefunc(chrom, *scoreparams) for scorefunc, scoreparams, chrom in izip(scorefuncs, scorefuncparams, p.chromosomes))
	
	return SCORES[p]

def scoreOnes(p):
	"""
		pre:
			isinstance(p, list)
			forall(p, lambda e: isinstance(e, str))
			forall(p, lambda e: len(e)==1)
			forall(p, lambda e: e in "01")
			
		post[p]:
			p == __old__.p
			isinstance(__return__, int)
			__return__ >= 0
	"""
	return p.count('1')

def scoreTSP(tour, DIST, testmode):
	"""
		pre:
			isinstance(tour, list)
			isinstance(DIST, dict)
			forall(tour, lambda e: isinstance(e, int))
			forall(DIST, lambda k: isinstance(k, int))
			forall(DIST, lambda k: isinstance(DIST[k], dict))
			forall(DIST, lambda k: forall(DIST[k], lambda e: isinstance(e, int)))
			forall(DIST, lambda k: forall(DIST[k], lambda e: isinstance(DIST[k][e], float)))
		
		post:
			isinstance(__return__, float)
		post[tour, DIST]:
			__old__.tour == tour
			__old__.DIST == DIST
			
	"""
	answer = 0
	numcities = len(tour)
	for i,source in enumerate(tour):
		if testmode:
			assert answer <= 0
		dest = tour[(i+1)%numcities]
		answer -= DIST[source][dest]
	return answer
