"""
 * A <em>Test</em> can be run and collect its results.
 *
 * @see TestResult
 **************************************
 * Ported to Python by Grig Gheorghiu *
 **************************************
"""
class Test:

    def countTestCases(self):
        """
         * Counts the number of test cases that will be run by this test.
         "Abstract" method
        """
        None
        
    def run(self, result):
        """
         * Runs a test and collects its result in a TestResult instance.
         "Abstract" method
        """
        None
        
    def shortDescription(self):
        return str(self)
        
