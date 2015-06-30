"""
 * The <code>LoadTest</code> is a test decorator that runs
 * a test with a simulated number of concurrent users and
 * iterations.
 * <p>
 * In its simplest form, a <code>LoadTest</code> is constructed 
 * with a test to decorate and the number of concurrent users.
 * </p>
 * <p>
 * For example, to create a load test of 10 concurrent users
 * with each user running <code>ExampleTest</code> once and 
 * all users started simultaneously, use:
 * <blockquote>
 * <pre>
 * Test loadTest = new LoadTest(new TestSuite(ExampleTest.class), 10);
 * </pre>
 * </blockquote>
 * or, to load test a single test method, use: 
 * <blockquote>
 * <pre>
 * Test loadTest = new LoadTest(new ExampleTest("testSomething"), 10);
 * </pre>
 * </blockquote>
 * </p>
 * <p>
 * The load can be ramped by specifying a pluggable 
 * <code>Timer</code> instance which prescribes the delay
 * between the addition of each concurrent user.  A
 * <code>ConstantTimer</code> has a constant delay, with 
 * a zero value indicating that all users will be started 
 * simultaneously. A <code>RandomTimer</code> has a random 
 * delay with a uniformly distributed variation.
 * </p>
 * <p>
 * For example, to create a load test of 10 concurrent users
 * with each user running <code>ExampleTest.testSomething()</code> once and 
 * with a one second delay between the addition of users, use:
 * <blockquote>
 * <pre>
 * Timer timer = new ConstantTimer(1000);
 * Test loadTest = new LoadTest(new ExampleTest("testSomething"), 10, timer);
 * </pre>
 * </blockquote>
 * </p>
 * <p>
 * In order to simulate each concurrent user running a test for a 
 * specified number of iterations, a <code>LoadTest</code> can be 
 * constructed to decorate a <code>RepeatedTest</code>. 
 * Alternatively, a <code>LoadTest</code> convenience constructor 
 * specifying the number of iterations is provided which creates a 
 * <code>RepeatedTest</code>. 
 * </p>
 * <p>
 * For example, to create a load test of 10 concurrent users
 * with each user running <code>ExampleTest.testSomething()</code> for 20 iterations, 
 * and with a one second delay between the addition of users, use:
 * <blockquote>
 * <pre>
 * Timer timer = new ConstantTimer(1000);
 * Test repeatedTest = new RepeatedTest(new ExampleTest("testSomething"), 20);
 * Test loadTest = new LoadTest(repeatedTest, 10, timer);
 * </pre>
 * </blockquote>
 * or, alternatively, use: 
 * <blockquote>
 * <pre>
 * Timer timer = new ConstantTimer(1000);
 * Test loadTest = new LoadTest(new ExampleTest("testSomething"), 10, 20, timer);
 * </pre>
 * </blockquote> 
 * A <code>LoadTest</code> can be decorated as a <code>TimedTest</code>
 * to test the elapsed time of the load test.  For example, to decorate 
 * the load test constructed above as a timed test with a maximum elapsed 
 * time of 2 seconds, use:
 * <blockquote>
 * <pre>
 * Test timedTest = new TimedTest(loadTest, 2000);
 * </pre>
 * </blockquote>
 * </p>
 * <p>
 * By default, a <code>LoadTest</code> does not enforce test 
 * atomicity (as defined in transaction processing) if its decorated 
 * test spawns threads, either directly or indirectly.  In other words, 
 * if a decorated test spawns a thread and then returns control without 
 * waiting for its spawned thread to complete, then the test is assumed 
 * to be transactionally complete.  
 * </p>
 * <p>
 * If threads are integral to the successful completion of 
 * a decorated test, meaning that the decorated test should not be 
 * treated as complete until all of its threads complete, then  
 * <code>setEnforceTestAtomicity(true)</code> should be invoked to 
 * enforce test atomicity.  This effectively causes the load test to 
 * wait for the completion of all threads belonging to the same 
 * <code>ThreadGroup</code> as the thread running the decorated test.
 * </p>
 * @author <b>Mike Clark</b>
 * @author Clarkware Consulting, Inc.
 * @author Ervin Varga
 **************************************
 * Ported to Python by Grig Gheorghiu *
 **************************************
"""

import time
from threading import Thread
from unittest import TestResult, TestCase
from Test import Test
from RepeatedTest import RepeatedTest
from ConstantTimer import ConstantTimer
from CustomExceptions import IllegalArgumentException
from ThreadBarrier import ThreadBarrier
from ThreadedTestGroup import ThreadedTestGroup
from ThreadedTest import ThreadedTest

try:
	bool = True
except:
	True = 1
	False = 0
	
class LoadTest(Test):

	def __init__(self, test, users, iterations=0, timer=None):
		"""
		 * Constructs a <code>LoadTest</code> to decorate 
		 * the specified test using the specified number 
		 * of concurrent users starting simultaneously and
		 * the number of iterations per user. If a Timer is
		 * indicated, then a delay is introduced
		 *
		 * @param test Test to decorate.
		 * @param users Number of concurrent users.
		 * @param iterations Number of iterations per user.
		 * @param timer Delay timer.
		"""
		if iterations:
			test = RepeatedTest(test, iterations)
		if timer is None:
			timer = ConstantTimer(0)
			
		if users < 1:
			raise IllegalArgumentException("Number of users must be > 0")
		if timer is None:
			raise IllegalArgumentException("Delay timer is null")
		if test is None:
			raise IllegalArgumentException("Decorated test is null")

		self.users = users
		self.timer = timer
		self.setEnforceTestAtomicity(False)
		self.barrier = ThreadBarrier(users)
		self.group = ThreadedTestGroup(self, "LoadTest:ThreadedTestGroup")
		self.test = ThreadedTest(test, self.group, self.barrier)
	
	def setEnforceTestAtomicity(self, isAtomic):
		"""
		 * Indicates whether test atomicity should be enforced.
		 * <p>
	 	 * If threads are integral to the successful completion of 
	 	 * a decorated test, meaning that the decorated test should not be 
	 	 * treated as complete until all of its threads complete, then  
	 	 * <code>setEnforceTestAtomicity(true)</code> should be invoked to 
	 	 * enforce test atomicity.  This effectively causes the load test to 
	 	 * wait for the completion of all threads belonging to the same 
	 	 * <code>ThreadGroup</code> as the thread running the decorated test.
	 	 * 
		 * @param isAtomic <code>true</code> to enforce test atomicity;
		 *                 <code>false</code> otherwise.
		 """
		self.enforceTestAtomicity = isAtomic
	
	def countTestCases(self):
		"""
		 * Returns the number of tests in this load test.
		 *
		 * @return Number of tests.
		"""
		return self.users * self.test.countTestCases()

	def run(self, result):
		"""
		 * Runs the test.
		 *
		 * @param result Test result.
		"""
		self.group.setTestResult(result)
		for i in range(self.users):
			#if result.shouldStop():
			#	self.barrier.cancelThreads(self.users - i)
			#	break
			self.test.run(result)
			self.sleep(self.getDelay())
		
		self.waitForTestCompletion()
		self.cleanup()

	def __call__(self, result):
		self.run(result)
	
	def waitForTestCompletion(self):
		"""
		// TODO: May require a strategy pattern
		//       if other algorithms emerge.
		"""
		if self.enforceTestAtomicity:
			self.waitForAllThreadsToComplete()
		else:
			self.waitForThreadedTestThreadsToComplete()

	def waitForThreadedTestThreadsToComplete(self):
		while not self.barrier.isReached():
			self.sleep(50)
	
	def waitForAllThreadsToComplete(self):
		while self.group.activeCount() > 0:
			self.sleep(50)
	
	def sleep(self, ms):
		try:
			time.sleep(ms*0.001)
		except:
			pass
	
	def cleanup(self):
		try:
			self.group.destroy()
		except:
			pass
	
	def __str__(self):
		if self.enforceTestAtomicity:
			return "LoadTest (ATOMIC): " + str(self.test)
		else:
			return "LoadTest (NON-ATOMIC): " + str(self.test)

	def getDelay(self):
		return self.timer.getDelay()
