"""
 * A Decorator that runs a test repeatedly.
 *
 **************************************
 * Ported to Python by Grig Gheorghiu *
 **************************************
"""

from TestDecorator import TestDecorator

class RepeatedTest(TestDecorator):
    
    def __init__(self, test, repeat):
        TestDecorator.__init__(self, test)
        if (repeat < 0):
            raise IllegalArgumentException("Repetition count must be > 0")
        self.test = test
        self.repeat = repeat
        
    def countTestCases(self):
        return self.timesRepeat * TestDecorator.countTestCases(self)
    
    def run(self, result):
        for i in range(self.repeat):
            #if result.shouldStop():
            #    break
            TestDecorator.run(self, result)
            
    def __call__(self, result):
        self.run(result)

    def __str__(self):
        return str(self.test) + "(repeated)"
    