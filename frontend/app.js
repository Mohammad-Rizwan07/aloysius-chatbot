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

    /* AI Processing animation */
    const processing = document.createElement("div");
    processing.className = "message bot-message";
    processing.innerHTML = `
        <div class="message-content processing-box">
            <span id="processText">Retrieving information</span>
            <span class="processing-dot"></span>
        </div>`;
    chatBox.appendChild(processing);
    scrollToBottom();

    const steps = [
        "Retrieving information",
        "Analyzing sources",
        "Preparing response"
    ];
    let stepIndex = 0;
    const stepEl = processing.querySelector("#processText");

    const interval = setInterval(() => {
        stepIndex = (stepIndex + 1) % steps.length;
        stepEl.textContent = steps[stepIndex];
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
            data.answer || "I couldn’t find official information on that.",
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

/* Render message */
function addMessage(text, sender, sources = []) {
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

/* Restore session */
window.onload = () => {
    const saved = sessionStorage.getItem("chat_history");
    if (saved) chatBox.innerHTML = saved;
};

/* Animated placeholder */
document.addEventListener("DOMContentLoaded", () => {
    const strip = document.getElementById("textStrip");
    strip.appendChild(strip.children[0].cloneNode(true));
    let i = 0;

    setInterval(() => {
        i++;
        strip.style.transition = "transform 0.8s ease";
        strip.style.transform = `translateY(-${i * 40}px)`;

        if (i === strip.children.length - 1) {
            strip.addEventListener("transitionend", () => {
                strip.style.transition = "none";
                strip.style.transform = "translateY(0)";
                i = 0;
            }, { once: true });
        }
    }, 2600);
});
