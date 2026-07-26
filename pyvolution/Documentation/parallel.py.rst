parallel.py
************

This module defines the worker-process functions that :func:`GA.runGA` dispatches
crossover and mutation work to, via ``multiprocessing`` queues, as part of the CPU
parallelization support added to the framework.

crossoverSlave(args, qIn, qOut)
==================================

.. function:: crossoverSlave(args, qIn, qOut)

   :param args: the full evolution settings namespace (see :func:`settings.getOneMaxSettings`), used for ``args.crossparams`` and ``args.crossfunc``
   :param qIn: a ``multiprocessing.Queue`` of ``(p1, p2)`` chromosome pairs to cross over. The loop ends when ``None`` is read from the queue
   :param qOut: a ``multiprocessing.Queue`` that each pair's crossover result is put onto

Worker-process loop: for each ``(p1, p2)`` pulled from ``qIn``, sets
``args.crossparams.p1``/``.p2`` and calls ``args.crossfunc(args.crossparams)``, putting
the result onto ``qOut``.

mutateSlave(args, qIn, qOut)
==============================

.. function:: mutateSlave(args, qIn, qOut)

   :param args: the full evolution settings namespace, used for ``args.mutparams`` and ``args.mutfunc``
   :param qIn: a ``multiprocessing.Queue`` of individuals to mutate. The loop ends when ``None`` is read from the queue
   :param qOut: a ``multiprocessing.Queue`` that each mutated individual is put onto; a final ``None`` sentinel is put once the loop ends

Worker-process loop: for each individual pulled from ``qIn``, sets
``args.mutparams.individual`` and calls ``args.mutfunc(args.mutparams)``, putting the
result onto ``qOut``.

.. note::

    This worker assumes the configured ``mutfunc`` reads its individual from
    ``args.mutparams.individual`` -- true for :func:`mutation.mutateSingleAllele`, but
    not for :func:`mutation.swapmut`/:func:`mutation.revmut`/:func:`mutation.shufflemut`,
    which read ``args.p`` instead (see the naming note in :doc:`mutation.py`).
