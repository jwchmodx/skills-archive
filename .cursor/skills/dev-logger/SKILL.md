# dev-logger

개발 로그를 **prd-builder로 fetch한 그 페이지**(또는 프로젝트 페이지) **안에 서브페이지**로 기록하는 스킬.

## 사전 조건

- `notion-connect` 스킬로 `.notion/config.json`에 **project_page_id**(, tasks_db_id) 설정 완료

## 사용법

### CLI로 로그 기록

```bash
# 프로젝트 페이지 안에 서브페이지로 로그 생성
python .cursor/skills/dev-logger/log.py "로그인 기능 구현"

# 타입 지정
python .cursor/skills/dev-logger/log.py "로그인 기능 구현" --type 기능

# 상세 내용 포함
python .cursor/skills/dev-logger/log.py "버그 수정" --type 버그 --content "null 체크 누락 수정"

# 특정 PRD 페이지 안에 서브페이지로 로그 생성 (prd-builder fetch한 그 페이지)
python .cursor/skills/dev-logger/log.py "API 구현" --prd "PRD-페이지-ID"
```

### 로그 목록

```bash
# 프로젝트 페이지 하위 서브페이지(로그) 목록
python .cursor/skills/dev-logger/log.py --list

# 특정 PRD 페이지 하위 로그 목록
python .cursor/skills/dev-logger/log.py --list --prd "PRD-페이지-ID"
```

### Cursor에서 사용

작업 완료 후 채팅에서:
```
@dev-logger 방금 작업한 내용 기록해줘
- 제목: 로그인 API 구현
- 타입: 기능
- 내용: JWT 기반 인증 구현
```

## 로그 저장 위치

- **--prd 없음**: `.notion/config.json`의 **project_page_id** 페이지 안에 **서브페이지**로 생성.
- **--prd 지정**: 해당 **PRD 페이지**(prd-builder fetch한 그 페이지) 안에 **서브페이지**로 생성.

각 로그는 한 개의 서브페이지이며, 본문에 `[날짜] [타입] 제목`과 상세 내용(선택)이 블록으로 들어간다.

## 자동 로깅 (선택)

git commit hook으로 자동 로깅:
```bash
# .git/hooks/post-commit
python .cursor/skills/dev-logger/log.py "$(git log -1 --pretty=%B)" --type 기능
```
