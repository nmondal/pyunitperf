"""
 * The <code>TimedTest</code> is a test decorator that 
 * runs a test and measures the elapsed time of the test.
 * <p>
 * A <code>TimedTest</code> is constructed with a specified
 * maximum elapsed time.  By default, a <code>TimedTest</code> 
 * will wait for the completion of its decorated test and
 * then fail if the maximum elapsed time was exceeded.
 * Alternatively, a <code>TimedTest</code> can be constructed 
 * to immediately signal a failure when the maximum elapsed time 
 * of its decorated test is exceeded.  In other words, the 
 * <code>TimedTest</code> will <b>not</b> wait for its decorated 
 * test to run to completion if the maximum elapsed time is 
 * exceeded.
 * </p>
 * <p>
 * For example, to decorate the <code>ExampleTest</code> 
 * as a <code>TimedTest</code> that waits for the 
 * <code>ExampleTest</code> test case to run 
 * to completion and then fails if the maximum elapsed 
 * time of 2 seconds is exceeded, use: 
 * <blockquote>
 * <pre>
 * Test timedTest = new TimedTest(new TestSuite(ExampleTest.class), 2000);
 * </pre>
 * </blockquote> 
 * or, to time a single test method, use: 
 * <blockquote>
 * <pre>
 * Test timedTest = new TimedTest(new ExampleTest("testSomething"), 2000);
 * </pre>
 * </blockquote> 
 * <p>
 * Alternatively, to decorate the <code>ExampleTest.testSomething()</code>
 * test as a <code>TimedTest</code> that fails immediately when
 * the maximum elapsed time of 2 seconds is exceeded, use:
 * <blockquote>
 * <pre>
 * Test timedTest = new TimedTest(new ExampleTest("testSomething"), 2000, false);
 * </pre>
 * </blockquote>
 * </p>
 * 
 * @author <b>Mike Clark</b>
 * @author Clarkware Consulting, Inc.
 * @author Ervin Varga
 **************************************
 * Ported to Python by Grig Gheorghiu *
 **************************************
"""

from unittest import TestResult
from threading import Thread
import sys, time

from CustomExceptions import AssertionFailedError
from TestDecorator import TestDecorator

try:
	bool = True
except:
	True = 1
	False = 0
	
class TimedTest(TestDecorator):

	def __init__(self, test, maxElapsedTime, waitForCompletion=True):
		"""
		 * Constructs a <code>TimedTest</code> to decorate the 
		 * specified test with the specified maximum elapsed time.
		 * 
		 * @param test Test to decorate.
		 * @param maxElapsedTime Maximum elapsed time (ms).
		 * @param waitForCompletion <code>true</code> (default) to 
		 *        indicate that the <code>TimedTest</code> should wait 
		 *        for its decorated test to run to completion and then 
		 *        fail if the maximum elapsed time was exceeded; 
		 *        <code>false</code> to indicate that the 
		 *        <code>TimedTest</code> should immediately signal 
		 *        a failure when the maximum elapsed time is exceeded.
		"""
		TestDecorator.__init__(self, test)
		self.maxElapsedTime = maxElapsedTime
		self.waitForCompletion = waitForCompletion
		self.maxElapsedTimeExceeded = False
		self.isQuiet = False
		self.test = test
	
	def setQuiet(self):
		"""
		 * Disables the output of the test's elapsed time.
		"""
		self.isQuiet = True
	

	def countTestCases(self):
		return TestDecorator.countTestCases(self)
	
	def outOfTime(self):
		"""
		 * Determines whether the maximum elapsed time of
		 * the test was exceeded.
		 *
		 * @return <code>true</code> if the max elapsed time
		 *         was exceeded; <code>false</code> otherwise.
		"""
		return self.maxElapsedTimeExceeded
	

	def run(self, result):
		"""
		// TODO: May require a strategy pattern
		//       if other algorithms emerge.
		"""
		if self.waitForCompletion:
			self.runUntilTestCompletion(result)
		else:
			self.runUntilTimeExpires(result)

	def __call__(self, result):
		self.run(result)
		
	def runUntilTestCompletion(self, result):
		"""
		 * Runs the test until test completion and then signals
		 * a failure if the maximum elapsed time was exceeded.
		 *
		 * @param result Test result.
		"""

		beginTime = time.time()
		TestDecorator.run(self, result)

		elapsedTime = self.getElapsedTime(beginTime)
		self.printElapsedTime(elapsedTime)
		if elapsedTime > self.maxElapsedTime:
			self.maxElapsedTimeExceeded = True
			result.addFailure(self.getTest(),
				(AssertionFailedError, AssertionFailedError("Maximum elapsed time exceeded!" +
				" Expected " + str(self.maxElapsedTime) + " sec., but was " +
				str(elapsedTime) + " sec."), None))
			#result.endTest(self.getTest())
			result.stop()
	
	def runUntilTimeExpires(self, result):
		"""
		 * Runs the test and immediately signals a failure 
		 * when the maximum elapsed time is exceeded.
		 *
		 * @param result Test result.
		"""
		runnable = Runnable(self, result)
		t = Thread(group=None, target=runnable)

		beginTime = time.time()
		
		t.start()

		try:
			t.join(self.maxElapsedTime)
		except:
			pass

		printElapsedTime(self.getElapsedTime(beginTime))
	
		if t.isAlive():
			self.maxElapsedTimeExceeded = True
			result.addFailure(self.getTest(),
				(AssertionFailedError, 
				AssertionFailedError("Maximum elapsed time (" + str(self.maxElapsedTime) + 
				" sec.) exceeded!"), None))
			#result.endTest(self.getTest())
			result.stop()

	def getElapsedTime(self, beginTime):
		endTime = time.time()
		return (endTime - beginTime)
	
	def printElapsedTime(self, elapsedTime):
		if not self.isQuiet:
			sys.stdout.write(str(self) + ": " + str(elapsedTime) + " sec.\n")
			sys.stdout.flush()
		
	def __str__(self):
		if self.waitForCompletion:
			return "TimedTest (WAITING): " + str(self.test) #str(TestDecorator(self))
		else:
			return "TimedTest (NON-WAITING): " + str(self.test) #str(TestDecorator(self))

class Runnable:
	
	def __init__(self, timed_test, result):
		self.timed_test = timed_test
		self.result = result
		
	def __call__(self):
		TestDecorator.run(timed_test, result)
		
		# IBM's JVM prefers this instead:
		# run(result);
		