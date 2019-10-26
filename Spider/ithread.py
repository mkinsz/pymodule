import threading

exited = False

class IThread(threading.Thread):
    """ Properties: 
            target: outside function
            args: params
    """
    def __init__(self, target, args):
        threading.Thread.__init__(self) #call constructor of father class
        self.target = target
        self.args = args

    def run(self):
        if exited:
            self.exit()
        self.target(self.args)

