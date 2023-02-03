const addMessages = (msg) => {
    // add messages to chat
    let loggedUser = getCookie('username');
    let msgContainer = document.getElementById('msgWrapper');
    let messageDiv = document.createElement('div');
    let messageText = document.createElement('p');
    let dateSmall = document.createElement('small');
    let nameB = document.createElement('b');
    let nameAndDateP = document.createElement('p');
    dateSmall.textContent = msg.date;
    messageText.textContent = msg.message;
    nameAndDateP.className = "msg-name-date";

    if (loggedUser === msg.name) {
        // right side
        messageDiv.className = "message text-right";
        nameB.textContent = ` ${loggedUser}`;
        nameAndDateP.appendChild(dateSmall);
        nameAndDateP.appendChild(nameB);
    }
    else {
        // left side
        messageDiv.className = "message";
        nameB.textContent = `${msg.name} `;
        nameAndDateP.appendChild(nameB);
        nameAndDateP.appendChild(dateSmall);
    };

    messageDiv.appendChild(messageText);
    messageDiv.appendChild(nameAndDateP);
    msgContainer.appendChild(messageDiv);
    msgContainer.scrollTop = msgContainer.scrollHeight;
};

const getName = async () => {
    try {
        const response = await fetch("/get-name");
        const data = await response.json();

        if (!response.ok) {
            console.log('something gone wrong.');
            return;
        } return data.name;
    } catch (error) { console.log(error); };
};

const getCookie = (cname) => {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let match = decodedCookie.match(new RegExp(name + "([^;]+)"));

    if (match) { return match[1]; }
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
        // block saving empty message
        if (inputValue === '') {
            return;
        }

        let date = new Date()
        // clear msg input
        msgInput.value = '';
        // push message
        socket.emit('event', {
            message: inputValue,
            name: userName,
            date: date.toLocaleString([],{
                year: 'numeric', 
                month: 'numeric', 
                day: 'numeric', 
                hour: '2-digit',
                minute: '2-digit'
            })
        })
    })
});

socket.on("message response", (msg) => { addMessages(msg); });

// load old messages
window.onload = async () => {
    try {
        const response = await fetch("/get-messages");
        const data = await response.json();

        if (!response.ok) {
            console.log('something gone wrong.');
            return;
        }

        data.forEach(element => { addMessages(element) });
    } catch (error) { console.log(error); };
}