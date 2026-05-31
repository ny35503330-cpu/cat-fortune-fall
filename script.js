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
  "焦らず毛づくろいの心なのです",
  "今日は早めに切り上げるのです",
  "おいしいものを味方にするのです",
  "できない日も猫様は見ています",
  "まず机の上を少し整えるのです",
  "会いたい人に一言送るのです",
  "大事なことは小さく分けるのです",
  "今日は比べない日なのです",
  "肩の力をぬくと道が見えるのです",
  "眠い時は無理しないのです",
  "直感を一度メモするのです",
  "急がばひなたぼっこなのです",
  "気になることは一つだけ片づけるのです",
  "やさしい声で自分に話すのです",
  "完璧よりごきげんが大事なのです",
  "小さなありがとうを集めるのです",
  "今日はいつもよりゆっくり歩くのです",
  "心配ごとは紙に出すのです",
  "好きな音を聞いて整えるのです",
  "もう十分がんばっているのです",
];

const specialMessages = [
  "猫様の特別加護です。今日は堂々としてよいのです",
  "大きな福がしっぽを振って近づいています",
  "今日は奇跡を受け取る準備をするのです",
  "猫様会議であなたの味方が決まりました",
  "金のひげが告げます。自信を持つのです",
];

const stage = document.querySelector("#stage");
const button = document.querySelector("#drawButton");

function pickFrom(list) {
  const index = Math.floor(Math.random() * list.length);
  return list[index];
}

function pickOracle() {
  const isSpecial = Math.random() < 0.1;

  return {
    isSpecial,
    message: isSpecial ? pickFrom(specialMessages) : pickFrom(messages),
  };
}

function createCatCard(oracle) {
  const card = document.createElement("div");
  card.className = oracle.isSpecial ? "cat-card is-special" : "cat-card";
  card.innerHTML = `
    ${oracle.isSpecial ? `
      <div class="sparkles" aria-hidden="true">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>
    ` : ""}
    <div class="cat">
      <img class="cat-art" src="assets/cat-sama-transparent.png" alt="札を持つありがたい猫様" />
      <p class="cat-message">${oracle.message}</p>
    </div>
  `;
  return card;
}

button.addEventListener("click", () => {
  stage.replaceChildren(createCatCard(pickOracle()));
});
