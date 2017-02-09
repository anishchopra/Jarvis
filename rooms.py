from light import PhillipsHueLight
from switch import BelkinWemoSwitch

ROOMS = {
	"room": {
		"lights": [
			PhillipsHueLight(1),
			PhillipsHueLight(2)
		],
		"fans": [
			BelkinWemoSwitch("192.168.0.13")
		]
	}
}