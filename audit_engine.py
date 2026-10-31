#!/usr/bin/env python3
"""
audit_engine.py — mathedu 전수 기계적 규칙 기반 감사 및 이상 탐지 엔진
(Mechanical Rule-Based Full Scan & Anomaly Detector)

원칙 준수 (GEMINI.md Rule 5):
1. 특정 오류 발생 시 LLM으로 판단 후, 본 스크립트를 통해 전체 페이지를 기계적으로 고속 전수 스캔(LLM 미사용).
2. 적출된 이상 지점 목록을 생성하여 LLM이 2차로 정밀 검증·일괄 수정할 수 있도록 지원.

주요 점검 항목:
- LaTeX 수식 문법 (달러 기호 짝, \x0c 등 제어문자 혼입, 미닫힌 환경)
- 국문/영문 다국어 대역 무결성 (누락, 비어있는 태그, 문장 중간 잘림 현상)
- 3단계 교육학적 솔루션 표준 구조 ([문제 분석], [단계별 상세 풀이], [정답 도출])
- 금지어 및 브랜딩 준수 (민은기 성명, 평생, 세계적인, 비수학 트레이딩 용어 격리)
- 반응형 UI/모바일 가로폭 넘침 방지 스타일 적용 여부
"""

import os
import sys
import re
import glob
import json
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
BOARD_DIR = os.path.join(REPO_DIR, 'board')
PRIVATE_DIR = os.path.join(REPO_DIR, 'board', 'private')
OFFLINE_DIR = os.path.join(REPO_DIR, 'offline')

PROHIBITED_TERMS = ["민은기", "평생수학", "세계적인", "왕국", "비트코인", "암호화폐", "트레이딩", "매매", "코인", "선물거래"]

def get_target_files(include_offline=True):
    """검사 대상 HTML 파일 목록 수집"""
    files = glob.glob(os.path.join(BOARD_DIR, '*.html'))
    if os.path.exists(PRIVATE_DIR):
        files.extend(glob.glob(os.path.join(PRIVATE_DIR, '*.html')))
    if include_offline and os.path.exists(OFFLINE_DIR):
        for f in glob.glob(os.path.join(OFFLINE_DIR, '*.html')):
            if not f.endswith('index.html'):
                files.append(f)
    return sorted(list(set(files)))

def check_file_rules(filepath, content):
    """단일 파일에 대해 기계적 규칙 검사 수행"""
    issues = []
    rel_path = os.path.relpath(filepath, REPO_DIR)
    
    # 1. 제어 문자 검사 (\x0c Form Feed 등)
    if '\x0c' in content:
        issues.append({
            'rule': 'NO_FORM_FEED',
            'severity': 'ERROR',
            'msg': 'ASCII 폼피드(\\x0c) 제어 문자가 포함되어 수식(\\frac 등)이 깨졌습니다.'
        })
        
    # 2. 금지어 및 도메인 분리 검사
    for term in PROHIBITED_TERMS:
        if term in content:
            issues.append({
                'rule': 'PROHIBITED_TERM',
                'severity': 'WARNING',
                'term': term,
                'msg': f"금지어 또는 비수학 영역 용어('{term}')가 검출되었습니다."
            })
            
    # 3. 풀이 블록(<div class="sol">) 정밀 구조 검사
    if '<div class="sol">' in content:
        sol_matches = re.findall(r'<div class="sol">(.*?)</div>(?=\s*<div class="q")', content, re.DOTALL)
        if not sol_matches:
            sol_matches = re.findall(r'<div class="sol">(.*?)</div>', content, re.DOTALL)
            
        if not sol_matches:
            issues.append({
                'rule': 'SOL_CLOSING_TAG',
                'severity': 'ERROR',
                'msg': '<div class="sol"> 태그가 올바르게 닫히지 않았거나 구문 오류가 있습니다.'
            })
        else:
            sol_text = sol_matches[0]
            
            # 3-1. LaTeX $ 짝 검사 (이스케이프 안 된 달러 기호 개수 홀짝 검사)
            pure_dollars = len(re.findall(r'(?<!\\)\$', sol_text))
            if pure_dollars % 2 != 0:
                issues.append({
                    'rule': 'LATEX_UNBALANCED_DOLLAR',
                    'severity': 'ERROR',
                    'count': pure_dollars,
                    'msg': f"LaTeX 수식 구분자($) 개수({pure_dollars}개)가 홀수입니다. 짝이 맞지 않습니다."
                })
                
            # 3-2. 다국어 대역 검사
            if 'bilingual-ko' not in sol_text:
                issues.append({
                    'rule': 'BILINGUAL_KO_MISSING',
                    'severity': 'ERROR',
                    'msg': '풀이 블록에 한국어 대역(.bilingual-ko)이 누락되었습니다.'
                })
            if 'bilingual-en' not in sol_text:
                issues.append({
                    'rule': 'BILINGUAL_EN_MISSING',
                    'severity': 'ERROR',
                    'msg': '풀이 블록에 영문 대역(.bilingual-en)이 누락되었습니다.'
                })
                
            # 3-3. 영문 풀이 중간 잘림(Truncation) 검사
            en_match = re.search(r'<div class="bilingual-en">(.*)</div>\s*$', sol_text, re.DOTALL)
            if not en_match:
                en_match = re.search(r'<div class="bilingual-en">(.*?)</div>', sol_text, re.DOTALL)
            if en_match:
                en_body = en_match.group(1).strip()
                if len(en_body) < 100 and not rel_path.endswith('index.html'):
                    issues.append({
                        'rule': 'BILINGUAL_EN_TRUNCATED',
                        'severity': 'WARNING',
                        'len': len(en_body),
                        'msg': f"영문 풀이 길이가 비정상적으로 짧습니다 ({len(en_body)}자)."
                    })
                if en_body.endswith('<br>') or en_body.endswith('is') or en_body.endswith('that is,'):
                    issues.append({
                        'rule': 'BILINGUAL_EN_INCOMPLETE',
                        'severity': 'ERROR',
                        'msg': '영문 풀이가 미완성 문장으로 잘려 있습니다.'
                    })
                    
            # 3-4. 3단계 교육학적 풀이 표준 구조 검사
            has_p1 = ("문제 분석" in sol_text) or ("Problem Analysis" in sol_text)
            has_p2 = ("상세 풀이" in sol_text) or ("Rigorous Derivation" in sol_text) or ("Step-by-Step" in sol_text)
            has_p3 = ("정답 도출" in sol_text) or ("Conclusion" in sol_text) or ("Takeaways" in sol_text)
            
            if not (has_p1 and has_p2 and has_p3):
                missing_parts = []
                if not has_p1: missing_parts.append('1단계(문제분석)')
                if not has_p2: missing_parts.append('2단계(상세풀이)')
                if not has_p3: missing_parts.append('3단계(정답도출)')
                # ac8dc374 같은 특별 템플릿은 제외
                if 'ac8dc374' not in rel_path:
                    issues.append({
                        'rule': 'PEDAGOGICAL_3TIER_STRUCTURE',
                        'severity': 'WARNING',
                        'missing': missing_parts,
                        'msg': f"3단계 교육학적 풀이 표준 항목 누락: {', '.join(missing_parts)}"
                    })
            if len(sol_text.strip()) < 1000 and not rel_path.endswith('index.html'):
                issues.append({
                    'rule': 'SOL_BLOCK_MIN_DEPTH',
                    'severity': 'WARNING',
                    'len': len(sol_text.strip()),
                    'msg': f"상세 풀이(<div class=\"sol\">) 길이가 너무 압축적입니다 ({len(sol_text.strip())}자, 최소 1000자 이상 권장)."
                })

            # 3-5. 도식화 풀이 및 의도적 시각 도형 작도 필수 검사 (GEMINI.md Rule 7)
            if not rel_path.endswith('index.html'):
                if '<svg' not in sol_text or 'math-visual-diagram' not in sol_text:
                    issues.append({
                        'rule': 'VISUAL_DIAGRAM_REQUIRED',
                        'severity': 'ERROR',
                        'msg': '풀이 블록(<div class="sol">)에 의도적으로 작도한 시각적 기하·개념 도형(<svg> / .math-visual-diagram)이 누락되었습니다.'
                    })
                if 'math-schematic-flow' not in sol_text:
                    issues.append({
                        'rule': 'SCHEMATIC_FLOW_REQUIRED',
                        'severity': 'ERROR',
                        'msg': '풀이 블록(<div class="sol">)에 도식화 풀이 흐름도(.math-schematic-flow)가 누락되었습니다.'
                    })
                    
    # 4. 반응형 UI 스타일 누락 검사
    if '<div class="sol">' in content and '.sol .bilingual-en' not in content:
        issues.append({
            'rule': 'STYLE_SOL_BILINGUAL_RESET',
            'severity': 'WARNING',
            'msg': '.sol .bilingual-en 스타일 리셋이 누락되어 영문 전환 시 레이아웃 이상 가능성이 있습니다.'
        })
        
    # 5. 초등학생 눈높이 무장벽 디딤돌 확장 검사 (GEMINI.md Rule 6)
    if '<div class="q"' in content and not rel_path.endswith('index.html'):
        all_exps = re.findall(r'data-exp="([^"]*)"', content)
        if all_exps and len(all_exps[-1]) < 500:
            issues.append({
                'rule': 'FINAL_EXP_DEPTH_CHECK',
                'severity': 'ERROR',
                'len': len(all_exps[-1]),
                'msg': f"최종 본문항의 해설(data-exp)이 너무 압축적입니다 ({len(all_exps[-1])}자, 최소 500자 이상 단계별 상세 풀이 포함 필수)."
            })
        stems = re.findall(r'<div class="stem">(.*?)</div>', content, re.DOTALL)
        lvls = re.findall(r'<div class="lvl">(.*?)</div>', content, re.DOTALL)
        if stems and lvls:
            s1 = re.sub(r'<.*?>', '', stems[0]).strip()
            l1 = re.sub(r'<.*?>', '', lvls[0]).strip()
            has_elem = any(k in s1 or k in l1 for k in ['초등', 'Elementary', '구구단', '사칙연산'])
            if not has_elem:
                issues.append({
                    'rule': 'SCAFFOLDING_ELEMENTARY_GROUNDING',
                    'severity': 'WARNING',
                    'msg': '1단계(Step 1)에 초등학생 눈높이 직관 디딤돌(초등 개념, 구구단, 사칙연산 연계)이 누락되었습니다.'
                })
        if '잠깐!' in content:
            issues.append({
                'rule': 'DRAFT_MARKER_LEAK',
                'severity': 'ERROR',
                'msg': "해설 또는 본문에 초안 작성 흔적('잠깐!')이 남아 있습니다."
            })
        base_slug = os.path.splitext(os.path.basename(rel_path))[0].replace('_offline', '')
        killer_min_steps = {
            'c261015': 8, 'c261021': 8, 'c261022': 8,
            'c2610p29': 8, 'c2610p30': 10,
            'c2610m28': 8, 'c2610m29': 8, 'c2610m30': 8,
            'c2610g28': 8, 'c2610g29': 8, 'c2610g30': 8,
        }
        if base_slug in killer_min_steps:
            # Each scaffolding step has one <div class="know"> block
            step_q_count = len(re.findall(r'<div class="know">', content))
            if step_q_count < killer_min_steps[base_slug]:
                issues.append({
                    'rule': 'KILLER_SCAFFOLDING_DEPTH',
                    'severity': 'ERROR',
                    'msg': f"고난도/킬러 문항({base_slug})의 디딤돌 단계 수({step_q_count}단계)가 최소 기준({killer_min_steps[base_slug]}단계)보다 적습니다."
                })

    # 6. 수식(MathJax / LaTeX) 무결성 검사 (GEMINI.md Rule 5)
    m_cfg = re.search(r'window\.MathJax\s*=\s*\{[^\n<]+', content)
    if m_cfg and r"'\('" in m_cfg.group(0):
        issues.append({
            'rule': 'MATHJAX_BROKEN_PAREN_DELIMITER',
            'severity': 'ERROR',
            'msg': "MathJax inlineMath 설정에 단일 백슬래시 ['\\(','\\)']가 포함되어 일반 괄호 ( ) 전체가 수식으로 오인식됩니다. ['\\\\(','\\\\)']로 수정하십시오."
        })

    no_script = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', content, flags=re.S | re.I)
    math_segments = []
    for attr in re.finditer(r'(data-exp(?:-en)?)="([^"]*)"', no_script):
        for m in re.finditer(r'\$\$[\s\S]*?\$\$|\$[^\$]*?\$', attr.group(2)):
            math_segments.append((attr.group(1), m.group(0)))
    no_attrs = re.sub(r'\b(?:data-[a-z-]+|alt|title|content)="[^"]*"', '', no_script)
    for m in re.finditer(r'\$\$[\s\S]*?\$\$|\$[^\$]*?\$', no_attrs):
        math_segments.append(('body', m.group(0)))

    for loc, raw_math in math_segments:
        inner = raw_math[2:-2] if raw_math.startswith('$$') else raw_math[1:-1]
        if re.search(r'[\x00-\x08\x09\x0b\x0c]', inner):
            issues.append({
                'rule': 'MATH_TAB_OR_CTRL_CORRUPTION',
                'severity': 'ERROR',
                'msg': f"[{loc}] 수식 내부에 탭(\\t) 또는 제어문자가 혼입되어 수식이 깨졌습니다: {repr(raw_math[:60])}"
            })
        if not re.search(r'\\begin\{(array|cases|aligned|align|matrix|pmatrix|bmatrix|vmatrix)\}', inner):
            if re.search(r'\\\\[a-zA-Z]', inner):
                issues.append({
                    'rule': 'MATH_DOUBLE_BACKSLASH_CORRUPTION',
                    'severity': 'ERROR',
                    'msg': f"[{loc}] 수식 내부에 이중 백슬래시(\\\\cmd)가 혼입되어 수식이 깨졌습니다: {raw_math[:60]}"
                })
        if loc == 'body' and re.search(r'<[a-zA-Z/!]', inner):
            issues.append({
                'rule': 'MATH_UNSPACED_LT_HTML_TAG',
                'severity': 'ERROR',
                'msg': f"[{loc}] 수식 내부의 '<문자'가 HTML 태그로 오인식되어 잘립니다('< '로 공백 추가 필요): {raw_math[:60]}"
            })
        
    return issues


def scan_repository(include_offline=True, custom_pattern=None, custom_missing=None):
    """전체 리포지토리 기계적 스캔 실행"""
    files = get_target_files(include_offline=include_offline)
    results = {
        'total_scanned': len(files),
        'clean_files': 0,
        'flagged_files': 0,
        'details': {}
    }
    
    for f in files:
        rel = os.path.relpath(f, REPO_DIR)
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                content = fp.read()
        except Exception as e:
            results['details'][rel] = [{
                'rule': 'FILE_READ_ERROR',
                'severity': 'FATAL',
                'msg': str(e)
            }]
            results['flagged_files'] += 1
            continue
            
        file_issues = check_file_rules(f, content)
        
        # 사용자 정의 패턴 검사 (지정된 경우)
        if custom_pattern:
            matches = re.findall(custom_pattern, content)
            if matches:
                file_issues.append({
                    'rule': 'CUSTOM_PATTERN_MATCH',
                    'severity': 'INFO',
                    'matches_count': len(matches),
                    'msg': f"사용자 정의 검색 패턴 '{custom_pattern}'이 {len(matches)}회 검출되었습니다."
                })
        if custom_missing:
            if not re.search(custom_missing, content):
                file_issues.append({
                    'rule': 'CUSTOM_PATTERN_MISSING',
                    'severity': 'WARNING',
                    'msg': f"필수 패턴 '{custom_missing}'이 본 파일에서 발견되지 않았습니다."
                })
                
        if file_issues:
            results['details'][rel] = file_issues
            results['flagged_files'] += 1
        else:
            results['clean_files'] += 1
            
    return results

def main():
    parser = argparse.ArgumentParser(description="mathedu Mechanical Rule-Based Full Scan Engine")
    parser.add_argument('--no-offline', action='store_true', help="offline 디렉토리 스캔 제외")
    parser.add_argument('--pattern', type=str, help="전체 파일에서 검출할 정규식 검색 패턴")
    parser.add_argument('--missing', type=str, help="전체 파일에서 반드시 포함되어야 할 필수 정규식 패턴")
    parser.add_argument('--json', action='store_true', help="JSON 포맷으로 결과 출력")
    args = parser.parse_args()
    
    include_offline = not args.no_offline
    report = scan_repository(
        include_offline=include_offline,
        custom_pattern=args.pattern,
        custom_missing=args.missing
    )
    
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
        
    print("=" * 70)
    print("🔍 [mathedu 기계적 전수 규칙 검사 보고서 (Rule-Based Full Scan)]")
    print(f"• 검사 대상 파일: {report['total_scanned']}개")
    print(f"• 무결성 합격 파일: {report['clean_files']}개")
    print(f"• 이상 감지 파일: {report['flagged_files']}개")
    print("=" * 70)
    
    if report['flagged_files'] == 0:
        print("\n✨ 전수 점검 통과! 모든 문항이 완벽한 무결성 상태입니다.\n")
    else:
        print("\n⚠️ 이상 탐지 항목 목록 (LLM 정밀 판단 및 일괄 수정 필요 지점):\n")
        for fpath, issues in report['details'].items():
            print(f"📁 {fpath} ({len(issues)}건 감지):")
            for iss in issues:
                sev = iss.get('severity', 'INFO')
                tag = f"[{sev}]"
                print(f"   - {tag:<10} ({iss['rule']}) {iss['msg']}")
            print()
            
if __name__ == '__main__':
    main()
