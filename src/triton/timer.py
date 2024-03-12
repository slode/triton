from timeit import default_timer as timer

class Stopwatch:
    def __init__(self, label=""):
        self.label = label
        self.samples = []
        self.start()

    def start(self):
        self._start = timer()

    def stop(self):
        self._stop = timer()
        self.samples.append(self._stop-self._start)
        self.start()

    def report(self):
        print("min: {}, max: {}, avg: {}, N: {}".
                format(
                    min(self.samples),
                    max(self.samples),
                    sum(self.samples)/len(self.samples),
                    len(self.samples)))
        self.samples = []


