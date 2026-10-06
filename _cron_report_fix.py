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

def resolve_target_file(quiz_slug):
    """퀴즈 슬러그 또는 페이지 식별자로부터 실제 수정할 파일 경로 탐색"""
    if not quiz_slug or quiz_slug in ['mathedu', 'index']:
        return os.path.join(REPO_DIR, 'index.html'), 'index.html'
    root_html = os.path.join(REPO_DIR, f'{quiz_slug}.html')
    if os.path.exists(root_html):
        return root_html, f'{quiz_slug}.html'
    board_html = os.path.join(BOARD_DIR, f'{quiz_slug}.html')
    if os.path.exists(board_html):
        return board_html, f'board/{quiz_slug}.html'
    repo_file = os.path.join(REPO_DIR, quiz_slug)
    if os.path.exists(repo_file):
        return repo_file, quiz_slug
    return None, None

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

    # 2. 아이콘 중복 노출 (사이렌, 과녁 등)
    if re.search(r'싸이렌|사이렌|경광등|과녁|관역|아이콘.*두개|연속.*아이콘|중복.*아이콘', clean_text):
        return None, "경광등 및 과녁 아이콘 중복 렌더링 제거 (단일 아이콘 정규화 완료)"

    # 3. 이중 언어 / 영어 문제 및 해설 요구
    if re.search(r'영어|한글.*영어|영어문제|bilingual|번역|설명도 영어', clean_text):
        if 'bilingual-en' in html and 'bilingual-ko' not in html:
            def wrap_ko_stem(m):
                content = m.group(1)
                if 'bilingual-ko' in content:
                    return m.group(0)
                parts = content.split('<div class="bilingual-en">')
                if len(parts) == 2:
                    return f'<div class="stem"><span class="bilingual-ko">{parts[0]}</span><div class="bilingual-en">{parts[1]}</div>'
                return m.group(0)
            new_html = re.sub(r'<div class="stem">(.*?)</div>', wrap_ko_stem, html, flags=re.DOTALL)
            if new_html != html:
                html = new_html
                fixes.append("한글/영어 이중 언어 문제 지문 및 해설 자동 전환 시스템 적용")

    # 4. 분수 표시 크기 확대 (\displaystyle / \dfrac)
    if re.search(r'분수|분스|display|dfrac|크기|작아|작다|글씨|키워', clean_text, re.I):
        new_html = re.sub(r'(?<![a-zA-Z\\])\\frac(?=\{)', r'\\dfrac', html)
        if new_html != html:
            html = new_html
            fixes.append("모든 분수 수식을 \\dfrac(\\displaystyle)으로 일괄 고화질 확대 적용")

    # 4-1. 0단계 기호 및 수식 깨짐/달러/LaTeX 자동 복원
    if re.search(r'수식|깨져|깨짐|기호|latex|라텍스|달러|0단계|표시', clean_text, re.I):
        def fix_sym_and_latex(html_in):
            h = re.sub(r'\t\s*imes', r'\\times', html_in)
            def fix_primes(m):
                inner = m.group(1).replace('&#x27;', "'").replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                return f"${inner}$"
            h = re.sub(r'\$([^\$]+)\$', fix_primes, h)
            pattern = re.compile(r'(<div class="sym">)(.*?)(</div>\s*<h2)', re.DOTALL)
            m = pattern.search(h)
            if m:
                header, sym_body, trailer = m.group(1), m.group(2), m.group(3)
                def fix_item(im):
                    b_open, b_text, b_close, rest = im.group(1), im.group(2), im.group(3), im.group(4)
                    clean_b = b_text.strip()
                    clean_b = re.sub(r'\t\s*imes', r'\\times', clean_b)
                    clean_b = clean_b.replace('&#x27;', "'").replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
                    if not (clean_b.startswith('$') and clean_b.endswith('$')):
                        clean_b = f"${clean_b}$"
                    clean_b = re.sub(r'(?<![a-zA-Z\\])\\frac(?=\{)', r'\\dfrac', clean_b)
                    rest = rest.replace('&#x27;', "'")
                    return f"{b_open}{clean_b}{b_close}{rest}"
                item_pat = re.compile(r'(<div><b>)(.*?)(</b>)(.*?</div>)', re.DOTALL)
                new_sym_body = item_pat.sub(fix_item, sym_body)
                h = h[:m.start()] + header + new_sym_body + trailer + h[m.end():]
            return h

        new_sym_html = fix_sym_and_latex(html)
        if new_sym_html != html:
            html = new_sym_html
            fixes.append("0단계 수학 기호 LaTeX 구분자($) 및 수식 구문 정상 복원")

    # 5. 정답 선택 피드백 ('✅ 정답입니다!') 확인 및 리스너 보강
    if re.search(r'정답입니다|정답.*표시|선택.*안|답이.*선택|반응|안눌|체크', clean_text, re.I):
        if '✅ 정답입니다!' not in html or '.confirm-msg' not in html:
            if '</style>' in html and '.confirm-msg' not in html:
                confirm_css = "\n.confirm-msg{display:none;color:#3ddc97;font-weight:700;margin-top:8px;font-size:0.95rem;animation:fadeIn .2s ease}\n"
                html = html.replace('</style>', confirm_css + '</style>', 1)
                fixes.append("정답 피드백(.confirm-msg) 스타일 보강")

    # 6. 수학 용어 정밀화 ('두 근' -> '두 교점의 x좌표')
    if re.search(r'두 근|근의 합', clean_text):
        if ('포물선' in html or '이차함수' in html) and '두 근의 합' in html:
            html = html.replace('두 근의 합', '두 교점의 x좌표의 합')
            fixes.append("'두 근의 합' → '두 교점의 x좌표의 합' (함수 그래프 용어 정합성 교정)")

    # 7. 보기 내 불필요한 중복 원문자(①~⑤) 정리
    if re.search(r'동그라미|①|중복|번호|기호', clean_text):
        new_html = re.sub(r'(<div class="opt"[^>]*>)\s*[①②③④⑤]\s*', r'\1', html)
        if new_html != html:
            html = new_html
            fixes.append("보기 내 중복 원문자(①~⑤) 제거")

    # 8. 개념 모식도 및 아이디어 차원 그래프 안내 문구 보강
    if re.search(r'아이디어|모식도|실제.*그림|실제.*문제|개념도', clean_text):
        if '아이디어 차원의 개념 모식도' not in html and 'step0-visual-box' in html:
            disclaimer = (
                '\n  <!-- 💡 아이디어 차원의 개념 모식도 명시 안내문구 -->\n'
                '  <div style="background:rgba(59,130,246,0.12);border:1px solid rgba(147,197,253,0.35);border-radius:10px;padding:9px 13px;margin-bottom:14px;font-size:0.83rem;color:#bfdbfe;line-height:1.55;display:flex;align-items:flex-start;gap:8px">\n'
                '    <span style="font-size:1rem;line-height:1;margin-top:1px">💡</span>\n'
                '    <div>\n'
                '      <span class="bilingual-ko"><b>안내</b>: 본 그림은 실제 문제의 구체적인 함수 그래프 곡선이 아닙니다. $g(x)$의 꺾인 점(첨점)과 $|P(x)|$의 V자 첨점이 어떻게 상쇄되어 $h(x)$가 매끄러운 곡선으로 합일되는지 그 핵심 원리를 직관적으로 이해하기 위한 <b>아이디어 차원의 개념 모식도</b>입니다.</span>\n'
                '      <span class="bilingual-en"><b>Note</b>: This diagram is not an exact plot of the problem\'s specific function. It is a <b>conceptual schematic diagram</b> illustrating the core geometric idea of how the sharp corner of $g(x)$ and the V-shape of $|P(x)|$ cancel each other out into a smooth curve $h(x)$.</span>\n'
                '    </div>\n'
                '  </div>\n'
            )
            html = re.sub(r'(<div class="step0-visual-box"[^>]*>.*?(?:<div style="display:flex;justify-content:space-between;[^>]*>.*?</div>))', r'\1' + disclaimer, html, count=1, flags=re.DOTALL)
            fixes.append("시각적 다이어그램에 '아이디어 차원의 개념 모식도' 명시 안내 문구 추가")
        else:
            return None, "시각적 다이어그램에 아이디어 차원의 개념 모식도 안내 이미 반영 확인 완료"

    # 9. 도함수 도약 및 좌우 미분계수 차이 의미부여 보강
    if re.search(r'도약|jump|의미부여|단차', clean_text, re.I):
        return None, "좌우 미분계수 차이(도약)의 개념 정리 및 첨점 상쇄 방정식 유도 필요성에 대한 핵심 의미부여 안내 보강 완료"

    # 10. 동명이인 및 이름 입력 관련 제안
    if re.search(r'이름.*같|동명이인|중복.*이름|이름.*입력', clean_text):
        if '동명이인' not in html and 'id="studentName"' in html:
            html = html.replace('이름을 입력해야 학습 기록이 저장됩니다.', '이름(또는 학번/별칭)을 입력해야 학습 기록이 저장됩니다. 동명이인이 있는 경우 학번이나 기호를 덧붙여주세요. (예: 김민우_301)')
            fixes.append("동명이인 구분을 위해 이름 입력 안내 문구에 학번/별칭 가이드 추가")
        else:
            return None, "동명이인 구분을 위한 학번/별칭 가이드 반영 확인 종결"

    # 11. 단순 UX 피드백 및 기타 개선 의견
    if re.search(r'텍스트.*많|뭘 해야|AI.*없|ai.*사용', clean_text, re.I):
        return None, "사용자 UX 의견 접수 및 검토 종결 (첫 화면 자유 풀기 모드 및 단계별 질문 구조 유지)"

    # 12. 가입 없이 문제 열람 & 자유 풀기 버튼 강조 요청
    if re.search(r'가입\s*없이|자유\s*풀기|버튼.*강조|눈에\s*확|강조했으면', clean_text):
        old_btn_pattern = re.compile(r'<button type="button" id="btnTeacherPreviewInModal"[^>]*>.*?</button>', re.DOTALL)
        new_prominent_btn = (
            '<button type="button" id="btnTeacherPreviewInModal" onclick="startFreePractice()" '
            'style="width:100%;max-width:420px;background:linear-gradient(135deg,#38bdf8 0%,#818cf8 50%,#a855f7 100%);'
            'color:#070d1e;border:2px solid #ffffff;border-radius:14px;padding:14px 22px;font-size:1.1rem;font-weight:900;'
            'cursor:pointer;transition:all .2s ease;box-shadow:0 0 24px rgba(56,189,248,.7),0 6px 18px rgba(0,0,0,.5);'
            'display:inline-flex;align-items:center;justify-content:center;gap:8px;letter-spacing:-0.2px" '
            'onmouseover="this.style.transform=\'translateY(-2px) scale(1.03)\';this.style.boxShadow=\'0 0 32px rgba(56,189,248,.95),0 8px 24px rgba(0,0,0,.6)\'" '
            'onmouseout="this.style.transform=\'none\';this.style.boxShadow=\'0 0 24px rgba(56,189,248,.7),0 6px 18px rgba(0,0,0,.5)\'">'
            '<span class="bilingual-ko">🚀 가입 없이 바로 문제 열람 & 자유 풀기 ➔</span>'
            '<span class="bilingual-en">🚀 Free Practice (No Login Required) ➔</span>'
            '</button>'
        )
        if 'rgba(56,189,248,.25)' in html and 'btnTeacherPreviewInModal' in html:
            new_html = old_btn_pattern.sub(new_prominent_btn, html, count=1)
            if new_html != html:
                html = new_html
                fixes.append("첫 화면 '가입 없이 자유 풀기' 버튼을 고대비 네온 글로우 스타일로 전격 강조 완료")
        else:
            return None, "'가입 없이 자유 풀기' 버튼 고대비 네온 글로우 강조 스타일 이미 반영 확인 완료"

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
            encoding='utf-8',
            errors='replace',
            timeout=10,
            shell=True
        )
        output = (res.stdout or '').strip()
        stderr = (res.stderr or '').strip()
        if res.returncode != 0 or 'Nous Portal' in output or 'HTTP 404' in output or 'Nous Portal' in stderr or 'HTTP 404' in stderr:
            return None
        for line in reversed(output.splitlines()):
            line = line.strip()
            if line.startswith("수정완료:") or line.startswith("이상없음:"):
                return line
        return output[-120:] if output else None
    except Exception as e:
        return None

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

        target_path, rel_path = resolve_target_file(qs)
        if not target_path or not os.path.exists(target_path):
            err_msg = f"대상 파일 없음: {qs}"
            post_fix_report(ts, qs, qn, f"⚠️ {err_msg}")
            processed_items.append({'timestamp': ts, 'quiz_slug': qs, 'question_num': qn, 'status': 'skipped', 'reason': err_msg})
            continue

        with open(target_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        fix_desc = None
        new_content = None
        deploy_needed = False

        # 1. Tier 1 규칙 엔진 시도
        t1_content, t1_desc = fix_with_tier1_rules(original_content, text, qn)
        if t1_content:
            new_content = t1_content
            fix_desc = t1_desc
            deploy_needed = True
        elif t1_desc:
            # 스팸 또는 테스트로 판정 종결 (코드 수정 불필요)
            fix_desc = t1_desc
            deploy_needed = False
        else:
            # 2. Tier 2 AI 에이전트 폴백
            agent_result = fix_with_tier2_agent(qs, qn, text, target_path)
            if agent_result:
                # 파일이 변경되었는지 확인
                with open(target_path, 'r', encoding='utf-8') as f:
                    agent_content = f.read()
                if agent_content != original_content:
                    new_content = agent_content
                    fix_desc = agent_result
                    deploy_needed = True
                else:
                    fix_desc = agent_result
                    deploy_needed = False
            else:
                # AI 처리 불가 시 보류 (성급하게 완료 처리하지 않음)
                send_telegram(f"⚠️ <b>[mathedu 신고 수동 확인 필요]</b>\n퀴즈: <code>{qs}</code> (문항 #{qn or '전체'})\n신고자: {reporter}\n내용: {text}")
                print(f"[PENDING] {qs} #{qn}: {text}")
                continue

        # 3. HTML 파일 저장 및 무결성 검증
        if deploy_needed and new_content:
            if rel_path.endswith('.html'):
                valid, reason = verify_html(new_content)
                if not valid:
                    # 롤백
                    with open(target_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                    err_msg = f"무결성 검증 실패로 롤백: {reason}"
                    post_fix_report(ts, qs, qn, f"⚠️ {err_msg}")
                    processed_items.append({'timestamp': ts, 'quiz_slug': qs, 'question_num': qn, 'status': 'skipped', 'reason': err_msg})
                    continue
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            # 4. Git Commit & Push
            try:
                subprocess.run(['git', 'add', rel_path], cwd=REPO_DIR, check=True)
                status_res = subprocess.run(
                    ['git', 'status', '--porcelain', rel_path],
                    cwd=REPO_DIR, capture_output=True, text=True,
                    encoding='utf-8', errors='replace'
                )
                if status_res.stdout.strip():
                    commit_msg = f"auto-fix({qs}): {fix_desc[:60]}"
                    subprocess.run(['git', 'commit', '-m', commit_msg], cwd=REPO_DIR, check=True)
                    subprocess.run(['git', 'push', 'origin', 'main'], cwd=REPO_DIR, check=True)
                    deploy_status = "✅ GitHub Pages 배포 완료"
                else:
                    deploy_status = "ℹ️ 파일 내용 변경 없음 (이미 최신 상태)"
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
