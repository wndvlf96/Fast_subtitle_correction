# 유튜브의 자동 생성 자막에 대한 교정 처리
## 기존 자동 생성된 자막에 대해서 바른AI, GPT에 대한 교정 결과

``` javascript

const API_URL = "https://api.bareun.ai/bareun.RevisionService/CorrectError";
const API_KEY = "koba-4FTYDTQ-YSOE4XA-UUNZYKQ-UMKWG6I";

let lastSentText = "";

function cleanText(text) {
  return text.replace(/^>>\s*/, "").trim();
}

function hasSentenceMark(text) {
  return /[.!?]/.test(text);
}

function collectCaptionLines() {
  const lines = document.querySelectorAll(".caption-visual-line");
  const spans = [];
  const texts = [];

  for (const line of lines) {
    const span = line.querySelector(".ytp-caption-segment");
    if (!span) continue;

    const text = cleanText(span.innerText);
    if (!text) continue;

    spans.push(span);
    texts.push(text);
  }

  return { spans, text: texts.join(" ") };
}

function highlightDiff(original, revised) {
  const o = original.split(/\s+/);
  const r = revised.split(/\s+/);

  const result = [];
  let i = 0;

  for (const word of r) {
    if (word === o[i]) {
      result.push(word);
      i++;
    } else {
      result.push(
        `<span style="color:#ff5555;font-weight:600;">${word}</span>`
      );
    }
  }

  return result.join(" ");
}

async function sendToAPI(originalText, spans) {
  console.log("[API 요청 원문]", originalText);

  const res = await fetch(API_URL, {
    method: "POST",
    headers: {
      accept: "application/json",
      "api-key": API_KEY,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      document: { content: originalText, language: "ko-KR" },
      encoding_type: "UTF32",
      config: { enable_sentence_check: true },
    }),
  });

  const data = await res.json();
  const revised = data.revised ?? originalText;

  console.log("[API revised]", revised);

  const highlighted = highlightDiff(originalText, revised);

  const lastSpan = spans[spans.length - 1];
  lastSpan.innerHTML = highlighted;
}

const observer = new MutationObserver(() => {
  const { spans, text } = collectCaptionLines();
  if (!text) return;

  if (hasSentenceMark(text) && text !== lastSentText) {
    lastSentText = text;
    sendToAPI(text, spans);
  }
});

observer.observe(document.body, {
  childList: true,
  subtree: true,
  characterData: true,
});

```
