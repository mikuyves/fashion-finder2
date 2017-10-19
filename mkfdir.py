# -*- coding: utf-8 -*-
import os
import re
import sys


# Define your own BASEPATH which is a ABS-PATH for saving the data.
from secret import BASEPATH


def mulinput(prompt):
    print(prompt, end='   --')
    print('[Press <CTRL-Z> or <CTRL-D> to stop, ENTER to Comfirm.]')
    lines = sys.stdin.readlines()
    return '\n'.join([line.strip() for line in lines])


brand = input('Enter brand:' ).strip()
title = input('Enter title:' ).strip()
fullname = ' - '.join((brand, title))
desc = mulinput('Enter description: ')
# detail = mulinput('Enter detail: ')
url = input('Enter URL: ')

base_filename = re.sub(r"[/\ ,']", '_', fullname)

folderpath = BASEPATH / base_filename

num = 1
while folderpath.exists():
    print('Duplicated folder.')
    if num == 1:
        answer = input('Do you want to change the name of this folder automatically? (y/n): ')
    if answer.lower() == 'y':
        folderpath = BASEPATH / (base_filename + '(%s)' % num)
    num += 2

folderpath.mkdir()

print('FOLDER: %s is created' % folderpath)

email_filepath = folderpath / 'ready_to_send.gml'
email_filepath.write_text(fullname, errors='replace')
print('Made a gml file for sending emails.')

filepath = folderpath / ('%s.txt' % base_filename)
filepath.write_text(title, errors='replace')

with open(str(folderpath) + '/%s.txt' % base_filename, mode='a', errors='replace') as f:
    f.write(
'''{fullname}

{desc}

{url}
'''.format(**locals())
    )
print('Made a txt file for item content.')
