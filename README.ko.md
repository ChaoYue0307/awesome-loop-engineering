# Awesome Loop Engineering

<!-- last-synced: 2026-06-19 -->

<p align="center">
  <img src="assets/awesome-loop-engineering-cover.png" alt="Awesome Loop Engineering cover" width="100%">
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
  <a href="TRANSLATIONS.md">번역 돕기</a> |
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/">랜딩 페이지</a> |
  <a href="https://huggingface.co/datasets/cy0307/awesome-loop-engineering">Hugging Face 미러</a>
</p>

> **Loop Engineering** 을 위한 구현 중심 큐레이션 목록입니다. Loop Engineering 은 prompt, context, harness engineering 위의 레이어로, 반복 실행되는 AI-agent 시스템을 설계합니다.

Prompt engineering 은 모델에게 무엇을 요청할지 개선합니다. Context engineering 은 모델이 무엇을 볼 수 있는지 개선합니다. Harness engineering 은 한 번의 agent 실행을 둘러싼 도구, 권한, sandbox, 검증을 개선합니다. **Loop Engineering 은 이 세 레이어 위에 있습니다**. agent 를 실행하고, 감독하고, 결과를 검증하고, 상태를 저장하고, 다시 실행하는 시스템을 설계하는 실천입니다.

Loop 는 작업을 발견하고, 하나 이상의 agents 에게 위임하고, 결과를 확인하고, 상태를 기록하고, 다음 행동을 결정한 뒤, 일정 cadence 또는 검증 가능한 목표에 도달할 때까지 다시 실행됩니다.

이 저장소는 AI agents / coding agents 맥락의 새로운 Loop Engineering 의미에만 집중합니다. software event loop, control theory, growth loop, 일반적인 workflow automation, 비 AI feedback loop 는 범위에 포함하지 않습니다.

목록 외에도 이 저장소는 15개의 loop 패턴, 각 패턴에 대한 스키마 검증 loop contract, 6개의 실행 가능한 loop 템플릿, 커뮤니티 gallery, 8개 언어를 제공합니다.

## 멘탈 모델

- Prompt engineering: 모델에게 무엇을 말해야 하는가?
- Context engineering: 모델이 어떤 상태와 지식을 봐야 하는가?
- Harness engineering: agent 주변에 어떤 도구, 권한, 테스트, sandbox, feedback 이 있어야 하는가?
- Loop engineering: 사람이 내부 루프에 있지 않을 때 어떤 반복 시스템이 작업을 발견하고, agents 에게 위임하고, 결과를 검증하고, 상태를 저장하고, 다음 행동을 결정하고, 다시 실행해야 하는가?

Prompt, context, harness engineering 은 한 번의 실행을 더 좋게 만듭니다. Loop Engineering 은 agent 작업을 시간에 걸쳐 반복 가능하고, 관찰 가능하고, 거버넌스 가능하게 만듭니다.

## Loop Contract

유용한 loop 는 보통 다음 요소를 명확히 해야 합니다.

| 요소                | 설계 질문                                          | 일반적인 산출물                                                    |
| ----------------- | ---------------------------------------------- | ----------------------------------------------------------- |
| Objective         | loop 는 무엇을 최적화하는가?                             | Goal, issue, PRD, runbook                                   |
| Trigger           | 언제 실행되는가?                                      | Schedule, webhook, `/loop`, `/goal`, automation             |
| Discover / Intake | 어떻게 작업을 발견하는가?                                 | GitHub query, Linear filter, CI failure, feedback stream    |
| Workspace         | agent 는 어디에서 안전하게 행동하는가?                       | Worktree, sandbox, branch, container                        |
| Context           | 어떤 지속 지식을 로드해야 하는가?                            | `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, docs                  |
| Delegation        | 어떤 agent 가 무엇을 담당하는가?                          | Explorer, implementer, reviewer, judge                      |
| Verification      | 무엇이 성공 또는 실패를 판단하는가?                           | Tests, typecheck, lint, evals, trace graders                |
| State             | 다음 실행까지 무엇이 남아야 하는가?                           | Progress file, checkpoint, trace, issue comment             |
| Budget            | 언제 비용 소비를 멈춰야 하는가?                             | Max turns, max retries, token budget, time box              |
| Escalation        | 언제 사람이 개입해야 하는가?                               | PR, issue, Slack alert, triage inbox                        |
| Exit              | loop 는 어떻게 완료를 판단하는가?                          | Acceptance criteria, passing checks, no work found          |

## 성숙도 모델

| 레벨   | 이름                         | 설명                                                                                           |
| ---- | -------------------------- | -------------------------------------------------------------------------------------------- |
| 0    | Manual prompting           | 사람이 상태를 읽고 다음 prompt 를 작성합니다.                                                                |
| 1    | Scripted retry             | script 가 오류를 agent 에게 다시 전달합니다.                                                              |
| 2    | Scheduled loop             | agent 가 일정 cadence 로 실행되고 결과를 보고합니다.                                                         |
| 3    | Stateful loop              | 파일, issue, checkpoint, trace 로 진행 상황이 유지됩니다.                                                 |
| 4    | Self-verifying loop        | 결정적 check 또는 evaluator agent 가 잘못된 완료를 막습니다.                                                 |
| 5    | Multi-agent loop           | 전문 agents 가 discovery, implementation, review, judgment 를 나눕니다.                              |
| 6    | Production-supervised loop | observability, budget, approval, rollback, human escalation 이 핵심 요소가 됩니다.                    |

## 시작하기

전체 리소스 목록은 영어 canonical README 에 있습니다: [README.md](README.md).

추천 시작 자료:

- [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) - 수동 prompting 에서 prompt, 검증, 지속을 수행하는 시스템 설계로 이동하는 흐름을 정의합니다.
- [Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex) - plan-edit-test-observe-repair-document-repeat 작업을 위한 실용 runbook.
- [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks) - `/loop`, scheduled tasks, recurring prompts 의 공식 메커니즘.
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) - workflows 와 agents 를 위한 composable patterns.

## 기여하기

Pull request 를 환영합니다. 먼저 [CONTRIBUTING.md](CONTRIBUTING.md) 를 읽어 주세요.

빠른 절차:

1. 리소스가 AI/coding-agent 맥락의 Loop Engineering 또는 직접적인 기반인지 확인합니다.
1. README 에서 중복 여부를 검색합니다.
1. 가장 구체적인 카테고리를 선택합니다.
1. 다음 형식으로 한 줄을 추가합니다.

```md
- 📄 **Paper** [Title](https://example.com) - One sentence explaining the resource's contribution to Loop Engineering.
```

1. PR 에서 관련성, 카테고리, 리소스 타입, builders 에게 주는 가치를 설명합니다.

## 번역

새 언어를 추가하거나 유지하고 싶다면 [TRANSLATIONS.md](TRANSLATIONS.md) 를 읽어 주세요. 번역은 scope boundary 를 지켜야 하며 event loop, growth loop, 일반 automation 을 범위에 섞지 않아야 합니다.
