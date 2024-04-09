const socket = io.connect(location.origin);

let username = '',
    room = '';

document.getElementById('join-form').addEventListener('submit', (e) => {
    e.preventDefault();

    username = document.getElementById('username').value.trim();
    room = document.getElementById('room').value.trim();

    if (username && room) {
        socket.emit('join', { username, room });
        document.getElementById('join-form').style.display = 'none';
    } else {
        alert("请输入完整的用户名和房间号！");
    }
});

function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;

    if (message) {
        socket.emit('chat_message', { username, message, room });
        messageInput.value = '';
    }
}

document.getElementById('send-button').addEventListener('click', sendMessage);

socket.on('connect_error', () => console.error('连接错误！'));
socket.on('connect_timeout', () => console.error('连接超时！'));
socket.on('disconnect', () => console.log("User disconnected"));

socket.on('chat_message', (data) => {
    const messagesDiv = document.getElementById('messages');

    if (!messagesDiv) return; // 检查元素存在性

    const newMessage = document.createElement('p');
    newMessage.textContent = `${data.username}: ${data.message}`;
    messagesDiv.appendChild(newMessage);

    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to bottom after adding new message
});

socket.on('user_entered', (data) => {
    const usersDiv = document.getElementById('users');

    if (!usersDiv) return; // 检查元素存在性

    const newUser = document.createElement('p');
    newUser.textContent = `${data.username} 进入了房间`;
    usersDiv.appendChild(newUser);
});

socket.on('user_left', (data) => {
    const usersDiv = document.getElementById('users');

    if (!usersDiv) return; // 检查元素存在性

    const leftUser = document.createElement('p');
    leftUser.textContent = `${data.username} 离开了房间`;
    usersDiv.appendChild(leftUser);
});