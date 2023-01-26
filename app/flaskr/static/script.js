const addMessages = (msg) => {

    if (msg.message == undefined){return 0;}

    let msgContainer = document.getElementById('msgContainer');
    let div = document.createElement('div');
    div.className = 'p-2 m-0 w-100 border-bottom';
    div.textContent = msg.message;
    // temporary
    div.style.minHeight = '45px';
    div.style.overflowWrap = 'break-word';
    div.style.textAlign = 'right';

    let name = document.createElement('b');
    name.textContent = 'NAME';
    
    let date = document.createElement('p');
    date.textContent = 'data';
    //temporary
    date.style.fontSize = '12px';
    date.className = 'm-0';

    // add children
    div.appendChild(name)
    div.appendChild(date)
    msgContainer.appendChild(div)
};

const socket = io.connect("http://" + document.domain + ":" + location.port);
socket.on('connect', () => {
    socket.emit('event', {data: 'I\'m connected!'})

    const form = $('form#msgForm').on('submit', (e) => {
        e.preventDefault();
        
        let msgInput = document.getElementById('msgInput');
        let inputValue = msgInput.value;

        // clear msg input
        msgInput.value = '';
        
        // push message
        socket.emit('event', {message: inputValue})
    })
});

socket.on("message response", (msg) => {
    addMessages(msg);
});