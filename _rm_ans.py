import re

path = "C:/Users/min/Desktop/mathedu/generator.py"
with open(path, encoding="utf-8") as f:
    src = f.read()

# Remove data-ans="..." from question html
src = re.sub(r'data-ans="[^"]*"', '', src)

with open(path, "w", encoding="utf-8") as f:
    f.write(src)
print("data-ans removed")
