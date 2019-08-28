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
import argparse
import concurrent.futures
import copy
import heapq
import multiprocessing as mp
import operator
from random import random as rand

import pystitia
import sanity
import selection
from individual import Individual
import parallel
from pystitia import contracts
from tqdm.patch import tqdm, print


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

	scoreme = [p for p in pop in p not in SCORES]
	scoreparams = []
	for s in scoreme:
		n = argparse.Namespace()
		for k,v in args.scoreparams.__dict__.items():
			setattr(n, k, v)
		n.individual = s
		scoreparams.append(s)

	with concurrent.futures.ProcessPoolExecutor() as E:
		for p, score in tqdm(zip(scoreme, E.map(args.scorefunc, scoreparams)), total=len(scoreme), desc='Computing Fitness'):
			SCORES[p] = score

	# for p in tqdm(pop, desc='Computing Fitness'):
	# 	if p not in SCORES:
	# 		args.scoreparams.individual = p
	# 		SCORES[p] = args.scorefunc(args.scoreparams)
	
	best = max(SCORES.items(), key=operator.itemgetter(1))  # indiv, score

	crossThese, mutThese, newKids = [mp.Queue() for _ in range(3)]
	numCrossProcs = 2 * ((mp.cpu_count()-2)/3)
	numMutProcs = (mp.cpu_count()-2)/3
	crossprocs = [mp.Process(target=parallel.crossoverSlave, args=(args, crossThese, mutThese)) for _ in range(numCrossProcs)]
	mutprocs = [mp.Process(target=parallel.mutateSlave, args=(args, mutThese, newKids)) for _ in range(numMutProcs)]
	for p in crossprocs: p.start()
	for p in mutprocs: p.start()

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
				crossThese.put(p1)
				crossThese.put(p2)
				# args.crossparams.p1 = p1
				# args.crossparams.p2 = p2
				children = args.crossfunc(args.crossparams)
			else:
				children = tuple(map(copy.deepcopy, (p1, p2)))
			for child in children:
				if rand() <= args.mutprob:
					mutThese.put(child)
				else:
					newpop.append(child)

		done = 0
		for c in newKids:
			if c is None:
				done += 1
				if done == numMutProcs: break

			newpop.append(c)
			if len(newpop) == len(pop): break

		scoreme = [p for p in newpop in p not in SCORES]
		scoreparams = []
		for s in scoreme:
			n = argparse.Namespace()
			for k, v in args.scoreparams.__dict__.items():
				setattr(n, k, v)
			n.individual = s
			scoreparams.append(s)

		with concurrent.futures.ProcessPoolExecutor() as E:
			for p, score in tqdm(zip(scoreme, E.map(args.scorefunc, scoreparams)), total=len(scoreme),
								 desc='Computing Fitness'):
				SCORES[p] = score

			pop = heapq.nlargest(args.genparams.popSize, pop+newpop, key=SCORES.__getitem__)
			fittest = max(pop, key=SCORES.__getitem__)
			fittest = fittest, SCORES[fittest]

			if fittest[1] > best[1]:
				best = fittest

				if best[1] >= args.targetscore:
					for p in crossprocs+mutprocs: p.terminate()
					return best[0], g

	for p in crossprocs + mutprocs: p.terminate()
	return best, g


if __name__ == "__main__":
	print('starting')
	import settings

	args = settings.getOneMaxSettings()
	pystitia.setTestMode(args.__testmode__)
	answer = args.func(args.args)

	print('done')