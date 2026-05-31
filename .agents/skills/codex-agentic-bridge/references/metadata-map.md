# Claude式YAML → Codex読み替え表

## 基本方針

Claude CodeのYAMLフロントマターは、Codexでは「そのままの実行設定」ではなく「意図のメモ」として読む。

Codexで本当に効かせる場所：

- スキル発火：`.agents/skills/<name>/SKILL.md` の `name` / `description`
- サブエージェント：`.codex/agents/*.toml`
- 全体指示：`AGENTS.md`
- 自動チェック：`.codex/hooks.json` または `config.toml` のhooks

## 対応表

| Claude式 | 意味 | Codexでの扱い |
|---|---|---|
| `name` | スキル/エージェント名 | Codexでも使う |
| `description` | 発火条件・役割説明 | Codexでは最重要。発火条件を具体的に書く |
| `user-invocable` | ユーザーが直接呼べるか | `agents/openai.yaml` の `policy.allow_implicit_invocation` 等で補助。強制ではない |
| `argument-hint` | 引数のヒント | 本文に「入力形式」として書く |
| `agent` | 委譲先 | Codexのサブエージェント種別、または `.codex/agents/*.toml` 候補に変換 |
| `context: fork` | 文脈を分ける | Codexのサブエージェント委譲時に `fork_context` が必要か判断する |
| `model` | Claudeモデル指定 | Codexでは作業難度・推論量のヒントとして扱う |
| `effort` | 推論量 | Codexの `model_reasoning_effort` のヒント |
| `tools` | 使える道具 | Codexでは強制権限ではなく、developer instructionsに「使ってよい/避ける」と明記 |
| `allowed-tools` | 使える道具 | 同上。権限境界ではない |
| `disable-model-invocation` | モデル起動抑制 | Codexに直接対応なし。スクリプト化・手順化を検討 |
| `autoInvoke` | 自動発火 | `description` 強化またはhooks化 |
| `pair` | 相棒スキル/評価役 | Generator/Evaluatorループとして明文化 |
| `maxTurns` | 最大ターン | Codexでは受入基準・完了条件・停止条件として明記 |
| `memory` | メモリ範囲 | AGENTS.md、references、Chronicle/メモリ設計に分ける |
| `background` | 背景実行 | CodexではGoal/長時間作業/サブエージェント運用として再設計 |
| `isolation` | 分離実行 | worktreeやsandboxの方針として再設計 |
| `hooks` | 自動処理 | Codex hooksへ移植。ただし対応イベント差に注意 |

## モデル読み替え

厳密な1:1対応ではなく、役割で読む。

| Claude側 | Codexでの意味 |
|---|---|
| `opus` | 難しい設計、評価、統合、判断 |
| `sonnet` | 実装、修正、通常の開発作業 |
| `haiku` | 軽い抽出、分類、整形、下調べ |

## 命名のおすすめ

Claude側の `assign-*`, `delegate-*`, `run-*`, `ref-*`, `wrap-*` はCodexでも残してよい。

ただしCodex側では、`description` に用途を明確に書く。

例：

```yaml
description: "スライド生成後の品質評価を行うEvaluator。直接修正せず、フィードバックファイルを出力する。run-slideやassign-slide-generatorの後に使う。"
```

## 一番大事な注意

Codex移植では、**YAMLを増やすより、descriptionと本文の実行手順を強くする**。

CodexはClaude式の独自キーを常に解釈するわけではない。  
だから、独自キーは「人間とCodexが読む設計図」として残し、本当に効かせる内容はCodexの正式な置き場へ写す。

