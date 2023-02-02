const addMessages = (msg) => {
    if (msg.message === undefined || msg.message === ''){return;};

    let loggedUser = getCookie('username');
    let date = new Date();

    if (loggedUser === msg.name) {
        // right side
        console.log(msg.message, loggedUser, date.toLocaleString(), 'right side');
    }
    else {
        // left side
        console.log(msg.message, msg.name, date.toLocaleString(), 'left side');
    };
};

const getName = async () => {
    try {
        const response = await fetch("/get-name");
        const data = await response.json();

        if (!response.ok) {
            console.log('something gone wrong.');
            return;
        } return data.name;
    } catch (error) {console.log(error);};
};

const getCookie = (cname) => {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let match = decodedCookie.match(new RegExp(name + "([^;]+)"));

    if (match) {return match[1];}
    return;
}

const socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on('connect', async () => {
    // save username to cookies
    let userName = await getName()
    document.cookie = `username=${userName};`

    $('form#msgForm').on('submit', (e) => {
        e.preventDefault();
        
        let msgInput = document.getElementById('msgInput');
        let inputValue = msgInput.value;
        // clear msg input
        msgInput.value = '';
        // push message
        socket.emit('event', {message: inputValue, name: userName})
    })
});

socket.on("message response", (msg) => {
    addMessages(msg);
});