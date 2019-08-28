import multiprocessing as mp
import crossover

def crossoverSlave(args, qIn, qOut):

    for p1, p2 in iter(qIn.get, None):
        args.crossparams.p1 = p1
        args.crossparams.p2 = p2
        qOut.put(args.crossfunc(args.crossparams))


def mutateSlave(args, qIn, qOut):

    for p in iter(qIn.get, None):
        args.mutparams.individual = p
        qOut.put(args.mutfunc(args.mutparams))

    qOut.put(None)