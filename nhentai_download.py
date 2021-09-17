import requests as rq
from bs4 import BeautifulSoup as bs
import sys
import os
import img2pdf

##########################################
six_num = sys.argv[:]
##########################################

for sn in six_num[1:]:
    if not os.path.isdir(f'./{sn}'):
        os.mkdir(sn)
    nref = f'https://nhentai.net/g/{sn}/'

    rr = rq.get(nref)
    soup = bs(rr.text, 'html.parser')
    sel = soup.select('div h2')
    print(sel[0].text)

    sel_tag = soup.select('div section span a')
    print('total pages', sel_tag[-1].text)

    ii = int(sel_tag[-1].text)
    img_list = []
    for i in range(ii):
        rr = rq.get(nref+str(i+1)+'/')
        soup = bs(rr.text, 'html.parser')
        sel = soup.select("div a img")
        img_src = sel[0]["src"]
        img_get = rq.get(img_src)
        img = img_get.content
        with open(f'./{sn}/_{i+1}.png', 'wb') as pic_out:
            pic_out.write(img)
        img_list.append(f'./{sn}/_{i+1}.png')
        print(f'Page {i+1} done!')
    with open(f'./{sn}/{sn}.pdf', 'wb') as f:
        f.write(img2pdf.convert(img_list))
