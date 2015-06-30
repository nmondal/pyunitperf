"""
 * The <code>ExampleTimedTest</code> demonstrates how to 
 * decorate a <code>Test</code> as a <code>TimedTest</code>.
 *
 * @author <b>Mike Clark</b>
 * @author Clarkware Consulting, Inc.
 *
 * @see com.clarkware.junitperf.LoadTest
 * @see com.clarkware.junitperf.TimedTest
 **************************************
 * Ported to Python by Grig Gheorghiu *
 **************************************
"""

from unittest import TestSuite, TextTestRunner
from ExampleTestCase import ExampleTestCase
from TimedTest import TimedTest

class ExampleTimedTest:

    def __init__(self):
        self.toleranceInSec = 0.05

    def suite(self):
        s = TestSuite()
        s.addTest(self.make1SecondResponseTimedTest())
        return s

    def make1SecondResponseTimedTest(self):
        """
         * Decorates a one second response time test as a
         * timed test with a maximum elapsed time of 1 second
         * 
         * @return Test.
        """ 
        maxElapsedTimeInSec = 1 + self.toleranceInSec

        testCase = ExampleTestCase("testOneSecondResponse")
        timedTest = TimedTest(testCase, maxElapsedTimeInSec)
        return timedTest


if __name__ == "__main__":
    TextTestRunner(verbosity=2).run(ExampleTimedTest().suite())

    