# Awesome Loop Engineering

<!-- last-synced: 2026-07-20 -->

<p align="center">
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/"><img src="assets/awesome-loop-engineering-cover.png" alt="Awesome Loop Engineering cover" width="100%"></a>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">中文</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.pt-BR.md">Português</a> |
  <a href="TRANSLATIONS.md">翻訳に協力する</a> |
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/">ランディングページ</a> |
  <a href="https://huggingface.co/datasets/cy0307/awesome-loop-engineering">Hugging Face ミラー</a>
</p>

> 明示的なトリガー、外部検証、永続状態、制限付き予算、人間への引き継ぎを備えた、繰り返し実行される AI-agent システムを設計します。

Prompt engineering はモデルに何を依頼するかを改善します。Context engineering はモデルが何を見られるかを改善します。Harness engineering は 1 回の agent 実行を取り巻くツール、権限、sandbox、検証を改善します。**Loop Engineering はその上位にあります**。agent を起動し、監督し、結果を検証し、状態を保存し、再実行するシステムを設計する実践です。

Loop は作業を発見し、1 つ以上の agents に委任し、結果を確認し、状態を記録し、次の行動を決め、一定の cadence または検証可能な目標に到達するまで再実行されます。

Loop Engineering は、明示的なトリガー、検証、永続状態を備えた反復型 AI agent / coding agent システムを対象とします。software event loop、制御理論、growth loop、一般的な workflow automation、非 AI の feedback loop は含みません。

601 件の監査済みリソース、20 個の運用パターン、20 個の schema 検証済み loop contract、8 個の runtime starter（3 個の実行ファイルと 5 個の適応可能なテンプレート）から始められます。コミュニティ gallery と 8 言語の導入も利用できます。

## メンタルモデル

- Prompt engineering: モデルに何を言うべきか？
- Context engineering: モデルはどの状態や知識を見るべきか？
- Harness engineering: agent の周囲にどのツール、権限、テスト、sandbox、feedback を置くべきか？
- Loop engineering: 人間が内側のループから離れたとき、どの反復システムが作業を発見し、agent に委任し、結果を検証し、状態を永続化し、次の行動を決め、再実行するべきか？

Prompt、context、harness engineering は 1 回の実行を良くします。Loop Engineering は agent の仕事を時間をまたいで反復可能、観測可能、統治可能にします。

## Loop Contract

有用な loop には通常、次の要素が必要です。

| 要素                | 設計上の問い                                        | 一般的な成果物                                                     |
| ----------------- | --------------------------------------------- | ----------------------------------------------------------- |
| Objective         | loop は何を最適化するのか？                              | Goal, issue, PRD, runbook                                   |
| Trigger           | いつ実行されるのか？                                    | Schedule, webhook, `/loop`, `/goal`, automation             |
| Discover / Intake | どのように作業を発見するのか？                               | GitHub query, Linear filter, CI failure, feedback stream    |
| Workspace         | agent はどこで安全に行動できるのか？                         | Worktree, sandbox, branch, container                        |
| Context           | どの永続的な知識を読み込むのか？                              | `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, docs                  |
| Delegation        | どの agent が何を担当するのか？                           | Explorer, implementer, reviewer, judge                      |
| Verification      | 何が成功または失敗を判断するのか？                             | Tests, typecheck, lint, evals, trace graders                |
| State             | 次回の実行に何を残すのか？                                 | Progress file, checkpoint, trace, issue comment             |
| Budget            | いつ消費を止めるのか？                                   | Max turns, max retries, token budget, time box              |
| Escalation        | いつ人間に引き継ぐのか？                                  | PR, issue, Slack alert, triage inbox                        |
| Exit              | loop はどう完了を判断するのか？                            | Acceptance criteria, passing checks, no work found          |

## 成熟度モデル

| レベル    | 名称                         | 説明                                                                                           |
| ------ | -------------------------- | -------------------------------------------------------------------------------------------- |
| 0      | Manual prompting           | 人間が状態を読み、次の prompt を書く。                                                                      |
| 1      | Scripted retry             | script がエラーを agent に戻す。                                                                      |
| 2      | Scheduled loop             | agent が一定の cadence で実行され、結果を報告する。                                                            |
| 3      | Stateful loop              | ファイル、issue、checkpoint、trace によって進捗が残る。                                                       |
| 4      | Self-verifying loop        | 決定的な check や evaluator agent が誤った完了を防ぐ。                                                      |
| 5      | Multi-agent loop           | 専門 agents が discovery、implementation、review、judgment を分担する。                                  |
| 6      | Production-supervised loop | observability、budget、approval、rollback、人間への escalation が一級の要素になる。                            |

## はじめに読むもの

すべてのリソースは英語の完全版ガイドで確認できます: [README.md](README.md)。

おすすめの入口:

- [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) - 手動プロンプティングから、自らプロンプトし検証し続行するシステムへの転換を示す Addy Osmani の定義。
- [Peter Steinberger による loop 設計論](https://x.com/steipete/status/2063697162748260627) - 「agent にプロンプトするのではなく、agent にプロンプトする loop を設計せよ」という 2026 年 6 月の議論の発端となった投稿。
- [Boris Cherny: agent を自律実行するための 5 つのコツ](https://x.com/bcherny/status/2063792263067754658) - Claude Code 作者による、数時間から数日の自律 loop のためのコンパクトなレシピ。
- [The New Stack: プロンプティングから loop へ](https://thenewstack.io/loop-engineering/) - 反復的な agent 作業のために loop を書くようになった Boris Cherny の転換についての報道。

## 貢献

Pull request は歓迎です。まず [CONTRIBUTING.md](CONTRIBUTING.md) を読んでください。

最短手順:

1. そのリソースが AI/coding-agent 文脈の Loop Engineering、またはその直接的な基盤であることを確認する。
1. README を検索して重複を避ける。
1. 最も具体的なカテゴリを選ぶ。
1. 次の形式で 1 行追加する。

```md
- 📄 **Paper** [Title](https://example.com) - One sentence explaining the resource's contribution to Loop Engineering.
```

1. PR で関連性、カテゴリ、リソース種別、builders にとっての価値を説明する。

## 翻訳

新しい言語を追加または維持したい場合は [TRANSLATIONS.md](TRANSLATIONS.md) を読んでください。翻訳では scope boundary を守り、event loop、growth loop、一般的な automation を混ぜないでください。
