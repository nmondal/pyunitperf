"""
 * The <code>ExampleTestCase</code> is an example
 * stateless <code>TestCase</code>.
 *
 * @author <b>Mike Clark</b>
 * @author Clarkware Consulting, Inc.
 **************************************
 * Ported to Python by Grig Gheorghiu *
 **************************************
"""

from unittest import TestCase, TestSuite, TextTestRunner, makeSuite
import time

class ExampleTestCase(TestCase):

    def __init__(self, name):
        TestCase.__init__(self, name)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testOneSecondResponse(self):
        time.sleep(1)
    
    def suite(self):
        return makeSuite(self.__class__)


if __name__ == "__main__":
    example = ExampleTestCase("testOneSecondResponse")
    runner = TextTestRunner()
    runner.run(example.suite())