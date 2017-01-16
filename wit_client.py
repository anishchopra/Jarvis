from wit import Wit 
import requests
import json
from flask import Flask, request
import os
import sys
from datetime import datetime
import subprocess
from functools import cmp_to_key
import signal
import glob

from info import *

with open('access_token', 'r') as f:
	access_token = f.read().strip()

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def send(request, response):
	print('in the random send method')
	print(response['text'])

def light(request):
	print('in light')
	context = request['context']
	entities = request['entities']

	on = first_entity_value(entities, 'on_off')
	brightness = first_entity_value(entities, 'number')

	print('on and brightness', on, brightness)

	if not on and not brightness:
		respond(request['session_id'], "I am sorry, I do not understand - %s" % request['text'])

		return context

	# My room is the default location
	place = first_entity_value(entities, 'place') or 'my room'

	response_place = place.replace('my', 'your')

	if brightness:
		on = 'on' # just in case
		respond(request['session_id'], "Okay, turning on the light in %s to %d%%" % (response_place, brightness))
		brightness = int(brightness * 2.54)
	else:
		respond(request['session_id'], "Okay, turning %s the light in %s" % (on, response_place))


	light_data = {"on": on=='on'}
	if brightness:
		light_data['bri'] = brightness

	light_data = json.dumps(light_data)

	for light_id in LIGHTS[place]:
		r = requests.put(
			"http://192.168.0.31/api/NCsuCpKqtu348SbK5dyyStFqhtVtxyC4lYL5juzO/lights/%d/state/" % light_id, 
			data=light_data)

	return context

def fan(request):
	context = request['context']
	entities = request['entities']

	on = first_entity_value(entities, 'on_off')
	print('fan should be %s' % on)

	if not on:
		respond(request['session_id'], "I am sorry, I do not understand - %s" % request['text'])

		return context

	# My room is the default location
	place = first_entity_value(entities, 'place') or 'my room'

	for fan in FANS[place]:
		os.system('python2 wemo.py %s %s &' % (fan, on))

	response_place = place.replace('my', 'your')

	respond(request['session_id'], "Okay, turning %s the fan in %s" % (on, response_place))

	return context

def alarm(request):
	context = request['context']
	entities = request['entities']

	on = first_entity_value(entities, 'on_off')
	datetime_str = first_entity_value(entities, 'datetime')
	list_val = first_entity_value(entities, 'list')

	if not on or not datetime_str:
		if list_val:
			alarms = glob.glob('alarm_*.txt')

			if len(alarms) == 0:
				respond(request['session_id'], "You do not have any alarms set")
			elif len(alarms) == 1:
				a = alarms[0].split('alarm_')[1].split('.txt')[0]
				respond(request['session_id'], "You have an alarm set for %s" % a)
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
				
				respond(request['sesssion_id'], "You have alarms set for %s" % ', '.join(alarm_strs))
		else:
			respond(request['session_id'], "I am sorry, I do not understand - %s" % request['text'])

		return context

	date_str = datetime_str.split('T')[0]
	time_str = datetime_str.split('T')[1].split('.')[0][:-3]

	print(date_str)
	print(time_str)

	datetime_total = date_str + ' ' + time_str

	filename = 'alarm_%s.txt' % time_str

	if on=='on':
		if os.path.isfile(filename):
			respond(request['session_id'], "You already have an alarm set for %s" % time_str)
		else:
			os.system('python3 new_alarm.py %s %s %s &' % (request['session_id'], date_str, time_str))
			respond(request['session_id'], "Okay, I have set an alarm for %s" % time_str)

	elif on=='off':
		if os.path.isfile(filename):
			with open(filename, 'r') as f:
				pid = f.read()
				os.system('kill %s' % pid)
			os.remove(filename)
			respond(request['session_id'], "Okay, I have turned off your %s alarm" % time_str)
		else:
			respond(request['session_id'], "You do not have an alarm set for %s" % time_str)

	return context

def scene(request):
	context = request['context']
	entities = request['entities']

	scene = first_entity_value(entities, 'scene')

	if not scene:
		respond(request['session_id'], "I am sorry, I do not understand - %s" % request['text'])

		return context

	if scene not in SCENES:
		respond(request['session_id'], "You do not have a scene named '%s'" % scene)

		return context

	respond(request['session_id'], "Okay, turning on your %s scene" % scene)

	scene_info = SCENES[scene]

	for place in scene_info:
		place_info = scene_info[place]

		if 'lights' in place_info:
			light_data = json.dumps(place_info['lights'])
			for light_id in LIGHTS[place]:
				r = requests.put(
					"http://192.168.0.31/api/NCsuCpKqtu348SbK5dyyStFqhtVtxyC4lYL5juzO/lights/%d/state/" % light_id, 
					data=light_data)

		if 'fan' in place_info:
			on = place_info['fan']['on']
			for fan in FANS[place]:
				os.system('python2 wemo.py %s %s &' % (fan, 'on' if on else 'off'))

		# TODO: handle 'alarm'

	return context

def handle_quick_reply(sender, message, payload):
	if message == 'Stop':
		filename = 'alarm_%s.txt' % payload
		if os.path.isfile(filename):
			with open(filename, 'r') as f:
				pid = f.read()
				os.system('kill %s' % pid)
			os.remove(filename)

			for fan in FANS['my room']:
				os.system('python2 wemo.py %s %s &' % (fan, 'off'))

				respond(sender, "Okay, I have turned off your %s alarm" % payload)
	elif message == 'Snooze':
		filename = 'alarm_%s.txt' % payload
		if os.path.isfile(filename):
			with open(filename, 'r') as f:
				pid = f.read()
				os.kill(int(pid), signal.SIGUSR1)

				respond(sender, "Okay, I have snoozed your %s alarm" % payload)

actions = {
	'send': send,
	'light': light,
	'fan': fan,
	'alarm': alarm,
	'scene': scene
}

client = Wit(access_token=access_token, actions=actions)

if __name__ == '__main__':
	sender = sys.argv[1]

	message = ' '.join(sys.argv[2:-1])
	quick_reply_payload = sys.argv[-1]

	if quick_reply_payload == 'none':
		client.run_actions(sender, message)
	else:
		handle_quick_reply(sender, message, quick_reply_payload)
