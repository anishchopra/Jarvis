import os

SUPPORTED_SCENES = set(['bed', 'day', 'sex'])
LIGHTS = {"my room": [1,2]}
FANS = {"my room": ["192.168.0.13"]}

SCENES = {
	"bed": {
		"my room": {
			"lights": {
				"on": False
			},
			"fan": {
				"on": True
			}
		}
	},
	"day": {
		"my room": {
			"lights": {
				"on": True,
				"bri": 254
			},
			"fan": {
				"on": False
			}
		}
	},
	"sex": {
		"my room": {
			"lights": {
				"on": True,
				"bri": 50
			},
			"fan": {
				"on": True
			}
		}
	}
}

ALARM_FILE = 'alarms.txt'

def respond(sender, message, quick_replies=[]):
	qr_str = ""
	for text,payload in quick_replies:
		qr_str += text + ' ' + payload + ' '
	print('node respond.js %s %s %s %s &' % (sender, len(quick_replies), qr_str, message))
	os.system('node respond.js %s %s %s %s &' % (sender, len(quick_replies), qr_str, message))