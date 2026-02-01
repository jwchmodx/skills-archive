# notion-connect

노션 PRD/Dev Log DB와 연동하는 스킬.

## 사용법

### 1. 노션에서 DB 만들기

프로젝트 페이지 아래에 두 DB 생성:
- **📋 PRD** - 요구사항 관리
- **📝 Dev Log** - 개발 로그

### 2. 연동 설정

```bash
python .cursor/skills/notion-connect/setup.py
```

URL 붙여넣기만 하면 자동으로 ID 추출:
```
📋 PRD DB URL: https://notion.so/PRD-abc123...
   → ID: abc123-...
📝 Dev Log DB URL: https://notion.so/Dev-Log-def456...
   → ID: def456-...

✅ 설정 완료! .notion/config.json
```

### 3. 수동 설정 (선택)

`.notion/config.json` 직접 생성:
```json
{
  "prd_db_id": "PRD-DB-ID",
  "dev_log_db_id": "Dev-Log-DB-ID"
}
```

## 필요 조건

- `~/.config/notion/api_key` 파일에 노션 API 키
- 노션 인테그레이션이 두 DB에 연결되어 있어야 함

## 관련 스킬

- `prd-builder`: PRD DB에서 요구사항 읽기
- `dev-logger`: Dev Log DB에 로그 기록
