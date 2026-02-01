---
name: prd-builder
description: Fetches PRD (requirements) from Notion tasks DB and guides building in Cursor. Creates a plan and todos from PRD content when user asks to implement. Use when user references PRD, asks to build from Notion tasks, or wants plan and todos from a PRD.
---

# prd-builder

프로젝트 페이지 안의 **작업 DB**에서 요구사항(PRD)을 읽어와 Cursor에서 빌드하는 스킬.

## 사전 조건

- `notion-connect` 스킬로 `.notion/config.json`에 **project_page_id**, **tasks_db_id** 설정 완료

## 사용법

### Cursor에서 PRD 가져오기

Cursor 채팅에서:
```
@prd-builder 현재 PRD 목록 보여줘
```

또는 CLI:
```bash
python .cursor/skills/prd-builder/fetch.py
```

### PRD 기반 작업

1. 노션 프로젝트 페이지의 작업 DB에 요구사항 작성
2. Cursor에서 `@prd-builder` 호출
3. PRD 내용을 컨텍스트로 받아서 코드 작성
4. 완료 후 `@dev-logger`로 로그 기록 (해당 스킬 사용 시)

## 작업 DB 구조

| 속성 | 타입 | 설명 |
|------|------|------|
| 이름 / Name | title | PRD 제목 |
| 상태 | select | 대기/진행중/완료/보류 |
| 우선순위 | select | 🔴높음/🟡중간/🟢낮음 |
| 설명 / 내용 | rich_text | 상세 요구사항 |

(정렬은 created_time 기준)

## PRD 기반 플랜·투두 자동 생성

사용자가 특정 PRD를 가져와 구현하거나 "플랜 짜고 투두 넣어줘"라고 하면:

1. **PRD 조회**
   - `python .cursor/skills/prd-builder/fetch.py`로 목록 조회 후, 지정된 제목(또는 "진행중")으로 항목 찾기.
   - 해당 항목의 `id`로 `python .cursor/skills/prd-builder/fetch.py detail <id>` 실행해 본문 수집.
   - 속성 `설명`(또는 `내용`)과 본문 블록을 합쳐 요구사항 정리.

2. **플랜 작성**
   - PRD 본문(헤딩, 리스트, 설명)에서 단계·기능·산출물을 추출.
   - create_plan 도구가 있으면 사용해 구조화된 플랜 생성(목표, 단계, 검증).
   - 없으면 마크다운으로 목표·단계·검증을 정리한 플랜 문서 작성.

3. **투두 생성**
   - 플랜의 각 단계(또는 주요 마일스톤)를 TodoWrite로 추가.
   - `id`: 단계를 반영(예: `prd-1`, `prd-2`), `content`: 한 줄 요약, `status`: `pending`.
   - 플랜 단계 수만큼 todo 항목 생성해 작업 순서를 명확히 함.

## Cursor Rules

`.cursor/rules/prd.mdc`에 규칙 추가:
```markdown
PRD를 참조할 때는 .cursor/skills/prd-builder/fetch.py를 실행해서
노션 작업 DB에서 최신 PRD를 가져온다.

진행중인 PRD를 우선적으로 처리한다.
```
