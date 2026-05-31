---
name: codex-agentic-bridge
description: "Claude Code仕様のYAMLフロントマター、サブエージェント委譲、Phase Delegation Table、Task()例、評価ループをCodexでも効く形に読み替える橋渡しスキル。Claude用の .claude/skills や .claude/agents をCodexで使いたい時、agent/pair/autoInvoke/model/context/maxTurns/tools などのメタデータをCodex流に解釈したい時、Codexの .agents/skills や .codex/agents へ移植・設計・監査したい時に使う。"
---

# Codexエージェント橋渡し

## 目的

Claude Code向けに育てた「YAMLフロントマターで委譲するスキル」を、Codexでも動く考え方に変換する。

大事な前提：

- Claude Codeの `Task(...)` や `agent:` は、Codexでそのまま自動実行されるわけではない。
- Codexでは、スキルは `.agents/skills/<name>/SKILL.md`、サブエージェントは `.codex/agents/*.toml` が基本。
- そのため、Claude式YAMLは「実行命令」ではなく、Codexが読むための**設計メモ**として扱い、Codexの道具に読み替える。

## まずやること

Claude式スキルやエージェントを扱う時は、最初に棚卸しする。

```bash
python3 .agents/skills/codex-agentic-bridge/scripts/audit_agentic_yaml.py --root .
```

出力から次を確認する。

- `agent`, `pair`, `autoInvoke`, `context`, `model`, `tools`, `maxTurns` を使っているファイル
- Codexへそのまま移せるもの
- Codexでは読み替えが必要なもの
- 危険な1:1移植になりそうなもの

## 読むべき参照

必要に応じて読む。

- `references/metadata-map.md`：Claude式YAML → Codexでの読み替え表
- `references/delegation-template.md`：Codexでサブエージェントへ渡す時の5要素テンプレ

## Codexでの実行方針

### 0. 基本3役

このリポジトリでは、最初のCodex用サブエージェントとして次を使う。

| 役割 | ファイル | 使う場面 |
|---|---|---|
| 設計役 | `.codex/agents/agentic_planner.toml` | Claude式YAMLをCodex設計へ読み替える |
| 実装役 | `.codex/agents/agentic_worker.toml` | 指定範囲だけCodex用ファイルへ移植する |
| 評価役 | `.codex/agents/agentic_evaluator.toml` | 移植結果を読み取り専用で評価する |

大量の `.claude/agents` を一気に移す前に、この3役で流れを作る。

### 1. スキルの発火

Codexで確実に効かせたい内容は、`SKILL.md` のフロントマターにある `description` へ寄せる。

Codexが常時見ている中心情報は：

- `name`
- `description`
- スキルの場所

Claude式の `user-invocable`, `argument-hint`, `agent`, `model` は、Codexでは補助情報として本文に残す。

### 2. サブエージェント委譲

ユーザーが「委譲」「サブエージェント」「並列」「エージェンティック」などを明示している場合、Codexのサブエージェント機能を使ってよい。

委譲する時は、Claude式 `Task(...)` をそのまま書くのではなく、次の5要素に変換して渡す。

1. 元の目標
2. この担当の責務
3. スコープ制限
4. 使用してよい道具・避ける道具
5. 受入基準

詳しい型は `references/delegation-template.md` を使う。

### 3. `agent:` / `pair:` の読み替え

Claude式：

```yaml
agent: general-purpose
pair: assign-slide-generator
```

Codex式の考え方：

- `agent:` は、候補となるCodexサブエージェント種別または `.codex/agents/*.toml` の候補として扱う。
- `pair:` は、Generator/Evaluatorの相棒関係として扱う。
- ただし、自動で必ず起動するのではなく、タスク分解上必要な時に明示的に委譲する。

### 4. `model:` の読み替え

Claude式の `opus/sonnet/haiku` は、Codexでは厳密に同じモデル指定ではない。

基本方針：

- `opus` 相当：難しい設計・評価・統合
- `sonnet` 相当：実装・修正・通常作業
- `haiku` 相当：軽い分類・抽出・整形

Codexではモデルを固定しすぎず、必要な時だけ「高めの推論」「軽めの処理」として読み替える。

### 5. `autoInvoke:` の読み替え

Claude式の `autoInvoke: true` は、Codexでは「自動で必ず発火する保証」ではない。

Codexでは次のどちらかにする。

- スキル `description` に発火条件を明記する
- 必ず走らせたい処理は `.codex/hooks.json` または Codex設定のhooksへ移す

### 6. Hooksの読み替え

Claude CodeのhooksとCodex hooksは完全一致しない。

Codexでは特に次を意識する。

- `PreToolUse`：危険なコマンドや編集の前に止める・注意を足す
- `PostToolUse`：コマンド後の確認
- `Stop`：最後の検証やまとめ
- `UserPromptSubmit`：ユーザー入力時の文脈追加

スキル内hooksはCodexでそのまま効くとは考えない。必要ならプロジェクトの `.codex/hooks.json` へ移す。

## 移植パターン

### 軽いスキル

対象：

- `user-invocable: true`
- `agent` なし
- `pair` なし
- 単一手順

対応：

- `.agents/skills/<name>/SKILL.md` に移す
- `description` をCodex向けに厚めに書く
- Claude専用の項目は本文の「参考メタデータ」に移す

### 委譲スキル

対象：

- `agent:`
- `context: fork`
- `Task(...)` 例あり
- Phase Delegation Tableあり

対応：

- `.agents/skills/<name>/SKILL.md` に移す
- 本文に「Codex委譲手順」を書く
- 必要なら `.codex/agents/*.toml` に専門エージェントを作る
- サブエージェントに渡す文は5要素テンプレにする

### Generator / Evaluator ペア

対象：

- `pair:`
- `assign-*`
- 評価→修正ループ

対応：

- Generator担当とEvaluator担当を分ける
- Evaluatorには原則、直接修正させない
- Evaluatorは評価ファイルやフィードバックを出す
- Generatorがフィードバックを読んで修正する
- 最後にメインが実体確認する

## 禁止する移植

以下はそのまま移さない。

- Claudeの `Task(...)` をCodexでそのまま実行される前提にする
- `allowed-tools` をCodexの強制権限だと思い込む
- `model: opus` などをCodexで完全同一モデル指定だと思い込む
- `autoInvoke: true` だけでCodexでも自動発火すると期待する
- スキル内hooksがCodexでも同じタイミングで効くと期待する
- サブエージェントの完了報告を、実体確認なしに信じる

## 完了時の確認

作業後は次を確認する。

- Codex用スキルの `name` と `description` が有効
- `.agents/skills` に配置されている
- 必要な専門エージェントが `.codex/agents/*.toml` にある
- Claude専用メタデータが本文か参照に退避されている
- サブエージェント委譲文が5要素になっている
- 評価役と修正役が混ざっていない
- 実行結果をメインが確認している

## 最後の説明

ユーザーには短く説明する。

> Claude式のYAMLを、Codexがそのまま実行するわけではありません。  
> 代わりに、YAMLを「役割分担の設計図」として読み、Codexのスキル・サブエージェント・hooksに変換して動かします。
