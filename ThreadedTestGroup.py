"""
 * The <code>ThreadedTestGroup</code> is a <code>ThreadGroup</code>
 * that catches and handles exceptions thrown by threads created 
 * and started by <code>ThreadedTest</code> instances.
 * <p>
 * If a thread managed by a <code>ThreadedTestGroup</code> throws 
 * an uncaught exception, then the exception is added to the current 
 * test's results and all other threads are immediately interrupted.
 * </p>
 * 
 * @author Ervin Varga
 * @author <b>Mike Clark</b>
 * @author Clarkware Consulting, Inc.
 **************************************
 * Ported to Python by Grig Gheorghiu *
 **************************************
"""

from CustomExceptions import AssertionFailedError
from ThreadedGroup import ThreadedGroup

class ThreadedTestGroup(ThreadedGroup):

	def __init__(self, test, name):
		"""
		Constructs a <code>ThreadedTestGroup</code> for the specified test.
		"""
		ThreadedGroup.__init__(self, name)
		self.name = name
		self.test = test
	
	def setTestResult(self, result):
		"""
		Sets the current test result.
		"""
		self.testResult = result

	def uncaughtException(self, t, e):
		"""
		Called when a thread in this thread group stops because of
		an uncaught exception.
		<p>
		If the uncaught exception is a <code>ThreadDeath</code>,
		then it is ignored.  If the uncaught exception is an
		<code>AssertionFailedError</code>, then a failure
		is added to the current test's result.  Otherwise, an
		error is added to the current test's result.
		"""
		
		if isinstance(e, ThreadDeath):
			return
		
		if isinstance(e, AssertionFailedError):
			self.testResult.addFailure(self.test, e)
		else:
			self.testResult.addError(self.test, e)
		
		ThreadGroup.interrupt(self)
