"""
 * The <code>ThreadBarrier</code> class provides a callback
 * method for threads to signal their completion. 
 *
 * @author <b>Mike Clark</b>
 * @author Clarkware Consulting, Inc.
 **************************************
 * Ported to Python by Grig Gheorghiu *
 **************************************
"""

class ThreadBarrier:

	def __init__(self, numDispatched):
		"""
		Constructs a <code>ThreadBarrier</code> with the
		specified number of threads to wait for.
		
		@param numDispatched Number of threads dispatched.
		"""
		self.returnedCount = 0
		self.dispatchedCount = numDispatched

	def onCompletion(self, t):
		"""
		Called when the specified thread is complete.

		@param t Completed thread.
		"""
		self.returnedCount += 1

	def isReached(self):
		"""
		Determines whether the thread barrier has been reached -
		when all dispatched threads have returned.

		@return <code>true</code> if the barrier has been reached;
				<code>false</code> otherwise.
		"""
		return (self.returnedCount >= self.dispatchedCount)


	def cancelThreads(self, threadCount):
		"""
		Cancels the specified number of threads.

		@param threadCount Number of threads to cancel.
		"""
		self.returnedCount += threadCount
