var admin = require("firebase-admin");

admin.initializeApp({
	credential: admin.credential.cert("firebase.json"),
	databaseURL: "https://jarvis-d7a74.firebaseio.com"
});

var db = admin.database();
var messageRef = db.ref('messages')

messageRef.on('child_added', function(data) {
	var message = data.val().message 
	var sender = data.val().sender
	var quick_reply = data.val().quick_reply;

	console.log(quick_reply)

	if (quick_reply === undefined) {
		quick_reply = 'none';
	}
	else {
		quick_reply = quick_reply.payload;
	}

	var exec = require('child_process').exec;
	var cmd = 'python3 wit_client.py ' + sender + ' ' + message + ' ' + quick_reply

	console.log(cmd)

	exec(cmd, function(error, stdout, stderr) {
			// command output is in stdout
		console.log(error)
		console.log(stdout)
		console.log(stderr)
	});

	data.ref.remove()
});