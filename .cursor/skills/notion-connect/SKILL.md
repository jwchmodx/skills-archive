# notion-connect

프로젝트 페이지 1개 + 그 안의 작업 DB와 연동하는 스킬.

## 사용법

### 실행

```bash
python .cursor/skills/notion-connect/setup.py
```

프로젝트 루트에서 실행. 선택지:

1. **새 작업 DB 생성** — 프로젝트 페이지 URL 1개 입력 → 템플릿 양식으로 작업 DB 자동 생성 후 `.notion/config.json` 연동
2. **기존 작업 DB 연동** — 프로젝트 페이지 URL 또는 작업 DB URL 1개 입력 → `.notion/config.json` 연동

### 예시 (새 작업 DB 생성)

```
1) 새 작업 DB 생성 — 프로젝트 페이지 URL 1개 입력 후 템플릿 양식으로 작업 DB 자동 생성
2) 기존 작업 DB 연동 — 프로젝트 페이지 URL 또는 작업 DB URL 1개 입력
선택 (1 또는 2): 1

프로젝트 페이지 URL: https://notion.so/My-Project-abc123...
   템플릿에서 작업 DB 스키마 가져오는 중...
   작업 DB 생성 중...

✅ 연동 완료: .notion/config.json
```

### 예시 (기존 작업 DB 연동)

```
선택 (1 또는 2): 2

URL: https://notion.so/My-Project-abc123...
   (해당 페이지의 작업 DB를 찾거나, 작업 DB URL이면 부모 페이지와 함께 저장)

✅ 연동 완료: .notion/config.json
```

### 수동 설정 (선택)

`.notion/config.json` 직접 생성:

```json
{
  "project_page_id": "프로젝트-페이지-UUID",
  "tasks_db_id": "작업-DB-UUID"
}
```

## 필요 조건

- `~/.config/notion/api_key` 파일에 노션 API 키
- **새 작업 DB 생성** 시: 인테그레이션이 프로젝트 페이지·템플릿 페이지(PRD)에 연결·접근 가능해야 함
- **기존 작업 DB 연동** 시: 인테그레이션이 해당 페이지 또는 작업 DB에 연결되어 있어야 함

## 관련 스킬

- `prd-builder`: 작업 DB에서 요구사항(PRD) 가져오기
