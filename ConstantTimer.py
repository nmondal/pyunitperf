"""
 * The <code>ConstantTimer</code> is a <code>Timer</code>
 * with a constant delay.
 * 
 * @author <b>Mike Clark</b>
 * @author Clarkware Consulting, Inc.
 *
 * @see com.clarkware.junitperf.Timer
 **************************************
 * Ported to Python by Grig Gheorghiu *
 **************************************
"""

from Timer import Timer

class ConstantTimer(Timer):

	def __init__(self, delay):
		"""
		 * Constructs a <code>ConstantTimer</code> with the
		 * specified delay.
		 *
		 * @param delay Delay (in milliseconds).
		"""
		self.delay = delay

	def getDelay(self):
		"""
		 * Returns the timer delay.
		 *
		 * @return Delay (in milliseconds).
		"""
		return self.delay
