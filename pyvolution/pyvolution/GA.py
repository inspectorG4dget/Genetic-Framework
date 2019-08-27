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

import heapq
import operator
import pystitia

import selection
import sanity
from individual import Individual

from random import random as rand
from tqdm.patch import tqdm, print
from pystitia import contracts


@contracts(
	preconditions=(
		lambda args: sanity.sanity(args),
		lambda args: hasattr(args, 'maxGens'),
		lambda args: args.maxGens > 0,
	),
	postconditions=(
		lambda args: __old__.args == args,
		lambda args: __return__[0][1] >= args.targetscore or __return__[1] >= args.maxGens,
		lambda: isinstance(__return__[0][0], Individual),
	)
)
def runGA(args):

	pop = args.genfunc(args.genparams)
	SCORES = args.SCORES
	for p in tqdm(pop, desc='Computing Fitness'):
		if p not in SCORES:
			args.scoreparams.individual = p
			SCORES[p] = args.scorefunc(args.scoreparams)
	
	best = max(SCORES.items(), key=operator.itemgetter(1))  # indiv, score

	for g in tqdm(range(args.maxGens), desc="Highest fitness: {:05f}".format(best[1])):
		if __testmode__:
			assert g < args.maxGens
			assert best[1] < args.targetscore
			
		args.selectparams.population = pop
		if args.getWheel:
			args.selectparams.pop = pop
			args.selectparams.wheel = selection.getRouletteWheel(args.selectparams)

		newpop = []
		for _ in tqdm(range(args.numCrossOvers), desc='Making offspring for the next generation'):
			if args.getWheel:
				p1 = args.selectfunc(args.selectparams)
				p2 = args.selectfunc(args.selectparams)
			else:
				p1, p2 = args.selectfunc(args.selectparams)
			if rand() <= args.crossprob:
				args.crossparams.p1 = p1
				args.crossparams.p2 = p2
				children = args.crossfunc(args.crossparams)
				for i, child in enumerate(children):
					if rand() <= args.mutprob:
						args.mutparams.individual = child
						child = args.mutfunc(args.mutparams)
						args.scoreparams.individual = child
					SCORES[child] = args.scorefunc(args.scoreparams)
					newpop.append(child)

		pop = heapq.nlargest(args.genparams.popSize, pop+newpop, key=SCORES.__getitem__)
		fittest = max(pop, key=SCORES.__getitem__)
		fittest = fittest, SCORES[fittest]
		
		if fittest[1] > best[1]:
			best = fittest
		
			if best[1] >= args.targetscore:
				return best[0], g

	return best, g


if __name__ == "__main__":
	print('starting')
	import settings

	args = settings.getOneMaxSettings()
	pystitia.setTestMode(args.__testmode__)
	answer = args.func(args.args)

	print('done')