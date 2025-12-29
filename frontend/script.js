const hero = document.getElementById("hero");
const chatSection = document.getElementById("chat-section");
const startBtn = document.getElementById("start-btn");

const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const typing = document.getElementById("typing");

const BACKEND_URL = "http://127.0.0.1:5000/chat";

/* Start button */
startBtn.onclick = () => {
  hero.style.display = "none";
  chatSection.hidden = false;
};

function formatAIResponse(text) {
  // Clean extra spaces
  text = text.replace(/\r/g, "").trim();

  // Bold **text**
  text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // Section titles (lines ending with :)
  text = text.replace(
    /^(.{3,40}:)$/gm,
    `<div class="mt-4 mb-2 text-blue-400 font-semibold">$1</div>`
  );

  // Soft bullet points (only real lists)
  text = text.replace(/^\- (.*)$/gm, "• $1");

  // Paragraph handling
  const paragraphs = text.split(/\n\n+/);

  let formatted = paragraphs.map(p => {
    // If paragraph has bullets
    if (p.includes("• ")) {
      const lines = p.split("\n").filter(Boolean);
      const items = lines
        .map(l => `<li class="mb-2">${l.replace("• ", "")}</li>`)
        .join("");
      return `<ul class="list-disc pl-6 my-3">${items}</ul>`;
    }

    // Normal paragraph
    return `<p class="mb-4 leading-relaxed">${p}</p>`;
  }).join("");

  return `
    <div class="ai-content text-gray-100">
      ${formatted}
    </div>
  `;
}


function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);

  if (sender === "ai") {
    msg.innerHTML = formatAI(text);
  } else {
    msg.innerText = text;
  }

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;

  addMessage(message, "user");
  userInput.value = "";
  typing.hidden = false;

  try {
    const response = await fetch(BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    typing.hidden = true;
    addMessage("🤖 " + data.reply, "ai");

  } catch {
    typing.hidden = true;
    addMessage("⚠️ Unable to reach server.", "ai");
  }
});
