import json

# Read current
with open('_processed_reports.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add new reports
new = [
    {
        "timestamp": "2026-09-24T16:02:36.000Z",
        "quiz_slug": "48d0d98f",
        "question_num": 1,
        "status": "fixed",
        "fix": "Added dynamic '정답입니다!' confirmation message that shows when correct answer is selected (applies to all questions)"
    },
    {
        "timestamp": "2026-09-24T16:03:21.000Z",
        "quiz_slug": "48d0d98f",
        "question_num": 2,
        "status": "fixed",
        "fix": "Added dynamic '정답입니다!' confirmation message that shows when correct answer is selected (applies to all questions)"
    },
    {
        "timestamp": "2026-09-24T16:07:47.000Z",
        "quiz_slug": "48d0d98f",
        "question_num": 2,
        "status": "fixed",
        "fix": "Added dynamic '정답입니다!' confirmation message that shows when correct answer is selected (applies to all questions)"
    }
]

data['processed'].extend(new)

with open('_processed_reports.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Processed reports updated")
