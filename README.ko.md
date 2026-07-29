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
  <a href="TRANSLATIONS.md">번역 돕기</a> |
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/">랜딩 페이지</a> |
  <a href="https://huggingface.co/datasets/cy0307/awesome-loop-engineering">Hugging Face 미러</a>
</p>

> 명시적인 트리거, 외부 검증, 지속 상태, 제한된 예산, 사람에게 넘기는 절차를 갖춘 반복 AI-agent 시스템을 설계합니다.

Prompt engineering 은 모델에게 무엇을 요청할지 개선합니다. Context engineering 은 모델이 무엇을 볼 수 있는지 개선합니다. Harness engineering 은 한 번의 agent 실행을 둘러싼 도구, 권한, sandbox, 검증을 개선합니다. **Loop Engineering 은 이 세 레이어 위에 있습니다**. agent 를 실행하고, 감독하고, 결과를 검증하고, 상태를 저장하고, 다시 실행하는 시스템을 설계하는 실천입니다.

Loop 는 작업을 발견하고, 하나 이상의 agents 에게 위임하고, 결과를 확인하고, 상태를 기록하고, 다음 행동을 결정한 뒤, 일정 cadence 또는 검증 가능한 목표에 도달할 때까지 다시 실행됩니다.

Loop Engineering 은 명시적 트리거, 검증, 지속 상태를 갖춘 반복 AI agent / coding agent 시스템을 다룹니다. software event loop, control theory, growth loop, 일반적인 workflow automation, 비 AI feedback loop 는 포함하지 않습니다.

797개의 감사된 리소스, 22개의 운영 loop 패턴, 22개의 스키마 검증 loop contract, 8개의 runtime starter(실행 파일 3개와 적용 가능한 템플릿 5개)로 바로 시작할 수 있습니다. 커뮤니티 gallery 와 8개 언어 안내도 제공합니다.

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

전체 리소스는 영어 전체 가이드에서 볼 수 있습니다: [README.md](README.md).

추천 시작 자료:

- [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) - 수동 프롬프팅에서 스스로 프롬프트하고 검증하며 계속 실행하는 시스템으로의 전환을 정의한 Addy Osmani의 글.
- [Peter Steinberger의 loop 설계론](https://x.com/steipete/status/2063697162748260627) - "이제 agent를 프롬프트하지 말고, agent를 프롬프트하는 loop를 설계하라"는 2026년 6월 논의를 촉발한 게시물.
- [Boris Cherny: agent 자율 실행을 위한 다섯 가지 팁](https://x.com/bcherny/status/2063792263067754658) - 몇 시간에서 며칠 동안 자율 실행되는 loop를 위한 Claude Code 창시자의 간결한 레시피.
- [The New Stack: 프롬프팅에서 loop로](https://thenewstack.io/loop-engineering/) - 반복적인 agent 작업을 위해 loop를 작성하게 된 Boris Cherny의 전환에 대한 보도.

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
