// const socket = io('https://d6d517de9c0c.ngrok-free.app');
// const socket = io('https://pisc-flask.ddns.net:5000');
const socket = io('http://192.168.1.44:5000');

const form = document.getElementById('message-form');
const user = "Test";
const messagesInput = document.getElementById('message-input');

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = messagesInput.value;
    
    if (user && message) {
        console.log(user, message);
        socket.emit('message', {user: user, message: message});
        messagesInput.value = '';
    }
});

function displayMessages(user, message) {
    const messageContainer = document.getElementById('message-container');
    messageContainer.innerHTML = '';
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'bg-gray-200', 'dark:bg-gray-700', 'p-2', 'rounded-md');
    const messageElement = document.createElement('p');
    messageElement.classList.add('text-gray-500', 'dark:text-white', 'flex-col');   
    const userElement = document.createElement('p');
    userElement.classList.add('text-gray-500', 'dark:text-white'); 
    userElement.innerText = user;
    messageElement.appendChild(userElement);
    const messageText = document.createElement('p');
    messageText.classList.add('text-gray-800', 'dark:text-white', 'flex-col');
    messageText.innerHTML = message;
    messageElement.appendChild(messageText);
    messageDiv.appendChild(messageElement);
    messageContainer.appendChild(messageDiv);
}

socket.on('new_message', (data) => {
    displayMessages(data.user, data.message);
});

socket.on('inital_messages', (messages) => {
    console.log('inital_messages', messages);
    messages.forEach(msg => {
        displayMessages(msg.user, msg.message);
    });
});