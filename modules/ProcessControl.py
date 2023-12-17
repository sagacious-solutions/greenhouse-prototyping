from multiprocessing import Process


class ProcessControl :

    def __init__ (self) :
        self.__processes = []

    def startProcess (self, name, fn, kwargs={}):
        newP = self.DeviceProcess(name, fn, kwargs)
        newP.process.start()
        self.__processes.append(newP)

    class DeviceProcess :
        def __init__ (self, name, fn, kwargs={}):
            self.name = name
            self.fn = fn
            self.kwargs = kwargs
            self.process = Process(target=fn, kwargs=kwargs)

