window.addEventListener("load", () => loadEmotions(false));

async function loadEmotions(forceUpdate = false) {
  const emotionList = document.getElementById("emotionList");

  if (!forceUpdate && emotionList.innerHTML.trim() === "") {
    emotionList.innerHTML = '<span class="spinner"></span> 読み込み中...';
  }

  if (forceUpdate) {
    const existingBtn = emotionList.querySelector(".refresh-item");
    if (existingBtn) {
      existingBtn.innerHTML = '<span class="spinner"></span> 更新中...';
      existingBtn.style.cursor = "wait";
      existingBtn.style.pointerEvents = "none";
    }
  }

  try {
    const endpoint = forceUpdate ? "/update_presets" : "/emotions";
    const options = forceUpdate ? { method: "POST" } : { method: "GET" };

    const response = await fetch(endpoint, options);
    if (!response.ok) throw new Error("Network response was not ok");
    const data = await response.json();

    if (data.emotions) {
      emotionList.innerHTML = "";

      if (data.emotions.length > 0) {
        data.emotions.forEach((emotion) => {
          const span = document.createElement("span");
          span.className = "emotion-item";
          span.textContent = emotion;
          span.id = `emotion-${emotion}`;
          span.onclick = () => switchPreset(emotion);
          emotionList.appendChild(span);
        });
      } else {
        const msg = document.createElement("span");
        msg.textContent = "プリセットなし";
        msg.style.color = "#888";
        msg.style.fontSize = "0.75rem";
        emotionList.appendChild(msg);
      }

      appendRefreshButton(emotionList, forceUpdate);

      if (forceUpdate) {
        addMessage("システム: プリセット情報を更新しました。", "ai", "通常");
      }
    }
  } catch (e) {
    console.error("Failed to load emotions", e);

    if (!forceUpdate) {
      emotionList.innerHTML = "読み込みエラー";
    }

    if (forceUpdate) {
      addMessage("システムエラー: 更新に失敗しました。", "ai", "ERROR");
      const btn = emotionList.querySelector(".refresh-item");
      if (btn) {
        btn.innerHTML = "↻ 更新";
        btn.style.cursor = "pointer";
        btn.style.pointerEvents = "auto";
      }
    } else {
      appendRefreshButton(emotionList, false, true);
    }
  }
}

function appendRefreshButton(container, wasUpdated, isRetry = false) {
  const refreshBtn = document.createElement("span");
  refreshBtn.className = "refresh-item";
  refreshBtn.innerHTML = wasUpdated
    ? "更新完了"
    : isRetry
      ? "↻ 再試行"
      : "↻ 更新";
  refreshBtn.title = "プリセット一覧を更新";
  refreshBtn.onclick = () => loadEmotions(true);

  if (wasUpdated) {
    refreshBtn.style.color = "var(--primary-color)";
    refreshBtn.style.borderColor = "var(--primary-color)";
    setTimeout(() => {
      refreshBtn.innerHTML = "↻ 更新";
      refreshBtn.style.color = "";
      refreshBtn.style.borderColor = "";
    }, 1500);
  }

  container.appendChild(refreshBtn);
}

async function sendMessage() {
  const input = document.getElementById("userInput");
  const button = document.getElementById("sendButton");
  const chatArea = document.getElementById("chatArea");
  const message = input.value.trim();

  if (!message) return;

  input.disabled = true;
  button.disabled = true;

  addMessage(message, "user");
  input.value = "";

  const loadingId = "loading-" + Date.now();
  const loadingDiv = document.createElement("div");
  loadingDiv.className = "loading";
  loadingDiv.id = loadingId;
  loadingDiv.innerHTML = '<span class="spinner"></span> AI思考中...';
  chatArea.appendChild(loadingDiv);
  scrollToBottom();

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    });

    if (!response.ok) throw new Error("API Error");

    const data = await response.json();

    document.getElementById(loadingId).remove();

    addMessage(data.content, "ai", data.emotion);
  } catch (error) {
    console.error("Error:", error);
    const loadingEl = document.getElementById(loadingId);
    if (loadingEl) loadingEl.remove();
    addMessage("システムエラー: 接続に失敗しました。", "ai", "ERROR");
  } finally {
    input.disabled = false;
    button.disabled = false;
    input.focus();
    scrollToBottom();
  }
}

function addMessage(text, sender, emotion = null) {
  const chatArea = document.getElementById("chatArea");
  const div = document.createElement("div");
  div.className = `message ${sender}`;

  if (emotion) {
    text += `<span class="emotion-tag">感情: ${emotion}</span>`;

    document
      .querySelectorAll(".emotion-item")
      .forEach((el) => el.classList.remove("active"));
    const activeItem = document.getElementById(`emotion-${emotion}`);
    if (activeItem) activeItem.classList.add("active");
  }

  div.innerHTML = text;
  chatArea.appendChild(div);
  scrollToBottom();
}

function scrollToBottom() {
  const chatArea = document.getElementById("chatArea");
  chatArea.scrollTop = chatArea.scrollHeight;
}

async function switchPreset(presetName) {
  try {
    document
      .querySelectorAll(".emotion-item")
      .forEach((el) => el.classList.remove("active"));
    const activeItem = document.getElementById(`emotion-${presetName}`);
    if (activeItem) activeItem.classList.add("active");

    const response = await fetch("/switch_preset", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: presetName }),
    });

    if (!response.ok) {
      throw new Error("プリセット切り替えに失敗しました");
    }

    const data = await response.json();
    addMessage(
      `プリセットを「${presetName}」に切り替えました`,
      "ai",
      presetName,
    );
  } catch (error) {
    console.error("Error switching preset:", error);
    addMessage(
      `エラー: プリセット切り替えに失敗しました (${presetName})`,
      "ai",
      "ERROR",
    );
  }
}
