#!/usr/bin/env python3
"""
prd-builder: 노션 PRD DB에서 요구사항 가져오기
"""
import os
import json
import requests
import sys

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

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

def fetch_prds(status_filter=None):
    """작업 DB에서 PRD(요구사항) 목록 가져오기"""
    config = get_config()
    db_id = config.get("tasks_db_id") or config.get("prd_db_id")
    if not db_id:
        raise KeyError("설정에 tasks_db_id 또는 prd_db_id가 없습니다. notion-connect로 project_page_id, tasks_db_id를 설정하세요.")

    # 정렬: created_time 사용 (생성일 속성 없어도 동작)
    query = {"sorts": [{"timestamp": "created_time", "direction": "descending"}]}
    if status_filter:
        query["filter"] = {"property": "상태", "select": {"equals": status_filter}}

    result = notion_request("POST", f"/databases/{db_id}/query", query)

    prds = []
    for page in result.get("results", []):
        props = page["properties"]

        # 속성 추출 (이름/Name, 설명/내용 등 폴백)
        name = ""
        for key in ("이름", "Name"):
            if props.get(key, {}).get("title"):
                name = props[key]["title"][0]["plain_text"]
                break
        status = props.get("상태", {}).get("select", {})
        status_name = status.get("name", "없음") if status else "없음"
        priority = props.get("우선순위", {}).get("select", {})
        priority_name = priority.get("name", "없음") if priority else "없음"
        desc = ""
        for key in ("설명", "내용", "Description"):
            if props.get(key, {}).get("rich_text"):
                desc = props[key]["rich_text"][0]["plain_text"]
                break
        
        prds.append({
            "id": page["id"],
            "이름": name,
            "상태": status_name,
            "우선순위": priority_name,
            "설명": desc[:200] + "..." if len(desc) > 200 else desc
        })
    
    return prds

def print_prds(prds):
    """PRD 목록 출력"""
    if not prds:
        print("📋 PRD가 없습니다.")
        return
    
    print(f"📋 PRD 목록 ({len(prds)}개)\n")
    for prd in prds:
        print(f"[{prd['상태']}] {prd['우선순위']} {prd['이름']}")
        if prd['설명']:
            print(f"    {prd['설명']}")
        print()

def get_prd_detail(prd_id):
    """PRD 상세 내용 (페이지 블록 포함)"""
    # 페이지 속성
    page = notion_request("GET", f"/pages/{prd_id}")
    
    # 페이지 내용 (블록)
    blocks = notion_request("GET", f"/blocks/{prd_id}/children")
    
    content = []
    for block in blocks.get("results", []):
        block_type = block["type"]
        if block_type == "paragraph":
            texts = block["paragraph"].get("rich_text", [])
            if texts:
                content.append(texts[0]["plain_text"])
        elif block_type == "heading_1":
            texts = block["heading_1"].get("rich_text", [])
            if texts:
                content.append(f"# {texts[0]['plain_text']}")
        elif block_type == "heading_2":
            texts = block["heading_2"].get("rich_text", [])
            if texts:
                content.append(f"## {texts[0]['plain_text']}")
        elif block_type == "bulleted_list_item":
            texts = block["bulleted_list_item"].get("rich_text", [])
            if texts:
                content.append(f"• {texts[0]['plain_text']}")
    
    return "\n".join(content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "진행중":
            prds = fetch_prds("진행중")
        elif sys.argv[1] == "대기":
            prds = fetch_prds("대기")
        elif sys.argv[1] == "detail" and len(sys.argv) > 2:
            print(get_prd_detail(sys.argv[2]))
            sys.exit(0)
        else:
            prds = fetch_prds()
    else:
        prds = fetch_prds()
    
    print_prds(prds)
