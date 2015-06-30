"""
 * The <code>ThreadedTest</code> is a test decorator that
 * runs a test in a separate thread.
 *
 * @author <b>Mike Clark</b>
 * @author Clarkware Consulting, Inc.
 **************************************
 * Ported to Python by Grig Gheorghiu *
 **************************************
"""
import time
from threading import currentThread
from ThreadInGroup import ThreadInGroup
from Test import Test
from ThreadBarrier import ThreadBarrier

class ThreadedTest(Test):

	def __init__(self, test, thread_group=None, thread_barrier=None):
		"""
		Constructs a <code>ThreadedTest</code> to decorate the
		specified test using the specified thread group and
		thread barrier.
		
		@param test Test to decorate.
		@param group Thread group.
		@param barrier Thread barrier.
		"""
		#self.test = test_class(test_name)
		self.test = test
		self.group = thread_group
		self.barrier = thread_barrier
		if self.barrier is None:
			self.barrier = ThreadBarrier(1)


	def countTestCases(self):
		"""
		Returns the number of test cases in this threaded test.
		
		@return Number of test cases.
		"""
		return self.test.countTestCases()


	def run(self, result):
		"""
		Runs this test.
		
		@param result Test result.
		"""
		test_runner = TestRunner(result, self.test, self.barrier)
		t = ThreadInGroup(group=self.group, target=test_runner)
		#print "ThreadedTest thread starting at:", time.time()
		t.start()
		#return t
		#t.join()

	def __str__(self):
		return "ThreadedTest: " + str(self.test)
		
class TestRunner:

	def __init__(self, result, test, barrier):
		self.result = result
		self.test = test
		self.barrier = barrier
	
	def __call__(self):
		self.test.run(self.result)
		self.barrier.onCompletion(currentThread())
	
