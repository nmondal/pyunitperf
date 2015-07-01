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


class TestCaseWithParameters(TestCase):

    def __init__(self, method, *args):
        TestCase.__init__(self, "test")
        self.call_container = CallContainer(method,*args)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        self.call_container()


    def __str__(self):
      return   str ( self.call_container.method.__name__ ) + "->" +  str( self.call_container.args )


    @staticmethod
    def load_test_case( method, max_time, users=10, iterations=3,  *args):
        testCase = TestCaseWithParameters( method, *args)
        loadTest = LoadTest(testCase, users, iterations)
        timedTest = TimedTest(loadTest, max_time)
        return timedTest
        pass



class ExampleLoadTestWithParameters :

    def __init__(self, tolerance=0.05):
        self.toleranceInSec = tolerance

    def method1(self, a,b):
        print("a=" + a + "b=" + b)

    def method2(self, a,b):
        print("a+b = " + str(a + b) )

    def suite(self):
        s = TestSuite()
        s.addTest( TestCaseWithParameters.load_test_case( self.method1, 10.05,
                                                          10, 2, "A1" , "B1" ))
        return s


if __name__ == "__main__":

     TextTestRunner(verbosity=1).run(ExampleLoadTestWithParameters().suite())