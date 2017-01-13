var admin = require("firebase-admin");

admin.initializeApp({
	credential: admin.credential.cert("firebase.json"),
	databaseURL: "https://jarvis-d7a74.firebaseio.com"
});

var db = admin.database();
var responseRef = db.ref('responses')

sender = process.argv[2]

response = "";
process.argv.forEach(function (val, index, array) {
	if (index >= 3) {
		response += val

		if (index < array.length - 1) {
			response += ' ';
		}
	}
	
});

var newResponseRef = responseRef.push();
newResponseRef.set({"message": response, "sender": sender}).then(function(res) {
	process.exit();
});

