const messages = [
  "まずは水を飲むのです",
  "今日は少しだけ休むのです",
  "小さく始めればよいのです",
  "返事は急がなくてよいのです",
  "好きなものを大事にするのです",
  "迷ったら寝てから決めるのです",
  "できた所までで十分えらいのです",
  "深呼吸してから進むのです",
  "自分にやさしくするのです",
  "一歩進めばもう勝ちなのです",
];

const stage = document.querySelector("#stage");
const button = document.querySelector("#drawButton");

function pickMessage() {
  const index = Math.floor(Math.random() * messages.length);
  return messages[index];
}

function createCatCard(message) {
  const card = document.createElement("div");
  card.className = "cat-card";
  card.innerHTML = `
    <div class="cat">
      <img class="cat-art" src="assets/cat-sama-transparent.png" alt="札を持つありがたい猫様" />
      <p class="cat-message">${message}</p>
    </div>
  `;
  return card;
}

button.addEventListener("click", () => {
  stage.replaceChildren(createCatCard(pickMessage()));
});
