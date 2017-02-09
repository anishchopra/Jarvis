from rooms import *
from scenes import day, bed, sex

SCENES = {"day": day, "bed": bed, "sex": sex}

CONTEXT_FILE = 'context.json'

ANISH_MESSENGER_ID = '1402438993121462'

CONTEXT_WAIT_KEY = 'waiting_on'

ALARM_RING_WAIT = 'alarm_ring_action'
ALARM_RING_INTENT = 'alarm_ring_intent'

ROOM_WAIT = 'room'

DATETIME_WAIT = 'datetime_wait'

SCENE_WAIT = 'scene'

RINGING_ALARMS_FILE = 'ringing_alarms.txt'