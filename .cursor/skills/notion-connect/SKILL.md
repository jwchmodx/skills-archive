# notion-connect

노션 프로젝트 페이지와 연동하는 스킬.

## 사용법

### 1. 초기 설정 (프로젝트당 1회)

```bash
# 프로젝트 루트에서
python .cursor/skills/notion-connect/setup.py
```

또는 수동으로 `.notion/config.json` 생성:

```json
{
  "project_page_id": "프로젝트-페이지-ID",
  "prd_db_id": "PRD-DB-ID",
  "dev_log_db_id": "개발로그-DB-ID"
}
```

### 2. 노션 페이지 ID 찾는 법

1. 노션에서 페이지 열기
2. 우측 상단 ⋯ → "링크 복사"
3. URL에서 ID 추출: `notion.so/페이지이름-{32자리ID}`

### 3. 자동 DB 생성

`setup.py` 실행하면:
- 프로젝트 페이지 아래에 **PRD DB** 자동 생성
- 프로젝트 페이지 아래에 **Dev Log DB** 자동 생성
- `.notion/config.json`에 ID 저장

## 필요 조건

- `~/.config/notion/api_key` 파일에 노션 API 키
- 노션 인테그레이션이 프로젝트 페이지에 연결되어 있어야 함

## 관련 스킬

- `prd-builder`: PRD DB에서 요구사항 읽어서 빌드
- `dev-logger`: 개발 로그를 Dev Log DB에 기록
