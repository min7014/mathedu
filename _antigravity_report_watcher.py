#!/usr/bin/env python3
"""
mathedu 안티그래비티 전용 실시간 신고 및 문제출제 감시 데몬 (Antigravity Realtime Watcher)
Google Sheets를 15초 주기로 폴링하여:
1. 신규 문제 출제 요청(_request_new) 감지 시: 
   AI 자동 퀴즈 빌더를 실행하여 5~8단계 인터랙티브 퀴즈 자동 제작, index.json 등록 및 Git 배포
2. 기존 문항 오류 신고 감지 시:
   안티그래비티 에이전트를 즉각 깨워(Reactive Wakeup) 실시간 수리 및 배포 진행
"""
import time, json, os, sys, urllib.request, subprocess

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

def save_processed(data):
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def post_fix_report(timestamp, quiz_slug, question_num, result):
    sheets_url = get_sheets_url()
    try:
        fix_data = json.dumps({
            'action': 'fix_report',
            'timestamp': timestamp,
            'quiz_slug': quiz_slug,
            'question_num': str(question_num),
            'result': result
        }).encode('utf-8')
        req = urllib.request.Request(
            sheets_url, data=fix_data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        resp = urllib.request.urlopen(req, timeout=15)
        resp.read()
        return True
    except Exception:
        return False

def check_reports():
    sheets_url = get_sheets_url()
    try:
        req = urllib.request.Request(f'{sheets_url}?action=reports')
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode('utf-8'))
        reports = data.get('reports', [])
    except Exception:
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

def handle_new_quiz_request(r):
    """신규 퀴즈 출제 요청을 처리합니다."""
    ts = r.get('timestamp', '')
    qn = str(r.get('question_num', '0'))
    reporter = r.get('reporter', '선생님')
    text = r.get('text', '')
    
    print(f"\n✨ [AI_BUILDER] 신규 퀴즈 생성 요청 처리 시작 (신청자: {reporter})", flush=True)
    try:
        from _auto_quiz_builder import parse_request_text, create_and_publish_quiz
        title, content, hint = parse_request_text(text)
        slug, quiz_url = create_and_publish_quiz(title, content, hint, reporter)
        
        # 구글 시트에 처리 완료 기록
        post_fix_report(ts, '_request_new', qn, f'✅ 생성완료: {quiz_url}')
        
        proc = load_processed()
        proc['processed'].append({
            'timestamp': ts,
            'quiz_slug': '_request_new',
            'question_num': qn,
            'status': 'fixed',
            'fix': f"신규 퀴즈 자동 생성 ({title}) → {quiz_url}"
        })
        save_processed(proc)
        print(f"✨ [AI_BUILDER] 신규 퀴즈 배포 완료: {quiz_url}\n", flush=True)
        return True
    except Exception as e:
        print(f"⚠️ [AI_BUILDER] 퀴즈 생성 중 오류 발생: {e}", flush=True)
        return False

def main():
    print("[ANTIGRAVITY_WATCHER_ONLINE] 안티그래비티 실시간 감시 데몬 (신고 수리 + 신규 퀴즈 자동 생성) 가동 중 (15초 주기)", flush=True)
    while True:
        try:
            new_reports = check_reports()
            if new_reports:
                for r in new_reports:
                    qs = r.get('quiz_slug', '')
                    if qs == '_request_new':
                        # 신규 퀴즈 자동 생성
                        handle_new_quiz_request(r)
                    else:
                        # 기존 퀴즈 수리 요청 트리거
                        print(f"\n🚨 [ANTIGRAVITY_TRIGGER] 신규 신고 감지!", flush=True)
                        print(json.dumps(r, ensure_ascii=False), flush=True)
                        print("\n안티그래비티 에이전트님, 위 신고 건을 직접 심층 분석하여 board/{quiz_slug}.html 수식 수정 및 배포를 진행하세요!\n", flush=True)
        except Exception:
            pass
        time.sleep(15)

if __name__ == '__main__':
    main()
