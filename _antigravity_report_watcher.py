#!/usr/bin/env python3
"""
mathedu 안티그래비티 전용 실시간 신고 감시 데몬 (Antigravity Realtime Watcher)
Google Sheets를 15초 주기로 폴링하여 신규 신고 발생 시
안티그래비티(Google DeepMind AI 에이전트)를 즉각 깨워(Reactive Wakeup)
안티그래비티의 최고급 추론 자원으로 문제를 직접 분석하고 실시간 수정하게 합니다.
"""
import time, json, os, sys, urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_FILE = os.path.join(REPO_DIR, '_processed_reports.json')
API_URL_FILE = os.path.join(REPO_DIR, 'progress-api-url.txt')

def get_sheets_url():
    if os.path.exists(API_URL_FILE):
        try:
            with open(API_URL_FILE, encoding='utf-8') as f:
                url = f.read().strip()
                if url.startswith('http'):
                    return url
        except:
            pass
    return 'https://script.google.com/macros/s/AKfycbxQBW1hKYFSHokaVJMRql-UJpk0t4qMeWMiiy_RFuCLZ5SE4iZytYQkGa9_yoCmm1Ak0Q/exec'

def load_processed():
    try:
        with open(PROCESSED_FILE, encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"processed": []}

def check_reports():
    sheets_url = get_sheets_url()
    try:
        req = urllib.request.Request(f'{sheets_url}?action=reports')
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode('utf-8'))
        reports = data.get('reports', [])
    except Exception as e:
        return []

    processed = load_processed()
    processed_items = processed.get('processed', [])

    new_reports = []
    for r in reports:
        ts = r.get('timestamp', '')
        qs = r.get('quiz_slug', '')
        qn = str(r.get('question_num', ''))

        if r.get('fix_timestamp'):
            continue

        already = any(
            p.get('timestamp') == ts and p.get('quiz_slug') == qs and str(p.get('question_num')) == qn
            and p.get('status') in ['fixed', 'resolved']
            for p in processed_items
        )
        if not already:
            new_reports.append(r)
    return new_reports

def main():
    print("[ANTIGRAVITY_WATCHER_ONLINE] 안티그래비티 실시간 신고 감시 데몬 가동 중 (폴링 간격: 15초)", flush=True)
    while True:
        try:
            new_reports = check_reports()
            if new_reports:
                print(f"\n🚨 [ANTIGRAVITY_TRIGGER] 신규 신고 {len(new_reports)}건 감지!", flush=True)
                for r in new_reports:
                    print(json.dumps(r, ensure_ascii=False), flush=True)
                print("\n안티그래비티 에이전트님, 위 신고 건을 직접 심층 분석하여 board/{quiz_slug}.html 수식 수정 및 배포를 진행하세요!\n", flush=True)
        except Exception:
            pass
        time.sleep(15)

if __name__ == '__main__':
    main()
