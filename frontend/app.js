const API_BASE_URL = "http://localhost:8000/api/v1";

async function sendMessage(event) {
    event.preventDefault();
    
    const input = document.getElementById("questionInput");
    const chatBox = document.getElementById("chatBox");
    const question = input.value.trim();
    
    if (!question) return;
    
    // Add user message to chat
    addMessageToChat(question, 'user');
    input.value = "";
    input.disabled = true;
    document.getElementById("sendBtn").disabled = true;
    
    // Show typing indicator
    const typingDiv = document.createElement("div");
    typingDiv.className = "message bot-message";
    typingDiv.innerHTML = `<div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>`;
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Remove typing indicator
        typingDiv.remove();
        
        // Add bot response
        addMessageToChat(data.answer, 'bot', data.sources, data.confidence);
        
    } catch (error) {
        typingDiv.remove();
        console.error("Error:", error);
        addMessageToChat(
            "Sorry, I encountered an error while processing your question. Please try again.",
            'bot'
        );
    } finally {
        input.disabled = false;
        document.getElementById("sendBtn").disabled = false;
        input.focus();
    }
}

function addMessageToChat(message, sender, sources = [], confidence = null) {
    const chatBox = document.getElementById("chatBox");
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}-message`;
    
    let content = `<div class="message-content"><p>${escapeHtml(message)}</p>`;
    
    if (sender === 'bot' && (sources.length > 0 || confidence !== null)) {
        if (sources.length > 0) {
            content += `<div class="sources-section">`;
            content += `<div class="sources-title">📚 Sources</div>`;
            sources.forEach(source => {
                content += `<div class="source-item">• ${escapeHtml(source)}</div>`;
            });
            content += `</div>`;
        }
        
        if (confidence !== null) {
            const confidencePercent = Math.round(confidence * 100);
            const confidenceColor = confidencePercent >= 75 ? '#2e7d32' : 
                                   confidencePercent >= 50 ? '#f57c00' : '#c62828';
            content += `<div class="confidence-badge" style="background-color: ${confidenceColor}20; color: ${confidenceColor};">
                Confidence: ${confidencePercent}%
            </div>`;
        }
    }
    
    content += `</div>`;
    messageDiv.innerHTML = content;
    
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Allow Enter key to send message
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById("questionInput");
    input.focus();
});
