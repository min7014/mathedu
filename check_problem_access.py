#!/usr/bin/env python3
"""
check_problem_access.py — 특정 문제 외부 접근자 수 및 풀이 기록 실시간 조회 도구
(Real-Time Problem Access & Progress Analytics Tool)

사용법:
  python check_problem_access.py             # 전체 문항 접근자 통계 요약
  python check_problem_access.py c270901     # 특정 문항(c270901)의 상세 접근자 및 풀이 기록
  python check_problem_access.py --recent 10 # 최근 10건의 접근 기록
"""

import sys
import json
import urllib.request
from collections import Counter, defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SHEETS_API_URL = "https://script.google.com/macros/s/AKfycbxQBW1hKYFSHokaVJMRql-UJpk0t4qMeWMiiy_RFuCLZ5SE4iZytYQkGa9_yoCmm1Ak0Q/exec"

def fetch_access_data():
    try:
        req = urllib.request.Request(SHEETS_API_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8', errors='ignore'))
            return data.get('items', [])
    except Exception as e:
        print(f"❌ 데이터 조회 실패: {e}")
        return []

def main():
    args = sys.argv[1:]
    target_slug = None
    recent_n = None
    
    if args:
        if args[0] == '--recent':
            recent_n = int(args[1]) if len(args) > 1 else 10
        elif not args[0].startswith('-'):
            target_slug = args[0]

    print("📡 구글 스프레드시트 실시간 접근 기록 서버에 연결 중...")
    items = fetch_access_data()
    if not items:
        print("기록된 데이터가 없습니다.")
        return

    print(f"✅ 총 수집된 접근 및 풀이 로그: {len(items)}건\n")

    if target_slug:
        # 특정 문제 상세 조회
        matched = [it for it in items if it.get('quiz_slug') == target_slug]
        print(f"🎯 [{target_slug}] 문항 접근 기록 분석:")
        print(f"• 총 접근 횟수: {len(matched)}회")
        unique_users = set(it.get('student_name', '') for it in matched if it.get('student_name'))
        print(f"• 고유 접근자(학습자) 수: {len(unique_users)}명 ({', '.join(unique_users) if unique_users else '없음'})")
        print("\n[상세 접근 및 풀이 로그]:")
        for i, it in enumerate(matched, 1):
            print(f"  {i:02d}. [{it.get('updated_at', '')}] 사용자: '{it.get('student_name', '')}' | 진행: {it.get('current_step', 0)}/{it.get('total_steps', 0)}단계 | 정답수: {it.get('correct', 0)}")
    
    elif recent_n:
        print(f"⏱️ 최근 {recent_n}건의 접근 기록:")
        for i, it in enumerate(items[:recent_n], 1):
            print(f"  {i:02d}. [{it.get('updated_at', '')}] 문항: {it.get('quiz_slug', '')} | 사용자: '{it.get('student_name', '')}' | 진행: {it.get('current_step', 0)}/{it.get('total_steps', 0)}단계 | 정답: {it.get('correct', 0)}")

    else:
        # 전체 문항 요약
        slug_counts = Counter(it.get('quiz_slug', 'unknown') for it in items)
        slug_users = defaultdict(set)
        for it in items:
            name = it.get('student_name', '')
            if name:
                slug_users[it.get('quiz_slug', 'unknown')].add(name)

        print("📊 [문항별 외부 접근 및 학습자 집계]")
        print("-" * 65)
        print(f"{'문항 ID (quiz_slug)':<25} | {'기록 횟수':<10} | {'고유 학습자 수'}")
        print("-" * 65)
        for slug, cnt in slug_counts.most_common():
            users = slug_users[slug]
            user_sample = [str(u) for u in list(users)[:3]]
            print(f"{slug:<25} | {cnt:<10} | {len(users)}명 ({', '.join(user_sample)}{'...' if len(users) > 3 else ''})")

        print("-" * 65)
        print("\n💡 특정 문제를 상세히 확인하려면:")
        print("   python check_problem_access.py <문항ID> (예: python check_problem_access.py c270901)")

if __name__ == '__main__':
    main()
