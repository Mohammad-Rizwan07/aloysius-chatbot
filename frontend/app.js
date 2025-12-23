const API_BASE_URL = "http://localhost:8000/api/v1";

/* Send Message */
async function sendMessage(event) {
    event.preventDefault();

    const input = document.getElementById("questionInput");
    const chatBox = document.getElementById("chatBox");
    const question = input.value.trim();

    if (!question) return;

    addMessage(question, "user");
    input.value = "";

    const typing = document.createElement("div");
    typing.className = "message bot-message";
    typing.innerHTML = `<div class="message-content">Typing...</div>`;
    chatBox.appendChild(typing);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });

        const data = await response.json();
        typing.remove();
        addMessage(data.answer, "bot", data.sources);

    } catch (error) {
        typing.remove();
        addMessage("An error occurred. Please try again.", "bot");
    }
}

/* Render Message */
function addMessage(text, sender, sources = []) {
    const chatBox = document.getElementById("chatBox");
    const msg = document.createElement("div");
    msg.className = `message ${sender}-message`;

    let html = `<div class="message-content">${escapeHtml(text)}`;

    if (sender === "bot" && sources.length) {
        html += `<div class="sources"><strong>Sources:</strong>`;
        sources.forEach(src => {
            html += `<div><a href="${src}" target="_blank">${src}</a></div>`;
        });
        html += `</div>`;
        html += `<button class="copy-btn" onclick="copyText(this)">Copy</button>`;
    }

    html += `</div>`;
    msg.innerHTML = html;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;

    sessionStorage.setItem("chat_history", chatBox.innerHTML);
}

/* Utilities */
function copyText(btn) {
    navigator.clipboard.writeText(btn.parentElement.innerText);
    btn.innerText = "Copied!";
    setTimeout(() => btn.innerText = "Copy", 1500);
}

function escapeHtml(text) {
    return text.replace(/[&<>"']/g, m =>
        ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m])
    );
}

/* Restore Chat */
window.onload = () => {
    const saved = sessionStorage.getItem("chat_history");
    if (saved) {
        document.getElementById("chatBox").innerHTML = saved;
    }
};

/* Animated Placeholder Logic */
document.addEventListener("DOMContentLoaded", () => {
    const strip = document.getElementById("textStrip");
    const firstItem = strip.children[0].cloneNode(true);
    strip.appendChild(firstItem);

    let index = 0;
    const itemHeight = 40;
    const total = strip.children.length;

    setInterval(() => {
        index++;
        strip.style.transition = "transform 0.8s ease";
        strip.style.transform = `translateY(-${index * itemHeight}px)`;

        if (index === total - 1) {
            strip.addEventListener("transitionend", () => {
                strip.style.transition = "none";
                strip.style.transform = "translateY(0)";
                index = 0;
            }, { once: true });
        }
    }, 2600);
});
