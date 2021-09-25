import img2pdf
import sys
import os

# input six number and total pages
dir = sys.argv[1:]

dirname = f'./{dir[0]}'
imgs = []
for fname in os.listdir(dirname):
    if not fname.endswith(".png"):
        continue
    path = os.path.join(dirname, fname)
    if os.path.isdir(path):
        continue
    imgs.append(path)

# make pdf with A-4 size
a4 = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
layout_fun = img2pdf.get_layout_fun(a4)

with open(f'./{dir[0]}/{dir[0]}.pdf', 'wb') as f:
    f.write(img2pdf.convert(imgs, layout_fun=layout_fun))
