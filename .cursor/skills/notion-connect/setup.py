#!/usr/bin/env python3
"""
notion-connect: 프로젝트와 노션 연동 설정 (수동)
"""
import os
import json
import re

def extract_id_from_url(url):
    """노션 URL에서 ID 추출"""
    # 패턴 1: notion.so/페이지이름-32자리ID
    # 패턴 2: notion.so/32자리ID?v=...
    # 패턴 3: notion.so/workspace/32자리ID
    
    # 32자리 hex (대시 없이)
    match = re.search(r'([a-f0-9]{32})', url.replace('-', ''))
    if match:
        raw_id = match.group(1)
        # UUID 형식으로 변환 (8-4-4-4-12)
        return f"{raw_id[:8]}-{raw_id[8:12]}-{raw_id[12:16]}-{raw_id[16:20]}-{raw_id[20:]}"
    
    return None

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
    
    print("노션에서 각 DB/페이지의 링크를 복사해서 붙여넣으세요.\n")
    
    # PRD DB URL
    prd_url = input("📋 PRD DB URL: ").strip()
    prd_id = extract_id_from_url(prd_url)
    if not prd_id:
        print("❌ PRD URL에서 ID를 찾을 수 없습니다.")
        return
    print(f"   → ID: {prd_id}")
    
    # Dev Log DB URL
    log_url = input("📝 Dev Log DB URL: ").strip()
    log_id = extract_id_from_url(log_url)
    if not log_id:
        print("❌ Dev Log URL에서 ID를 찾을 수 없습니다.")
        return
    print(f"   → ID: {log_id}")
    
    config = {
        "prd_db_id": prd_id,
        "dev_log_db_id": log_id
    }
    
    # 저장
    os.makedirs(config_dir, exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 설정 완료! {config_path}")
    print(json.dumps(config, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    setup()
