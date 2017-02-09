from exceptions import UnsupportedOp
import os

class AssistantInterface(object):
	def __init__(self, *args):
		raise UnsupportedOp()

	def send_message(self, text, **args):
		raise UnsupportedOp()

class MessengerInterface(AssistantInterface):
	def __init__(self, user_id):
		self.user_id = user_id

	def send_message(self, message, quick_replies=[]):
		qr_str = ""
		for text,payload in quick_replies:
			qr_str += text + ' ' + payload + ' '
		os.system('node respond.js %s %s %s %s &' % (self.user_id, len(quick_replies), qr_str, message))