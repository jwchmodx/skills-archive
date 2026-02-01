#!/usr/bin/env python3
"""
notion-connect: 프로젝트와 노션 연동 설정
"""
import os
import json
import requests

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2025-09-03"

def get_api_key():
    key_path = os.path.expanduser("~/.config/notion/api_key")
    if os.path.exists(key_path):
        with open(key_path) as f:
            return f.read().strip()
    raise FileNotFoundError("노션 API 키가 없습니다. ~/.config/notion/api_key 파일을 생성하세요.")

def notion_request(method, endpoint, data=None):
    headers = {
        "Authorization": f"Bearer {get_api_key()}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    url = f"{NOTION_API}{endpoint}"
    resp = requests.request(method, url, headers=headers, json=data)
    resp.raise_for_status()
    return resp.json()

def create_database(parent_page_id, title, properties):
    """노션에 새 데이터베이스 생성"""
    data = {
        "parent": {"page_id": parent_page_id},
        "title": [{"text": {"content": title}}],
        "properties": properties
    }
    result = notion_request("POST", "/databases", data)
    return result["id"]

def setup():
    print("🔗 notion-connect 설정\n")
    
    # 설정 디렉토리
    config_dir = ".notion"
    config_path = f"{config_dir}/config.json"
    
    # 기존 설정 확인
    if os.path.exists(config_path):
        with open(config_path) as f:
            existing = json.load(f)
        print(f"기존 설정 발견: {config_path}")
        print(json.dumps(existing, indent=2, ensure_ascii=False))
        if input("\n덮어쓸까요? (y/N): ").lower() != 'y':
            return
    
    # 프로젝트 페이지 ID
    print("\n노션 프로젝트 페이지 ID를 입력하세요.")
    print("(페이지 URL에서 마지막 32자리, 또는 대시 포함 UUID)")
    project_page_id = input("프로젝트 페이지 ID: ").strip()
    
    if not project_page_id:
        print("❌ 페이지 ID가 필요합니다.")
        return
    
    # 자동 DB 생성 여부
    auto_create = input("\nPRD/Dev Log DB를 자동 생성할까요? (Y/n): ").lower() != 'n'
    
    config = {"project_page_id": project_page_id}
    
    if auto_create:
        print("\n📦 PRD 데이터베이스 생성 중...")
        prd_props = {
            "이름": {"title": {}},
            "상태": {"select": {"options": [
                {"name": "대기", "color": "gray"},
                {"name": "진행중", "color": "blue"},
                {"name": "완료", "color": "green"},
                {"name": "보류", "color": "red"}
            ]}},
            "우선순위": {"select": {"options": [
                {"name": "🔴 높음", "color": "red"},
                {"name": "🟡 중간", "color": "yellow"},
                {"name": "🟢 낮음", "color": "green"}
            ]}},
            "설명": {"rich_text": {}},
            "생성일": {"created_time": {}}
        }
        config["prd_db_id"] = create_database(project_page_id, "📋 PRD", prd_props)
        print(f"  ✅ PRD DB: {config['prd_db_id']}")
        
        print("📝 Dev Log 데이터베이스 생성 중...")
        log_props = {
            "제목": {"title": {}},
            "날짜": {"date": {}},
            "타입": {"select": {"options": [
                {"name": "기능", "color": "blue"},
                {"name": "버그", "color": "red"},
                {"name": "리팩토링", "color": "purple"},
                {"name": "문서", "color": "gray"}
            ]}},
            "내용": {"rich_text": {}},
            "관련 PRD": {"relation": {"database_id": config["prd_db_id"]}}
        }
        config["dev_log_db_id"] = create_database(project_page_id, "📝 Dev Log", log_props)
        print(f"  ✅ Dev Log DB: {config['dev_log_db_id']}")
    else:
        config["prd_db_id"] = input("PRD DB ID: ").strip()
        config["dev_log_db_id"] = input("Dev Log DB ID: ").strip()
    
    # 저장
    os.makedirs(config_dir, exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 설정 완료! {config_path}")
    print(json.dumps(config, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    setup()
