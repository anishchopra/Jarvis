var admin = require("firebase-admin");

admin.initializeApp({
	credential: admin.credential.cert("firebase.json"),
	databaseURL: "https://jarvis-d7a74.firebaseio.com"
});

var db = admin.database();
var messageRef = db.ref('messages')

messageRef.on('child_added', function(data) {
	message = data.val().message 
	sender = data.val().sender

	var exec = require('child_process').exec;
	var cmd = 'python wit_client.py ' + sender + ' ' + message

	console.log(cmd)

	exec(cmd, function(error, stdout, stderr) {
			// command output is in stdout
		console.log(error)
		console.log(stdout)
		console.log(stderr)
	});

	data.ref.remove()
});