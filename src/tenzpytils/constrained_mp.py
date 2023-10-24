import multiprocessing as mp
from time import sleep
from random import random


class ResourceConstrainedPool:
    def __init__(self, resources):
        self.queue = mp.Queue()
        for r in resources:
            self.queue.put(r)

    def runfunc(self, *args):
        r = self.queue.get()
        self.func(r, *args)
        self.queue.put(r)

    def starmap(self, func, args):
        self.func = func
        procs = [mp.Process(target=self.runfunc, args=(*a,)) for a in  args]
        for p in procs:
            p.start()
        for p in procs:
            p.join()


def whee(res, inp):
    print(res, inp)
    sleep(random())


if __name__ == '__main__':
    resources = [6, 7]
    rcp = ResourceConstrainedPool(resources)
    rcp.starmap(whee, [(i,) for i in range(20)])

