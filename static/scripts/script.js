let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];

function displayChat() {
    const chatDiv = document.getElementById('chat');
    chatDiv.innerHTML = '';
    chatHistory.forEach(entry => {
        const messageDiv = document.createElement('div');
        messageDiv.className = entry.speaker;
        messageDiv.textContent = entry.message;
        chatDiv.appendChild(messageDiv);
    });
    // Scroll to the bottom
    chatDiv.scrollTop = chatDiv.scrollHeight;
}

displayChat();
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
document.getElementById('chat-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const messageInput = document.getElementById('message-input');
    const userMessage = messageInput.value.trim();
    if (userMessage === '') return;
    messageInput.value = '';

    // Display user's message immediately
    chatHistory.push({speaker: 'user', message: userMessage});
    displayChat();

    // Prepare chat history for the server
    const chatHistoryForServer = chatHistory.map(entry => {
        return `${entry.speaker === 'user' ? 'User' : 'Assistant'}: ${entry.message}`;
    }).join('\n');

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: 'message=' + encodeURIComponent(userMessage) + '&chat_history=' + encodeURIComponent(chatHistoryForServer)
    })
    .then(response => {
        if (!response.ok) {
            // Handle HTTP errors
            return response.json().then(data => {
                throw new Error(data.error || 'An error occurred');
            });
        }
        return response.json();
    })
    .then(data => {
        chatHistory.push({speaker: 'bot', message: data.assistant});
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
        displayChat();
    })
    .catch(error => {
        alert(error.message);
        chatHistory.push({speaker: 'bot', message: error.message});
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
        displayChat();
    });
});

document.getElementById('reset-button').addEventListener('click', function() {
    fetch('/reset', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'An error occurred');
            });
        }
        return response.json();
    })
    .then(data => {
        chatHistory = [];
        localStorage.removeItem('chatHistory');
        displayChat();
    })
    .catch(error => {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('Error', {
                body: error.message,
            });
        } else {
            alert(error.message);
        }
    });
});