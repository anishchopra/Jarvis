import signal
import os
import sys
import time
import pygame
from datetime import datetime
import json
import requests
from info import *

def snooze(signum, stack):
	print('snoozing')
	time.sleep(540) # 9 minute snooze
	print('done snoozing')
	respond(sender, "Wake up!!! What would you like to do?", [("Snooze", time_str), ("Stop", time_str)])

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

			light_data = {"on":True, "bri":int(25.4*i)}
			light_data = json.dumps(light_data)

			for light_id in LIGHTS['my room']:
				r = requests.put(
					"http://192.168.0.31/api/NCsuCpKqtu348SbK5dyyStFqhtVtxyC4lYL5juzO/lights/%d/state/" % light_id, 
					data=light_data)

				print(r.content)

			time.sleep(diff // 10)

	print('PLAYING ALARM')

	respond(sender, "Wake up!!! What would you like to do?", [("Snooze", time_str), ("Stop", time_str)])

	pygame.mixer.init()
	pygame.mixer.music.load('alarm.wav')
	while True:
		pygame.mixer.music.play()
		time.sleep(0.5)


