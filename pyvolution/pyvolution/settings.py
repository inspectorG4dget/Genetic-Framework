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

import fitness, selection, mutation, crossover, population, GA

from collections import defaultdict
from math import sqrt
from itertools import count


# class City:
# 	ID = count()
# 	def __init__(self, (X, Y, blah)):
# 		self.id = self.ID.next()
# 		self.x = float(X)
# 		self.y = float(Y)
#
# 	def __hash__(self):
# 		return self.id
#
# 	def __repr__(self):
# 		return str(self.id)
#
# 	def __eq__(self, other):
# 		if isinstance(other, City): return self.id == other.id
# 		elif isinstance(other, int): return self.id == other
#
#
# def readfromfile(infilepath):
# 	cities = []
# 	infile = open(infilepath)
# 	for line in infile:
# 		cities.append(City(tuple(line.strip().split(','))))
# 	return cities
#
# def getAdjMatrix(cities):
# 	answer = defaultdict(dict)
# 	for c1 in cities:
# 		for c2 in cities:
# 			answer[c1.id][c2.id] = sqrt((c1.x - c2.x)**2 + (c1.y - c2.y)**2)
#
# 	return dict(answer)
#
# def getTSPSettings():
#
# 	answer = argparse.Namespace()
#
# 	answer.algorithm = GA.runGA
# 	answer.__testmode__ = False
# 	answer.maxGens = 200
# 	answer.targetscore = -7542
# 	answer.popsize = 1000
#
# 	cities = readfromfile('berlin52.txt')
# 	DIST = getAdjMatrix(cities)
# 	COORDS = {city.id:(city.x, city.y) for city in cities}
# 	chromlen0 = 52
# 	numCrossovers = answer.popsize
# 	SCORES = {}
#
# 	answer.genfunc = population.genPop
# 	answer.genparams = argparse.Namespace()
# 	answer.genparams.popsize = answer.popsize
# 	answer.genparams.genfuncs = []
# 	answer.genparams.genfuncs.append(argparse.Namespace())
# 	answer.genparams.funcs[-1].func = population.genTour
# 	answer.genparams.funcs[-1].args = [(chromlen0,)]
#
# 	scorefunc = fitness.score
# 	scoreparams = ([fitness.scoreTSP], [(DIST,testmode)], SCORES)
#
# 	selectfunc = selection.tournamentSelect
# 	tournsize = 4
# 	numwinners = 2
# 	numselect = 2
# 	selectparams = (tournsize, numwinners, numselect, scorefunc, scoreparams)
#
# 	crossfunc = crossover.oneChildCrossover
# 	crossfuncs = (crossover.injectionco,)
# 	crossparams = [()]
#
# 	mutfunc = mutation.revmut
# 	mutparams = (0,)
#
# 	crossprob = 0.7
# 	mutprob = 0.05
#
# 	rouletteWheelRequireres = {selection.rouletteWheelSelect}
# 	getWheel = selectfunc in rouletteWheelRequireres
#
# 	visualize = True
# 	screenWidth = 640
# 	screenHeight = 640
# 	if visualize:
# 		makeScreenParams = (screenWidth, screenHeight)
# 		drawParams = (screenWidth, screenHeight, SCORES, COORDS)
# 		pg.init()
# 		pg.display.init()
# 		fon = pg.font.SysFont('monospace', 15)
# 		fontParams = (False, (0,255,255))
# 		labelParams = ((500,600),)
#
# 	sanity = """maxGens targetscore SCORES
# 				visualize
# 				genfunc genparams
# 				scorefunc scoreparams
# 				selectfunc selectparams
# 				crossfunc crossfuncs crossparams crossprob numcross
# 				mutfunc mutparams mutprob
# 				getWheel""".split()
# 	answer = {
# 			'algorithm' : algorithm,
# 			'testmode' : testmode,
# 			'maxGens' : maxGens,
# 			'targetscore' : targetscore,
# 			'SCORES' : SCORES,
# 			'genfunc' : genfunc,
# 			'genparams' : genparams,
# 			'inputs' : genparams,
# 			'scorefunc' : scorefunc,
# 			'scoreparams' : scoreparams,
# 			'selectfunc' : selectfunc,
# 			'selectparams' : selectparams,
# 			'crossfunc' : crossfunc,
# 			'crossfuncs' : crossfuncs,
# 			'crossprob' : crossprob,
# 			'numcross' : numCrossovers,
# 			'crossparams' : crossparams,
# 			'mutfunc' : mutfunc,
# 			'mutparams' : mutparams,
# 			'mutprob' : mutprob,
# 			'getWheel' : getWheel,
# 			'visualize' : visualize,
# 			'sanity' : sanity
# 			}
# 	if visualize:
# 		answer['makeScreenParams'] = makeScreenParams
# 		answer['drawParams'] = drawParams
# 		answer['font'] = fon
# 		answer['fontParams'] = fontParams
# 		answer['labelParams'] = labelParams
#
# 		answer['sanity'].extend("drawParams makeScreenParams font fontParams labelParams".split())
# 	return answer


def getOneMaxSettings():
	__testmode__ = False

	answer = argparse.Namespace()

	# Evolutionary Parameters
	answer.genfunc = population.genPop
	answer.maxGens = 100
	answer.targetscore = 30

	# Population Generation
	genparams = argparse.Namespace()
	answer.genparams = genparams
	genparams.popSize = 1000

	# Chromosome Generation
	genFuncs = []
	genparams.chromGens = genFuncs
	func1 = population.genCharsChrom
	params = argparse.Namespace()
	genFuncs.append((func1, params))
	params.bases = '01'
	params.numGenes = 30

	# Fitness
	answer.SCORES = {}
	answer.scorefunc = fitness.score
	scoreparams = argparse.Namespace()
	answer.scoreparams = scoreparams

	scoreparams.scorefuncs = []
	scoreparams.scorefuncs.append((fitness.scoreOnes, argparse.Namespace()))
	scoreparams.SCORES = answer.SCORES

	# Selection
	rouletteWheelRequireres = {selection.rouletteWheelSelect}
	selectfunc = selection.rouletteWheelSelect
	answer.getWheel = selectfunc in rouletteWheelRequireres
	selectparams = argparse.Namespace()
	selectparams.SCORES = answer.SCORES
	selectparams.scorefunc = answer.scorefunc
	selectparams.scoreparams = answer.scoreparams

	answer.selectfunc = selectfunc
	answer.selectparams = selectparams

	# Crossover
	answer.numCrossOvers = genparams.popSize
	answer.crossprob = 0.9
	answer.crossfunc = crossover.twoChildCrossover
	crossparams = []
	answer.crossparams = argparse.Namespace()
	answer.crossparams.crossparams = crossparams
	crossparams.append((crossover.crossOnes, argparse.Namespace()))

	# Mutation
	answer.mutprob = 0.05
	answer.mutfunc = mutation.mutateSingleAllele
	mutparams = argparse.Namespace()
	answer.mutparams = mutparams
	mutparams.chrom = 0
	mutparams.chars = answer.genparams.chromGens[0][1].bases

	# Final repackaging for run
	args = argparse.Namespace()
	args.args = answer
	answer = args
	answer.func = GA.runGA

	# debug
	answer.__testmode__ = __testmode__

	return answer
