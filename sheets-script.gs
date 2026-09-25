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

// Normalize timestamp to "YYYY-MM-DD HH:MM:SS" format
// Handles ISO strings and Date objects. Uses LOCAL time consistently.
function normalizeTs(ts) {
  if (!ts) return '';
  // If ts is a Date object (from Google Sheets getValues), format it as local time
  if (ts instanceof Date) {
    return formatLocalTs(ts);
  }
  ts = ts.toString();
  // ISO format "2026-09-24T15:12:09.000Z" — convert to local time representation
  if (ts.indexOf('T') >= 0) {
    // Parse the ISO string and format as local time
    var d = new Date(ts);
    if (!isNaN(d.getTime())) {
      return formatLocalTs(d);
    }
  }
  // Already a local string, just truncate
  return ts.substring(0, 19);
}

// Format a Date object as "YYYY-MM-DD HH:MM:SS" in local time
function formatLocalTs(date) {
  var y = date.getFullYear();
  var m = ('0' + (date.getMonth() + 1)).slice(-2);
  var d = ('0' + date.getDate()).slice(-2);
  var h = ('0' + date.getHours()).slice(-2);
  var mi = ('0' + date.getMinutes()).slice(-2);
  var s = ('0' + date.getSeconds()).slice(-2);
  return y + '-' + m + '-' + d + ' ' + h + ':' + mi + ':' + s;
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
    // Use local time (not UTC via toISOString) to match how the sheet stores timestamps
    var fixTimeStr = formatLocalTs(now);
    
    var targetTs = normalizeTs(data.timestamp || '');
    var targetQuiz = (data.quiz_slug || '').toString();
    var targetQ = (data.question_num || '').toString();
    
    // Find the report by timestamp + quiz_slug + question_num
    for (var i = 1; i < sheetData.length; i++) {
      var rowTs = normalizeTs(sheetData[i][0]);
      var rowQuiz = sheetData[i][1] ? sheetData[i][1].toString() : '';
      var rowQ = sheetData[i][2] ? sheetData[i][2].toString() : '';
      
      if (rowTs === targetTs && rowQuiz === targetQuiz && (rowQ === targetQ || targetQ === '')) {
        // Update columns 6 (fix_timestamp) and 7 (fix_result)
        sheet.getRange(i + 1, 6, 1, 2).setValues([[fixTimeStr, (data.result || '').toString()]]);
        
        // 📧 문제 제작 완료 이메일 발송 처리
        var email = (data.email || '').toString().trim();
        var reportText = (sheetData[i][4] || '').toString();
        if (!email) {
          var emailMatch = reportText.match(/이메일:\s*([^\s\n\r]+@[^\s\n\r]+)/);
          if (emailMatch) {
            email = emailMatch[1].trim();
          }
        }

        var emailSent = false;
        if (email && email.indexOf('@') > 0) {
          try {
            var quizUrl = (data.quiz_url || data.result || '').toString();
            var urlMatch = quizUrl.match(/https?:\/\/[^\s]+/);
            if (urlMatch) quizUrl = urlMatch[0];

            var title = (data.title || '').toString();
            if (!title) {
              var titleMatch = reportText.match(/제목:\s*(.*?)(?=\n내용:|\n정답|\n이메일|\Z)/);
              title = titleMatch ? titleMatch[1].trim() : '신규 출제 수학 퀴즈';
            }

            var reporter = (sheetData[i][3] || '선생님').toString();
            var subject = '[mathedu] 요청하신 수학 퀴즈(' + title + ')가 제작 완료되었습니다!';
            var htmlBody = '<div style="font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,sans-serif;line-height:1.7;color:#1e293b;max-width:620px;margin:20px auto;padding:28px;border:1px solid #e2e8f0;border-radius:16px;background:#ffffff;box-shadow:0 4px 20px rgba(0,0,0,0.05);">'
              + '<div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;">'
              + '  <span style="font-size:28px;">🎉</span>'
              + '  <h2 style="color:#1d4ed8;margin:0;font-size:20px;font-weight:700;">요청하신 수학 퀴즈가 제작 완료되었습니다!</h2>'
              + '</div>'
              + '<p style="font-size:15px;color:#334155;">안녕하세요, <b>' + reporter + '</b>님!<br>'
              + 'mathedu 안티그래비티 AI가 요청하신 문제의 단계별 인터랙티브 퀴즈 제작 및 배포를 완료하였습니다.</p>'
              + '<div style="background:#f8fafc;border:1px solid #cbd5e1;border-left:5px solid #2563eb;padding:16px 20px;margin:22px 0;border-radius:8px;">'
              + '  <div style="font-size:14px;color:#64748b;margin-bottom:6px;">📌 <b>문제 제목</b></div>'
              + '  <div style="font-size:16px;font-weight:700;color:#0f172a;margin-bottom:14px;">' + title + '</div>'
              + '  <div style="font-size:14px;color:#64748b;margin-bottom:6px;">🔗 <b>완성된 퀴즈 바로가기</b></div>'
              + '  <a href="' + quizUrl + '" style="display:inline-block;background:#2563eb;color:#ffffff;text-decoration:none;padding:10px 20px;border-radius:8px;font-weight:700;font-size:14px;">👉 퀴즈 풀러 가기 / 수업 열기</a>'
              + '  <div style="margin-top:10px;font-size:12px;color:#64748b;word-break:break-all;">URL: <a href="' + quizUrl + '" style="color:#2563eb;">' + quizUrl + '</a></div>'
              + '</div>'
              + '<div style="background:#eff6ff;padding:14px 18px;border-radius:8px;font-size:13px;color:#1e40af;margin-bottom:20px;">'
              + '💡 <b>수업 활용 팁:</b><br>'
              + '링크로 접속 후 상단의 <b>[🚀 이 퀴즈로 수업 열기]</b> 버튼을 누르시면, 학생들에게 공유할 6자리 방 코드와 대형 QR코드가 자동 발급됩니다.'
              + '</div>'
              + '<hr style="border:none;border-top:1px solid #f1f5f9;margin:24px 0;">'
              + '<div style="font-size:12px;color:#94a3b8;text-align:center;">가입 없는 수학 퀴즈 & 실시간 모니터링 생태계 · mathedu</div>'
              + '</div>';

            MailApp.sendEmail({
              to: email,
              subject: subject,
              htmlBody: htmlBody
            });
            emailSent = true;
          } catch(mailErr) {}
        }

        return jsonOutput({ ok: true, row: i + 1, email_sent: emailSent });
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
      formatLocalTs(now),
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


function doOptions() {
  return ContentService.createTextOutput('')
    .setMimeType(ContentService.MimeType.JSON);
}