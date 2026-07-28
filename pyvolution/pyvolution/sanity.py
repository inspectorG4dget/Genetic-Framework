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

REQUIRED_ATTRS = (
	'maxGens', 'targetscore', 'SCORES',
	'genfunc', 'genparams',
	'scorefunc', 'scoreparams',
	'selectfunc', 'selectparams', 'getWheel',
	'numCrossOvers', 'crossfunc', 'crossparams', 'crossprob',
	'mutfunc', 'mutparams', 'mutprob',
)


def sanity(args):
	""" Validate that `args` (the settings Namespace passed to GA.runGA) has
		everything runGA needs before evolution starts. Raises on the first
		problem found; returns True if args is sane.
	"""

	for attr in REQUIRED_ATTRS:
		if not hasattr(args, attr):
			raise AttributeError(f"settings is missing required attribute: {attr!r}")

	if args.maxGens <= 0:
		raise ValueError(f"maxGens must be > 0, got {args.maxGens!r}")

	if not (0 <= args.crossprob <= 1):
		raise ValueError(f"crossprob must be between 0 and 1, got {args.crossprob!r}")

	if not (0 <= args.mutprob <= 1):
		raise ValueError(f"mutprob must be between 0 and 1, got {args.mutprob!r}")

	return True
