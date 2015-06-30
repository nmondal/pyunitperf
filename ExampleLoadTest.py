"""
 * The <code>ExampleLoadTest</code> demonstrates how to 
 * decorate a <code>Test</code> as a <code>LoadTest</code>.
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
from LoadTest import LoadTest
from TimedTest import TimedTest

class ExampleLoadTest:

    def __init__(self):
        self.toleranceInSec = 0.05

    def suite(self):
        s = TestSuite()
        s.addTest(self.make1SecondResponseSingleUserLoadTest())
        s.addTest(self.make1SecondResponseMultipleUserLoadTest())
        s.addTest(self.make1SecondResponse1UserLoadIterationTest())
        return s

    def make1SecondResponseSingleUserLoadTest(self):
        """
         * Decorates a one second response time test as a one
         * user load test with a maximum elapsed time of 1 second
         * and a 0 second delay between users.
         * 
         * @return Test.
        """ 
        users = 1
        maxElapsedTimeInSec = 1 + self.toleranceInSec

        testCase = ExampleTestCase("testOneSecondResponse")

        loadTest = LoadTest(testCase, users)
        timedTest = TimedTest(loadTest, maxElapsedTimeInSec)
        return timedTest
    
    def make1SecondResponseMultipleUserLoadTest(self):
        """
         * Decorates a one second response time test as a multiple-user
         * load test with a maximum elapsed time of 1.5 
         * seconds and a 0 second delay between users.
         * 
         * @return Test.
        """ 
        users = 10
        maxElapsedTimeInSec = 1.5 + self.toleranceInSec

        testCase = ExampleTestCase("testOneSecondResponse")

        loadTest = LoadTest(testCase, users)
        timedTest = TimedTest(loadTest, maxElapsedTimeInSec)

        return timedTest

    def make1SecondResponse1UserLoadIterationTest(self):
        """
         * Decorates a one second response time test as a one
         * user load test with 10 iterations per user, a maximum 
         * elapsed time of 10 seconds, and a 0 second delay
         * between users.
         * 
         * @see testOneSecondResponseOneUserLoadRepeatedTest
         * @return Test.
        """ 

        users = 1
        iterations = 10
        maxElapsedTimeInSec = 10 + self.toleranceInSec

        testCase = ExampleTestCase("testOneSecondResponse");

        loadTest = LoadTest(testCase, users, iterations)
        timedTest = TimedTest(loadTest, maxElapsedTimeInSec)

        return timedTest
        
"""

    /**
     * Decorates a one second response time test as a one
     * user load test with 10 iterations per user, a maximum 
     * elapsed time of 12 seconds, and a 0 second delay
     * between users.
     * 
     * @see testOneSecondResponseOneUserLoadIterationTest
     * @return Test.
     */ 
    protected static Test make1SecondResponse1UserLoadRepeatedTest() {

        int users = 1;
        int iterations = 10;
        long maxElapsedTimeInMillis = 10000 + toleranceInMillis;

        Test testCase = new ExampleTestCase("testOneSecondResponse");

        Test repeatedTest = new RepeatedTest(testCase, iterations);
        Test loadTest = new LoadTest(repeatedTest, users);
        Test timedTest = new TimedTest(loadTest, maxElapsedTimeInMillis);

        return timedTest;
    }

    /**
     * Decorates a one second response time test as a two
     * user load test with a maximum elapsed time of 4 seconds
     * and a 2 second delay between users.
     * 
     * @return Test.
     */ 
    protected static Test make1SecondResponse2UserLoad2SecondDelayTest() {

        int users = 2;
        Timer timer = new ConstantTimer(2000);
        long maxElapsedTimeInMillis = 4000 + toleranceInMillis;

        Test testCase = new ExampleTestCase("testOneSecondResponse");

        Test loadTest = new LoadTest(testCase, users, timer);
        Test timedTest = new TimedTest(loadTest, maxElapsedTimeInMillis);

        return timedTest;
    }

    /**
     * Decorates a one second response time test as a 10
     * user load test with 10 iterations per user, a maximum 
     * elapsed time of 20 seconds, and a 1 second delay
     * between users.
     * 
     * @return Test.
     */ 
    protected static Test 
    make1SecondResponse10UserLoad1SecondDelayIterationTest() {

        int users = 10;
        int iterations = 10;
        Timer timer = new ConstantTimer(1000);
        long maxElapsedTimeInMillis = 20000 + toleranceInMillis;

        Test testCase = new ExampleTestCase("testOneSecondResponse");

        Test loadTest = new LoadTest(testCase, users, iterations, timer);
        Test timedTest = new TimedTest(loadTest, maxElapsedTimeInMillis);

        return timedTest;
    }

    protected static Test makeStateful10UserLoadTest() {
        /**
         * Decorates a stateful test as a 10 user load test,
         * providing each user with a different test instance
         * to ensure thread safety.
         * 
         * @return Test.
         **/

        users = 10
        iterations = 1;

        Test factory = new TestFactory(ExampleStatefulTestCase.class);

        Test loadTest = new LoadTest(factory, users, iterations);

        return loadTest;
    }

    /**
     * Decorates a stateful test method as a 10 user load test,
     * providing each user with a different test instance
     * to ensure thread safety.
     * 
     * @return Test.
     */ 
    protected static Test makeStateful10UserLoadTestMethod() {

        int users = 10;
        int iterations = 1;

        Test factory = 
            new TestMethodFactory(ExampleStatefulTestCase.class, "testState");

        Test loadTest = new LoadTest(factory, users, iterations);

        return loadTest;
    }
"""

if __name__ == "__main__":
    TextTestRunner(verbosity=1).run(ExampleLoadTest().suite())

    