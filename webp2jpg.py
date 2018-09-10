import os
from pathlib import Path

from PIL import Image


folder_path = input('Enter the whole path of the folder: ')

folder = Path(folder_path)

small_jpg_num = 0
for i in folder.glob('*.jpg'):
    if os.path.getsize(i) < 100_000:
        small_jpg_num += 1
        print(f'Find small jpg x {small_jpg_num}.')
        i.rename(folder / i.name.replace('.jpg', '.webp'))

for n, i in enumerate(folder.glob('*.webp'), start=1):
    im = Image.open(i).convert('RGB')
    im_name = folder / i.name.replace('.webp', '.jpg')
    im.save(im_name, 'jpeg')
    print(f'{n} webp -> jpg, done!')

print('All done!')

