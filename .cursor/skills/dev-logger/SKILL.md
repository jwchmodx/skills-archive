# dev-logger

개발 로그를 노션 Dev Log DB에 기록하는 스킬.

## 사전 조건

- `notion-connect` 스킬로 `.notion/config.json` 설정 완료

## 사용법

### CLI로 로그 기록

```bash
# 기본 로그
python .cursor/skills/dev-logger/log.py "로그인 기능 구현"

# 타입 지정
python .cursor/skills/dev-logger/log.py "로그인 기능 구현" --type 기능

# 상세 내용 포함
python .cursor/skills/dev-logger/log.py "버그 수정" --type 버그 --content "null 체크 누락 수정"

# PRD 연결
python .cursor/skills/dev-logger/log.py "API 구현" --prd "PRD-페이지-ID"
```

### Cursor에서 사용

작업 완료 후 채팅에서:
```
@dev-logger 방금 작업한 내용 기록해줘
- 제목: 로그인 API 구현
- 타입: 기능
- 내용: JWT 기반 인증 구현
```

## Dev Log DB 구조

| 속성 | 타입 | 설명 |
|------|------|------|
| 제목 | title | 로그 제목 |
| 날짜 | date | 작업 날짜 |
| 타입 | select | 기능/버그/리팩토링/문서 |
| 내용 | rich_text | 상세 내용 |
| 관련 PRD | relation | PRD DB 연결 |

## 자동 로깅 (선택)

git commit hook으로 자동 로깅:
```bash
# .git/hooks/post-commit
python .cursor/skills/dev-logger/log.py "$(git log -1 --pretty=%B)" --type 기능
```
