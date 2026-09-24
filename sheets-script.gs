// ============================================================
// Google Apps Script — mathedu 학습 진행 저장
// ============================================================
// 사용법:
//   1. Google Drive에서 새 스프레드시트 만들기
//   2. 확장 프로그램 → Apps Script
//   3. 이 코드 붙여넣기 (기존 코드 대체)
//   4. 배포 → 새 배포 → 유형: 웹 앱
//   5. 액세스 권한: 모든 사용자 → 배포
//   6. 생성된 URL을 progress-api-url.txt에 저장
// ============================================================

// 웹 앱 엔트리 포인트 (POST 요청 처리)
function doPost(e) {
  try {
    var sheet = getSheet();
    var data = JSON.parse(e.postData.contents);
    
    var quizSlug = data.quiz_slug || '';
    var studentName = data.student_name || '';
    var currentStep = parseInt(data.current_step) || 0;
    var totalSteps = parseInt(data.total_steps) || 0;
    var correct = parseInt(data.correct) || 0;
    var pct = totalSteps > 0 ? Math.round(correct / totalSteps * 1000) / 10 : 0;
    
    if (!quizSlug || !studentName) {
      return ContentService.createTextOutput(JSON.stringify({
        ok: false, error: '필수 필드 누락 (quiz_slug, student_name)'
      })).setMimeType(ContentService.MimeType.JSON);
    }
    
    // 기존 행 찾기 (quiz_slug + student_name 기준)
    var existingRow = findRow(sheet, quizSlug, studentName);
    var now = new Date().toISOString().replace('T', ' ').substring(0, 19);
    
    if (existingRow > 0) {
      // 업데이트
      sheet.getRange(existingRow, 3, 1, 5).setValues([[
        currentStep, totalSteps, correct, pct, now
      ]]);
    } else {
      // 새 행 추가
      sheet.appendRow([
        quizSlug, studentName, currentStep, totalSteps, correct, pct, now
      ]);
    }
    
    return ContentService.createTextOutput(JSON.stringify({
      ok: true, pct: pct
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      ok: false, error: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// 조회 (GET 요청 — 대시보드용)
function doGet(e) {
  try {
    var sheet = getSheet();
    var quizFilter = (e.parameter.quiz || '').trim();
    var data = sheet.getDataRange().getValues();
    var headers = data[0];
    var items = [];
    
    for (var i = 1; i < data.length; i++) {
      var row = data[i];
      var item = {
        quiz_slug: row[0],
        student_name: row[1],
        current_step: row[2],
        total_steps: row[3],
        correct: row[4],
        pct: row[5],
        updated_at: row[6] ? row[6].toString() : ''
      };
      if (!quizFilter || item.quiz_slug === quizFilter) {
        items.push(item);
      }
    }
    
    // updated_at 기준 정렬 (최신 먼저)
    items.sort(function(a, b) {
      return (b.updated_at || '').localeCompare(a.updated_at || '');
    });
    
    return ContentService.createTextOutput(JSON.stringify({
      items: items.slice(0, 200)
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      ok: false, error: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// 시트 가져오기 (없으면 헤더 생성)
function getSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('progress');
  if (!sheet) {
    sheet = ss.insertSheet('progress');
    sheet.appendRow([
      'quiz_slug', 'student_name', 'current_step', 
      'total_steps', 'correct', 'pct', 'updated_at'
    ]);
    sheet.getRange(1, 1, 1, 7).setFontWeight('bold');
  }
  return sheet;
}

// 기존 행 찾기
function findRow(sheet, quizSlug, studentName) {
  var data = sheet.getDataRange().getValues();
  for (var i = 1; i < data.length; i++) {
    if (data[i][0] === quizSlug && data[i][1] === studentName) {
      return i + 1; // 1-based row index
    }
  }
  return 0;
}
