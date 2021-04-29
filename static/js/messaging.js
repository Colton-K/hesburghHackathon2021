
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function setCookie(cname, cvalue) {
    document.cookie = cname + "=" + cvalue + ";";
}

function messagingWS_onopen() {
    messagingWS.send(JSON.stringify({
        'user_id' : getCookie('user_id'),
        'session_id' : getCookie('session_id')
    }));
}

function messagingWS_onmessage(msg) {
    msg = JSON.parse(msg.data);

    topic = msg.topic;
    message = msg.message;

    if (topic == 'auth_fail') {
        messagingWS.send("ack");
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

function registerListener(topic, func) {
    if (messagingListeners[topic]) {
        messagingListeners[topic].push(func);
    }
    else {
        messagingListeners[topic] = [func];
    }
}

var messagingListeners = {};
var messagingWS = new WebSocket(`ws://${window.location.hostname}:6789`);
var messagingWS_tryReconnect = true;

messagingWS.onopen = messagingWS_onopen;
messagingWS.onmessage = messagingWS_onmessage;
messagingWS.onclose = messagingWS_onclose;