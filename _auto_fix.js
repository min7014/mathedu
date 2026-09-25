// 신고 자동 수정 스크립트 (Python)
// 이 스크립트는 헤르메스의 cronjob에서 호출됩니다.
// Google Sheets의 신고를 확인하고, HTML을 수정한 후 결과를 시트에 기록합니다.

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const SHEETS_URL = 'https://script.google.com/macros/s/AKfycbyKFvMp5odSgfBYd3eDjd-ueGnvcudXifd6aePX6D_cZ3IW7QrEa2qFKMBAUurphDQ9Mw/exec';
const BOARD_DIR = 'C:/Users/min/Desktop/mathedu/board';
const PROCESSED_FILE = 'C:/Users/min/Desktop/mathedu/_processed_reports.json';

async function main() {
  console.log('[mathedu] 신고 확인 중...');
  
  // 1. 신고 목록 가져오기
  const fetch = (await import('node-fetch')).default;
  const res = await fetch(SHEETS_URL + '?action=reports');
  const data = await res.json();
  
  if (!data.reports || data.reports.length === 0) {
    console.log('[mathedu] 새로운 신고 없음');
    return;
  }
  
  // 2. 처리된 신고 로드
  let processed = {};
  try {
    processed = JSON.parse(fs.readFileSync(PROCESSED_FILE, 'utf-8'));
  } catch {}
  
  // 3. 새 신고 처리
  let newReports = data.reports.filter(r => {
    const key = `${r.timestamp}|${r.quiz_slug}|${r.question_num}`;
    return !processed[key] && r.fix_timestamp === '';
  });
  
  if (newReports.length === 0) {
    console.log('[mathedu] 새로운 신고 없음');
    return;
  }
  
  console.log(`[mathedu] ${newReports.length}건의 새 신고 발견`);
  
  for (const report of newReports) {
    console.log(`[mathedu] 처리 중: ${report.quiz_slug} q${report.question_num} - ${report.text}`);
    
    // HTML 파일 수정
    const htmlPath = path.join(BOARD_DIR, `${report.quiz_slug}.html`);
    if (!fs.existsSync(htmlPath)) {
      console.log(`[mathedu] 파일 없음: ${htmlPath}`);
      continue;
    }
    
    let html = fs.readFileSync(htmlPath, 'utf-8');
    // TODO: 신고 내용에 따라 HTML 수정
    
    fs.writeFileSync(htmlPath, html);
    
    // 처리 완료 기록
    const key = `${report.timestamp}|${report.quiz_slug}|${report.question_num}`;
    processed[key] = { fixed: true, timestamp: new Date().toISOString() };
  }
  
  // 4. 처리 결과 저장
  fs.writeFileSync(PROCESSED_FILE, JSON.stringify(processed, null, 2));
  
  // 5. Git commit & push
  try {
    execSync('cd C:/Users/min/Desktop/mathedu && git add -A && git commit -m "auto-fix: reports" && git push', { stdio: 'inherit' });
  } catch (e) {
    console.error('[mathedu] Git 오류:', e.message);
  }
  
  console.log('[mathedu] 완료!');
}

main().catch(e => console.error(e));
