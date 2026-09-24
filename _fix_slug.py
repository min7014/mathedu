path = "C:/Users/min/Desktop/mathedu/generator.py"
with open(path, encoding="utf-8") as f:
    src = f.read()

old_body = """      quiz_slug: '{slug_js}',"""

new_body = """      quiz_slug: '{quiz_slug_val}',"""

src = src.replace(old_body, new_body)

# Also replace the format call to include quiz_slug_val
old_format = """    html = TEMPLATE.format(
        title=_esc(data.get("title", "퀴즈")),
        original_block=original_block,
        symbols_block=symbols_block, levels_block=levels_block,
        solution_block=solution_block, final_ans=_esc(final_ans),
        tracking_block=tracking_block)"""

new_format = """    html = TEMPLATE.format(
        title=_esc(data.get("title", "퀴즈")),
        original_block=original_block,
        symbols_block=symbols_block, levels_block=levels_block,
        solution_block=solution_block, final_ans=_esc(final_ans),
        tracking_block=tracking_block,
        quiz_slug_val=data.get("slug", "").replace("'", "\\\\'"))"""

src = src.replace(old_format, new_format)

with open(path, "w", encoding="utf-8") as f:
    f.write(src)
print("OK")
