# prd-builder

노션 PRD 데이터베이스에서 요구사항을 읽어와 Cursor에서 빌드하는 스킬.

## 사전 조건

- `notion-connect` 스킬로 `.notion/config.json` 설정 완료

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

1. 노션 PRD DB에 요구사항 작성
2. Cursor에서 `@prd-builder` 호출
3. PRD 내용을 컨텍스트로 받아서 코드 작성
4. 완료 후 `@dev-logger`로 로그 기록

## PRD DB 구조

| 속성 | 타입 | 설명 |
|------|------|------|
| 이름 | title | PRD 제목 |
| 상태 | select | 대기/진행중/완료/보류 |
| 우선순위 | select | 🔴높음/🟡중간/🟢낮음 |
| 설명 | rich_text | 상세 요구사항 |
| 생성일 | created_time | 자동 |

## Cursor Rules

`.cursor/rules/prd.mdc`에 규칙 추가:
```markdown
PRD를 참조할 때는 .cursor/skills/prd-builder/fetch.py를 실행해서
노션에서 최신 PRD를 가져온다.

진행중인 PRD를 우선적으로 처리한다.
```
