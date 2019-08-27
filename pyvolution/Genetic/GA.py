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

from Genetic import selection, visualization as vis

from random import random as rand
import logging as log
import pygame as pg #@UnresolvedImport

#for mod in [crossover, fitness, individual, mutation, population, selection, vis]:
#	contract.checkmod(mod)

log.basicConfig(format='%(levelname)s|%(message)s', level=log.DEBUG)

def runTSPGA(kwargs):
	"""
		pre:
			isinstance(kwargs, dict)
			'maxGens' in kwargs
			kwargs['maxGens'] > 0
		
		post[kwargs]:
			__old__.kwargs == kwargs
			__return__[0][1] >= kwargs['targetscore'] or __return__[1] == kwargs['maxGens']
			isinstance(__return__[0][0], Individual)
	"""
	
	# # # # # # PARAMETERS # # # # # #
	
	testmode = kwargs['testmode']
	
	maxGens = kwargs['maxGens']
	targetscore = kwargs['targetscore']
	genfunc = kwargs['genfunc']
	genparams = kwargs['genparams']

	scorefunc = kwargs['scorefunc']
	scoreparams = kwargs['scoreparams']

	selectfunc = kwargs['selectfunc']
	selectparams = kwargs['selectparams']
	
	numcross = kwargs['numcross']
	crossfunc = kwargs['crossfunc']
	crossfuncs = kwargs['crossfuncs']
	crossprob = kwargs['crossprob']
	crossparams = kwargs['crossparams']

	mutfunc = kwargs['mutfunc']
	mutprob = kwargs['mutprob']
	mutparams = kwargs['mutparams']
	
	SCORES = kwargs['SCORES']
	visualize = kwargs['visualize']
	getWheel = kwargs['getWheel']
	
	if visualize:
		makeScreenParams = kwargs['makeScreenParams']
		drawParams = kwargs['drawParams']
		font = kwargs['font']
		fontParams = kwargs['fontParams']
		labelParams = kwargs['labelParams']

	# # # # # # /PARAMETERS # # # # # #
	
	pop = genfunc(*genparams)
	for p in pop:
		if p not in SCORES:
			SCORES[p] = scorefunc(p, *scoreparams)
	
	best = max(SCORES, key=SCORES.__getitem__)
	best = best, SCORES[best]	# indiv, score
	
	if visualize:
		screen = vis.makeScreen(*makeScreenParams)
		label = font.render("%d / %d" %(best[1], targetscore), *fontParams)
		screen.blit(label, *labelParams)
		pg.display.init()
		vis.draw(best[0], screen, *drawParams)
	
	g = 0
	while g < maxGens:
		if testmode:
			assert g < maxGens
			assert best[1] < targetscore
			
		if getWheel:
			wheel = selection.getRouletteWheel(pop, SCORES)
		
		newpop = []
		for _ in xrange(numcross):
			if getWheel:
				p1 = selectfunc(wheel, *selectparams)
				p2 = selectfunc(wheel, *selectparams)
			else:
				p1, p2 = selectfunc(pop, *selectparams)
			if rand() <= crossprob:
				c1 = crossfunc(p1, p2, crossfuncs, crossparams)
				c2 = crossfunc(p2, p1, crossfuncs, crossparams)
				newpop.extend([c1,c2])
		
		for i,p in enumerate(newpop):
			if rand() <= mutprob:
				newpop[i] = mutfunc(p, *mutparams)
				p = newpop[i]
			SCORES[p] = scorefunc(p, *scoreparams)
		
		pop = sorted(pop+newpop, key=SCORES.__getitem__, reverse=True)[:len(pop)]
		
		fittest = max(pop, key=SCORES.__getitem__)
		fittest = fittest, SCORES[fittest]
		log.info("Generation %03d | highest fitness: %s | fittest indiv: %r" %(g, fittest[1], fittest[0].chromosomes[0]) )
		
		if fittest[1] > best[1]:
			best = fittest
			if visualize:
				screen = vis.makeScreen(*makeScreenParams)
				label = font.render("%d / %d" %(best[1], targetscore), *fontParams)
				screen.blit(label, *labelParams)
				pg.display.init()
				vis.draw(fittest[0], screen, *drawParams)
		
			if best[1] >= targetscore:
				if vis:
					raw_input("Hit <ENTER> to kill visualization: ")
					vis.killscreen()
				
				return best[0], g
		g += 1
	if vis:
		raw_input("Hit <ENTER> to kill visualization: ")
		vis.killscreen()
	
	if testmode:
		assert (g == maxGens) or best[1] >= targetscore

	return best, g

def runGA(kwargs, testmode=False):
	"""
		pre:
			isinstance(kwargs, dict)
			'maxGens' in kwargs
			kwargs['maxGens'] > 0
		
		post[kwargs]:
			__old__.kwargs == kwargs
			__return__[0][1] >= kwargs['targetscore'] or __return__[1] == kwargs['maxGens']
			isinstance(__return__[0][0], Individual)
	"""
	
	# # # # # # PARAMETERS # # # # # #
	
	maxGens = kwargs['maxGens']
	targetscore = kwargs['targetscore']
	genfunc = kwargs['genfunc']
	genparams = kwargs['genparams']

	scorefunc = kwargs['scorefunc']
	scoreparams = kwargs['scoreparams']

	selectfunc = kwargs['selectfunc']
	selectparams = kwargs['selectparams']
	
	numcross = kwargs['numcross']
	crossfunc = kwargs['crossfunc']
	crossfuncs = kwargs['crossfuncs']
	crossprob = kwargs['crossprob']
	crossparams = kwargs['crossparams']

	mutfunc = kwargs['mutfunc']
	mutprob = kwargs['mutprob']
	mutparams = kwargs['mutparams']
	
	SCORES = kwargs['SCORES']
	getWheel = kwargs['getWheel']

	# # # # # # /PARAMETERS # # # # # #
	
	pop = genfunc(*genparams)
	for p in pop:
		if p not in SCORES:
			SCORES[p] = scorefunc(p, *scoreparams)
	
	best = max(SCORES, key=SCORES.__getitem__)
	best = best, SCORES[best]	# indiv, score
	
	g = 0
	while g < maxGens:
		if testmode:
			assert g < maxGens
			assert best[1] < targetscore

		if getWheel:
			wheel = selection.getRouletteWheel(pop, SCORES)
		
		newpop = []
		for _ in xrange(numcross):
			if getWheel:
				p1 = selectfunc(wheel, *selectparams)
				p2 = selectfunc(wheel, *selectparams)
			else:
				p1, p2 = selectfunc(pop, *selectparams)
			if rand() <= crossprob:
				p1, p2 = crossfunc(p1, p2, crossfuncs, crossparams)
			newpop.extend([p1,p2])
		
		for i,p in enumerate(newpop):
			if rand() <= mutprob:
				newpop[i] = mutfunc(p, *mutparams)
				p = newpop[i]
			SCORES[p] = scorefunc(p, *scoreparams)
		
		pop = newpop
		
		fittest = max(pop, key=SCORES.__getitem__)
		fittest = fittest, SCORES[fittest]
		log.info("Generation %03d | highest fitness: %s | fittest indiv: %r" %(g, fittest[1], ''.join(fittest[0].chromosomes[0])) )
		if fittest[1] > best[1]:
			best = fittest
			if best[1] >= targetscore:
				return best, g
		g += 1
	
	if testmode:
		assert (g == maxGens) or best[1] >= targetscore
		
	return best[0], g

def run(kwargs):
	expected = "sanity testmode algorithm".split()
	for expect in expected:
		if expect not in kwargs:
			raise TypeError("Expected argument '%s' not found" %expect)

	arguments = kwargs.pop('sanity')
	
	if len(kwargs) < len(arguments):
		raise TypeError("Missing Arguements: %s" %' '.join([a for a in arguments if a not in kwargs]))

	testmode = kwargs['testmode']
	if testmode:
		import contract
		from Genetic import mutation, crossover, fitness, individual, population
		from Genetic.individual import Individual #@UnusedImport 
		contract.checkmod(__name__)
		for mod in [crossover, fitness, individual, mutation, population, selection, vis]:
			contract.checkmod(mod)
	
	kwargs.pop('algorithm')(kwargs)

if __name__ == "__main__":
	print 'starting'
	from Genetic import settings
#	kwargs = settings.getTSPSettings()
#	answer = run(kwargs)

	settings = settings.getOneMaxSettings()
	answer = run(settings)

	print 'done'