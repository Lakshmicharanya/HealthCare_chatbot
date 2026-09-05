const messageInput = document.getElementById("message");
const chatBox = document.getElementById("chat-box");


function addMessage(type, text) {

    const message = document.createElement("div");

    message.classList.add("message");

    if (type === "user") {

        message.classList.add("user-message");

        const label = document.createElement("strong");
        label.textContent = "You: ";

        const textElement = document.createElement("span");
        textElement.textContent = text;

        message.appendChild(label);
        message.appendChild(textElement);

    } else {

        message.classList.add("bot-message");

        const label = document.createElement("strong");
        label.textContent = "Bot: ";

        const textElement = document.createElement("span");
        textElement.textContent = text;

        message.appendChild(label);
        message.appendChild(textElement);
    }

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;
}


async function sendMessage() {

    const message = messageInput.value.trim();

    if (message === "") {
        return;
    }

    addMessage("user", message);

    messageInput.value = "";

    try {

        const response = await fetch("/send_message", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });


        const data = await response.json();


        if (data.response) {

            addMessage("bot", data.response);

        } else {

            addMessage(
                "bot",
                data.error || "Something went wrong."
            );
        }

    } catch (error) {

        addMessage(
            "bot",
            "Unable to connect to the server."
        );
    }
}


messageInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {
            sendMessage();
        }

    }
);