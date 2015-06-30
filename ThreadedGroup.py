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

class ThreadedGroup:

	def __init__(self, name):
		self.name = name
		self.threads = []
		
	def addThread(self, thread):
		self.threads.append(thread)
		
	def delThread(self, thread):
		self.threads.remove(thread)

	def activeCount(self):
		return len(self.threads)
		
	def getName(self):
		return self.name
