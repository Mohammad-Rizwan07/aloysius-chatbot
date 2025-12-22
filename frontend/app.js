async function send() {
  const input = document.getElementById("question");
  const chat = document.getElementById("chat");
  const question = input.value;
  input.value = "";

  chat.innerHTML += `<div class="user"><b>You:</b> ${question}</div>`;

  const res = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question})
  });

  const data = await res.json();

  chat.innerHTML += `<div class="bot"><b>Bot:</b> ${data.answer}</div>`;
  chat.innerHTML += `<small>Sources: ${data.sources.join(", ")}</small><hr>`;
}
