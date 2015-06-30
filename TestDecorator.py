"""
 * A Decorator for Tests. Use TestDecorator as the base class
 * for defining new test decorators. Test decorator subclasses
 * can be introduced to add behaviour before or after a test
 * is run.
 *
 **************************************
 * Ported to Python by Grig Gheorghiu *
 **************************************
"""

#from unittest import TestCase
from Test import Test

class TestDecorator(Test):
    
    def __init__(self, test):
        self.test = test

    def basicRun(self, result):
        self.test.run(result)
    
    def countTestCases(self):
        return self.test.countTestCases()
    
    def run(self, result):
        self.basicRun(result)
    
    def __str__(self):
        return str(self.test)

    def getTest(self):
        return self.test
