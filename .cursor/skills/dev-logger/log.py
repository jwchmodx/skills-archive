#!/usr/bin/env python3
"""
dev-logger: 개발 로그를 노션 Dev Log DB에 기록
"""
import os
import json
import requests
import argparse
from datetime import datetime

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2025-09-03"

def get_api_key():
    key_path = os.path.expanduser("~/.config/notion/api_key")
    with open(key_path) as f:
        return f.read().strip()

def get_config():
    config_path = ".notion/config.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError("설정 파일이 없습니다. notion-connect 스킬을 먼저 실행하세요.")
    with open(config_path) as f:
        return json.load(f)

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

def create_log(title, log_type="기능", content="", prd_id=None):
    """Dev Log DB에 새 로그 생성"""
    config = get_config()
    db_id = config["dev_log_db_id"]
    
    properties = {
        "제목": {"title": [{"text": {"content": title}}]},
        "날짜": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
        "타입": {"select": {"name": log_type}}
    }
    
    if content:
        properties["내용"] = {"rich_text": [{"text": {"content": content}}]}
    
    if prd_id:
        properties["관련 PRD"] = {"relation": [{"id": prd_id}]}
    
    data = {
        "parent": {"database_id": db_id},
        "properties": properties
    }
    
    result = notion_request("POST", "/pages", data)
    return result["id"]

def list_logs(limit=10):
    """최근 로그 목록"""
    config = get_config()
    db_id = config["dev_log_db_id"]
    
    query = {
        "sorts": [{"property": "날짜", "direction": "descending"}],
        "page_size": limit
    }
    
    result = notion_request("POST", f"/databases/{db_id}/query", query)
    
    logs = []
    for page in result.get("results", []):
        props = page["properties"]
        
        title = ""
        if props.get("제목", {}).get("title"):
            title = props["제목"]["title"][0]["plain_text"]
        
        date = props.get("날짜", {}).get("date", {})
        date_str = date.get("start", "") if date else ""
        
        log_type = props.get("타입", {}).get("select", {})
        type_name = log_type.get("name", "") if log_type else ""
        
        logs.append({
            "날짜": date_str,
            "타입": type_name,
            "제목": title
        })
    
    return logs

def print_logs(logs):
    """로그 목록 출력"""
    if not logs:
        print("📝 로그가 없습니다.")
        return
    
    print(f"📝 최근 개발 로그 ({len(logs)}개)\n")
    for log in logs:
        print(f"[{log['날짜']}] [{log['타입']}] {log['제목']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="개발 로그 기록")
    parser.add_argument("title", nargs="?", help="로그 제목")
    parser.add_argument("--type", "-t", default="기능", 
                        choices=["기능", "버그", "리팩토링", "문서"],
                        help="로그 타입")
    parser.add_argument("--content", "-c", default="", help="상세 내용")
    parser.add_argument("--prd", "-p", default=None, help="관련 PRD 페이지 ID")
    parser.add_argument("--list", "-l", action="store_true", help="최근 로그 목록")
    
    args = parser.parse_args()
    
    if args.list:
        logs = list_logs()
        print_logs(logs)
    elif args.title:
        log_id = create_log(args.title, args.type, args.content, args.prd)
        print(f"✅ 로그 기록됨: {args.title}")
        print(f"   ID: {log_id}")
    else:
        parser.print_help()
