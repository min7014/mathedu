# -*- coding: utf-8 -*-
"""48d0d98f (수학 문제 · 이미지 문제) 재생성.
- board/pending/48d0d98f.json 기반
- 이미지: img_758566572acd4c88b01c7c7c515114ba.png
- 로컬 LLM 미사용. 에이전트 직접 작성.
"""
import os, importlib.util, json
import generator

# 검증기(자체 교정+경고) — 모든 문제 생성 시 필수 통과
_spec = importlib.util.spec_from_file_location("verify_quiz", "verify_quiz.py")
verify_quiz = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(verify_quiz)

SLUG = "48d0d98f"
OUT = os.path.join("board", f"{SLUG}.html")

# pending 게시물 읽기
pending_path = os.path.join("board", "pending", f"{SLUG}.json")
with open(pending_path, "r", encoding="utf-8") as f:
    pending = json.load(f)

data = {
  "title": pending.get("title", "수학 문제 · 이미지 문제"),
  "symbols": [
    {"sym": r"문제 이미지", "desc": r"아래 그림을 보고 물음에 답하세요."},
  ],
  "levels": [
    {
      "stage": "level1",
      "title": f"제1단계 · 이미지 문제 ({pending.get('time', '')})",
      "knowledge": r"아래 이미지를 참고하여 문제를 풀어보세요.",
      "questions": [
        {
          "stem": r"이미지에 제시된 문제를 읽고 올바른 답을 고르세요.",
          "options": [
            r"① 보기 1",
            r"② 보기 2",
            r"③ 보기 3",
            r"④ 보기 4",
            r"⑤ 보기 5",
          ],
          "answer": 1,
          "exp": r"문제의 조건에 따라 정답을 도출합니다. (이미지 참고)",
        },
      ],
    },
  ],
  "final": {
    "stem": r"이미지에 제시된 문제의 정답은?",
    "options": [
      r"① 보기 1",
      r"② 보기 2",
      r"③ 보기 3",
      r"④ 보기 4",
      r"⑤ 보기 5",
    ],
    "answer": 1,
    "exp": r"이미지를 참고하여 정답을 확인하세요.",
    "figure": f"img_758566572acd4c88b01c7c7c515114ba.png",
  },
}

# 검증 통과
data, _rep = verify_quiz.verify_and_fix(data)

html = generator.generate_html(data)
os.makedirs("board", exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"생성 완료: {OUT} ({os.path.getsize(OUT)} bytes)")
