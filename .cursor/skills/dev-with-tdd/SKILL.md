---
name: dev-with-tdd
description: When developing features or implementing code, applies test-driven development by using the test-driven-development skill. Use when the user asks to develop, implement, build, or code something. Keywords: develop, implement, build, code, feature, TDD, test-first.
---

# 개발 시 TDD 함께 사용

개발(구현·빌드·코딩) 요청 시 **test-driven-development** 스킬을 함께 적용한다.

## 적용 시점

- 사용자가 "만들어줘", "구현해줘", "개발해줘", "빌드해줘", "코드 짜줘" 등으로 요청할 때
- PRD/플랜 기반으로 구현할 때
- 새 기능·컴포넌트·API 등을 추가할 때

## 사용 방법

1. **TDD 스킬 참조**: `.cursor/skills/test-driven-development/SKILL.md`를 참조해 테스트 우선·품질 게이트·단계 구조를 따른다.
2. **테스트 우선**: 구현 전에 실패하는 테스트를 먼저 작성(Red) → 최소 구현으로 통과(Green) → 리팩터(Refactor).
3. **품질 게이트**: test-driven-development 스킬의 Quality Gate Standards를 만족한 뒤 다음 단계로 진행한다.
4. **플랜이 있을 때**: `docs/plans/` 등에 phase 플랜이 있으면 그 단계별 TDD 작업 순서를 따른다.

## 요약

- 개발 요청 시 **test-driven-development** 스킬을 함께 적용한다.
- 테스트 먼저 작성 → 구현 → 리팩터 순서를 유지한다.
- 품질 게이트 통과 후 다음 작업으로 넘긴다.
