import os

root = r'C:\Users\min\Desktop\mathedu'
path = os.path.join(root, '_regen_cron_runner.py')
with open(path, encoding='utf-8') as fh:
    content = fh.read()
print(content[2000:6000])
