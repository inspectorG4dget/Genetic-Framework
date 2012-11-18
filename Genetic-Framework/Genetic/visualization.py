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

import pygame as pg #@UnresolvedImport
from Genetic.individual import Individual #@UnusedImport # used only for contract checking

def makeScreen(W, H):
	"""
		pre:
			isinstance(W, int)
			isinstance(H, int)
		
		post[W, H]:
			__old__.W == W
			__old__.H == H
	"""
	
	pg.init()
	window = pg.display.set_mode((W, H))
	return window

def normalize(point, (olow, ohigh), (low, high)):
	"""
		pre:
			isinstance(ohigh, float) ^ isinstance(ohigh, int)
			isinstance(high, float) ^ isinstance(high, int)
			isinstance(olow, float) ^ isinstance(olow, int)
			isinstance(low, float) ^ isinstance(low, int)
			isinstance(point, float) ^ isinstance(point, int)
		
		post:
			isinstance(__return__, float)
		post[low, high, olow, ohigh, point]:
			low <= __return__ <= high
			__old__.low == low
			__old__.high == high
			__old__.olow == olow
			__old__.ohigh == ohigh
			__old__.point == point
	"""
	
	return low + ((point/(ohigh-olow)) * (high-low))

def draw(tour, window, W, H, SCORES, COORDS):
	"""
		pre:
			isinstance(tour, Individual)
			forall(tour.chromosomes[0], lambda c: isinstance(c, int))
			isinstance(W, int)
			isinstance(H, int)
			isinstance(SCORES, dict)
			isinstance(COORDS, dict)
			forall(tour.chromosomes[0], lambda c: c in COORDS)
			forall(tour.chromosomes[0], lambda c: isinstance(COORDS[c], tuple))
			forall(tour.chromosomes[0], lambda c: isinstance(COORDS[c][0], int) ^ isinstance(COORDS[c][0], float))
			forall(tour.chromosomes[0], lambda c: isinstance(COORDS[c][1], int) ^ isinstance(COORDS[c][1], float))
			
		post[tour, W, H, SCORES, COORDS]:
			__old__.tour == tour
			__old__.W == W
			__old__.H == H
			__old__.SCORES == SCORES
			__old__.COORDS == COORDS
	"""
	
	tour = tour.chromosomes[0]
	numcities = len(tour)
	for i, source in enumerate(tour):
		dest = tour[(i+1) %numcities]
		x,y = COORDS[source]
		a,b = COORDS[dest]
		x,a = map(lambda x: normalize(x, (0.0,1800.0), (0,W)), [x,a])
		y,b = map(lambda x: normalize(x, (0.0,1200.0), (0,H)), [y,b])
		
		pg.draw.circle(window, (255,0,0), (int(x),int(y)), 3, 0)
		pg.draw.line(window, (255,255,255), (x,y), (a,b))
	
	pg.display.flip()

def killscreen():
	pg.display.quit()
