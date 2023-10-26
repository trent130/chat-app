/*document.addEventListener("DOMContentLoaded", function() {
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const chatMessages = document.getElementById("chat-messages");

    // Create a WebSocket connection
    const socket = new WebSocket("ws://localhost:8080");

    // Event listener for sending a message
    sendButton.addEventListener("click", function() {
        const message = messageInput.value;
        if (message) {
            // Send the message to the server
            socket.send(message);
            messageInput.value = "";
        }
    });

    // Event listener for receiving a message
    socket.addEventListener("message", function(event) {
        const message = event.data;
        // Display the message in the chat interface
        const messageElement = document.createElement("div");
        messageElement.innerText = message;
        chatMessages.appendChild(messageElement);
    });
});
*/
document.addEventListener("DOMContentLoaded", function() {
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const chatMessages = document.getElementById("chat-messages");

    // Event listener for sending a message
    sendButton.addEventListener("click", function() {
        const message = messageInput.value;
        if (message) {
            // Send the message to the server (you will need to implement this part)
            // Display the message in the chat interface
            const messageElement = document.createElement("div");
            messageElement.innerText = message;
            chatMessages.appendChild(messageElement);
            messageInput.value = "";
        }
    });

    // You'll need to add code for receiving and displaying messages from the server.
});
