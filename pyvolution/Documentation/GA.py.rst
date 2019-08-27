GA.py
******
    
runTSPGA(kwargs)
=================

Run a GA that solves the Traveling Salesman Problem with the settings generated in settings.py


runGA(kwargs)
=============

Run a simple fitness-maximizing GA that solves any applicable problem. At the time of writing this document, it was applied to the One-Max problem

run(kwargs)
===========

This is the main driver function that runs the required evolutionary algorithm. But before it does that, it also checks the sanity and makes sure to import PyContract if required (as indicated by the ``testmode`` flag)