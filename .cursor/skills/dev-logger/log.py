#!/usr/bin/env python3
"""
dev-logger: 개발 로그를 prd-builder fetch한 페이지(또는 프로젝트 페이지) 안에 서브페이지로 기록
"""
import os
import json
import requests
import argparse
from datetime import datetime

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
        "Content-Type": "application/json",
    }
    url = f"{NOTION_API}{endpoint}"
    resp = requests.request(method, url, headers=headers, json=data)
    resp.raise_for_status()
    return resp.json()


def _parent_page_id(config, prd_id=None):
    """로그를 넣을 부모 페이지: --prd가 있으면 그 PRD 페이지, 없으면 프로젝트 페이지."""
    if prd_id:
        return prd_id
    pid = config.get("project_page_id")
    if not pid:
        raise KeyError(
            "config에 project_page_id가 없습니다. notion-connect로 프로젝트 페이지를 설정하세요."
        )
    return pid


def create_log(title, log_type="기능", content="", prd_id=None):
    """부모 페이지(PRD 페이지 또는 프로젝트 페이지) 안에 서브페이지로 로그 생성."""
    config = get_config()
    parent_id = _parent_page_id(config, prd_id)

    # 서브페이지 생성 (제목만)
    data = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]},
        },
    }
    page = notion_request("POST", "/pages", data)
    new_page_id = page["id"]

    # 본문에 날짜·타입·내용 블록 추가
    date_str = datetime.now().strftime("%Y-%m-%d")
    meta_line = f"[{date_str}] [{log_type}] {title}"
    children = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": meta_line}}],
            },
        },
    ]
    if content:
        children.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": content}}],
                },
            }
        )
    notion_request("PATCH", f"/blocks/{new_page_id}/children", {"children": children})

    return new_page_id


def list_logs(limit=10, prd_id=None):
    """부모 페이지(프로젝트 또는 PRD) 하위 서브페이지(로그) 목록."""
    config = get_config()
    parent_id = _parent_page_id(config, prd_id)

    result = notion_request("GET", f"/blocks/{parent_id}/children")
    logs = []
    for block in result.get("results", []):
        if block.get("type") != "child_page":
            continue
        cp = block.get("child_page") or {}
        title = cp.get("title") or "(제목 없음)"
        logs.append({"id": block["id"], "제목": title})
        if len(logs) >= limit:
            break
    return logs


def print_logs(logs):
    if not logs:
        print("📝 로그가 없습니다.")
        return
    print(f"📝 개발 로그 ({len(logs)}개)\n")
    for log in logs:
        print(f"  • {log['제목']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="개발 로그 기록 (서브페이지)")
    parser.add_argument("title", nargs="?", help="로그 제목")
    parser.add_argument(
        "--type", "-t", default="기능",
        choices=["기능", "버그", "리팩토링", "문서"],
        help="로그 타입",
    )
    parser.add_argument("--content", "-c", default="", help="상세 내용")
    parser.add_argument(
        "--prd", "-p", default=None,
        help="관련 PRD 페이지 ID (지정하면 해당 페이지 안에 서브페이지로 생성)",
    )
    parser.add_argument("--list", "-l", action="store_true", help="로그 목록 (서브페이지)")
    parser.add_argument("--limit", default=10, type=int, help="목록 개수 (기본 10)")

    args = parser.parse_args()

    if args.list:
        logs = list_logs(limit=args.limit, prd_id=args.prd)
        print_logs(logs)
    elif args.title:
        log_id = create_log(args.title, args.type, args.content, args.prd)
        print(f"✅ 로그 기록됨: {args.title}")
        print(f"   ID: {log_id}")
    else:
        parser.print_help()
