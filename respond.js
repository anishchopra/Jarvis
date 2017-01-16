var admin = require("firebase-admin");

admin.initializeApp({
	credential: admin.credential.cert("firebase.json"),
	databaseURL: "https://jarvis-d7a74.firebaseio.com"
});

var db = admin.database();
var responseRef = db.ref('responses')

sender = process.argv[2]
quick_replies_num = parseInt(process.argv[3])

response = "";
quick_replies = [];

var i=4;
for (var j=0; j < quick_replies_num; j++) {
	reply = {content_type: 'text', title: process.argv[i], payload: process.argv[i+1]};
	quick_replies.push(reply);
	i+=2
}

for (; i<process.argv.length; i++) {
	response += process.argv[i];

	if (i < process.argv.length - 1) {
		response += ' ';
	}
}

var newResponseRef = responseRef.push();

if (quick_replies.length > 0) {
	newResponseRef.set({"message": response, "sender": sender, "quick_replies": quick_replies}).then(function(res) {
		process.exit();
	});
}
else {
	newResponseRef.set({"message": response, "sender": sender}).then(function(res) {
		process.exit();
	});
}


