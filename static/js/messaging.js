

var messagingListeners = {};

var messagingWS = new WebSocket(`ws://${window.location.hostname}:6789`);
var messagingWS_tryReconnect = true;

function messagingWS_onopen() {
    messagingWS.send(JSON.stringify({
        'user_id' : '__TODO__',
        'session_id' : '__TODO__'
    }));
}

function messagingWS_onmessage(msg) {
    msg = JSON.parse(msg.data);

    topic = msg.topic;
    message = msg.message;

    if (topic == 'auth_fail') {
        messagingWS_tryReconnect = false;
    }
    
    if (messagingListeners[topic]) {
        for (var i = 0; i < messagingListeners[topic].length; i++) {
            messagingListeners[topic][i](message);
        }
    }
}

function messagingWS_onclose() {
    if (messagingWS_tryReconnect) {
        setTimeout(() => {
            console.log('messagingWS trying to reconnect');

            messagingWS = new WebSocket(`ws://${window.location.hostname}:6789`);
            messagingWS.onopen = messagingWS_onopen;
            messagingWS.onmessage = messagingWS_onmessage;
            messagingWS.onclose = messagingWS_onclose;
        }, 5000);
    }
}

messagingWS.onopen = messagingWS_onopen;
messagingWS.onmessage = messagingWS_onmessage;
messagingWS.onclose = messagingWS_onclose;

function registerListener(topic, func) {
    if (messagingListeners[topic]) {
        messagingListeners[topic].push(func);
    }
    else {
        messagingListeners[topic] = [func];
    }
}