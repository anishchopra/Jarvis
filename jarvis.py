import sys
import os
from wit import Wit 
import json
from assistant_interfaces import AssistantInterface, MessengerInterface 
from globals import *
from exceptions import *
import glob
from functools import cmp_to_key
import signal

with open('access_token', 'r') as f:
	wit_access_token = f.read().strip()

client = Wit(access_token=wit_access_token)

class Jarvis(object):	
	client = Wit(access_token=wit_access_token)

	def __init__(self, response_interface: AssistantInterface):
		self.interface = response_interface
		self.context = {}

	def load_context(self):
		if os.path.isfile(CONTEXT_FILE):
			with open(CONTEXT_FILE, 'r') as f:
				self.context = json.load(f)
		else:
			self.context = {}

	def save_context(self):
		with open(CONTEXT_FILE, 'w') as f:
			f.write(json.dumps(self.context))

	def copy_entities_to_context(self, entities):
		for key in entities:
			self.context[key] = entities[key][0]['value']
		

	def control_device(self, info: dict):
		device = None
		mode = None
		room = None
		num = None

		entities = info['entities']

		if 'room' in entities:
			room = entities['room'][0]['value']
			self.context['room'] = entities['room'][0]['value']
		elif 'room' in self.context:
			room = self.context['room']
		else:
			# No need to prompt user for location. Just use default value
			room = 'room'

		if 'device' in entities:
			device = entities['device'][0]['value']
		else:
			self.context[CONTEXT_WAIT_KEY] = ROOM_WAIT
			self.interface.send_message("Which device?")
			# Since we need more info, we need to save all the context we can
			self.copy_entities_to_context(entities)
			return

		if 'on_off' in entities:
			mode = entities['on_off'][0]['value']
		else:
			self.interface.send_message("Sorry, I do not understand this request.")
			self.context = {}
			return

		if 'number' in entities:
			num = entities['number'][0]['value']
			try:
				num = int(num)
			except:
				raise InternalJarvisError("Invalid number value")

		assert(room is not None)
		assert(device is not None)
		assert(mode is not None or num is not None)

		room = room.lower()

		if room not in ROOMS:
			self.interface.send_message("%s is not a valid room" % room)
		else:
			location = ROOMS[room]

			# The reason I use 'not None' instead of just 'not num' is because num can be 0, but that is still valid
			if num is not None:
				if num >= 0 and num <= 100:
					if device == 'light':
						for light in location['lights']:
							light.set_brightness(num)
						self.interface.send_message("Okay, I have set the brightness of your lights to %d%%" % num)
					else:
						self.interface.send_message("I am sorry, I do not understand this request")
				else:
					self.interface.send_message("Sorry, that is not a valid value")

			elif mode == 'on':
				if device == 'light':
					for light in location['lights']:
						light.on()

					self.interface.send_message("Okay, I have turned on you lights")
				elif device == 'fan':
					for fan in location['fans']:
						fan.on()

					self.interface.send_message("Okay, I have turned on your fan")

			elif mode == 'off':
				if device == 'light':
					for light in location['lights']:
						light.off()

					self.interface.send_message("Okay, I have turned off you lights")
				elif device == 'fan':
					for fan in location['fans']:
						fan.off()

					self.interface.send_message("Okay, I have turned off your fan")

			else:
				raise InternalJarvisError("This doesn't make sense")

		self.context = {}
		self.context['room'] = room


	def create_alarm(self, info: dict):
		datetime_str = None

		entities = info['entities']


		if 'datetime' in entities:
			datetime_str = entities['datetime'][0]['value']
		elif 'datetime' in self.context:
			datetime_str = self.context['datetime']
		else:
			self.context = {}
			self.context[CONTEXT_WAIT_KEY] = DATETIME_WAIT
			self.copy_entities_to_context(entities)

			self.interface.send_message("Okay, when should I set your alarm for?")
			return

		assert(datetime_str)

		date_str = datetime_str.split('T')[0]
		time_str = datetime_str.split('T')[1].split('.')[0][:-3]

		datetime_total = date_str + ' ' + time_str

		filename = 'alarm_%s.txt' % time_str

		if os.path.isfile(filename):
			self.interface.send_message("You already have an alarm set for %s" % time_str)
		else:
			# Alarms will always be sent to Facebook Messenger
			os.system('python3 new_alarm.py %s %s %s &' % (ANISH_MESSENGER_ID, date_str, time_str))
			self.interface.send_message("Okay, I have set an alarm for %s" % time_str)

		# The only context we might need from here on out is the time
		self.context = {}
		self.context['datetime'] = datetime_str

	def delete_alarm(self, info: dict):
		datetime_str = None

		entities = info['entities']


		if 'datetime' in entities:
			datetime_str = entities['datetime'][0]['value']
		elif 'datetime' in self.context:
			datetime_str = self.context['datetime']
		else:
			self.context = {}
			self.context[CONTEXT_WAIT_KEY] = DATETIME_WAIT
			self.copy_entities_to_context(entities)

			self.interface.send_message("Which alarm do you want me to turn off?")
			return

		assert(datetime_str)

		date_str = datetime_str.split('T')[0]
		time_str = datetime_str.split('T')[1].split('.')[0][:-3]

		datetime_total = date_str + ' ' + time_str

		filename = 'alarm_%s.txt' % time_str

		if os.path.isfile(filename):
			with open(filename, 'r') as f:
				pid = f.read()
				os.system('kill %s' % pid)
			os.remove(filename)
			self.interface.send_message("Okay, I have turned off your %s alarm" % time_str)
		else:
			self.interface.send_message("You do not have an alarm set for %s" % time_str)

		# The only context we might need from here on out is the time
		self.context = {}
		self.context['datetime'] = datetime_str

	def list_alarm(self, info: dict):
		alarms = glob.glob('alarm_*.txt')

		if len(alarms) == 0:
			self.interface.send_message("You do not have any alarms set")
		elif len(alarms) == 1:
			a = alarms[0].split('alarm_')[1].split('.txt')[0]
			self.interface.send_message("You have an alarm set for %s" % a)
		else:
			alarm_strs = []
			for a in alarms:
				alarm_strs.append(a.split('alarm_')[1].split('.txt')[0])

			def cmp(a,b):
				hour_a = int(a.split(':')[0])
				minute_a = int(a.split(':')[1])
				hour_b = int(b.split(':')[0])
				minute_b = int(b.split(':')[1])

				if hour_a < hour_b:
					return -1
				elif hour_a > hour_b:
					return 1
				else:
					if minute_a < minute_b:
						return -1
					elif minute_a > minute_b:
						return 1
					else:
						return 0

			alarm_strs.sort(key=cmp_to_key(cmp))
			
			self.interface.send_message("You have alarms set for %s" % ', '.join(alarm_strs))

		self.context = {}

	def scene(self, info: dict):
		scene = None

		entities = info['entities']

		if 'scene' in entities:
			scene = entities['scene'][0]['value']
		elif 'scene' in self.context:
			scene = self.context['scene']
		else:
			self.context[CONTEXT_WAIT_KEY] = SCENE_WAIT
			self.copy_entities_to_context(entities)

			self.interface.send_message("Which scene?")
			return

		assert(scene)

		if scene in SCENES:
			SCENES[scene]()

			self.interface.send_message("Okay, I have turned on your %s scene" % scene)
		else:
			self.interface.send_message("Sorry, %s is not a valid scene" % scene)

		self.context = {}

	def alarm_ringing(self, info:dict):
		alarm_action = None

		entities = info['entities']

		if 'alarm_action' in entities:
			alarm_action = entities['alarm_action'][0]['value']
		elif 'alarm_action' in self.context:
			alarm_action = self.context['alarm_action']
		else:
			self.interface.send_message("I am sorry, I do not understand what you mean by that.")
			self.context = {}
			return

		assert(alarm_action)

		ringing_alarms = []

		with open(RINGING_ALARMS_FILE, 'r') as f:
			for line in f:
				ringing_alarms.append(line.strip())

		def clear():
			with open(RINGING_ALARMS_FILE, 'w') as f:
				pass

		if alarm_action.lower() == 'snooze':
			for alarm in ringing_alarms:
				filename = 'alarm_%s.txt' % alarm
				if os.path.isfile(filename):
					with open(filename, 'r') as f:
						pid = f.read()
						os.kill(int(pid), signal.SIGUSR1)
					
			clear()

			self.interface.send_message("Okay, I have snoozed your alarm.")
		elif alarm_action.lower() == 'stop':
			for alarm in ringing_alarms:
				filename = 'alarm_%s.txt' % alarm
				if os.path.isfile(filename):
					with open(filename, 'r') as f:
						pid = f.read()
						os.system('kill %s' % pid)

					os.remove(filename)
			clear()

			self.interface.send_message("Okay, I have turned off your alarm.")
		else:
			self.interface.send_message("Sorry, I do not understand what you mean by that.")

		self.context = {}

	def handle_intent(self, info):
		assert(self.context['intent'])

		if self.context['intent'] == 'control_device':
			self.control_device(info)
		elif self.context['intent'] == 'create_alarm':
			self.create_alarm(info)
		elif self.context['intent'] == 'delete_alarm':
			self.delete_alarm(info)
		elif self.context['intent'] == 'list_alarm':
			self.list_alarm(info)
		elif self.context['intent'] == 'scene':
			self.scene(info)
		elif self.context['intent'] == ALARM_RING_INTENT:
			self.alarm_ringing(info)
		else:
			raise InternalJarvisError("Invalid intent - %s" % self.context['intent'])

	def handle_message(self, message):
		self.load_context()

		info = client.message(message)
		print(info)

		if CONTEXT_WAIT_KEY not in self.context:
			if 'entities' in info and 'intent' in info['entities']:
				self.context['intent'] = info['entities']['intent'][0]['value']
			else:
				self.interface.send_message("Sorry, I am not sure what you mean by that.")
				return
		
		self.handle_intent(info)

		self.save_context()

if __name__ == '__main__':
	# Must be called with a file containing information about the request
	if len(sys.argv) == 2:
		request_info_filename = sys.argv[1]

		if os.path.isfile(request_info_filename):
			with open(request_info_filename) as f:
				info = json.load(f)

			if 'message' not in info:
				raise Exception("Invalid request")

			# Messenger is currently the only supported interface
			if 'interface' in info and info['interface'] == 'messenger' and 'messenger_id' in info:
				interface = MessengerInterface(info['messenger_id'])
			else:
				raise Exception("Invalid interface")

			jarvis = Jarvis(interface)
			jarvis.handle_message(info['message'])

		else:
			raise Exception("Invalid filename '%s'" % request_info_filename)

	elif len(sys.argv) > 2:
		raise Exception("Invalid input paramters.")

	else:
		raise Exception("No request file specified.")
