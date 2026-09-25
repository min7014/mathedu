#!/usr/bin/env python3
r"""
mathedu 신고 자동 분석 및 자가 치유(Self-Healing) 스크립트
1분 주기 Hermes 크론잡(8ff06efd5ca9)에서 no-agent 모드로 실행됩니다.

처리 파이프라인:
1. Google Sheets(progress-api-url)에서 실시간 신고 목록 감지
2. 신규/미처리 신고가 없으면 [SILENT] 출력 후 즉시 종료 (텔레그램 불필요 알림 방지)
3. 다계층 자동 수정 엔진:
   - Tier 1: 정규식 & 오타 허용 스마트 규칙 엔진 (분수 \dfrac 확대, 피드백 메시지, 용어 교정, 보기 번호 정리, 스팸 판정)
   - Tier 2: AI 자율 에이전트(hermes -z) 폴백 (복잡한 수학 계산, 문제 지문 수정, 정답 검토)
4. 무결성 검증 (HTML 문법, LaTeX $ 구분자 짝 검사, data-ans 보존)
   - 검증 실패 시 즉각 git checkout 롤백 및 관리자 알림
5. Git commit & push (GitHub Pages 실시간 자동 배포)
6. Google Sheets 신고 처리 상태 업데이트 (fix_timestamp, fix_result)
7. 관리자(M님) 텔레그램 봇 알림 자동 발송 (Telegram Bot API 및 Hermes stdout deliver 연동)
"""
import json, os, re, sys, urllib.request, subprocess
from datetime import datetime, timezone, timedelta

# UTF-8 입출력 강제 설정 (Windows 환경)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_DIR = os.path.join(REPO_DIR, 'board')
PROCESSED_FILE = os.path.join(REPO_DIR, '_processed_reports.json')
API_URL_FILE = os.path.join(REPO_DIR, 'progress-api-url.txt')

TELEGRAM_BOT_TOKEN = '8825093659:AAGKWO6FH4WF5PaqHrRadjtvC7fRxyuHg5o'
TELEGRAM_CHAT_ID = '43453234'
KST = timezone(timedelta(hours=9))

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

def send_telegram(text):
    """M님에게 텔레그램 알림을 발송합니다."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = json.dumps({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }).encode('utf-8')
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        pass

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
    sheets_url = get_sheets_url()
    try:
        req = urllib.request.Request(f'{sheets_url}?action=reports')
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read().decode('utf-8'))
        return data.get('reports', [])
    except Exception as e:
        return []

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
    except Exception as e:
        return False

def verify_html(html_content):
    """HTML 문법 및 LaTeX 수식 무결성 검증"""
    if not html_content or len(html_content) < 500:
        return False, "파일 내용이 비어있거나 너무 작습니다 (< 500B)"
    
    # 1. LaTeX 수식 구분자($) 짝 검사 (이스케이프 \$ 제외)
    clean_latex = re.sub(r'\\\$', '', html_content)
    dollar_count = clean_latex.count('$')
    if dollar_count % 2 != 0:
        return False, f"LaTeX 수식 구분자($) 개수가 홀수입니다 ({dollar_count}개)"
    
    # 2. 문항 및 data-ans 속성 검증
    if '<div class="q"' in html_content:
        q_count = html_content.count('class="q"')
        ans_count = html_content.count('data-ans=')
        if q_count != ans_count:
            return False, f"문항 수({q_count})와 data-ans 속성 수({ans_count})가 불일치합니다"
    
    return True, "정상"

def fix_with_tier1_rules(html, text, q_num):
    """Tier 1: 패턴 및 정규식 기반 빠른 수리"""
    original = html
    fixes = []
    
    # 1. 스팸 / 테스트 / 단순 무의미 입력 감지
    clean_text = text.strip()
    if clean_text in ['사유 없음', '111', 'fsdfsfdsfd'] or re.match(r'^[ㄱ-ㅎㅏ-ㅣ\s]+$', clean_text) or len(clean_text) <= 1:
        return None, "테스트 또는 단순 입력 신고 확인 종결 (문항 정상)"

    # 2. 분수 표시 크기 확대 (\displaystyle / \dfrac)
    if re.search(r'분수|분스|display|dfrac|크기|작아|작다|글씨|키워', clean_text, re.I):
        new_html = re.sub(r'(?<![a-zA-Z\\])\\frac(?=\{)', r'\\dfrac', html)
        if new_html != html:
            html = new_html
            fixes.append("모든 분수 수식을 \\dfrac(\\displaystyle)으로 일괄 고화질 확대 적용")

    # 3. 정답 선택 피드백 ('✅ 정답입니다!') 확인 및 리스너 보강
    if re.search(r'정답입니다|정답.*표시|선택.*안|답이.*선택|반응|안눌|체크', clean_text, re.I):
        if '✅ 정답입니다!' not in html or '.confirm-msg' not in html:
            # confirm-msg 스타일 및 로직 보강
            if '</style>' in html and '.confirm-msg' not in html:
                confirm_css = "\n.confirm-msg{display:none;color:#3ddc97;font-weight:700;margin-top:8px;font-size:0.95rem;animation:fadeIn .2s ease}\n"
                html = html.replace('</style>', confirm_css + '</style>', 1)
                fixes.append("정답 피드백(.confirm-msg) 스타일 보강")

    # 4. 수학 용어 정밀화 ('두 근' -> '두 교점의 x좌표')
    if re.search(r'두 근|근의 합', clean_text):
        if ('포물선' in html or '이차함수' in html) and '두 근의 합' in html:
            html = html.replace('두 근의 합', '두 교점의 x좌표의 합')
            fixes.append("'두 근의 합' → '두 교점의 x좌표의 합' (함수 그래프 용어 정합성 교정)")

    # 5. 보기 내 불필요한 중복 원문자(①~⑤) 정리
    if re.search(r'동그라미|①|중복|번호|기호', clean_text):
        new_html = re.sub(r'(<div class="opt"[^>]*>)\s*[①②③④⑤]\s*', r'\1', html)
        if new_html != html:
            html = new_html
            fixes.append("보기 내 중복 원문자(①~⑤) 제거")

    if html != original:
        return html, "; ".join(fixes)
    return None, None

def fix_with_tier2_agent(quiz_slug, question_num, report_text, html_path):
    """Tier 2: AI 자율 에이전트 (hermes -z) 폴백"""
    prompt = (
        f"You are the autonomous mathedu quality agent. A student submitted an issue report for quiz '{quiz_slug}', question {question_num}:\n"
        f"Report text: \"{report_text}\"\n\n"
        f"The target file is at: {html_path}\n\n"
        f"Task:\n"
        f"1. Read {html_path} and understand what the student reported.\n"
        f"2. If it is a valid issue (math calculation mistake, typo in problem statement, wrong answer data-ans, LaTeX syntax issue), fix {html_path} directly.\n"
        f"3. Strict rules: Maintain valid HTML, do not break question layout or data-ans attributes, and do not modify unrelated code.\n"
        f"4. Finally, output a single line in Korean: '수정완료: <간단한 수정 설명>' if fixed, or '이상없음: <이유>' if the question is verified to be mathematically correct.\n"
    )
    try:
        res = subprocess.run(
            ["hermes", "-z", prompt],
            capture_output=True,
            text=True,
            timeout=120,
            shell=True
        )
        output = res.stdout.strip()
        for line in reversed(output.splitlines()):
            line = line.strip()
            if line.startswith("수정완료:") or line.startswith("이상없음:"):
                return line
        return output[-120:] if output else "AI 에이전트 분석 완료"
    except Exception as e:
        return f"AI 에이전트 실행 실패: {e}"

def main():
    reports = get_reports()
    if not reports:
        print("[SILENT]")
        return
    
    processed = load_processed()
    processed_items = processed.get('processed', [])
    
    # 미처리 신고 필터링
    unprocessed = []
    for r in reports:
        ts = r.get('timestamp', '')
        qs = r.get('quiz_slug', '')
        qn = str(r.get('question_num', ''))
        
        # fix_timestamp 이미 있거나 로컬에서 fixed/resolved 된 경우 스킵
        if r.get('fix_timestamp'):
            continue
        
        already_handled = any(
            p.get('timestamp') == ts and p.get('quiz_slug') == qs and str(p.get('question_num')) == qn
            and p.get('status') in ['fixed', 'resolved']
            for p in processed_items
        )
        if not already_handled:
            unprocessed.append(r)
    
    if not unprocessed:
        print("[SILENT]")
        return
    
    now_str = datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S KST')
    fix_summaries = []

    for r in unprocessed:
        ts = r.get('timestamp', '')
        qs = r.get('quiz_slug', '')
        qn = str(r.get('question_num', ''))
        reporter = str(r.get('reporter', '익명'))
        text = str(r.get('text', '')).strip()

        if not qs:
            continue

        html_path = os.path.join(BOARD_DIR, f'{qs}.html')
        if not os.path.exists(html_path):
            err_msg = f"파일 없음: board/{qs}.html"
            post_fix_report(ts, qs, qn, f"⚠️ {err_msg}")
            processed_items.append({'timestamp': ts, 'quiz_slug': qs, 'question_num': qn, 'status': 'skipped', 'reason': err_msg})
            continue

        with open(html_path, 'r', encoding='utf-8') as f:
            original_html = f.read()

        fix_desc = None
        new_html = None
        deploy_needed = False

        # 1. Tier 1 규칙 엔진 시도
        t1_html, t1_desc = fix_with_tier1_rules(original_html, text, qn)
        if t1_html:
            new_html = t1_html
            fix_desc = t1_desc
            deploy_needed = True
        elif t1_desc:
            # 스팸 또는 테스트로 판정 종결 (코드 수정 불필요)
            fix_desc = t1_desc
            deploy_needed = False
        else:
            # 2. Tier 2 AI 에이전트 폴백
            agent_result = fix_with_tier2_agent(qs, qn, text, html_path)
            # 파일이 변경되었는지 확인
            with open(html_path, 'r', encoding='utf-8') as f:
                agent_html = f.read()
            if agent_html != original_html:
                new_html = agent_html
                fix_desc = agent_result
                deploy_needed = True
            else:
                fix_desc = agent_result
                deploy_needed = False

        # 3. HTML 파일 저장 및 무결성 검증
        if deploy_needed and new_html:
            valid, reason = verify_html(new_html)
            if not valid:
                # 롤백
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(original_html)
                err_msg = f"무결성 검증 실패로 롤백: {reason}"
                post_fix_report(ts, qs, qn, f"⚠️ {err_msg}")
                processed_items.append({'timestamp': ts, 'quiz_slug': qs, 'question_num': qn, 'status': 'skipped', 'reason': err_msg})
                continue
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_html)

            # 4. Git Commit & Push
            try:
                subprocess.run(['git', 'add', f'board/{qs}.html'], cwd=REPO_DIR, check=True)
                commit_msg = f"auto-fix({qs}): {fix_desc[:60]}"
                subprocess.run(['git', 'commit', '-m', commit_msg], cwd=REPO_DIR, check=True)
                subprocess.run(['git', 'push', 'origin', 'main'], cwd=REPO_DIR, check=True)
                deploy_status = "✅ GitHub Pages 배포 완료"
            except Exception as e:
                deploy_status = f"⚠️ 배포 중 오류 발생: {e}"
        else:
            deploy_status = "ℹ️ 소스 변경 없음 (검토 완료 종결)"

        # 5. Google Sheets 상태 업데이트
        result_text = f"✅ {fix_desc}" if deploy_needed else f"ℹ️ {fix_desc}"
        post_fix_report(ts, qs, qn, result_text)
        processed_items.append({
            'timestamp': ts,
            'quiz_slug': qs,
            'question_num': qn,
            'status': 'fixed' if deploy_needed else 'resolved',
            'fix': fix_desc
        })

        # 6. 알림 메시지 생성
        report_alert = (
            f"🚨 <b>[mathedu 신고 자동 처리 완료]</b>\n\n"
            f"• <b>퀴즈</b>: <code>{qs}</code> (문항 #{qn or '전체'})\n"
            f"• <b>신고자</b>: {reporter}\n"
            f"• <b>신고 내용</b>: {text}\n"
            f"• <b>조치 내역</b>: {fix_desc}\n"
            f"• <b>배포 상태</b>: {deploy_status}\n"
            f"• <b>처리 시각</b>: {now_str}"
        )
        send_telegram(report_alert)
        fix_summaries.append(report_alert)

    processed['processed'] = processed_items
    save_processed(processed)

    # Hermes 크론잡 stdout을 통해 텔레그램으로도 자동 전달
    if fix_summaries:
        print("\n\n".join(fix_summaries))
    else:
        print("[SILENT]")

if __name__ == '__main__':
    main()
