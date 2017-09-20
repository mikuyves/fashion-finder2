# -*- coding: utf-8 -*-
import os
import re


# Define your own BASEPATH which is a ABS-PATH for saving the data.
from secret import BASEPATH


fullname = input('Enter full name: ')
desc = input('Enter description: ')
detail = input('Enter detail: ')
url = input('Enter URL: ')

base_filename = re.sub(r"[/\ ,']", '_', fullname)

folderpath = os.path.join(BASEPATH, base_filename)
os.mkdir(folderpath)
print('FOLDER: %s is created' % folderpath)

with open(folderpath + '/ready_to_send.gml', 'w') as f:
    f.write(fullname)
print('Made a gml file for sending emails.')

with open(folderpath + '/%s.txt' % base_filename, 'w') as f:
    f.write(fullname)
    f.write('''

%s

%s

%s
''' % (desc,
    detail,
    url)
    )
print('Made a txt file for item content.')
