SUPPORTED_SCENES = set(['bed', 'day', 'sex'])
LIGHTS = {"my room": [1,2]}

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
				"off": True
			}
		}
	}
}

ALARM_FILE = 'alarms.txt'