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

from individual import Individual
from pystitia import contracts


@contracts(
	preconditions=(
		lambda args: isinstance(args.individual, Individual),
		lambda args: isinstance(args.scorefuncs, list),
		lambda args: all(hasattr(f, '__call__') for f,_ in args.scorefuncs),
		lambda args: isinstance(args.scorefuncs, list),
		lambda args: all(isinstance(s, tuple) for _, s in enumerate(args.scorefuncs)),
		lambda args: isinstance(args.SCORES, dict)
	),
	postconditions=(
		lambda args: args.individual == __old__.args.individual,
		lambda args: args.individual in args.SCORES,
		# lambda args: args.scorefuncs == __old__.args.scorefuncs,
		lambda args: (args.individual in __old__.args.SCORES and len(__old__.args.SCORES) == len(args.SCORES)) ^ (args.individual not in __old__.args.SCORES and len(__old__.args.SCORES)+1 == len(args.SCORES))
	)
)
def score(args): #p, scorefuncs, scorefuncparams, SCORES):
	if args.individual not in args.SCORES:
		total = 0
		for i, (scorefunc, scoreparams) in enumerate(args.scorefuncs):
			scoreparams.individual = args.individual
			scoreparams.chrom = i
			total += scorefunc(scoreparams)
			del scoreparams.individual

		args.SCORES[args.individual] = total

	return args.SCORES[args.individual]


@contracts(
	preconditions=(
		lambda args: isinstance(args.individual, Individual),
		lambda args: all(isinstance(e, list) for e in args.individual),
		lambda args: all(e in '01' for e in args.individual[0])
	),
	postconditions=(
		lambda args: args.individual == __old__.args.individual,
		lambda : isinstance(__return__, int),
		lambda : __return__ >= 0
	)
)
def scoreOnes(args):
	return args.individual[args.chrom].count('1')


@contracts(
	preconditions=(
		lambda args: isinstance(args.tour, list),
		lambda args: all(isinstance(e, int) for e in args.tour),
		lambda args: isinstance(args.DIST, dict),
		lambda args: all(isinstance(k, int) for k in args.DIST),
		lambda args: all(isinstance(v, dict) for v in args.DIST.values()),
		lambda args: all(isinstance(e, int) for k in args.DIST for e in args.DIST[k]),
		lambda args: all(isinstance(args.DIST[k][e], float) for k in args.DIST for e in args.DIST[k]),
	),
	postconditions=(
		lambda : isinstance(__return__, float),
		lambda tour: __old__.args.tour == tour,
		lambda DIST: __old__.args.DIST == DIST,
	)
)
def scoreTSP(args): #tour, DIST):
	answer = 0
	numcities = len(args.tour)
	for i,source in enumerate(args.tour):
		if __testmode__:
			assert answer <= 0
		dest = args.tour[(i+1)%numcities]
		answer -= args.DIST[source][dest]
	return answer
