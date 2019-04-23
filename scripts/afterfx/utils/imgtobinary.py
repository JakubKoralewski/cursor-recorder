# path_to_img

import os
from pathlib import Path

scripts_path = Path(os.path.split(__file__)[0])
image_path = Path(scripts_path.parent.parent.parent / 'docs' / 'img' / 'logo_small.png')
#print(image_path)

bin_img = open(image_path, 'rb').read()
out = open(Path(scripts_path / 'image.txt'), 'w+').write(bin_img.__str__())