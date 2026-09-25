// Google Apps Script — mathedu 학습 진행 저장
// 사용법: 새 시트 → 확장 프로그램 → Apps Script → 붙여넣기 → 배포 → 웹 앱 → 모든 사용자

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    
    // Handle fix_report action
    if (data.action === 'fix_report') {
      return updateReportFix(data);
    }
    
    var sheet = getOrCreateSheet();
    
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

function updateReportFix(data) {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName('reports');
    if (!sheet) {
      return jsonOutput({ ok: false, error: 'reports sheet not found' });
    }
    
    var sheetData = sheet.getDataRange().getValues();
    var now = new Date();
    var fixTimeStr = now.toISOString().replace('T', ' ').substring(0, 19);
    
    // Find the report by timestamp + quiz_slug + question_num
    for (var i = 1; i < sheetData.length; i++) {
      var rowTs = sheetData[i][0] ? sheetData[i][0].toString() : '';
      var rowQuiz = sheetData[i][1] ? sheetData[i][1].toString() : '';
      var rowQ = sheetData[i][2] ? sheetData[i][2].toString() : '';
      
      if (rowTs === (data.timestamp || '') && rowQuiz === (data.quiz_slug || '') && rowQ === (data.question_num || '')) {
        // Update columns 6 (fix_timestamp) and 7 (fix_result)
        sheet.getRange(i + 1, 6, 1, 2).setValues([[fixTimeStr, (data.result || '').toString()]]);
        return jsonOutput({ ok: true, row: i + 1 });
      }
    }
    
    return jsonOutput({ ok: false, error: 'report not found' });
  } catch (err) {
    return jsonOutput({ ok: false, error: err.toString() });
  }
}

function doGet(e) {
  // Handle report action
  if (e && e.parameter && e.parameter.action === 'report') {
    return handleReport(e.parameter);
  }
  
  // Handle list reports action
  if (e && e.parameter && e.parameter.action === 'reports') {
    return listReports();
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
    var sheet = getOrCreateReportSheet();
    
    var now = new Date();
    sheet.appendRow([
      now.toISOString().replace('T', ' ').substring(0, 19),
      (params.quiz || '').toString(),
      (params.q || '').toString(),
      (params.name || '익명').toString(),
      (params.text || '').toString(),
      '',  // fix_timestamp
      ''   // fix_result
    ]);
    
    // Return 1x1 transparent GIF (for Image beacon)
    return ContentService.createTextOutput('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7')
      .setMimeType(ContentService.MimeType.GIF);
  } catch (err) {
    return ContentService.createTextOutput('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7')
      .setMimeType(ContentService.MimeType.GIF);
  }
}

function listReports() {
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName('reports');
    if (!sheet) {
      return jsonOutput({ reports: [] });
    }
    var data = sheet.getDataRange().getValues();
    var reports = [];
    for (var i = 1; i < data.length; i++) {
      reports.push({
        timestamp: data[i][0] || '',
        quiz_slug: data[i][1] || '',
        question_num: data[i][2] || '',
        reporter: data[i][3] || '',
        text: data[i][4] || '',
        fix_timestamp: data[i][5] || '',
        fix_result: data[i][6] || ''
      });
    }
    return jsonOutput({ reports: reports });
  } catch (err) {
    return jsonOutput({ ok: false, error: err.toString() });
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

function getOrCreateReportSheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('reports');
  if (!sheet) {
    sheet = ss.insertSheet('reports');
    sheet.appendRow(['timestamp', 'quiz_slug', 'question_num', 'reporter', 'text', 'fix_timestamp', 'fix_result']);
    sheet.getRange(1, 1, 1, 7).setFontWeight('bold');
  }
  // Ensure headers include fix columns (for existing sheets)
  var headers = sheet.getRange(1, 1, 1, 7).getValues()[0];
  if (headers[5] !== 'fix_timestamp' || headers[6] !== 'fix_result') {
    sheet.getRange(1, 6, 1, 2).setValues([['fix_timestamp', 'fix_result']]);
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
