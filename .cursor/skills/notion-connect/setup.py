#!/usr/bin/env python3
"""
notion-connect: 프로젝트와 노션 연동 설정
"""
import os
import json
import re

def extract_id_from_url(url):
    """노션 URL에서 ID 추출"""
    match = re.search(r'([a-f0-9]{32})', url.replace('-', ''))
    if match:
        raw_id = match.group(1)
        return f"{raw_id[:8]}-{raw_id[8:12]}-{raw_id[12:16]}-{raw_id[16:20]}-{raw_id[20:]}"
    return None

def setup():
    prd_url = input("PRD DB URL: ").strip()
    prd_id = extract_id_from_url(prd_url)
    if not prd_id:
        print("❌ URL에서 ID를 찾을 수 없음")
        return
    
    log_url = input("Dev Log DB URL: ").strip()
    log_id = extract_id_from_url(log_url)
    if not log_id:
        print("❌ URL에서 ID를 찾을 수 없음")
        return
    
    config = {
        "prd_db_id": prd_id,
        "dev_log_db_id": log_id
    }
    
    os.makedirs(".notion", exist_ok=True)
    with open(".notion/config.json", 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ 완료")

if __name__ == "__main__":
    setup()
