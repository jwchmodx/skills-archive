#!/usr/bin/env python3
"""
notion-connect: 프로젝트 페이지 1개 + 그 안의 작업 DB 연동
"""
import os
import json
import re
import sys
import urllib.request
import urllib.error

NOTION_VERSION = "2022-06-28"
NOTION_BASE = "https://api.notion.com"
API_KEY_PATH = os.path.expanduser("~/.config/notion/api_key")
CONFIG_DIR = ".notion"
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
TEMPLATE_PAGE_ID = "2fa9589f-b79f-8096-be44-c3b5741ec9d1"


def load_api_key():
    if not os.path.exists(API_KEY_PATH):
        print(f"❌ API 키 없음: {API_KEY_PATH}")
        print("   노션 인테그레이션에서 API 키를 발급해 저장하세요.")
        return None
    with open(API_KEY_PATH) as f:
        return f.read().strip()


def extract_id_from_url(url):
    match = re.search(r"([a-f0-9]{32})", url.replace("-", ""))
    if match:
        raw = match.group(1)
        return f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"
    return None


def notion_request(api_key, method, path, data=None):
    url = NOTION_BASE + path
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"❌ Notion API 오류 ({e.code}): {err_body}")
        return None


def get_template_tasks_schema(api_key):
    """템플릿 페이지에서 작업 DB 스키마(properties) 복사."""
    # 블록 자식 목록
    blocks = notion_request(
        api_key, "GET", f"/v1/blocks/{TEMPLATE_PAGE_ID}/children"
    )
    if not blocks or "results" not in blocks:
        return None
    # child_database 블록 찾기 (제목 "작업" 우선, 없으면 첫 번째)
    db_block_id = None
    for b in blocks["results"]:
        if b.get("type") != "child_database":
            continue
        title = (b.get("child_database") or {}).get("title") or ""
        if title.strip() == "작업":
            db_block_id = b["id"]
            break
        if db_block_id is None:
            db_block_id = b["id"]
    if not db_block_id:
        return None
    # DB 조회 후 properties만 생성용 형태로 변환
    db = notion_request(api_key, "GET", f"/v1/databases/{db_block_id}")
    if not db or "properties" not in db:
        return None
    props = db["properties"]
    create_props = {}
    for name, val in props.items():
        ptype = val.get("type")
        if not ptype:
            continue
        inner = val.get(ptype)
        if inner is None:
            inner = {}
        create_props[name] = {ptype: inner}
    return create_props if create_props else None


def create_database(api_key, parent_page_id, title, properties=None):
    if properties is None:
        properties = {"Name": {"title": {}}}
    data = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": properties,
    }
    res = notion_request(api_key, "POST", "/v1/databases", data)
    return res.get("id") if res else None


def save_config(project_page_id, tasks_db_id):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    config = {"project_page_id": project_page_id, "tasks_db_id": tasks_db_id}
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"\n✅ 연동 완료: {CONFIG_PATH}")
    print(json.dumps(config, indent=2, ensure_ascii=False))


def mode_create(api_key):
    print("\n📋 프로젝트 페이지 URL을 입력하세요 (이 페이지 안에 '작업' DB가 생성됩니다).")
    page_url = input("프로젝트 페이지 URL: ").strip()
    project_page_id = extract_id_from_url(page_url)
    if not project_page_id:
        print("❌ URL에서 페이지 ID를 찾을 수 없습니다.")
        return False
    print("   템플릿에서 작업 DB 스키마 가져오는 중...")
    schema = get_template_tasks_schema(api_key)
    if not schema:
        print("   (템플릿 접근 불가 또는 작업 DB 없음 → 기본 스키마로 생성)")
        schema = {"Name": {"title": {}}}
    print("   작업 DB 생성 중...")
    tasks_db_id = create_database(api_key, project_page_id, "작업", schema)
    if not tasks_db_id:
        return False
    save_config(project_page_id, tasks_db_id)
    return True


def mode_existing(api_key):
    print("\n📋 프로젝트 페이지 URL 또는 작업 DB URL 1개를 입력하세요.")
    url = input("URL: ").strip()
    raw_id = extract_id_from_url(url)
    if not raw_id:
        print("❌ URL에서 ID를 찾을 수 없습니다.")
        return False
    # 페이지 자식 블록으로 시도 → child_database 있으면 작업 DB로 사용
    blocks = notion_request(api_key, "GET", f"/v1/blocks/{raw_id}/children")
    if blocks and blocks.get("results"):
        for b in blocks["results"]:
            if b.get("type") == "child_database":
                tasks_db_id = b["id"]
                save_config(raw_id, tasks_db_id)
                return True
    # DB로 조회 시도 → parent가 page면 project_page_id 사용
    db = notion_request(api_key, "GET", f"/v1/databases/{raw_id}")
    if db and db.get("object") == "database":
        parent = db.get("parent") or {}
        if parent.get("type") == "page_id":
            project_page_id = parent.get("page_id")
            if project_page_id:
                save_config(project_page_id, raw_id)
                return True
        print("❌ 해당 DB의 부모가 페이지가 아닙니다.")
        return False
    print("❌ 프로젝트 페이지 또는 작업 DB URL을 입력해 주세요.")
    return False


def setup():
    print("🔗 notion-connect\n")
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            existing = json.load(f)
        print(f"기존 설정: {CONFIG_PATH}")
        print(json.dumps(existing, indent=2, ensure_ascii=False))
        if "prd_db_id" in existing or "dev_log_db_id" in existing:
            print("\n기존 설정(prd_db_id 등)이 있습니다. 프로젝트 페이지 URL을 입력하면 새 형식(project_page_id, tasks_db_id)으로 바꿉니다.")
        if input("\n덮어쓸까요? (y/N): ").lower() != "y":
            return

    print("1) 새 작업 DB 생성 — 프로젝트 페이지 URL 1개 입력 후 템플릿 양식으로 작업 DB 자동 생성")
    print("2) 기존 작업 DB 연동 — 프로젝트 페이지 URL 또는 작업 DB URL 1개 입력")
    choice = input("선택 (1 또는 2): ").strip() or "1"

    api_key = load_api_key()
    if not api_key:
        sys.exit(1)
    if choice == "1":
        if not mode_create(api_key):
            sys.exit(1)
    else:
        if not mode_existing(api_key):
            sys.exit(1)


if __name__ == "__main__":
    setup()
