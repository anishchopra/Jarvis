import time
import sys
from datetime import datetime
import json
import requests

from info import *

if __name__ == '__main__':
	date_str = sys.argv[2]
	time_str = sys.argv[3]
	datetime_obj = datetime.strptime(date_str + ' ' + time_str + ' EST', '%Y-%m-%d %H:%M %Z')
	
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



