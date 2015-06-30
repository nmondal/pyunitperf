"""
Port of jUnitPerf to Python
 **************************************
 * Ported to Python by Grig Gheorghiu *
 **************************************
"""

from threading import Thread

class ThreadInGroup(Thread):

	def __init__(self, group, target, name=None):
		Thread.__init__(self, group=None, target=target, name=name)
		self.group = group
		self.group.addThread(self)

	def __del__(self):
		self.group.delThread(self)
		
