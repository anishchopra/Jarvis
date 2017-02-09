import signal
import os
import sys
import time
import pygame
from datetime import datetime
import json
import requests
from assistant_interfaces import MessengerInterface
from globals import *
import json

def respond(sender, msg, quick_replies=[]):
	interface = MessengerInterface(sender)
	interface.send_message(msg, quick_replies)

def snooze(signum, stack):
	print('snoozing')
	time.sleep(30)#540) # 9 minute snooze
	set_context()
	print('done snoozing')
	respond(sender, "Wake up!!! What would you like to do?", [("Snooze", time_str), ("Stop", time_str)])

def set_context():
	with open(CONTEXT_FILE, 'r') as f:
		info = json.load(f)

	info[CONTEXT_WAIT_KEY] = ALARM_RING_WAIT
	info['intent'] = ALARM_RING_INTENT

	with open(CONTEXT_FILE, 'w') as f:
		f.write(json.dumps(info))

	with open(RINGING_ALARMS_FILE, 'a') as f:
		f.write(time_str+'\n')

if __name__ == '__main__':
	# Register to recieve snooze events
	signal.signal(signal.SIGUSR1, snooze)

	pid = os.getpid()

	sender = sys.argv[1]
	date_str = sys.argv[2]
	time_str = sys.argv[3]

	# Save PID
	with open('alarm_%s.txt' % time_str, 'w') as f:
		f.write(str(pid))

	datetime_obj = datetime.strptime(date_str + ' ' + time_str + ' -0500', '%Y-%m-%d %H:%M %z')

	t = time.mktime(datetime_obj.timetuple()) + datetime_obj.microsecond / 1E6
	now = time.mktime(datetime.now().timetuple()) + datetime.now().microsecond / 1E6

	print(t)
	print(now)
	print(t-now)

	if t - now > 0:
		start = t - now - 600

		diff = 600

		if start < 0:
			start = 0

			diff = t - now


		time.sleep(start)

		for i in range(1,11):
			print('here')

			for light in ROOMS['room']['lights']:
				light.set_brightness(i*10)

			time.sleep(diff // 10)

	print('PLAYING ALARM')

	respond(sender, "Wake up!!! What would you like to do?", [("Snooze", time_str), ("Stop", time_str)])

	set_context()

	pygame.mixer.init()
	pygame.mixer.music.load('alarm.wav')
	while True:
		pygame.mixer.music.play()
		time.sleep(0.5)


