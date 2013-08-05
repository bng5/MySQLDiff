
import sys
import os

class Persistence:
    def __init__(self, userDataDir):
        if not os.path.exists(userDataDir):
            os.makedirs(userDataDir)
        self.userDataDir = userDataDir

#if __name__=="__main__":
#    print UserData("some.ini", _ConfigDefault)
