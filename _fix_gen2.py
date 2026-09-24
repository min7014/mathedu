"""Fix generator.py: remove data-ans, use JS array for answers."""
path = "C:/Users/min/Desktop/mathedu/generator.py"
with open(path, encoding="utf-8") as f:
    src = f.read()

# Replace the scoring logic to use window._answers instead of q.dataset.ans
old = """qs.forEach(q=>{{const ans=+q.dataset.ans;const exp=q.querySelector('.exp');
exp.innerHTML=q.dataset.exp;const opts=q.querySelectorAll('.opt');"""

new = """qs.forEach(q=>{{const idx=Array.from(qs).indexOf(q);const ans=+window._answers[idx]||1;
const exp=q.querySelector('.exp');exp.innerHTML=q.dataset.exp||'';
const opts=q.querySelectorAll('.opt');"""

src = src.replace(old, new)

# Also remove data-ans from _question_html and final question
src = src.replace("data-ans=\"{q.get(\"answer\\,1)}\"", "data-ans=\\\"\\\"")
src = src.replace("data-ans=\"{f.get(\"answer\\,1)}\"", "data-ans=\\\"\\\"")

with open(path, "w", encoding="utf-8") as f:
    f.write(src)
print("generator.py updated")
