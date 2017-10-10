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
title = input('Enter brand:' ).strip()
fullname = ' - '.join((brand, title))
desc = mulinput('Enter description: ')
detail = mulinput('Enter detail: ')
url = input('Enter URL: ')

base_filename = re.sub(r"[/\ ,']", '_', fullname)

folderpath = os.path.join(BASEPATH, base_filename)
os.mkdir(folderpath)
print('FOLDER: %s is created' % folderpath)

with open(folderpath + '/ready_to_send.gml', 'w') as f:
    f.write(fullname)
print('Made a gml file for sending emails.')

with open(folderpath + '/%s.txt' % base_filename, 'w') as f:
    f.write(
'''{fullname}

{desc}

{detail}

{url}
'''.format(**locals())
    )
print('Made a txt file for item content.')
