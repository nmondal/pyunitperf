"""
 * The <code>Timer</code> interface defines the common interface 
 * implemented by all classes whose instances serve as pluggable timers.
 * 
 * @author <b>Mike Clark</b>
 * @author Clarkware Consulting, Inc.
 **************************************
 * Ported to Python by Grig Gheorghiu *
 **************************************
"""

class Timer:

	def getDelay(self):
		"""
		 Returns the timer delay.
		 
		 "Abstract" class
		"""
		None
