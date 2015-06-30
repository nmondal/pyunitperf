__author__ = 'noga'

from unittest import TestSuite, TextTestRunner, TestCase
from ExampleTestCase import ExampleTestCase
from LoadTest import LoadTest
from TimedTest import TimedTest
import time

class CallContainer:

    def __init__(self, method, *args):
        self.method = method
        self.args = args
        self.timing = None
        self.result = None
        self.error = None
    pass

    def __call__(self, *args, **kwargs):
        try:
            st = time.time()
            self.result = self.method(*self.args)
            self.timing = time.time() - st
            self.error = None
        except Exception as e:
            self.error = e
            self.result = None
        pass



class ExampleLoadTestWithParameters :

    def __init__(self, tolerance=0.05):
        self.toleranceInSec = tolerance

    def test1(self, a,b):
        print("a=" + a + "b=" + b)

    def test2(self, a,b):
        print("a+b = " + str(a + b) )


    def suite(self):
        s = TestSuite()
        s.addTest(CallContainer(self.test1, "A1","B1" ) )
        s.addTest(CallContainer(self.test1, "A2","B2" ) )
        return s


if __name__ == "__main__":

     TextTestRunner(verbosity=1).run(ExampleLoadTestWithParameters().suite())