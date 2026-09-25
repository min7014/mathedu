#!/usr/bin/env python3
"""
mathedu 신고 자동 수정 스크립트 (no_agent 크론잡용)
stdout에 결과를 출력하면 크론잡이 자동으로 배포합니다.
"""
import json, os, re, sys, urllib.request
from datetime import datetime, timezone

SHEETS_URL = 'https://script.google.com/macros/s/AKfycbyKFvMp5odSgfBYd3eDjd-ueGnvcudXifd6aePX6D_cZ3IW7QrEa2qFKMBAUurphDQ9Mw/exec'
BOARD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'board')
PROCESSED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_processed_reports.json')

def load_processed():
    try:
        with open(PROCESSED_FILE, encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"processed": []}

def save_processed(data):
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_reports():
    try:
        req = urllib.request.Request(f'{SHEETS_URL}?action=reports')
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read())
        return data.get('reports', [])
    except Exception as e:
        print(f"신고 목록 가져오기 실패: {e}")
        return []

def post_fix_report(timestamp, quiz_slug, question_num, result):
    try:
        fix_data = json.dumps({
            'action': 'fix_report',
            'timestamp': timestamp,
            'quiz_slug': quiz_slug,
            'question_num': str(question_num),
            'result': result
        }).encode('utf-8')
        req = urllib.request.Request(
            SHEETS_URL, data=fix_data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        resp = urllib.request.urlopen(req, timeout=15)
        resp.read()
        return True
    except Exception as e:
        print(f"  fix_report 전송 실패: {e}")
        return False

def fix_html(report):
    """신고 내용을 분석하여 HTML을 수정합니다. (수동 패턴 매칭)"""
    quiz_slug = report.get('quiz_slug', '')
    text = report.get('text', '').strip()
    q_num = report.get('question_num', '')
    
    if not quiz_slug:
        return None, "quiz_slug 없음"
    
    html_path = os.path.join(BOARD_DIR, f'{quiz_slug}.html')
    if not os.path.exists(html_path):
        return None, f"파일 없음: {html_path}"
    
    with open(html_path, encoding='utf-8') as f:
        html = f.read()
    
    original = html
    fixes = []
    
    # 패턴 1: "정답입니다" 관련 신고
    if '정답입니다' in text or '정답' in text:
        # 이미 수정되었는지 확인
        if '✅ 정답입니다!' in html:
            fixes.append("이미 '정답입니다!' 메시지 적용됨")
        else:
            # 신고 접수 메시지 변경
            old_msg = '✅ 신고가 접수되었어요. 확인 후 고칠게요!'
            new_msg = '✅ 정답입니다! 신고가 접수되었어요.'
            if old_msg in html:
                html = html.replace(old_msg, new_msg)
                fixes.append("신고 접수 메시지를 '정답입니다!'로 변경")
    
    # 패턴 2: displaystyle 관련 신고
    if 'displaystyle' in text or '분수' in text:
        # .know 블록의 \frac 앞에 \displaystyle 추가
        def add_displaystyle(match):
            block = match.group(0)
            # 이미 \displaystyle이 없는 \frac만 교체
            block = re.sub(r'(?<!\\displaystyle)\\frac', r'\\displaystyle\\frac', block)
            return block
        
        new_html = re.sub(r'<div class="know">.*?</div>', add_displaystyle, html, flags=re.DOTALL)
        if new_html != html:
            html = new_html
            fixes.append("\\displaystyle 추가 (know 섹션의 분수)")
    
    # 패턴 3: "두 근" → 함수에서는 "교점"으로 수정
    if '두 근' in text or '근의 합' in text:
        if '포물선' in html and '두 근의 합' in html:
            html = html.replace('두 근의 합', '두 교점의 x좌표의 합')
            fixes.append("'두 근의 합' → '두 교점의 x좌표의 합' (함수이므로)")
    
    if html == original:
        return None, "해당하는 패턴 없음 (이미 수정되었거나 수동 확인 필요)"
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return "; ".join(fixes), None

def main():
    print(f"[mathedu] 신고 자동 수정 시작 ({datetime.now(timezone.utc).strftime('%H:%M:%S')} UTC)")
    
    reports = get_reports()
    if not reports:
        print("[mathedu] 새로운 신고 없음")
        return
    
    processed = load_processed()
    processed_items = processed.get('processed', [])
    
    new_count = 0
    for r in reports:
        ts = r.get('timestamp', '')
        qs = r.get('quiz_slug', '')
        qn = str(r.get('question_num', ''))
        text = r.get('text', '')
        
        # 이미 처리되었는지 확인
        already = any(
            p.get('timestamp') == ts and p.get('quiz_slug') == qs and str(p.get('question_num')) == qn
            for p in processed_items
        )
        # 이미 fix_timestamp이 있는지 확인
        if r.get('fix_timestamp'):
            already = True
        
        if already:
            continue
        
        print(f"\n[mathedu] 새 신고: {qs} q{qn} - {text[:60]}")
        
        # HTML 수정
        fix_desc, err = fix_html(r)
        if err:
            print(f"  ↳ 스킵: {err}")
            processed_items.append({
                'timestamp': ts, 'quiz_slug': qs, 'question_num': qn,
                'status': 'skipped', 'reason': err
            })
            continue
        
        new_count += 1
        print(f"  ↳ 수정: {fix_desc}")
        
        # Git commit & push
        try:
            repo_dir = os.path.dirname(os.path.abspath(__file__))
            os.system(f'cd {repo_dir} && git add -A && git commit -m "auto-fix: {qs} q{qn} - {fix_desc[:50]}" && git push')
            print(f"  ↳ ✅ 푸시 완료")
        except Exception as e:
            print(f"  ↳ ⚠️ 푸시 실패: {e}")
        
        # reports 시트에 결과 기록
        result_text = f'✅ 처리완료: {fix_desc}'
        post_fix_report(ts, qs, qn, result_text)
        
        processed_items.append({
            'timestamp': ts, 'quiz_slug': qs, 'question_num': qn,
            'status': 'fixed', 'fix': fix_desc
        })
    
    processed['processed'] = processed_items
    save_processed(processed)
    if new_count > 0:
        print(f"\n[mathedu] 총 {new_count}건 처리 완료")
    else:
        print("[mathedu] 새로운 신고 없음")

if __name__ == '__main__':
    main()
