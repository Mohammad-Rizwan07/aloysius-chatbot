const API_BASE_URL = "http://localhost:8000/api/v1";

const chatForm = document.getElementById("chatForm");
const input = document.getElementById("questionInput");
const sendBtn = document.getElementById("sendBtn");
const chatBox = document.getElementById("chatBox");

chatForm.addEventListener("submit", sendMessage);

async function sendMessage(e) {
    e.preventDefault();

    const question = input.value.trim();
    if (!question) return;

    addMessage(question, "user");
    input.value = "";
    input.disabled = true;
    sendBtn.disabled = true;

    const processing = document.createElement("div");
    processing.className = "message bot-message";
    processing.innerHTML = `
        <div class="message-content processing-box">
            <span id="processText">Retrieving information</span>
            <span class="processing-dot"></span>
        </div>`;
    chatBox.appendChild(processing);
    scrollToBottom();

    const steps = ["Retrieving information", "Analyzing sources", "Preparing response"];
    let i = 0;
    const stepEl = processing.querySelector("#processText");

    const interval = setInterval(() => {
        i = (i + 1) % steps.length;
        stepEl.textContent = steps[i];
    }, 700);

    try {
        const res = await fetch(`${API_BASE_URL}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });

        const data = await res.json();
        clearInterval(interval);
        processing.remove();

        addMessage(
            data.answer || "I do not have this information from the official website.",
            "bot",
            data.sources || []
        );
    } catch {
        clearInterval(interval);
        processing.remove();
        addMessage("An error occurred. Please try again.", "bot");
    } finally {
        input.disabled = false;
        sendBtn.disabled = false;
        input.focus();
    }
}

/* ✅ Markdown → HTML renderer (ChatGPT-like) */
function renderMarkdownToHtml(text) {
    let safe = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

    // Bold **text**
    safe = safe.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

    const lines = safe.split("\n");
    let html = "";
    let inList = false;

    lines.forEach(line => {
        if (line.trim().startsWith("* ")) {
            if (!inList) {
                html += "<ul>";
                inList = true;
            }
            html += `<li>${line.replace("* ", "").trim()}</li>`;
        } else {
            if (inList) {
                html += "</ul>";
                inList = false;
            }
            if (line.trim()) {
                html += `<p>${line}</p>`;
            }
        }
    });

    if (inList) html += "</ul>";
    return html;
}

/* Render message */
function addMessage(text, sender, sources = []) {
    const msg = document.createElement("div");
    msg.className = `message ${sender}-message`;

    let html = `<div class="message-content">`;

    if (sender === "bot") {
        html += renderMarkdownToHtml(text);
    } else {
        html += escapeHtml(text);
    }

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
    scrollToBottom();

    sessionStorage.setItem("chat_history", chatBox.innerHTML);
}

function scrollToBottom() {
    requestAnimationFrame(() => {
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

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

window.onload = () => {
    const saved = sessionStorage.getItem("chat_history");
    if (saved) chatBox.innerHTML = saved;
};
