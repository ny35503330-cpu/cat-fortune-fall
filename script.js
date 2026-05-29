const fortunes = [
  "新しい発見がある日",
  "ゆっくり進めば大吉",
  "小さな挑戦が実る",
  "笑顔が幸運を呼ぶ",
  "休むほど力が戻る",
  "思いつきを試す日",
  "やさしい言葉が吉",
  "一歩だけ前へ進む",
  "好きなものに近づく",
  "深呼吸で道が開く",
];

const stage = document.querySelector("#stage");
const button = document.querySelector("#drawButton");

function pickFortune() {
  const index = Math.floor(Math.random() * fortunes.length);
  return fortunes[index];
}

function createCatCard(message) {
  const card = document.createElement("div");
  card.className = "cat-card";
  card.innerHTML = `
    <div class="cat" aria-hidden="true">
      <div class="ear ear-left"></div>
      <div class="ear ear-right"></div>
      <div class="head">
        <div class="stripe stripe-one"></div>
        <div class="stripe stripe-two"></div>
        <div class="stripe stripe-three"></div>
        <div class="eye eye-left"></div>
        <div class="eye eye-right"></div>
        <div class="muzzle">
          <div class="nose"></div>
          <div class="mouth"></div>
        </div>
        <div class="whisker whisker-left"></div>
        <div class="whisker whisker-right"></div>
      </div>
      <div class="paw paw-left"></div>
      <div class="paw paw-right"></div>
    </div>
    <div class="fortune">
      <p class="fortune-label">猫からの札</p>
      <p class="fortune-message">${message}</p>
    </div>
  `;
  return card;
}

button.addEventListener("click", () => {
  stage.replaceChildren(createCatCard(pickFortune()));
});
