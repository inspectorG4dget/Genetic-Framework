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

from Genetic import fitness, selection, mutation, crossover, population, GA

from collections import defaultdict
from math import sqrt
from itertools import count

import pygame as pg #@UnresolvedImport


class City:
	ID = count()
	def __init__(self, (X, Y, blah)):
		self.id = self.ID.next()
		self.x = float(X)
		self.y = float(Y)
		
	def __hash__(self):
		return self.id
	
	def __repr__(self):
		return str(self.id)
	
	def __eq__(self, other):
		if isinstance(other, City): return self.id == other.id
		elif isinstance(other, int): return self.id == other


def readfromfile(infilepath):
	cities = []
	infile = open(infilepath)
	for line in infile:
		cities.append(City(tuple(line.strip().split(','))))
	return cities

def getAdjMatrix(cities):
	answer = defaultdict(dict)
	for c1 in cities:
		for c2 in cities:
			answer[c1.id][c2.id] = sqrt((c1.x - c2.x)**2 + (c1.y - c2.y)**2)
	
	return dict(answer)

def getTSPSettings():
	
	algorithm = GA.runTSPGA
	testmode = False
	maxGens = 200
	targetscore = -7542
	popsize = 1000
	
	cities = readfromfile('berlin52.txt')
	DIST = getAdjMatrix(cities)
	COORDS = {city.id:(city.x, city.y) for city in cities}
	chromlen0 = 52
	numCrossovers = popsize
	SCORES = {}
	
	genfunc = population.genPop
	genparams = (popsize, [population.genTour], [(chromlen0,)])
	
	scorefunc = fitness.score
	scoreparams = ([fitness.scoreTSP], [(DIST,testmode)], SCORES)
	
	selectfunc = selection.tournamentSelect
	tournsize = 4
	numwinners = 2
	numselect = 2
	selectparams = (tournsize, numwinners, numselect, scorefunc, scoreparams)
	
	crossfunc = crossover.oneChildCrossover
	crossfuncs = (crossover.injectionco,)
	crossparams = [()]
	
	mutfunc = mutation.revmut
	mutparams = (0,)
	
	crossprob = 0.7
	mutprob = 0.05
	
	rouletteWheelRequireres = {selection.rouletteWheelSelect}
	getWheel = selectfunc in rouletteWheelRequireres
	
	visualize = True
	screenWidth = 640
	screenHeight = 640
	if visualize:
		makeScreenParams = (screenWidth, screenHeight)
		drawParams = (screenWidth, screenHeight, SCORES, COORDS)
		pg.init()
		pg.display.init()
		fon = pg.font.SysFont('monospace', 15)
		fontParams = (False, (0,255,255))
		labelParams = ((500,600),)
	
	sanity = """maxGens targetscore SCORES 
				visualize
				genfunc genparams
				scorefunc scoreparams 
				selectfunc selectparams 
				crossfunc crossfuncs crossparams crossprob numcross
				mutfunc mutparams mutprob 
				getWheel""".split()
	answer = {
			'algorithm' : algorithm,
			'testmode' : testmode,
			'maxGens' : maxGens,
			'targetscore' : targetscore,
			'SCORES' : SCORES,
			'genfunc' : genfunc,
			'genparams' : genparams,
			'inputs' : genparams,
			'scorefunc' : scorefunc,
			'scoreparams' : scoreparams,
			'selectfunc' : selectfunc,
			'selectparams' : selectparams,
			'crossfunc' : crossfunc,
			'crossfuncs' : crossfuncs,
			'crossprob' : crossprob,
			'numcross' : numCrossovers,
			'crossparams' : crossparams,
			'mutfunc' : mutfunc,
			'mutparams' : mutparams,
			'mutprob' : mutprob,
			'getWheel' : getWheel,
			'visualize' : visualize,
			'sanity' : sanity
			}
	if visualize:
		answer['makeScreenParams'] = makeScreenParams
		answer['drawParams'] = drawParams
		answer['font'] = fon
		answer['fontParams'] = fontParams
		answer['labelParams'] = labelParams
		
		answer['sanity'].extend("drawParams makeScreenParams font fontParams labelParams".split())
	return answer

def getOneMaxSettings():
	
	maxGens = 10
	targetscore = 30
	popsize = 1000
	alleles0 = '01'
	chromlen0 = 30
	numCrossovers = popsize
	SCORES = {}
	testmode = True
	
	genfunc = population.genPop
	genparams = (popsize, [population.genCharsChrom], [(chromlen0, alleles0)])
	
	scorefunc = fitness.score
	scoreparams = ([fitness.scoreOnes], [()], SCORES)
	
#	selectfunc = selection.tournamentSelect
#	tournsize = 10
#	numwinners = 1
#	numselect = 2
#	selectparams = (tournsize, numwinners, numselect, scorefunc, scoreparams)
	
	selectfunc = selection.rouletteWheelSelect
	selectparams = ()
	
	crossprob = 0.9
	mutprob = 0.05
	
	crossfunc = crossover.twoChildCrossover
	crossfuncs = (crossover.crossOnes,)
	crossparams = [()]
	
	mutfunc = mutation.mutateSingleAllele
	mutparams = (0, alleles0)
	
	rouletteWheelRequireres = {selection.rouletteWheelSelect}
	getWheel = selectfunc in rouletteWheelRequireres
	
	sanity = """maxGens targetscore SCORES
				genfunc genparams
				scorefunc scoreparams 
				selectfunc selectparams 
				crossfunc crossfuncs crossparams crossprob numcross
				mutfunc mutparams mutprob 
				getWheel""".split()
	answer = {
			'algorithm' : GA.runGA,
			'testmode' : testmode,
			'maxGens' : maxGens,
			'targetscore' : targetscore,
			'SCORES' : SCORES,
			'genfunc' : genfunc,
			'genparams' : genparams,
			'inputs' : genparams,
			'scorefunc' : scorefunc,
			'scoreparams' : scoreparams,
			'selectfunc' : selectfunc,
			'selectparams' : selectparams,
			'crossfunc' : crossfunc,
			'crossfuncs' : crossfuncs,
			'crossprob' : crossprob,
			'numcross' : numCrossovers,
			'crossparams' : crossparams,
			'mutfunc' : mutfunc,
			'mutparams' : mutparams,
			'mutprob' : mutprob,
			'getWheel' : getWheel,
			'sanity' : sanity
			}
	return answer
