// Google Apps Script — mathedu 학습 진행 저장
// 사용법: 새 시트 → 확장 프로그램 → Apps Script → 붙여넣기 → 배포 → 웹 앱 → 모든 사용자

function doPost(e) {
  try {
    var sheet = getOrCreateSheet();
    var data = JSON.parse(e.postData.contents);
    
    var quizSlug = (data.quiz_slug || '').toString();
    var studentName = (data.student_name || '').toString();
    var currentStep = parseInt(data.current_step) || 0;
    var totalSteps = parseInt(data.total_steps) || 0;
    var correct = parseInt(data.correct) || 0;
    var pct = totalSteps > 0 ? Math.round(correct / totalSteps * 1000) / 10 : 0;
    
    if (!quizSlug || !studentName) {
      return jsonOutput({ ok: false, error: '필수 필드 누락' });
    }
    
    var existingRow = findRow(sheet, quizSlug, studentName);
    var now = new Date();
    var timeStr = now.toISOString().replace('T', ' ').substring(0, 19);
    
    if (existingRow > 0) {
      sheet.getRange(existingRow, 3, 1, 5).setValues([[currentStep, totalSteps, correct, pct, timeStr]]);
    } else {
      sheet.appendRow([quizSlug, studentName, currentStep, totalSteps, correct, pct, timeStr]);
    }
    
    return jsonOutput({ ok: true, pct: pct });
  } catch (err) {
    return jsonOutput({ ok: false, error: err.toString() });
  }
}

function doGet(e) {
  // Handle report action
  if (e && e.parameter && e.parameter.action === 'report') {
    return handleReport(e.parameter);
  }
  
  try {
    var sheet = getOrCreateSheet();
    var quizFilter = ((e && e.parameter && e.parameter.quiz) || '').trim();
    var data = sheet.getDataRange().getValues();
    var items = [];
    
    for (var i = 1; i < data.length; i++) {
      var row = data[i];
      var item = {
        quiz_slug: row[0] || '',
        student_name: row[1] || '',
        current_step: row[2] || 0,
        total_steps: row[3] || 0,
        correct: row[4] || 0,
        pct: row[5] || 0,
        updated_at: row[6] ? row[6].toString() : ''
      };
      if (!quizFilter || item.quiz_slug === quizFilter) {
        items.push(item);
      }
    }
    
    items.sort(function(a, b) { return (b.updated_at || '').localeCompare(a.updated_at || ''); });
    return jsonOutput({ items: items.slice(0, 200) });
  } catch (err) {
    return jsonOutput({ ok: false, error: err.toString() });
  }
}

function handleReport(params) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName('reports');
    if (!sheet) {
      sheet = ss.insertSheet('reports');
      sheet.appendRow(['timestamp', 'quiz_slug', 'question_num', 'reporter', 'text']);
      sheet.getRange(1, 1, 1, 5).setFontWeight('bold');
    }
    
    var now = new Date();
    sheet.appendRow([
      now.toISOString().replace('T', ' ').substring(0, 19),
      (params.quiz || '').toString(),
      (params.q || '').toString(),
      (params.name || '익명').toString(),
      (params.text || '').toString()
    ]);
    
    // Return 1x1 transparent GIF (for Image beacon)
    return ContentService.createTextOutput('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7')
      .setMimeType(ContentService.MimeType.GIF);
  } catch (err) {
    return ContentService.createTextOutput('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7')
      .setMimeType(ContentService.MimeType.GIF);
  }
}

function jsonOutput(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function getOrCreateSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('progress');
  if (!sheet) {
    sheet = ss.insertSheet('progress');
    sheet.appendRow(['quiz_slug', 'student_name', 'current_step', 'total_steps', 'correct', 'pct', 'updated_at']);
    sheet.getRange(1, 1, 1, 7).setFontWeight('bold');
  }
  return sheet;
}

function findRow(sheet, quizSlug, studentName) {
  var data = sheet.getDataRange().getValues();
  for (var i = 1; i < data.length; i++) {
    if (String(data[i][0]) === String(quizSlug) && String(data[i][1]) === String(studentName)) {
      return i + 1;
    }
  }
  return 0;
}
