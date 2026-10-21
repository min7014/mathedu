import os, glob

board = '/c/Users/min/Desktop/mathedu/board'
site = '/c/Users/min/Desktop/mathedu/__site_board_urls.txt'

site_files = set()
with open(site) as f:
    for line in f:
        line = line.strip()
        if line.endswith('.html'):
            site_files.add(os.path.basename(line))

board_files = set(os.path.basename(f) for f in glob.glob(board + '/*.html'))

print('board files:', len(board_files))
print('site files:', len(site_files))
print('extra in board (not in site_urls):', sorted(board_files - site_files))
print('missing in board (in site_urls):', sorted(site_files - board_files))
