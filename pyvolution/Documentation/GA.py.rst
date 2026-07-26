GA.py
******

This module contains the main evolution driver. Earlier versions of this framework had
separate ``runTSPGA``/``run`` driver functions; the current source only defines
:func:`runGA`.

runGA(args)
============

.. function:: runGA(args)

   :param args.genfunc: generates the initial population, called as ``args.genfunc(args.genparams)``
   :param args.genparams: parameters for ``args.genfunc``
   :param args.SCORES: a dict caching individual -> fitness, shared with ``args.scoreparams``/``args.selectparams``
   :param args.scorefunc: evaluates an individual's fitness, dispatched across a process pool
   :param args.scoreparams: parameters for ``args.scorefunc``
   :param args.selectfunc: chooses individuals for reproduction, called as ``args.selectfunc(args.selectparams)``
   :param args.selectparams: parameters for ``args.selectfunc``
   :param args.getWheel: whether a roulette wheel must be (re)computed each generation before selection
   :param args.crossfunc: combines two parents into children, called as ``args.crossfunc(args.crossparams)``
   :param args.crossparams: parameters for ``args.crossfunc``
   :param args.crossprob: probability, in ``[0, 1]``, that a given pair of selected parents is crossed over (otherwise they are copied through unchanged)
   :param args.mutfunc: mutates a single child, called as ``args.mutfunc(args.mutparams)``
   :param args.mutprob: probability, in ``[0, 1]``, that a given child is mutated
   :param args.numCrossOvers: how many crossover operations to attempt per generation
   :param args.maxGens: the maximum number of generations to run
   :param args.targetscore: the fitness value at which evolution stops early
   :rtype: a 2-tuple ``((fittest individual, its score), generation reached)``

Generate the initial population via ``args.genfunc``, score it, and then repeat for up
to ``args.maxGens`` generations: select parents, cross them over (with probability
``args.crossprob``) and mutate the children (with probability ``args.mutprob``), score
the new population, and keep the fittest ``len(pop)`` individuals for the next
generation. Crossover and mutation work for a generation is dispatched to worker
processes defined in :doc:`parallel.py`. Evolution stops as soon as the fittest
individual's score reaches ``args.targetscore``, or after ``args.maxGens`` generations,
whichever comes first.

See :func:`settings.getOneMaxSettings` for a complete, concrete ``args`` for this
function.

.. warning::

    ``runGA`` currently raises ``NameError`` as soon as it is called: it contains
    ``scoreme = [p for p in pop in p not in SCORES]``, which is not valid population
    filtering (compare to the intended ``[p for p in pop if p not in SCORES]``) and
    fails before that expression's ``p`` is ever bound. ``runGA`` also does
    ``import sanity`` and calls ``sanity.sanity(args)`` as a precondition, but no
    ``sanity`` module exists anywhere in this repository. There is currently no way to
    run a full evolution end-to-end -- see the top-level README's Known Issues.

``if __name__ == "__main__"``
================================

Running ``GA.py`` directly builds the One-Max settings via
``settings.getOneMaxSettings()``, sets ``pystitia``'s test mode from
``args.__testmode__``, and calls ``args.func(args.args)`` (i.e. :func:`runGA`). Given
the bug above, this currently fails rather than running an evolution.
