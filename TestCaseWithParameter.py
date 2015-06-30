__author__ = 'noga'

from unittest import TestSuite, TextTestRunner, TestCase
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


class TestCaseWithParameter(TestCase):

    def __init__(self, method, *args):
        TestCase.__init__(self, "test")
        self.call_container = CallContainer(method,*args)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        self.call_container()



class ExampleLoadTestWithParameters :

    def __init__(self, tolerance=0.05):
        self.toleranceInSec = tolerance

    def method1(self, a,b):
        print("a=" + a + "b=" + b)

    def method2(self, a,b):
        print("a+b = " + str(a + b) )

    def makeMethod1Test(self):
        """
         * Decorates a one second response time test as a one
         * user load test with 10 iterations per user, a maximum
         * elapsed time of 10 seconds, and a 0 second delay
         * between users.
         *
         * @see testOneSecondResponseOneUserLoadRepeatedTest
         * @return Test.
        """

        users = 10
        iterations = 2
        maxElapsedTimeInSec = 10 + self.toleranceInSec
        testCase = TestCaseWithParameter( self.method1, "A1", "B1")
        loadTest = LoadTest(testCase, users, iterations)
        timedTest = TimedTest(loadTest, maxElapsedTimeInSec)

        return timedTest

    def suite(self):
        s = TestSuite()
        s.addTest(self.makeMethod1Test())
        return s


if __name__ == "__main__":

     TextTestRunner(verbosity=1).run(ExampleLoadTestWithParameters().suite())