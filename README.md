# Jarvis
Jarvis: My own personal home assistant

I created Jarvis to help me with some simple home automation tasks. Jarvis currently communicates over Facebook Messenger. It uses Natural Language Processing which I trained on wit.ai. I have included the access token in this repo so that anyone can use my trained model. I can tell Jarvis to do things in multiple different ways. For example, I can set an alarm by saying something like "Set an alarm for 9am", or I could also say "Wake me up at 9:00". My trained model on wit.ai should still be able to successfully extract the intent and the entities of the message and perform the desired command.

Here is a list of things Jarvis can currently do:

- Control my lights (including dimming my lights by saying something like "set my lights to 50%")
- Control my fan
- Turn on different "scenes" (for example, asking Jarvis to "turn on my night scene" will turn off my lights and turn on my fan)
- Wake me up in the morning by gradually turning on my lights over the span of 10 minutes prior to my alarm, and then sound an alarm at the desired time. Then, it will send me a message providing me with 2 buttons, one to snooze and one to stop the alarm. After I stop the alarm, Jarvis will also turn off my fan.
- Responds to every command with a confirmation of what action it just performed.

Future plans:

- I will soon also create an iOS app that is integrated with Siri so that I can simply communicate with Jarvis by speaking. Furthermore, I will also create iOS lock screen widgets to perform common tasks.
- After I stop my alarm, Jarvis will tell me the weather for the day and let me know if I need to bring an umbrella with me.
- Make it seem more "human" by randomizing certain greetings and phrases

Note: As you can see in the source code, the wit client currently listens on a Firebase database for incoming messages. The reason that I do this is because Facebook Messenger requires an https server to handle the messages, however my smart devices require the server to be run locallly on my home network, thus I created a sercure server on Heroku to handle the incoming Facebook Messenger messages, which it then pushes to Firebase. For obvious reasons, I have ommitted the Firebase credentials from this repo.
