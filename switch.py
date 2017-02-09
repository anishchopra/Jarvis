from exceptions import UnsupportedOp, NoDeviceConnection
import os

class Switch(object):
	def __init__(self, *args):
		raise UnsupportedOp()

	def on(self):
		raise UnsupportedOp()

	def off(self):
		raise UnsupportedOp()

	def toggle(self):
		raise UnsupportedOp()


class BelkinWemoSwitch(Switch):
	def __init__(self, ip):
		self.ip = ip

	def on(self):
		os.system('python2 wemo.py %s %s &' % (self.ip, 'on'))

	def off(self):
		os.system('python2 wemo.py %s %s &' % (self.ip, 'off'))