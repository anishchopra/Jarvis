from exceptions import UnsupportedOp, NoDeviceConnection
import json
import requests

class Light(object):
	def __init__(self, *args):
		raise UnsupportedOp()

	def status(self) -> bool:
		raise UnsupportedOp()

	def on(self):
		raise UnsupportedOp()

	def off(self):
		raise UnsupportedOp()

	def toggle(self):
		raise UnsupportedOp()

	def set_brightness(bri: int):
		raise UnsupportedOp()

class PhillipsHueLight(Light):
	ip_address = "http://192.168.0.31"

	def __init__(self, uid):
		self.uid = uid

	# Returns True iff the light is on
	def status(self) -> bool:
		try:
			r = requests.get("%s/api/NCsuCpKqtu348SbK5dyyStFqhtVtxyC4lYL5juzO/lights/%s/" % (PhillipsHueLight.ip_address, self.uid))
			if r.status_code == 200:
				device_info = json.loads(r.text)

				return device_info["state"]["on"]
			else:
				raise NoDeviceConnection()
		except:
			raise NoDeviceConnection()

	def set_state(self, light_data):
		light_data = json.dumps(light_data)

		try:
			requests.put(
				"%s/api/NCsuCpKqtu348SbK5dyyStFqhtVtxyC4lYL5juzO/lights/%d/state/" % (PhillipsHueLight.ip_address, self.uid), 
				data=light_data)
		except:
			raise NoDeviceConnection()

	def on(self):
		light_data = {"on": True}
		self.set_state(light_data)

	def off(self):
		light_data = {"on": False}
		self.set_state(light_data)

	def toggle(self):
		if self.status():
			self.off()
		else:
			self.on()

	def set_brightness(self, bri: int):
		brightness = int(bri * 2.54)

		light_data = {"bri": brightness}

		if not self.status():
			light_data["on"] = True

		self.set_state(light_data)

