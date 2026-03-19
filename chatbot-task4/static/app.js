const chatEl = document.getElementById("chat");
const formEl = document.getElementById("form");
const msgEl = document.getElementById("msg");
const sendEl = document.getElementById("send");

function addBubble({ who, text, meta }) {
  const wrap = document.createElement("div");
  wrap.className = `msg ${who}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  wrap.appendChild(bubble);

  if (meta) {
    const metaEl = document.createElement("div");
    metaEl.className = "meta";
    metaEl.textContent = meta;
    bubble.appendChild(metaEl);
  }

  chatEl.appendChild(wrap);
  chatEl.scrollTop = chatEl.scrollHeight;
}

async function sendMessage(message) {
  sendEl.disabled = true;
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      const err = data?.reply || "Something went wrong.";
      addBubble({ who: "bot", text: err });
      return;
    }

    const meta = data?.meta?.matched
      ? `matched: ${data.meta.tag} (score: ${data.meta.score})`
      : "no confident match";
    addBubble({ who: "bot", text: data.reply, meta });
  } catch (e) {
    addBubble({ who: "bot", text: "Network error. Is the server running?" });
  } finally {
    sendEl.disabled = false;
  }
}

formEl.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = (msgEl.value || "").trim();
  if (!message) return;
  msgEl.value = "";
  addBubble({ who: "me", text: message });
  await sendMessage(message);
});

addBubble({
  who: "bot",
  text: "Hi! I’m your website assistant. Ask me about hours, pricing, or support.",
  meta: "ready",
});

