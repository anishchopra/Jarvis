var admin = require("firebase-admin");
var fs = require("fs")

admin.initializeApp({
	credential: admin.credential.cert("firebase.json"),
	databaseURL: "https://jarvis-d7a74.firebaseio.com"
});

var db = admin.database();
var messageRef = db.ref('messages')

messageRef.on('child_added', function(data) {
	var message = data.val().message 
	var sender = data.val().sender

	var filename = sender + ".json"

	var requestObj = {"interface": "messenger",
					"messenger_id": sender,
					"message": message}

	fs.writeFile(filename, JSON.stringify(requestObj), function (err) {
  		if (err) throw err;
	});

	console.log(sender);

	var exec = require('child_process').exec;
	var cmd = 'python3 jarvis.py ' + filename

	console.log(cmd)

	exec(cmd, function(error, stdout, stderr) {
			// command output is in stdout
		console.log(error)
		console.log(stdout)
		console.log(stderr)
	});

	data.ref.remove()
});