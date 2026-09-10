const chatHistory = document.getElementById("chat-history");
const messageInput = document.getElementById("message");
const sendButton = document.querySelector(".input-area button");

let isSending = false;

function addMessage(content, role) {
  const div = document.createElement("div");

  div.classList.add(
    "message",
    role === "user" ? "user-message" : "ai-message"
  );

  div.textContent = content;
  chatHistory.appendChild(div);
  scrollToBottom();

  return div;
}

function scrollToBottom() {
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

async function loadHistory() {
  const response = await fetch("/history");

  if (!response.ok) {
    throw new Error("Could not load chat history.");
  }

  const history = await response.json();

  chatHistory.replaceChildren();

  history.forEach((message) => {
    addMessage(message.content, message.role);
  });
}

// Wait for initial history before allowing messages to be sent.
const historyReady = loadHistory().catch((error) => {
  console.error(error);
  addMessage("Could not load previous messages.", "assistant");
});

async function sendMessage() {
  const message = messageInput.value.trim();

  if (!message || isSending) return;

  isSending = true;
  sendButton.disabled = true;

  // Clear the input immediately.
  messageInput.value = "";
  messageInput.focus();

  let loadingBubble;

  try {
    await historyReady;

    // Show the user's message and a placeholder.
    addMessage(message, "user");
    loadingBubble = addMessage(". . .", "assistant");
    loadingBubble.classList.add("loading");

    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error("Chat request failed.");
    }

    const data = await response.json();

    // Replace the placeholder with the answer.
    loadingBubble.textContent = data.reply;
  } catch (error) {
    console.error(error);

    if (loadingBubble) {
      loadingBubble.textContent =
        "Something went wrong. Please try again.";
    }
  } finally {
    loadingBubble?.classList.remove("loading");
    isSending = false;
    sendButton.disabled = false;
    scrollToBottom();
  }
}

messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.isComposing) {
    event.preventDefault();
    sendMessage();
  }
});