import requests as rq
from bs4 import BeautifulSoup as bs
import sys
import os
import img2pdf
from concurrent.futures import ThreadPoolExecutor

##########################################
six_num = sys.argv[:]
##########################################


def get_image(img_src, sn):
    img = rq.get(img_src, stream=True).content
    i = img_src.split('/')[5].split('.')[0]
    print(f'./{sn}/_{i}.png')
    with open(f'./{sn}/_{i}.png', 'wb') as pic_out:
        pic_out.write(img)


for sn in six_num[1:]:
    if not os.path.isdir(f'./{sn}'):
        os.mkdir(sn)
    nref = f'https://nhentai.net/g/{sn}/'

    rr = rq.get(nref)
    soup = bs(rr.text, 'html.parser')
    sel = soup.select('div h2')
    print(sel[0].text)

    sel_tag = soup.select('div section span a')
    print('Total pages', sel_tag[-1].text)
    rr = rq.get(nref+'1/')
    soup = bs(rr.text, 'html.parser')
    sel = soup.select("div a img")
    base_src = sel[0]["src"].split('1.png')[0]
    img_src = [f'{base_src}{i}.png' for i in range(
        1, int(sel_tag[-1].text))]
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(get_image, (img_src, sn))
#    with open(f'./{sn}/{sn}.pdf', 'wb') as f:
#        f.write(img2pdf.convert([f'./{sn}/_{i}.png' for i in range(
#            1, int(sel_tag[-1].text))]))
