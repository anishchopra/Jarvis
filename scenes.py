from rooms import ROOMS 

def day():
	room = ROOMS["room"]

	for light in room["lights"]:
		light.set_brightness(100)

	for fan in room["fans"]:
		fan.off()

def bed():
	room = ROOMS["room"]

	for light in room["lights"]:
		light.off()

	for fan in room["fans"]:
		fan.on()

def sex():
	room = ROOMS["room"]

	for light in room["lights"]:
		light.set_brightness(20)

	for fan in room["fans"]:
		fan.on()